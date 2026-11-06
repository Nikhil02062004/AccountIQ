"use client";

import React, { useState } from "react";
import { AccountDetail, TechnologyVendor } from "@/types";
import {
  Building2, Globe, Server, Target, Zap, Shield,
  CheckCircle2, AlertTriangle, HelpCircle, Layers, Filter
} from "lucide-react";

interface AccountIntelligenceTabProps {
  account: AccountDetail;
}

export const AccountIntelligenceTab: React.FC<AccountIntelligenceTabProps> = ({ account }) => {
  const [techFilter, setTechFilter] = useState<string>("ALL");

  const filteredTechnologies = account.technologies.filter((t) => {
    if (techFilter === "ALL") return true;
    return t.deployment_status === techFilter;
  });

  return (
    <div className="space-y-8">
      
      {/* 1. Company Overview & Footprint */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
          <Building2 className="w-5 h-5 text-sky-600" />
          <h2 className="text-base font-bold text-slate-900 tracking-tight">1. Company Overview & Global Footprint</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Legal Entity</div>
            <div className="text-sm font-bold text-slate-900 mt-1">{account.legal_name || account.name}</div>
            <div className="text-xs text-slate-500 mt-0.5">Ticker: {account.ticker || (account.id === "siemens-ag" ? "ETR: SIE" : "Unlisted / Private")}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Headquarters</div>
            <div className="text-sm font-bold text-slate-900 mt-1">{account.headquarters || "UNKNOWN"}</div>
            <div className="text-xs text-slate-500 mt-0.5">{account.id === "siemens-ag" ? "Primary Campus: Werner-von-Siemens-Str. 1" : "Principal Corporate Headquarters"}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Industry Classification</div>
            <div className="text-sm font-bold text-slate-900 mt-1">{account.industry || "Enterprise"}</div>
            <div className="text-xs text-slate-500 mt-0.5">{account.id === "siemens-ag" ? "Sectors: Automation, Infrastructure, Mobility" : `Sector: ${account.industry || "Commercial Operations"}`}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Workforce Distribution</div>
            <div className="text-sm font-bold text-slate-900 mt-1">{account.global_workforce || "UNKNOWN"}</div>
            <div className="text-xs text-slate-500 mt-0.5">{account.id === "siemens-ag" ? "Source: Audited Annual Report FY2024" : "Source: Primary Corporate Filings"}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Financial Scale</div>
            <div className="text-sm font-bold text-slate-900 mt-1">{account.annual_revenue || "UNKNOWN"}</div>
            <div className="text-xs text-slate-500 mt-0.5">{account.id === "siemens-ag" ? "Fiscal Year ended Sept 30, 2024" : "Latest Disclosed Financial Period"}</div>
          </div>

          <div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Geographic Scale</div>
            <div className="text-sm font-bold text-slate-900 mt-1">{account.geographic_presence || (account.id === "siemens-ag" ? "190+ Countries Worldwide" : "Global Operations")}</div>
            <div className="text-xs text-slate-500 mt-0.5">{account.id === "siemens-ag" ? "200+ major production facilities" : "Multi-region international presence"}</div>
          </div>
        </div>

        <div className="mt-6 pt-5 border-t border-slate-100 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-100">
            <div className="text-xs font-bold text-slate-700">Operating Business Units</div>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              {account.business_units || (account.id === "siemens-ag" ? "Digital Industries (DI), Smart Infrastructure (SI), Mobility, Siemens Healthineers (majority-owned subsidiary), Siemens Financial Services (SFS)." : `Corporate divisions and commercial operations across global operating entities for ${account.name}.`)}
            </p>
          </div>

          <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-100">
            <div className="text-xs font-bold text-slate-700">Major Facilities &amp; Hubs</div>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              {account.major_facilities || (account.id === "siemens-ag" ? "Munich HQ, Berlin, Erlangen, Amberg Electronic Works (lighthouse smart factory), Bad Neustadt, and international manufacturing hubs in US, China, and India." : `Principal operational hubs and facilities in ${account.headquarters || "corporate headquarters region"}.`)}
            </p>
          </div>
        </div>
      </div>

      {/* 2. Zscaler Portfolio Footprint & Expansion Whitespace Map */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-sky-600" />
            <h2 className="text-base font-bold text-slate-900 tracking-tight">2. Zscaler Product Footprint &amp; Whitespace Map</h2>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            {account.zscaler_products.length} Modules Indexed
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <th className="py-3 px-4">Product Module</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Deployment Status</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Evidence &amp; Whitespace Analysis</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {account.zscaler_products.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900">{p.product_name}</div>
                    <div className="text-[11px] text-slate-500 font-mono">{p.product_code}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-600">{p.category}</td>
                  <td className="py-3.5 px-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                      p.status === "CONFIRMED_DEPLOYED"
                        ? "bg-emerald-100 text-emerald-800"
                        : p.status === "PARTNERSHIP"
                        ? "bg-indigo-100 text-indigo-800"
                        : "bg-amber-100 text-amber-800"
                    }`}>
                      {p.status.replace("_", " ")}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-medium text-slate-700">
                    {Math.round(p.confidence * 100)}%
                  </td>
                  <td className="py-3.5 px-4 text-slate-700 max-w-md">
                    <p className="leading-relaxed">{p.evidence_summary}</p>
                    {p.expansion_hypothesis && (
                      <div className="mt-1 text-[11px] text-sky-800 bg-sky-50 p-2 rounded border border-sky-100 font-medium">
                        <strong>Expansion Hypothesis:</strong> {p.expansion_hypothesis}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 3. Technology Stack Table */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Server className="w-5 h-5 text-sky-600" />
            <h2 className="text-base font-bold text-slate-900 tracking-tight">3. Enterprise Technology Stack &amp; Infrastructure</h2>
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
            {["ALL", "CONFIRMED_CURRENT", "PARTNERSHIP", "HISTORICAL", "UNKNOWN"].map((status) => (
              <button
                key={status}
                onClick={() => setTechFilter(status)}
                className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all shrink-0 ${
                  techFilter === status
                    ? "bg-sky-600 text-white shadow-xs"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {status.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <th className="py-3 px-4">Technology Category</th>
                <th className="py-3 px-4">Vendor &amp; Solution</th>
                <th className="py-3 px-4">Deployment Status</th>
                <th className="py-3 px-4">Source Date</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Evidence Passage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredTechnologies.map((t) => (
                <tr key={t.id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4 font-semibold text-slate-900">{t.category}</td>
                  <td className="py-3.5 px-4">
                    <span className="font-bold text-slate-800">{t.vendor}</span>
                    {t.product_name && <span className="text-slate-500 ml-1">({t.product_name})</span>}
                  </td>
                  <td className="py-3.5 px-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                      t.deployment_status === "CONFIRMED_CURRENT"
                        ? "bg-emerald-100 text-emerald-800"
                        : t.deployment_status === "PARTNERSHIP"
                        ? "bg-indigo-100 text-indigo-800"
                        : t.deployment_status === "HISTORICAL"
                        ? "bg-slate-200 text-slate-700"
                        : t.deployment_status === "INFERENCE"
                        ? "bg-sky-100 text-sky-800"
                        : "bg-amber-100 text-amber-800"
                    }`}>
                      {t.deployment_status.replace("_", " ")}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-500 font-mono text-[11px]">{t.source_date || "Current"}</td>
                  <td className="py-3.5 px-4 font-mono font-medium text-slate-700">{Math.round(t.confidence * 100)}%</td>
                  <td className="py-3.5 px-4 text-slate-600 max-w-sm leading-relaxed">{t.evidence_summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. Strategic Priorities Linked to Zscaler Use Cases */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
          <Target className="w-5 h-5 text-sky-600" />
          <h2 className="text-base font-bold text-slate-900 tracking-tight">4. Strategic Business Priorities &amp; Zscaler Alignment</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {account.priorities.map((p) => (
            <div key={p.id} className="p-4 rounded-lg border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-colors">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-900">{p.title}</span>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-sky-100 text-sky-800">
                  {p.category}
                </span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">{p.description}</p>
              
              {p.supporting_quote && (
                <div className="mt-2.5 pl-2.5 border-l-2 border-sky-400 text-[11px] italic text-slate-700">
                  "{p.supporting_quote}"
                </div>
              )}

              <div className="mt-3 pt-2.5 border-t border-slate-200 text-xs text-sky-800 font-medium flex items-start gap-1">
                <span className="font-bold text-slate-700 shrink-0">Zscaler Opportunity:</span>
                <span>{p.zscaler_use_case}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 5. Buying Triggers & Catalysts */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
          <Zap className="w-5 h-5 text-sky-600" />
          <h2 className="text-base font-bold text-slate-900 tracking-tight">5. Urgent Buying Triggers &amp; Impact Analysis</h2>
        </div>

        <div className="space-y-4">
          {account.triggers.map((tr) => (
            <div key={tr.id} className="p-4 rounded-lg border border-slate-200 bg-white shadow-xs">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-100">
                <div className="flex items-center gap-2.5">
                  <span className="font-bold text-slate-900 text-sm">{tr.title}</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-emerald-100 text-emerald-800">
                    {tr.event_type}
                  </span>
                </div>
                <span className="text-xs text-slate-500 font-mono">{tr.date_occurred}</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3 text-xs">
                <div>
                  <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">What Happened</div>
                  <p className="text-slate-700 mt-1 leading-relaxed">{tr.description}</p>
                </div>
                <div>
                  <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Business Impact &amp; Urgency</div>
                  <p className="text-slate-700 mt-1 leading-relaxed">{tr.business_impact}</p>
                  {tr.affected_stakeholders && (
                    <div className="mt-2 text-[11px] text-slate-500">
                      <strong>Affected:</strong> {tr.affected_stakeholders}
                    </div>
                  )}
                </div>
                <div className="bg-sky-50/70 p-3 rounded-lg border border-sky-100">
                  <div className="font-bold text-sky-900 uppercase tracking-wide text-[10px]">Relevant Zscaler Capability</div>
                  <p className="text-sky-800 mt-1 leading-relaxed font-medium">{tr.zscaler_use_case}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
