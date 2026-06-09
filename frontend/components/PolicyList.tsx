"use client";

import { FileText } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { Policy } from "@/lib/types";
import { cn } from "@/lib/utils";

type Props = {
  policies: Policy[];
  selectedId?: string;
  onSelect: (policy: Policy) => void;
};

export function PolicyList({ policies, selectedId, onSelect }: Props) {
  if (!policies.length) {
    return <p className="rounded-lg border bg-white p-4 text-sm text-muted-foreground">No policies yet.</p>;
  }

  return (
    <div className="space-y-2">
      {policies.map((policy) => (
        <Button
          className={cn("h-auto w-full justify-start p-3 text-left", selectedId === policy.id && "border-primary bg-muted")}
          key={policy.id}
          onClick={() => onSelect(policy)}
          variant="outline"
        >
          <FileText className="h-4 w-4 shrink-0" />
          <span className="min-w-0 flex-1">
            <span className="block truncate text-sm font-medium">{policy.file_url.split("/").pop()}</span>
            <span className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
              <Badge>{policy.insurance_type || "Pending type"}</Badge>
              {policy.uploaded_at ? new Date(policy.uploaded_at).toLocaleDateString() : ""}
            </span>
          </span>
        </Button>
      ))}
    </div>
  );
}

