# Form Integration Guide: SupportForm.jsx

This guide explains how to integrate the **SupportForm.jsx** component into your existing React or Next.js application.

## 1. Prerequisites
- React 18+
- Modern browser support

## 2. Component Installation
Copy the `production/web-form/SupportForm.jsx` file into your project's components directory (e.g., `src/components/SupportForm.jsx`).

## 3. Usage

### Basic Integration
```javascript
import SupportForm from './components/SupportForm';

function ContactPage() {
  return (
    <div className="contact-container">
      <h1>Help & Support</h1>
      <SupportForm apiEndpoint="https://api.techflow.io/support/submit" />
    </div>
  );
}
```

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `apiEndpoint` | `string` | `'/api/support/submit'` | The URL where the form data will be POSTed. |

## 4. Customizing Styles
The component uses inline styles for maximum portability and zero-dependency installation. To customize the look and feel, you can:
1.  **Modify the `styles` object** at the bottom of the `SupportForm.jsx` file.
2.  **Pass a `className` prop** (requires minor modification to the component's root div) and use your own CSS/Tailwind classes.

## 5. Handling Success
When a submission is successful, the form displays a "Thank You" message and the generated **Ticket ID**. The user can then click "Submit Another Request" to reset the form.

## 6. Validation Rules
- **Name**: Minimum 2 characters.
- **Email**: Must match standard email regex.
- **Subject**: Minimum 5 characters.
- **Message**: Minimum 10 characters.
- **Category/Priority**: Must be selected from the provided dropdowns.
