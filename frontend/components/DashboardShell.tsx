"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LogOut, RefreshCw, ShieldCheck } from "lucide-react";
import type { Session } from "@supabase/supabase-js";

import { AnalysisCards } from "@/components/AnalysisCards";
import { ChatPanel } from "@/components/ChatPanel";
import { PolicyList } from "@/components/PolicyList";
import { UploadDropzone } from "@/components/UploadDropzone";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getAnalysis, listPolicies } from "@/lib/api";
import { supabase } from "@/lib/supabase";
import type { Analysis, Policy } from "@/lib/types";

export function DashboardShell() {
  const router = useRouter();
  const [session, setSession] = useState<Session | null>(null);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [selectedPolicy, setSelectedPolicy] = useState<Policy | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (!data.session) {
        router.push("/login");
        return;
      }
      setSession(data.session);
      void loadPolicies(data.session.access_token);
    });
  }, [router]);

  async function loadPolicies(token = session?.access_token) {
    if (!token) return;
    setLoading(true);
    setError("");
    try {
      const rows = (await listPolicies(token)) as Policy[];
      setPolicies(rows);
      const first = selectedPolicy ? rows.find((item) => item.id === selectedPolicy.id) : rows[0];
      if (first) {
        await selectPolicy(first, token);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load policies");
    } finally {
      setLoading(false);
    }
  }

  async function selectPolicy(policy: Policy, token = session?.access_token) {
    if (!token) return;
    setSelectedPolicy(policy);
    const result = (await getAnalysis(policy.id, token)) as Analysis | null;
    setAnalysis(result);
  }

  async function signOut() {
    await supabase.auth.signOut();
    router.push("/login");
  }

  if (!session) {
    return <main className="p-8 text-sm text-muted-foreground">Loading session...</main>;
  }

  return (
    <main className="min-h-screen">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-5 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md bg-primary text-primary-foreground">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <div>
              <h1 className="text-xl font-semibold">Insurance Policy Analyzer</h1>
              <p className="text-sm text-muted-foreground">{session.user.email}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button onClick={() => void loadPolicies()} variant="outline">
              <RefreshCw className="h-4 w-4" />
              Refresh
            </Button>
            <Button onClick={signOut} variant="ghost">
              <LogOut className="h-4 w-4" />
              Sign out
            </Button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-5 px-4 py-6 lg:grid-cols-[320px_minmax(0,1fr)]">
        <aside className="space-y-5">
          <UploadDropzone
            token={session.access_token}
            onComplete={(policy, result) => {
              setPolicies((current) => [policy, ...current.filter((item) => item.id !== policy.id)]);
              setSelectedPolicy(policy);
              setAnalysis(result);
            }}
          />
          <Card>
            <CardHeader>
              <CardTitle>Your policies</CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? <p className="text-sm text-muted-foreground">Loading...</p> : null}
              {error ? <p className="mb-3 text-sm text-destructive">{error}</p> : null}
              <PolicyList policies={policies} selectedId={selectedPolicy?.id} onSelect={(policy) => void selectPolicy(policy)} />
            </CardContent>
          </Card>
        </aside>

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
          <AnalysisCards analysis={analysis} />
          <ChatPanel token={session.access_token} policy={selectedPolicy} />
        </section>
      </div>
    </main>
  );
}

