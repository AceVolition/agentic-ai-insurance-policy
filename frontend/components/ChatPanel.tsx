"use client";

import { FormEvent, useState } from "react";
import { SendHorizonal } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { askPolicy } from "@/lib/api";
import type { ChatMessage, Policy } from "@/lib/types";

type Props = {
  token: string;
  policy?: Policy | null;
};

export function ChatPanel({ token, policy }: Props) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!policy || !message.trim()) return;
    const userMessage = message.trim();
    setMessages((current) => [...current, { role: "user", content: userMessage }]);
    setMessage("");
    setLoading(true);
    setError("");
    try {
      const result = (await askPolicy(policy.id, userMessage, token)) as { response: string };
      setMessages((current) => [...current, { role: "assistant", content: result.response }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Chat request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Policy chat</CardTitle>
        <CardDescription>Ask follow-up questions grounded in the uploaded PDF and saved analysis.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="max-h-[420px] min-h-[180px] space-y-3 overflow-y-auto rounded-lg border bg-white p-3">
          {messages.length ? (
            messages.map((item, index) => (
              <div
                className={item.role === "user" ? "ml-auto max-w-[90%] rounded-md bg-primary p-3 text-sm text-primary-foreground" : "mr-auto max-w-[90%] rounded-md bg-muted p-3 text-sm"}
                key={`${item.role}-${index}`}
              >
                <p className="analysis-copy">{item.content}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted-foreground">Select a policy and ask about coverage, exclusions, denial reasons, or appeal prep.</p>
          )}
        </div>
        <form className="space-y-3" onSubmit={submit}>
          <Textarea
            disabled={!policy || loading}
            onChange={(event) => setMessage(event.target.value)}
            placeholder={policy ? "Ask a question about this policy..." : "Select a policy first"}
            value={message}
          />
          {error ? <p className="text-sm text-destructive">{error}</p> : null}
          <Button disabled={!policy || loading || !message.trim()} type="submit">
            <SendHorizonal className="h-4 w-4" />
            {loading ? "Asking..." : "Ask"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

