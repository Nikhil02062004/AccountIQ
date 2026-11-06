"use client";

import React, { useState, useEffect } from "react";
import { EvidenceExplorerData, EvidenceClaim, Source } from "@/types";
import { fetchEvidenceData } from "@/lib/api";
import {
  FileText, ExternalLink, ShieldCheck, AlertCircle,
  Filter, CheckCircle2, Layers, Search
} from "lucide-react";

interface EvidenceExplorerTabProps {
  accountId: string;
}

export const EvidenceExplorerTab: React.FC<EvidenceExplorerTabProps> = ({ accountId }) => {
  const [data, setData] = useState<EvidenceExplorerData | null>(null);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [conflictOnly, setConflictOnly] = useState(false);
  const [entityFilter, setEntityFilter] = useState("ALL");
  const [search, setSearch] = useState("");

  const loadData = () => {
    setLoading(true);
    fetchEvidenceData(accountId, {
      verification_status: statusFilter === "ALL" ? undefined : statusFilter,
      is_conflicting: conflictOnly ? true : undefined,
      entity_type: entityFilter === "ALL" ? undefined : entityFilter,
    })
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load evidence", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadData();
  }, [accountId, statusFilter, conflictOnly, entityFilter]);

  const filteredClaims = (data?.claims || []).filter((c) => {
    if (search === "") return true;
    return (
      c.claim_text.toLowerCase().includes(search.toLowerCase()) ||
      c.excerpt.toLowerCase().includes(search.toLowerCase()) ||
      c.source_name.toLowerCase().includes(search.toLowerCase())
    );
  });

  return (
    <div className="space-y-6">
      
      {/* Evidence Stats & Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-sky-600" />
              <h2 className="text-base font-bold text-slate-900 tracking-tight">Evidence Explorer &amp; Data Provenance</h2>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Inspect supporting passages, publication timestamps, and confidence classifications for every extracted claim.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-sm font-bold text-slate-900">{data?.total_claims || 0} Claims</div>
              <div className="text-[11px] text-slate-500">{data?.total_sources || 0} Official Sources</div>
            </div>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 pt-4 text-xs">
          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Verification Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-md p-1.5"
            >
              <option value="ALL">All Verification Statuses</option>
              <option value="VERIFIED">Verified</option>
              <option value="CORROBORATED">Corroborated</option>
              <option value="INFERRED">Inferred</option>
              <option value="UNKNOWN">Unknown</option>
              <option value="STALE">Stale</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Entity Domain</label>
            <select
              value={entityFilter}
              onChange={(e) => setEntityFilter(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-md p-1.5"
            >
              <option value="ALL">All Entities</option>
              <option value="METRIC">Account Metrics</option>
              <option value="TECH">Technology Stack</option>
              <option value="PRIORITY">Strategic Priorities</option>
              <option value="TRIGGER">Buying Triggers</option>
              <option value="CONTACT">Stakeholders</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Data Conflict Flag</label>
            <button
              onClick={() => setConflictOnly(!conflictOnly)}
              className={`w-full p-1.5 rounded-md text-xs font-semibold border transition-all text-left flex items-center justify-between ${
                conflictOnly
                  ? "bg-rose-50 border-rose-300 text-rose-800"
                  : "bg-slate-50 border-slate-300 text-slate-700"
              }`}
            >
              <span>Conflicting Claims Only</span>
              <span className={`w-2 h-2 rounded-full ${conflictOnly ? "bg-rose-600" : "bg-slate-400"}`}></span>
            </button>
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Search Claims</label>
            <input
              type="text"
              placeholder="Search claim text or source..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-md p-1.5"
            />
          </div>
        </div>
      </div>

      {/* Conflicting Claims Banner if filtered */}
      {conflictOnly && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-xs text-amber-900 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold">Transparent Conflict Resolution:</span>
            <p className="mt-1 leading-relaxed">
              AccountIQ does not overwrite or discard diverging public metrics. For example, enterprises often report differing employee counts across continuing operations versus total headcount before divestments. Competing claims are preserved below with their respective reporting boundaries.
            </p>
          </div>
        </div>
      )}

      {/* Extracted Claims List */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
        <div className="p-4 bg-slate-50/80 border-b border-slate-200 flex items-center justify-between">
          <span className="text-xs font-bold text-slate-700 uppercase tracking-wide">
            Extracted Evidence Claims ({filteredClaims.length})
          </span>
          <span className="text-xs text-slate-500">
            0% Data Fabrication Guarantee
          </span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs text-slate-500">
            Loading evidence provenance...
          </div>
        ) : filteredClaims.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500">
            No claims match the active filter criteria.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {filteredClaims.map((claim) => (
              <div key={claim.id} className="p-5 hover:bg-slate-50/60 transition-colors">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
                      claim.verification_status === "VERIFIED"
                        ? "bg-emerald-100 text-emerald-800"
                        : claim.verification_status === "CORROBORATED"
                        ? "bg-sky-100 text-sky-800"
                        : claim.verification_status === "INFERRED"
                        ? "bg-indigo-100 text-indigo-800"
                        : "bg-amber-100 text-amber-800"
                    }`}>
                      {claim.verification_status}
                    </span>

                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                      {claim.entity_type}
                    </span>

                    {claim.is_conflicting && (
                      <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-rose-100 text-rose-800 border border-rose-200">
                        Preserved Conflict
                      </span>
                    )}
                  </div>

                  <div className="text-[11px] font-mono text-slate-500 flex items-center gap-2">
                    <span>Confidence: <strong>{Math.round(claim.confidence_score * 100)}%</strong></span>
                    <span>•</span>
                    <span>Retrieved: {claim.date_retrieved}</span>
                  </div>
                </div>

                <div className="mt-2 text-xs font-semibold text-slate-900 leading-relaxed">
                  {claim.claim_text}
                </div>

                {/* Supporting Excerpt */}
                <div className="mt-2 bg-slate-50 p-3 rounded-lg border-l-3 border-sky-500 text-xs text-slate-700 italic">
                  "{claim.excerpt}"
                </div>

                {claim.conflict_details && (
                  <div className="mt-2 text-[11px] text-amber-800 bg-amber-50/80 p-2 rounded border border-amber-200">
                    <strong>Conflict Context:</strong> {claim.conflict_details}
                  </div>
                )}

                {/* Provenance Footer */}
                <div className="mt-3 pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[11px] text-slate-500 border-t border-slate-100">
                  <div className="flex items-center gap-1.5">
                    <span>Source: <strong>{claim.source_name}</strong></span>
                    {claim.publication_date && <span>({claim.publication_date})</span>}
                  </div>
                  {claim.source_url && claim.source_url !== "#" && (
                    <a
                      href={claim.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-sky-600 hover:text-sky-700 font-semibold"
                    >
                      <span>Verify Exact URL</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Sources Directory Card */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
          Registered Primary Sources ({data?.sources.length || 0})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          {(data?.sources || []).map((s) => (
            <div key={s.id} className="p-3 rounded-lg border border-slate-100 bg-slate-50 flex flex-col justify-between">
              <div>
                <div className="font-bold text-slate-900">{s.name}</div>
                <div className="text-[11px] text-slate-500 mt-0.5">{s.source_type} • Published: {s.publication_date || "N/A"}</div>
                {s.notes && <p className="text-[11px] text-slate-600 mt-1">{s.notes}</p>}
              </div>
              <div className="mt-2 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px]">
                <span className="text-emerald-700 font-medium">Reliability Weight: {Math.round(s.reliability_weight * 100)}%</span>
                <a
                  href={s.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-sky-600 hover:text-sky-700 font-semibold inline-flex items-center gap-0.5"
                >
                  <span>Open</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
