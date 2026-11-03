import {
  AccountSummary, AccountDetail, TechnologyVendor, Contact,
  Recommendation, EvidenceExplorerData, QualityReport, ResearchProgress
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export async function fetchAccounts(): Promise<AccountSummary[]> {
  const res = await fetch(`${API_BASE}/accounts`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch accounts");
  return res.json();
}

export async function fetchAccountDetail(id: string): Promise<AccountDetail> {
  const res = await fetch(`${API_BASE}/accounts/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch account ${id}`);
  return res.json();
}

export async function fetchCommitteeGraph(id: string): Promise<{ nodes: any[]; edges: any[] }> {
  const res = await fetch(`${API_BASE}/accounts/${id}/committee-graph`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch committee graph");
  return res.json();
}

export async function fetchEvidenceData(
  id: string,
  params?: { verification_status?: string; is_conflicting?: boolean; entity_type?: string }
): Promise<EvidenceExplorerData> {
  const url = new URL(`${API_BASE}/accounts/${id}/evidence`);
  if (params?.verification_status) url.searchParams.set("verification_status", params.verification_status);
  if (params?.is_conflicting !== undefined) url.searchParams.set("is_conflicting", String(params.is_conflicting));
  if (params?.entity_type) url.searchParams.set("entity_type", params.entity_type);

  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch evidence data");
  return res.json();
}

export async function fetchQualityReport(id: string): Promise<QualityReport> {
  const res = await fetch(`${API_BASE}/accounts/${id}/quality-report`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch data quality report");
  return res.json();
}

export async function startNewResearch(data: {
  company_name: string;
  industry?: string;
  is_existing_customer?: boolean;
}): Promise<ResearchProgress> {
  const res = await fetch(`${API_BASE}/research/new`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to initiate research run");
  return res.json();
}

export async function checkResearchProgress(runId: string): Promise<ResearchProgress> {
  const res = await fetch(`${API_BASE}/research/${runId}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to poll research run");
  return res.json();
}

export async function deleteContactRecord(contactId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/contacts/${contactId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete contact record");
  return res.json();
}
