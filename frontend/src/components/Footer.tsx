import Link from "next/link";
import { Activity, Mail, ExternalLink, Globe } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-background border-t border-border mt-auto relative overflow-hidden">
      {/* Subtle Background Glow */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="container mx-auto px-4 pt-20 pb-10 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-20">
          {/* Brand Identity */}
          <div className="md:col-span-1 flex flex-col gap-6">
            <div className="flex items-center gap-2">
              <Activity className="h-6 w-6 text-primary" />
              <span className="text-xl font-bold tracking-tighter text-foreground uppercase">TechFlow Pro</span>
            </div>
            <p className="text-sm text-muted-foreground font-light leading-relaxed">
              Pioneering the autonomous workforce. Our AI agents handle complex customer success protocols with 24/7 reliability and human-level nuance.
            </p>
            <div className="flex gap-4">
              <SocialLink icon={<Globe className="h-4 w-4" />} href="#" />
              <SocialLink icon={<Activity className="h-4 w-4" />} href="#" />
              <SocialLink icon={<Mail className="h-4 w-4" />} href="#" />
            </div>
          </div>

          {/* Links Column 1 */}
          <div className="flex flex-col gap-6">
            <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-foreground">Navigation</span>
            <ul className="flex flex-col gap-3">
              <FooterLink href="/" label="Operations Dashboard" />
              <FooterLink href="/support/new" label="Initialize Protocol" />
              <FooterLink href="/support/track" label="Track Status" />
              <FooterLink href="/metrics" label="System Analytics" />
            </ul>
          </div>

          {/* Links Column 2 */}
          <div className="flex flex-col gap-6">
            <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-foreground">Documentation</span>
            <ul className="flex flex-col gap-3">
              <FooterLink href="#" label="API Specification" external />
              <FooterLink href="#" label="Deployment Guide" external />
              <FooterLink href="#" label="Brand Standards" external />
              <FooterLink href="#" label="Security Audit" external />
            </ul>
          </div>

          {/* Newsletter / Contact */}
          <div className="flex flex-col gap-6">
            <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-foreground">Pulse Update</span>
            <p className="text-xs text-muted-foreground font-light">
              Receive weekly intelligence reports on autonomous systems performance.
            </p>
            <div className="flex flex-col gap-2">
              <div className="relative group">
                <input 
                  type="email" 
                  placeholder="agent@techflow.pro" 
                  className="w-full bg-background border border-border px-4 py-3 text-xs focus:outline-none focus:border-primary transition-colors rounded-none placeholder:text-zinc-700"
                />
                <button className="absolute right-3 top-1/2 -translate-y-1/2 text-primary hover:text-foreground transition-colors">
                  <Mail className="h-4 w-4" />
                </button>
              </div>
              <span className="text-[9px] text-muted-foreground italic uppercase tracking-wider">Join 1,200+ Operators</span>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-border pt-10 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex flex-wrap justify-center gap-8 text-[10px] uppercase tracking-[0.2em] font-medium text-muted-foreground">
            <Link href="#" className="hover:text-foreground transition-colors">Privacy Protocol</Link>
            <Link href="#" className="hover:text-foreground transition-colors">Terms of Service</Link>
            <Link href="#" className="hover:text-foreground transition-colors">SLA Agreement</Link>
          </div>
          <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest bg-muted px-4 py-2 border border-border/50">
            TechFlow Pro v2.4.0 — SECURED BY NEURAL AUTH
          </div>
        </div>
      </div>
    </footer>
  );
}

function FooterLink({ href, label, external = false }: { href: string; label: string; external?: boolean }) {
  return (
    <li>
      <Link 
        href={href} 
        className="text-xs text-muted-foreground hover:text-primary transition-all flex items-center gap-1 group"
      >
        {label}
        {external && <ExternalLink className="h-2 w-2 opacity-0 group-hover:opacity-100 transition-opacity" />}
      </Link>
    </li>
  );
}

function SocialLink({ icon, href }: { icon: React.ReactNode; href: string }) {
  return (
    <Link 
      href={href} 
      className="h-9 w-9 border border-border flex items-center justify-center text-muted-foreground hover:text-foreground hover:border-primary transition-all bg-background"
    >
      {icon}
    </Link>
  );
}
