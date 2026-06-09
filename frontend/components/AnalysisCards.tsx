"use client";

import { AlertTriangle, Ban, FileSearch, MessageSquareWarning, Scale, ScrollText } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Analysis } from "@/lib/types";

const sections = [
  { key: "summary", title: "Plain-English summary", icon: ScrollText },
  { key: "exclusions", title: "Exclusions", icon: Ban },
  { key: "risks", title: "Risk alerts", icon: AlertTriangle },
  { key: "denial_explanations", title: "Claim denial explanations", icon: MessageSquareWarning },
  { key: "appeal_recommendations", title: "Appeal recommendations", icon: Scale },
  { key: "policy_comparison", title: "Policy comparison checklist", icon: FileSearch },
] as const;

export function AnalysisCards({ analysis }: { analysis?: Analysis | null }) {
  if (!analysis) {
    return <p className="rounded-lg border bg-white p-5 text-sm text-muted-foreground">Select a policy or upload one to run analysis.</p>;
  }

  return (
    <div className="grid gap-4 xl:grid-cols-2">
      {sections.map((section) => {
        const Icon = section.icon;
        const content = analysis[section.key];
        return (
          <Card key={section.key}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Icon className="h-4 w-4 text-primary" />
                {section.title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="analysis-copy text-sm leading-6 text-muted-foreground">
                {content || "No result stored yet."}
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}

