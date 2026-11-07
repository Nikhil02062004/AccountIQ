"use client";

import React, { useState } from "react";
import { AccountDetail } from "@/types";
import {
  Compass, ArrowRight, Copy, Check, AlertTriangle, ShieldCheck,
  Building2, Users, FileText, ExternalLink, Sparkles
} from "lucide-react";

interface RecommendedWayInTabProps {
  account: AccountDetail;
  onNavigateToTab: (tab: string) => void;
}

export const RecommendedWayInTab: React.FC<RecommendedWayInTabProps> = ({
  account,
  onNavigateToTab,
}) => {
  const [copied, setCopied] = useState(false);
  const rec = account.recommendation;
  const firstContact = rec?.first_contact;
  const secondContact = rec?.second_contact;

  const handleCopyOpener = () => {
    if (rec?.suggested_opener_draft) {
      navigator.clipboard.writeText(rec.suggested_opener_draft);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (!rec) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-8 text-center text-slate-500">
        No sales recommendation generated for this account yet.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      
      {/* Strategic Header Banner */}
      <div className="bg-gradient-to-r from-sky-900 to-indigo-900 text-white rounded-xl p-6 shadow-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-sky-800/80 text-sky-200 text-xs font-semibold uppercase tracking-wider mb-2">
              <Compass className="w-3.5 h-3.5" />
              <span>Executive Sales Execution Blueprint</span>
            </div>
            <h1 className="text-xl md:text-2xl font-bold tracking-tight">
              {rec.outreach_angle}
            </h1>
            <p className="text-xs text-sky-200/90 mt-1 max-w-3xl leading-relaxed">
              {account.id === "siemens-ag"
                ? "Synthesizing account triggers ($10B Altair acquisition, Industrial Copilot, OT NIS2 compliance) with verified stakeholder mandates."
                : `Synthesizing corporate triggers and technology context for ${account.name} with verified stakeholder priorities.`}
            </p>
          </div>

          <div className="shrink-0 flex flex-col items-end gap-1">
            <span className="text-[11px] text-sky-300">Timing Score</span>
            <div className="text-2xl font-black text-white">{account.timing_score}/100</div>
          </div>
        </div>
      </div>

      {/* Core Answering Block: Why This Account & Why Now */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <Building2 className="w-4 h-4 text-sky-600" />
            <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">1. Why This Account?</h2>
          </div>
          <p className="text-xs text-slate-700 leading-relaxed">
            {rec.why_this_account}
          </p>
          <div className="mt-3 text-[11px] text-sky-700 bg-sky-50 p-2.5 rounded border border-sky-100 font-medium">
            <strong>Key Anchor:</strong> {account.is_existing_customer ? (account.id === "siemens-ag" ? "Existing Zscaler enterprise customer across 300,000+ seats; zero-trust is already proven and endorsed at the Managing Board level." : "Existing enterprise customer with proven zero-trust adoption and significant whitespace.") : `Major enterprise prospect in ${account.industry || "target market"} undergoing digital modernization.`}
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <Compass className="w-4 h-4 text-emerald-600" />
            <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">2. Why Now? (Timing &amp; Urgency)</h2>
          </div>
          <p className="text-xs text-slate-700 leading-relaxed">
            {rec.why_now}
          </p>
          <div className="mt-3 text-[11px] text-emerald-800 bg-emerald-50 p-2.5 rounded border border-emerald-100 font-medium">
            <strong>Urgency Catalyst:</strong> {account.triggers?.[0]?.title ? `${account.triggers[0].title}` : (account.id === "siemens-ag" ? "Altair simulation software integration underway + NIS2 compliance deadline for 200+ global factories." : "Active enterprise transformation and cloud workload scaling window.")}
          </div>
        </div>
      </div>

      {/* Recommended First Contact Deep-Dive */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2.5">
            <div className="h-10 w-10 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center text-sm">
              1st
            </div>
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">First Stakeholder to Approach</span>
              <h3 className="text-lg font-bold text-slate-900">
                {firstContact?.full_name || "Stakeholder Verification Pending"}
              </h3>
              <p className="text-xs text-slate-600">
                {firstContact?.current_title || "No verified public executive profile"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-100 text-emerald-800">
              {firstContact?.buying_role || "STAKEHOLDER"}
            </span>
            <span className="text-xs font-mono font-bold text-sky-700 bg-sky-50 px-2.5 py-1 rounded-full border border-sky-100">
              Relevance: {firstContact ? `${firstContact.relevance_score}/100` : "N/A"}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-5 text-xs">
          <div>
            <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Why This Stakeholder?</div>
            <p className="text-slate-700 mt-1 leading-relaxed">{rec.why_this_stakeholder}</p>
          </div>

          <div>
            <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Business Problem to Discuss</div>
            <p className="text-slate-700 mt-1 leading-relaxed">{rec.business_problem}</p>
          </div>

          <div>
            <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Relevant Zscaler Capability</div>
            <p className="text-sky-800 font-medium mt-1 leading-relaxed">{rec.relevant_zscaler_capability}</p>
          </div>
        </div>
      </div>

      {/* Suggested Conversation Opener (Draft Only) */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-sky-600" />
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Suggested Conversation Opener</h3>
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200">
              Draft Only — Never Sent Automatically
            </span>
          </div>

          <button
            onClick={handleCopyOpener}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-xs font-semibold text-slate-700 transition-colors shadow-xs"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span className="text-emerald-700">Copied to Clipboard!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-slate-500" />
                <span>Copy Opener Draft</span>
              </>
            )}
          </button>
        </div>

        <div className="mt-4 bg-slate-50 border border-slate-200 rounded-lg p-5 font-mono text-xs text-slate-800 whitespace-pre-wrap leading-relaxed">
          {rec.suggested_opener_draft}
        </div>
      </div>

      {/* Recommended Second Contact & Orchestration */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
          <div className="h-8 w-8 rounded-full bg-indigo-100 text-indigo-800 font-bold flex items-center justify-center text-xs">
            2nd
          </div>
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Recommended Next Stakeholder</span>
            <h4 className="text-sm font-bold text-slate-900">
              {secondContact
                ? `${secondContact.full_name} — ${secondContact.current_title}`
                : (account.id === "siemens-ag" ? "Natalia Oropeza — Global Chief Cybersecurity Officer" : "Secondary Stakeholder Mapping Pending")}
            </h4>
          </div>
        </div>

        <p className="text-xs text-slate-700 mt-3 leading-relaxed">
          {rec.why_second_stakeholder}
        </p>
      </div>

      {/* Risks, Unknowns & Additional Info Required */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="bg-amber-50/60 border border-amber-200 rounded-xl p-5 text-xs">
          <div className="flex items-center gap-2 text-amber-900 font-bold mb-2">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            <span>Risks and Unknowns</span>
          </div>
          <p className="text-amber-900/90 whitespace-pre-wrap leading-relaxed">
            {rec.risks_and_unknowns}
          </p>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-xs">
          <div className="flex items-center gap-2 text-slate-900 font-bold mb-2">
            <FileText className="w-4 h-4 text-sky-600" />
            <span>Additional Discovery Required</span>
          </div>
          <p className="text-slate-700 leading-relaxed">
            {rec.additional_info_needed}
          </p>
        </div>
      </div>

      {/* Supporting Evidence Provenance */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex items-center justify-between text-xs">
        <div className="flex items-center gap-2 text-slate-600">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>{rec.supporting_evidence_summary}</span>
        </div>
        <button
          onClick={() => onNavigateToTab("evidence-explorer")}
          className="text-sky-600 hover:text-sky-700 font-semibold shrink-0 ml-4 inline-flex items-center gap-1"
        >
          <span>Audit in Evidence Explorer</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
};
