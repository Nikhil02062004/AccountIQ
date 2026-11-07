import {
  AccountSummary, AccountDetail, TechnologyVendor, Contact,
  Recommendation, EvidenceExplorerData, QualityReport, ResearchProgress
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      let errorDetail = `HTTP ${res.status}: ${res.statusText}`;
      try {
        const errorJson = await res.json();
        if (errorJson && errorJson.detail) {
          errorDetail = typeof errorJson.detail === "string"
            ? errorJson.detail
            : JSON.stringify(errorJson.detail);
        }
      } catch {
        try {
          const text = await res.text();
          if (text) errorDetail = text;
        } catch {}
      }
      throw new Error(errorDetail);
    }
    return res.json();
  } catch (err: any) {
    if (
      err.message &&
      (err.message.includes("Failed to fetch") ||
       err.message.includes("NetworkError") ||
       err.name === "TypeError")
    ) {
      throw new Error(
        "Unable to connect to the AccountIQ research server (http://127.0.0.1:8000). Please verify that the backend is running."
      );
    }
    throw err;
  }
}

export async function fetchAccounts(): Promise<AccountSummary[]> {
  return apiFetch<AccountSummary[]>("/accounts", { cache: "no-store" });
}

export async function fetchAccountDetail(id: string): Promise<AccountDetail> {
  return apiFetch<AccountDetail>(`/accounts/${id}`, { cache: "no-store" });
}

export async function fetchCommitteeGraph(id: string): Promise<{ nodes: any[]; edges: any[] }> {
  return apiFetch<{ nodes: any[]; edges: any[] }>(`/accounts/${id}/committee-graph`, { cache: "no-store" });
}

export async function fetchEvidenceData(
  id: string,
  params?: { verification_status?: string; is_conflicting?: boolean; entity_type?: string }
): Promise<EvidenceExplorerData> {
  const url = new URL(`${API_BASE}/accounts/${id}/evidence`);
  if (params?.verification_status) url.searchParams.set("verification_status", params.verification_status);
  if (params?.is_conflicting !== undefined) url.searchParams.set("is_conflicting", String(params.is_conflicting));
  if (params?.entity_type) url.searchParams.set("entity_type", params.entity_type);

  return apiFetch<EvidenceExplorerData>(url.toString(), { cache: "no-store" });
}

export async function fetchQualityReport(id: string): Promise<QualityReport> {
  return apiFetch<QualityReport>(`/accounts/${id}/quality-report`, { cache: "no-store" });
}

export async function startNewResearch(data: {
  company_name: string;
  industry?: string;
  is_existing_customer?: boolean;
}): Promise<ResearchProgress> {
  return apiFetch<ResearchProgress>("/research/new", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function checkResearchProgress(runId: string): Promise<ResearchProgress> {
  return apiFetch<ResearchProgress>(`/research/${runId}`, { cache: "no-store" });
}

export async function deleteContactRecord(contactId: string): Promise<any> {
  return apiFetch<any>(`/contacts/${contactId}`, {
    method: "DELETE",
  });
}
