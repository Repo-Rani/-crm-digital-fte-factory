import React, { useState } from 'react';

/**
 * SupportForm.jsx
 * REQUIRED Production Web Support Form
 * Features:
 * - Field validation (Client-side)
 * - Category/Priority selection
 * - Real-time character counter
 * - Ticket ID retrieval
 * - Modern inline-styled UI
 */

const CATEGORIES = [
  { value: 'general', label: 'General Question' },
  { value: 'technical', label: 'Technical Support' },
  { value: 'billing', label: 'Billing Inquiry' },
  { value: 'bug_report', label: 'Bug Report' },
  { value: 'feedback', label: 'Feedback' }
];

const PRIORITIES = [
  { value: 'low', label: 'Low — Not urgent' },
  { value: 'medium', label: 'Medium — Need help soon' },
  { value: 'high', label: 'High — Urgent issue' }
];

export default function SupportForm({ apiEndpoint = '/api/support/submit' }) {
  const [formData, setFormData] = useState({
    name: '', email: '', subject: '',
    category: 'general', priority: 'medium', message: ''
  });
  const [status, setStatus] = useState('idle'); // 'idle', 'submitting', 'success', 'error'
  const [ticketId, setTicketId] = useState(null);
  const [error, setError] = useState(null);
  const [fieldErrors, setFieldErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (fieldErrors[name]) {
      setFieldErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const errors = {};
    if (!formData.name || formData.name.trim().length < 2)
      errors.name = 'Name must be at least 2 characters';
    if (!formData.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email))
      errors.email = 'Please enter a valid email address';
    if (!formData.subject || formData.subject.trim().length < 5)
      errors.subject = 'Subject must be at least 5 characters';
    if (!formData.message || formData.message.trim().length < 10)
      errors.message = 'Description must be at least 10 characters';
    
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    if (!validate()) return;
    
    setStatus('submitting');
    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Submission failed.');
      }
      
      const data = await response.json();
      setTicketId(data.ticket_id);
      setStatus('success');
    } catch (err) {
      setError(err.message);
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <div style={styles.container}>
        <div style={styles.successBox}>
          <div style={styles.checkCircle}>✓</div>
          <h2 style={styles.successTitle}>Request Submitted!</h2>
          <p>Our AI assistant will respond shortly.</p>
          <div style={styles.ticketBox}>
            <p style={styles.ticketLabel}>Your Ticket ID</p>
            <p style={styles.ticketId}>{ticketId}</p>
          </div>
          <button onClick={() => { setStatus('idle'); setFormData({name:'', email:'', subject:'', category:'general', priority:'medium', message:''}); }} style={styles.btnPrimary}>
            Submit Another Request
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Contact Support</h2>
      <p style={styles.subtitle}>AI-Powered Customer Success</p>

      {error && <div style={styles.errorAlert}>{error}</div>}

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.fieldGroup}>
          <label style={styles.label}>Name *</label>
          <input name="name" value={formData.name} onChange={handleChange} style={{...styles.input, ...(fieldErrors.name ? styles.inputError : {})}} />
          {fieldErrors.name && <span style={styles.fieldError}>{fieldErrors.name}</span>}
        </div>

        <div style={styles.fieldGroup}>
          <label style={styles.label}>Email *</label>
          <input name="email" type="email" value={formData.email} onChange={handleChange} style={{...styles.input, ...(fieldErrors.email ? styles.inputError : {})}} />
          {fieldErrors.email && <span style={styles.fieldError}>{fieldErrors.email}</span>}
        </div>

        <div style={styles.fieldGroup}>
          <label style={styles.label}>Subject *</label>
          <input name="subject" value={formData.subject} onChange={handleChange} style={{...styles.input, ...(fieldErrors.subject ? styles.inputError : {})}} />
          {fieldErrors.subject && <span style={styles.fieldError}>{fieldErrors.subject}</span>}
        </div>

        <div style={styles.row}>
          <div style={{...styles.fieldGroup, flex: 1}}>
            <label style={styles.label}>Category</label>
            <select name="category" value={formData.category} onChange={handleChange} style={styles.select}>
              {CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
            </select>
          </div>
          <div style={{...styles.fieldGroup, flex: 1}}>
            <label style={styles.label}>Priority</label>
            <select name="priority" value={formData.priority} onChange={handleChange} style={styles.select}>
              {PRIORITIES.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
            </select>
          </div>
        </div>

        <div style={styles.fieldGroup}>
          <label style={styles.label}>Message *</label>
          <textarea name="message" value={formData.message} onChange={handleChange} rows={5} style={{...styles.textarea, ...(fieldErrors.message ? styles.inputError : {})}} />
          <div style={styles.charCount}>{formData.message.length}/2000</div>
          {fieldErrors.message && <span style={styles.fieldError}>{fieldErrors.message}</span>}
        </div>

        <button type="submit" disabled={status === 'submitting'} style={{...styles.btnPrimary, ...(status === 'submitting' ? styles.btnDisabled : {})}}>
          {status === 'submitting' ? 'Submitting...' : 'Submit Support Request'}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: { maxWidth: 600, margin: '20px auto', padding: '30px', border: '1px solid #eee', borderRadius: '12px', fontFamily: 'sans-serif' },
  title: { fontSize: '24px', marginBottom: '8px' },
  subtitle: { color: '#666', marginBottom: '24px' },
  form: { display: 'flex', flexDirection: 'column', gap: '16px' },
  fieldGroup: { display: 'flex', flexDirection: 'column', gap: '6px' },
  label: { fontSize: '14px', fontWeight: 'bold' },
  input: { padding: '10px', borderRadius: '6px', border: '1px solid #ccc' },
  inputError: { borderColor: 'red' },
  textarea: { padding: '10px', borderRadius: '6px', border: '1px solid #ccc', resize: 'vertical' },
  select: { padding: '10px', borderRadius: '6px', border: '1px solid #ccc' },
  row: { display: 'flex', gap: '16px' },
  btnPrimary: { padding: '12px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' },
  btnDisabled: { backgroundColor: '#ccc' },
  fieldError: { color: 'red', fontSize: '12px' },
  errorAlert: { padding: '10px', backgroundColor: '#fff5f5', border: '1px solid red', borderRadius: '6px', color: 'red', marginBottom: '16px' },
  charCount: { textAlign: 'right', fontSize: '12px', color: '#999' },
  successBox: { textAlign: 'center' },
  checkCircle: { fontSize: '48px', color: 'green', marginBottom: '16px' },
  ticketBox: { backgroundColor: '#f8f9fa', padding: '20px', borderRadius: '8px', margin: '20px 0' },
  ticketLabel: { fontSize: '12px', color: '#666' },
  ticketId: { fontSize: '20px', fontWeight: 'bold', fontFamily: 'monospace' }
};
