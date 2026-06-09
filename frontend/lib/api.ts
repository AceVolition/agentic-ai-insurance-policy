const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, token: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(init?.headers || {}),
    },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

export async function listPolicies(token: string) {
  return request("/policies", token);
}

export async function getAnalysis(policyId: string, token: string) {
  return request(`/analysis/${policyId}`, token);
}

export async function uploadPolicy(file: File, token: string) {
  const form = new FormData();
  form.append("file", file);
  return request("/policies/upload", token, { method: "POST", body: form });
}

export async function runAnalysis(policyId: string, token: string) {
  return request(`/analysis/run/${policyId}`, token, { method: "POST" });
}

export async function askPolicy(policyId: string, message: string, token: string) {
  return request(`/chat/${policyId}`, token, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
}

