export type Policy = {
  id: string;
  user_id: string;
  file_url: string;
  insurance_type?: string | null;
  uploaded_at?: string | null;
  signed_url?: string | null;
};

export type Analysis = {
  id: string;
  policy_id: string;
  summary?: string | null;
  exclusions?: string | null;
  risks?: string | null;
  denial_explanations?: string | null;
  appeal_recommendations?: string | null;
  policy_comparison?: string | null;
  created_at?: string | null;
};

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

