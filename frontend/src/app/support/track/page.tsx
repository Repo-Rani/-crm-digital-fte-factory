"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Loader2, Calendar, Tag, ShieldCheck, User, Bot, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import api from "@/lib/api";

function TrackTicketContent() {
  const searchParams = useSearchParams();
  const [ticketId, setTicketId] = useState(searchParams.get("id") || "");
  const [ticket, setTicket] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const id = searchParams.get("id");
    if (id) {
      handleTrack(id);
    }
  }, [searchParams]);

  async function handleTrack(id: string = ticketId) {
    if (!id) return;
    setLoading(true);
    try {
      const response = await api.get(`/support/ticket/${id}`);
      setTicket(response.data);
    } catch (error: any) {
      console.error("Tracking failed", error);
      toast.error("Ticket Not Found", { 
        description: "Verify the ID and try again." 
      });
      setTicket(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="flex gap-4 mb-12">
        <Input 
          placeholder="ENTER TICKET ID (e.g. TKT-1234)" 
          value={ticketId}
          onChange={(e) => setTicketId(e.target.value.toUpperCase())}
          className="bg-black border-white/10 rounded-none h-14 text-lg font-mono tracking-widest focus-visible:ring-white/20"
          onKeyDown={(e) => e.key === "Enter" && handleTrack()}
        />
        <Button 
          onClick={() => handleTrack()}
          className="bg-white text-black hover:bg-zinc-200 h-14 px-8 font-bold uppercase tracking-widest rounded-none whitespace-nowrap"
          disabled={loading}
        >
          {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <><Search className="mr-2 h-5 w-5" /> Locate</>}
        </Button>
      </div>

      <AnimatePresence mode="wait">
        {ticket ? (
          <motion.div
            key="ticket-data"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8"
          >
            {/* Ticket Info Card */}
            <div className="lg:col-span-1 flex flex-col gap-6">
              <Card className="bg-zinc-950 border-white/5 rounded-none">
                <CardHeader>
                  <CardTitle className="text-xs uppercase tracking-[0.2em] text-zinc-500">Protocol Metadata</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col gap-6">
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] uppercase text-zinc-600 tracking-widest font-bold">Current Status</span>
                    <Badge className={cnStatus(ticket.status)}>
                      {ticket.status.toUpperCase()}
                    </Badge>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] uppercase text-zinc-600 tracking-widest font-bold">Category</span>
                    <div className="flex items-center gap-2 text-sm text-white font-medium">
                      <Tag className="h-4 w-4 text-zinc-500" /> {ticket.category.replace('_', ' ')}
                    </div>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] uppercase text-zinc-600 tracking-widest font-bold">Initialized At</span>
                    <div className="flex items-center gap-2 text-sm text-white font-medium">
                      <Calendar className="h-4 w-4 text-zinc-500" /> {new Date(ticket.created_at).toLocaleString()}
                    </div>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-[10px] uppercase text-zinc-600 tracking-widest font-bold">Integrity Check</span>
                    <div className="flex items-center gap-2 text-sm text-green-500 font-mono font-bold">
                      <ShieldCheck className="h-4 w-4" /> VERIFIED
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Message History */}
            <div className="lg:col-span-2">
              <Card className="bg-black border-white/5 h-[600px] flex flex-col rounded-none">
                <CardHeader className="border-b border-white/5">
                  <CardTitle className="text-xs uppercase tracking-[0.2em] text-zinc-500">Communication Timeline</CardTitle>
                </CardHeader>
                <CardContent className="flex-1 p-0 overflow-hidden">
                  <ScrollArea className="h-full p-6">
                    <div className="flex flex-col gap-8">
                      {ticket.messages.map((msg: any, idx: number) => (
                        <div key={idx} className={`flex flex-col gap-3 ${msg.role === 'customer' ? 'items-end' : 'items-start'}`}>
                          <div className={`flex items-center gap-2 text-[10px] uppercase tracking-widest font-bold ${msg.role === 'customer' ? 'text-zinc-500 flex-row-reverse' : 'text-white'}`}>
                            {msg.role === 'customer' ? <><User className="h-3 w-3" /> Customer</> : <><Bot className="h-3 w-3" /> TechFlow AI</>}
                            <span className="text-zinc-700 font-normal">[{new Date(msg.timestamp || Date.now()).toLocaleTimeString()}]</span>
                          </div>
                          <div className={`max-w-[85%] p-4 text-sm font-light leading-relaxed ${
                            msg.role === 'customer' 
                            ? 'bg-zinc-900 text-zinc-300 border-l border-white/10' 
                            : 'bg-white text-black font-medium'
                          }`}>
                            {msg.content}
                          </div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </div>
          </motion.div>
        ) : (
          !loading && ticketId && (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              className="text-center py-20 border border-dashed border-white/10"
            >
              <p className="text-zinc-500 font-mono uppercase tracking-widest">No active protocol located for ID: {ticketId}</p>
            </motion.div>
          )
        )}
      </AnimatePresence>
    </>
  );
}

export default function TrackTicket() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <Link href="/" className="flex items-center gap-2 text-zinc-500 hover:text-white transition-colors mb-8 text-sm group">
        <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Back to Dashboard
      </Link>

      <div className="flex flex-col gap-2 mb-10">
        <h1 className="text-4xl font-bold tracking-tighter uppercase">Track Support Protocol</h1>
        <p className="text-zinc-500 font-light">
          Monitor real-time status and communication history for your inquiry.
        </p>
      </div>

      <Suspense fallback={
        <div className="flex flex-col items-center justify-center py-20 gap-4">
          <Loader2 className="h-8 w-8 animate-spin text-zinc-500" />
          <p className="text-zinc-500 font-mono uppercase tracking-widest">Initializing Tracking Engine...</p>
        </div>
      }>
        <TrackTicketContent />
      </Suspense>
    </div>
  );
}

function cnStatus(status: string) {
  const base = "w-fit py-1 px-3 rounded-none text-[10px] font-bold tracking-widest border";
  switch (status.toLowerCase()) {
    case 'open': return `${base} bg-white/5 text-white border-white/20`;
    case 'processing': return `${base} bg-zinc-900 text-white border-zinc-700 animate-pulse`;
    case 'resolved': return `${base} bg-white text-black border-white`;
    case 'escalated': return `${base} bg-red-950/30 text-red-500 border-red-900`;
    default: return `${base} bg-zinc-900 text-zinc-500 border-zinc-800`;
  }
}
