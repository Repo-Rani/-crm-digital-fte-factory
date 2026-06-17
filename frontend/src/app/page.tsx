"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { 
  ArrowRight, 
  CheckCircle2, 
  Zap, 
  Globe, 
  Mail, 
  MessageCircle,
  Sparkles,
  Shield,
  Clock
} from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import api from "@/lib/api";

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const response = await api.get("/metrics/channels");
        setMetrics(response.data);
      } catch (error) {
        console.error("Failed to fetch metrics", error);
      } finally {
        setLoading(false);
      }
    }
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  };

  return (
    <div className="flex flex-col gap-24 pb-24 overflow-hidden">
      {/* Hero Section with Animated Background */}
      <section className="relative min-h-[90vh] flex items-center justify-center pt-20">
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-background" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,120,120,0.1),transparent_50%)]" />
          {/* Animated Grid Lines */}
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
        </div>

        <div className="container relative z-10 mx-auto px-4">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="flex flex-col items-center text-center gap-8"
          >
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Badge variant="outline" className="px-6 py-2 text-[10px] uppercase tracking-[0.3em] border-primary/20 bg-primary/5 text-primary backdrop-blur-sm">
                <Sparkles className="mr-2 h-3 w-3" /> Next-Gen AI Operations
              </Badge>
            </motion.div>

            <h1 className="text-6xl md:text-9xl font-bold tracking-tighter max-w-5xl leading-[0.85] text-foreground">
              THE FUTURE OF <span className="text-muted-foreground italic">SUPPORT.</span>
            </h1>

            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-muted-foreground max-w-2xl text-lg md:text-xl font-light leading-relaxed"
            >
              Deploy an autonomous digital workforce that masters your product knowledge. 
              Integrated. Intelligent. Instant.
            </motion.p>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 mt-8"
            >
              <Link 
                href="/support/new" 
                className={cn(
                  buttonVariants({ size: "lg" }), 
                  "bg-foreground text-background hover:bg-foreground/90 h-16 px-10 text-lg font-bold rounded-none transition-all hover:scale-105 active:scale-95"
                )}
              >
                INITIALIZE PROTOCOL <ArrowRight className="ml-3 h-5 w-5" />
              </Link>
              <Link 
                href="/metrics" 
                className={cn(
                  buttonVariants({ variant: "outline", size: "lg" }), 
                  "border-border bg-background/50 backdrop-blur-sm hover:bg-accent h-16 px-10 text-lg font-medium rounded-none transition-all"
                )}
              >
                SYSTEM METRICS
              </Link>
            </motion.div>
          </motion.div>
        </div>

        {/* Floating Background Elements */}
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background to-transparent z-10" />
      </section>

      {/* Metrics Section with Staggered Animation */}
      <section className="container mx-auto px-4 relative z-20">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <MetricCard 
            variants={itemVariants}
            title="Web Gateway" 
            icon={<Globe className="h-6 w-6" />} 
            value={metrics?.web_form?.total_conversations || 0}
            resolved={metrics?.web_form?.resolved || 0}
            loading={loading}
          />
          <MetricCard 
            variants={itemVariants}
            title="Email Protocol" 
            icon={<Mail className="h-6 w-6" />} 
            value={metrics?.email?.total_conversations || 0}
            resolved={metrics?.email?.resolved || 0}
            loading={loading}
          />
          <MetricCard 
            variants={itemVariants}
            title="Neural Engine" 
            icon={<MessageCircle className="h-6 w-6" />} 
            value={metrics?.whatsapp?.total_conversations || 0}
            resolved={metrics?.whatsapp?.resolved || 0}
            loading={loading}
          />
        </motion.div>
      </section>

      {/* Feature Grid with Hover Effects */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div 
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="flex flex-col gap-8"
          >
            <h2 className="text-4xl md:text-6xl font-bold tracking-tight leading-none">
              BUILT FOR <br/> <span className="text-muted-foreground font-light">HIGH-STAKES</span> OPS.
            </h2>
            <p className="text-muted-foreground text-lg font-light leading-relaxed max-w-lg">
              TechFlow Pro operates with surgical precision, leveraging your authoritative 
              documentation to provide consistent, compliant, and accurate resolutions.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
              <FeatureItem icon={<Zap className="h-5 w-5" />} title="Sub-3s Response" description="Instant analysis and resolution." />
              <FeatureItem icon={<Shield className="h-5 w-5" />} title="CRM Unified" description="Direct PostgreSQL integration." />
              <FeatureItem icon={<Clock className="h-5 w-5" />} title="24/7 Availability" description="Never sleeps, never misses." />
              <FeatureItem icon={<CheckCircle2 className="h-5 w-5" />} title="99.9% Uptime" description="Enterprise-grade reliability." />
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="relative aspect-square md:aspect-video bg-black border border-white/10 overflow-hidden group"
          >
            {/* High-Tech Pulse Monitor Visual */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.03),transparent)]" />
            
            {/* Moving Scanning Line */}
            <motion.div 
              animate={{ top: ["-10%", "110%"] }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
              className="absolute left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-primary/30 to-transparent z-10"
            />

            <div className="relative h-full w-full flex flex-col p-8 gap-8 z-20">
              <div className="flex justify-between items-start">
                <div className="flex flex-col gap-1">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-primary animate-ping" />
                    <span className="text-[10px] uppercase tracking-[0.4em] text-primary font-bold">Pulse Monitoring</span>
                  </div>
                  <span className="text-2xl font-bold tracking-tighter font-mono">LIVE_STREAM_ACTIVE</span>
                </div>
                <div className="text-right flex flex-col gap-1">
                  <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Encryption</span>
                  <span className="text-xs font-mono text-zinc-500">AES-256-GCM</span>
                </div>
              </div>
              
              {/* Animated EKG / Heartbeat Wave */}
              <div className="flex-1 relative flex items-center justify-center border-y border-white/5 bg-zinc-950/20">
                <svg viewBox="0 0 400 100" className="w-full h-32 text-primary opacity-80">
                  <motion.path
                    d="M 0 50 L 50 50 L 60 40 L 70 60 L 80 50 L 120 50 L 130 10 L 145 90 L 155 50 L 200 50 L 210 50 L 220 40 L 230 60 L 240 50 L 280 50 L 290 10 L 305 90 L 315 50 L 400 50"
                    fill="transparent"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{ 
                      pathLength: [0, 1],
                      opacity: [0, 1, 1, 0],
                      x: [0, 0, 0]
                    }}
                    transition={{ 
                      duration: 3, 
                      repeat: Infinity, 
                      ease: "linear",
                    }}
                  />
                  {/* Static faint background wave */}
                  <path
                    d="M 0 50 L 50 50 L 60 40 L 70 60 L 80 50 L 120 50 L 130 10 L 145 90 L 155 50 L 200 50 L 210 50 L 220 40 L 230 60 L 240 50 L 280 50 L 290 10 L 305 90 L 315 50 L 400 50"
                    fill="transparent"
                    stroke="currentColor"
                    strokeWidth="1"
                    className="opacity-10"
                  />
                </svg>
                <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent_0%,rgba(0,0,0,0.8)_100%)] pointer-events-none" />
              </div>

              <div className="grid grid-cols-3 gap-8">
                <div className="flex flex-col gap-1">
                  <span className="text-[9px] uppercase tracking-widest text-muted-foreground">Neural Load</span>
                  <span className="text-sm font-mono text-white">12.4%</span>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[9px] uppercase tracking-widest text-muted-foreground">Sync Rate</span>
                  <span className="text-sm font-mono text-white">0.002ms</span>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[9px] uppercase tracking-widest text-muted-foreground">Uptime</span>
                  <span className="text-sm font-mono text-green-500">99.999%</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}

function VisualStat({ label, value, width }: any) {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex justify-between text-[9px] uppercase tracking-widest text-muted-foreground">
        <span>{label}</span>
        <span className="font-mono">{value}</span>
      </div>
      <div className="h-[2px] w-full bg-muted">
        <motion.div 
          initial={{ width: 0 }}
          whileInView={{ width }}
          transition={{ duration: 1.5, ease: "circOut" }}
          className="h-full bg-primary"
        />
      </div>
    </div>
  );
}

function MetricCard({ title, icon, value, resolved, loading, variants }: any) {
  return (
    <motion.div variants={variants}>
      <Card className="bg-background/50 border-border hover:border-primary/30 transition-all rounded-none overflow-hidden group backdrop-blur-md">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4 border-b border-border/50">
          <CardTitle className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.3em]">{title}</CardTitle>
          <div className="text-muted-foreground group-hover:text-primary transition-colors">
            {icon}
          </div>
        </CardHeader>
        <CardContent className="pt-6">
          {loading ? (
            <div className="h-12 w-24 animate-pulse bg-muted rounded-none" />
          ) : (
            <div className="text-5xl font-bold tracking-tighter">{value}</div>
          )}
          <div className="flex justify-between items-end mt-4">
            <p className="text-[10px] text-muted-foreground uppercase tracking-widest">
              {resolved} Issues Resolved
            </p>
            <span className="text-[10px] font-mono text-primary font-bold">
              {value > 0 ? Math.round((resolved / value) * 100) : 0}% EFFICIENCY
            </span>
          </div>
          <div className="mt-4 h-1 w-full bg-muted overflow-hidden">
            <motion.div 
              className="h-full bg-primary" 
              initial={{ width: 0 }}
              whileInView={{ width: value > 0 ? `${(resolved / value) * 100}%` : "0%" }}
              transition={{ duration: 1.5, ease: "circOut" }}
              viewport={{ once: true }}
            />
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function FeatureItem({ icon, title, description }: any) {
  return (
    <div className="flex gap-4 p-4 border border-border/50 hover:bg-accent/50 transition-colors">
      <div className="mt-1 text-primary">{icon}</div>
      <div className="flex flex-col gap-1">
        <span className="text-xs font-bold uppercase tracking-widest">{title}</span>
        <span className="text-xs text-muted-foreground font-light">{description}</span>
      </div>
    </div>
  );
}

function Activity({ className }: { className?: string }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
    >
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  );
}
