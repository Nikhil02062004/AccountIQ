"use client";

import React, { useState, useEffect } from "react";
import { fetchQualityReport } from "@/lib/api";
import { QualityReport } from "@/types";
import { ShieldCheck, X, CheckCircle2, AlertTriangle, HelpCircle, FileText } from "lucide-react";

interface QualityReportModalProps {
  accountId: string;
  isOpen: boolean;
  onClose: () => void;
}

export const QualityReportModal: React.FC<QualityReportModalProps> = ({
  accountId,
  isOpen,
  onClose,
}) => {
  const [report, setReport] = useState<QualityReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetchQualityReport(accountId)
        .then((res) => {
          setReport(res);
          setLoading(false);
        })
        .catch((err) => {
          console.error("Failed to load quality report", err);
          setLoading(false);
        });
    }
  }, [isOpen, accountId]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
            <h3 className="text-base font-bold text-slate-900">
              Audit Data Quality &amp; Precision Report
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        {loading || !report ? (
          <div className="p-12 text-center text-xs text-slate-500">
            Calculating data precision &amp; provenance audit metrics...
          </div>
        ) : (
          <div className="space-y-5 pt-4 text-xs">
            {/* Measured Verification Rate Card */}
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800">Measured Verification Rate</span>
                <div className="text-3xl font-extrabold text-emerald-700 mt-0.5">
                  {report.verification_rate}%
                </div>
                <div className="text-[11px] text-emerald-900/80 mt-1">
                  {report.verified_claims} Verified + {report.corroborated_claims} Corroborated / {report.total_claims} Total Claims
                </div>
              </div>
              <div className="text-right max-w-xs text-[11px] text-emerald-900 leading-relaxed">
                Strict adherence to Part 11: no synthetic precision percentages. Grounded directly in primary disclosures.
              </div>
            </div>

            {/* Claims Breakdown Grid */}
            <div>
              <h4 className="font-bold text-slate-800 uppercase tracking-wide text-[11px] mb-2.5">
                Claims Integrity Breakdown
              </h4>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                  <div className="text-slate-500 text-[10px] font-semibold uppercase">Total Claims</div>
                  <div className="text-lg font-bold text-slate-900 mt-0.5">{report.total_claims}</div>
                </div>

                <div className="p-3 rounded-lg border border-emerald-200 bg-emerald-50/50">
                  <div className="text-emerald-700 text-[10px] font-semibold uppercase">Directly Verified</div>
                  <div className="text-lg font-bold text-emerald-800 mt-0.5">{report.verified_claims}</div>
                </div>

                <div className="p-3 rounded-lg border border-sky-200 bg-sky-50/50">
                  <div className="text-sky-700 text-[10px] font-semibold uppercase">Corroborated</div>
                  <div className="text-lg font-bold text-sky-800 mt-0.5">{report.corroborated_claims}</div>
                </div>

                <div className="p-3 rounded-lg border border-indigo-200 bg-indigo-50/50">
                  <div className="text-indigo-700 text-[10px] font-semibold uppercase">Inferred Claims</div>
                  <div className="text-lg font-bold text-indigo-800 mt-0.5">{report.inferred_claims}</div>
                </div>

                <div className="p-3 rounded-lg border border-amber-200 bg-amber-50/50">
                  <div className="text-amber-700 text-[10px] font-semibold uppercase">Flagged Unknown</div>
                  <div className="text-lg font-bold text-amber-800 mt-0.5">{report.unknown_claims}</div>
                </div>

                <div className="p-3 rounded-lg border border-rose-200 bg-rose-50/50">
                  <div className="text-rose-700 text-[10px] font-semibold uppercase">Preserved Conflicts</div>
                  <div className="text-lg font-bold text-rose-800 mt-0.5">{report.conflicting_claims}</div>
                </div>
              </div>
            </div>

            {/* Stakeholder Quality Grid */}
            <div>
              <h4 className="font-bold text-slate-800 uppercase tracking-wide text-[11px] mb-2.5">
                Stakeholder &amp; Contact Quality
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                  <div className="text-slate-500 text-[10px] font-semibold uppercase">Total Contacts</div>
                  <div className="text-lg font-bold text-slate-900 mt-0.5">{report.total_contacts}</div>
                </div>

                <div className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                  <div className="text-slate-500 text-[10px] font-semibold uppercase">Verified Titles</div>
                  <div className="text-lg font-bold text-slate-900 mt-0.5">{report.contacts_with_verified_titles}</div>
                </div>

                <div className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                  <div className="text-slate-500 text-[10px] font-semibold uppercase">Public Reachability</div>
                  <div className="text-lg font-bold text-slate-900 mt-0.5">{report.contacts_with_verified_reachability}</div>
                </div>
              </div>
            </div>

            {/* Methodology & Denominator Note */}
            <div className="p-3.5 bg-slate-50 rounded-lg border border-slate-200 text-slate-700 text-[11px] leading-relaxed">
              <span className="font-bold text-slate-900">Audit Methodology: </span>
              {report.methodology_notes}
            </div>

            <div className="pt-3 border-t border-slate-100 flex justify-end">
              <button
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-white hover:bg-slate-900 shadow-sm"
              >
                Close Audit Report
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
