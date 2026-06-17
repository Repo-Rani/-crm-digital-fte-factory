"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BarChart3, Activity, PieChart, TrendingUp, ArrowLeft, RefreshCcw } from "lucide-react";
import Link from "next/link";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  async function fetchMetrics() {
    setLoading(true);
    try {
      const response = await api.get("/metrics/channels");
      setMetrics(response.data);
    } catch (error) {
      console.error("Failed to fetch metrics", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchMetrics();
  }, []);

  const totalConvos = metrics ? Object.values(metrics).reduce((acc: number, curr: any) => acc + curr.total_conversations, 0) : 0;
  const totalResolved = metrics ? Object.values(metrics).reduce((acc: number, curr: any) => acc + curr.resolved, 0) : 0;
  const avgResolutionRate = totalConvos > 0 ? (totalResolved / totalConvos) * 100 : 0;

  return (
    <div className="container mx-auto px-4 py-12">
      <Link href="/" className="flex items-center gap-2 text-zinc-500 hover:text-white transition-colors mb-8 text-sm group">
        <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-1" /> Back to Dashboard
      </Link>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-12">
        <div className="flex flex-col gap-2">
          <h1 className="text-4xl font-bold tracking-tighter uppercase">Operations Intelligence</h1>
          <p className="text-zinc-500 font-light max-w-xl">
            Real-time performance analytics across all autonomous support channels.
          </p>
        </div>
        <Button 
          variant="outline" 
          onClick={fetchMetrics} 
          className="border-white/10 hover:bg-white/5 rounded-none h-12 px-6 uppercase tracking-widest text-[10px] font-bold"
          disabled={loading}
        >
          <RefreshCcw className={`mr-2 h-3 w-3 ${loading ? 'animate-spin' : ''}`} /> Refresh Data
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <StatCard title="Global Volume" value={totalConvos} icon={<Activity className="h-4 w-4" />} />
        <StatCard title="Resolved Issues" value={totalResolved} icon={<TrendingUp className="h-4 w-4" />} />
        <StatCard title="Resolution Rate" value={`${avgResolutionRate.toFixed(1)}%`} icon={<PieChart className="h-4 w-4" />} />
        <StatCard title="AI Confidence" value="98.4%" icon={<BarChart3 className="h-4 w-4" />} />
      </div>

      <Card className="bg-black border-white/5 rounded-none overflow-hidden">
        <CardHeader className="bg-zinc-950 border-b border-white/5">
          <CardTitle className="text-xs uppercase tracking-[0.2em] text-zinc-500">Channel Breakdown</CardTitle>
          <CardDescription className="text-[10px] uppercase tracking-widest text-zinc-700">Metrics for last 24-hour cycle</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-zinc-950/50">
              <TableRow className="border-white/5 hover:bg-transparent">
                <TableHead className="w-[200px] text-zinc-500 uppercase tracking-widest text-[10px] py-6">Channel</TableHead>
                <TableHead className="text-zinc-500 uppercase tracking-widest text-[10px]">Status</TableHead>
                <TableHead className="text-zinc-500 uppercase tracking-widest text-[10px]">Total Inquiries</TableHead>
                <TableHead className="text-zinc-500 uppercase tracking-widest text-[10px]">Resolved</TableHead>
                <TableHead className="text-zinc-500 uppercase tracking-widest text-[10px] text-right">Success Rate</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array(3).fill(0).map((_, i) => (
                  <TableRow key={i} className="border-white/5">
                    <TableCell><div className="h-4 w-24 bg-zinc-900 animate-pulse rounded" /></TableCell>
                    <TableCell><div className="h-4 w-16 bg-zinc-900 animate-pulse rounded" /></TableCell>
                    <TableCell><div className="h-4 w-12 bg-zinc-900 animate-pulse rounded" /></TableCell>
                    <TableCell><div className="h-4 w-12 bg-zinc-900 animate-pulse rounded" /></TableCell>
                    <TableCell className="text-right"><div className="h-4 w-16 bg-zinc-900 animate-pulse rounded ml-auto" /></TableCell>
                  </TableRow>
                ))
              ) : (
                Object.entries(metrics || {}).map(([key, data]: [string, any]) => (
                  <TableRow key={key} className="border-white/5 hover:bg-white/5 transition-colors group">
                    <TableCell className="font-mono text-sm uppercase tracking-wider py-6">
                      {key.replace('_', ' ')}
                    </TableCell>
                    <TableCell>
                      <Badge className="bg-green-950/20 text-green-500 border-green-900 rounded-none text-[8px] uppercase tracking-widest px-2">Active</Badge>
                    </TableCell>
                    <TableCell className="text-lg font-bold tracking-tighter">{data.total_conversations}</TableCell>
                    <TableCell className="text-lg font-bold tracking-tighter text-zinc-400">{data.resolved}</TableCell>
                    <TableCell className="text-right font-mono text-sm">
                      {data.total_conversations > 0 ? ((data.resolved / data.total_conversations) * 100).toFixed(1) : "0.0"}%
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

function StatCard({ title, value, icon }: any) {
  return (
    <Card className="bg-zinc-950 border-white/5 rounded-none">
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[10px] uppercase tracking-[0.2em] text-zinc-500 font-bold">{title}</span>
          <div className="p-2 bg-black border border-white/5 text-zinc-400">
            {icon}
          </div>
        </div>
        <div className="text-3xl font-bold tracking-tighter">{value}</div>
      </CardContent>
    </Card>
  );
}
