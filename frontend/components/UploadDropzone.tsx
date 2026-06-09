"use client";

import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { FileUp, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { uploadPolicy, runAnalysis } from "@/lib/api";
import type { Analysis, Policy } from "@/lib/types";

type Props = {
  token: string;
  onComplete: (policy: Policy, analysis: Analysis) => void;
};

export function UploadDropzone({ token, onComplete }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function handleFile(file?: File) {
    if (!file) return;
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      setError("Please upload a PDF policy.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const policy = (await uploadPolicy(file, token)) as Policy;
      const analysis = (await runAnalysis(policy.id, token)) as Analysis;
      onComplete(policy, analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  function onDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    void handleFile(event.dataTransfer.files[0]);
  }

  function onChange(event: ChangeEvent<HTMLInputElement>) {
    void handleFile(event.target.files?.[0]);
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload policy PDF</CardTitle>
        <CardDescription>PDF parsing starts immediately, followed by the supervisor analysis workflow.</CardDescription>
      </CardHeader>
      <CardContent>
        <div
          className="flex min-h-[180px] cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-primary/50 bg-white px-6 py-8 text-center transition hover:bg-muted"
          onClick={() => inputRef.current?.click()}
          onDragOver={(event) => event.preventDefault()}
          onDrop={onDrop}
          role="button"
          tabIndex={0}
        >
          {busy ? <Loader2 className="mb-4 h-10 w-10 animate-spin text-primary" /> : <FileUp className="mb-4 h-10 w-10 text-primary" />}
          <p className="text-sm font-medium">{busy ? "Analyzing policy..." : "Drop a PDF here or choose a file"}</p>
          <p className="mt-1 text-sm text-muted-foreground">The file is stored in Supabase Storage and tied to your user.</p>
          <input ref={inputRef} className="hidden" type="file" accept="application/pdf" onChange={onChange} />
          <Button className="mt-5" disabled={busy} type="button">
            {busy ? "Running agents" : "Select PDF"}
          </Button>
        </div>
        {error ? <p className="mt-3 text-sm text-destructive">{error}</p> : null}
      </CardContent>
    </Card>
  );
}

