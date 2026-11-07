"use client";

import React, { useState, useEffect } from "react";
import { startNewResearch, checkResearchProgress } from "@/lib/api";
import { ResearchProgress } from "@/types";
import { PlusCircle, X, Terminal, CheckCircle2, AlertCircle, ArrowRight, ShieldCheck } from "lucide-react";

interface NewResearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAccountCreated: (accountId: string) => void;
}

export const NewResearchModal: React.FC<NewResearchModalProps> = ({
  isOpen,
  onClose,
  onAccountCreated,
}) => {
  const [companyName, setCompanyName] = useState("");
  const [industry, setIndustry] = useState("");
  const [isExisting, setIsExisting] = useState(false);
  const [activeRun, setActiveRun] = useState<ResearchProgress | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Poll progress if activeRun is running
  useEffect(() => {
    let interval: any = null;
    if (activeRun && activeRun.status === "RUNNING") {
      interval = setInterval(async () => {
        try {
          const updated = await checkResearchProgress(activeRun.run_id);
          setActiveRun(updated);
          if (
            updated.status === "COMPLETED" ||
            updated.status === "PARTIALLY_COMPLETED" ||
            updated.status === "FAILED"
          ) {
            clearInterval(interval);
          }
        } catch (e: any) {
          console.error("Polling error", e);
        }
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [activeRun]);

  if (!isOpen) return null;

  const handleStartResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!companyName.trim()) {
      setError("Please enter a valid company name to initiate research.");
      return;
    }

    setError(null);
    setIsSubmitting(true);
    try {
      const cleanInd = industry.trim();
      const industryPayload =
        !cleanInd || cleanInd.toLowerCase() === "automatic"
          ? undefined
          : cleanInd;

      const res = await startNewResearch({
        company_name: companyName.trim(),
        industry: industryPayload,
        is_existing_customer: isExisting,
      });
      setActiveRun(res);
    } catch (err: any) {
      setError(err.message || "Failed to start research run");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFinish = () => {
    if (activeRun) {
      onAccountCreated(activeRun.account_id);
      setActiveRun(null);
      setCompanyName("");
      setIndustry("");
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 max-w-xl w-full p-6 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <PlusCircle className="w-5 h-5 text-sky-600" />
            <h3 className="text-base font-bold text-slate-900">
              Run Intelligence Pipeline on New Account
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        {!activeRun ? (
          <form onSubmit={handleStartResearch} className="space-y-4 pt-4 text-xs">
            <div className="bg-sky-50 p-3 rounded-lg border border-sky-100 text-sky-800 text-[11px] leading-relaxed">
              <span className="font-bold">Strict Account Isolation: </span>
              AccountIQ separates generic pipeline logic from account-specific evidence. The new company will never inherit Siemens contacts, technologies, or priorities. Unavailable facts will be flagged as UNKNOWN.
            </div>

            <div>
              <label className="font-semibold text-slate-700 block mb-1">Company Legal Name *</label>
              <input
                type="text"
                required
                placeholder="e.g. ABB Ltd, Schneider Electric, BMW Group..."
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2.5 focus:bg-white focus:ring-2 focus:ring-sky-500"
              />
            </div>

            <div>
              <label className="font-semibold text-slate-700 block mb-1">Primary Industry Sector</label>
              <input
                type="text"
                placeholder="e.g. Industrial Automation, Energy, Automotive..."
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                className="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2.5 focus:bg-white focus:ring-2 focus:ring-sky-500"
              />
            </div>

            <div className="flex items-center gap-2 pt-1">
              <input
                type="checkbox"
                id="isExisting"
                checked={isExisting}
                onChange={(e) => setIsExisting(e.target.checked)}
                className="rounded border-slate-300 text-sky-600 focus:ring-sky-500"
              />
              <label htmlFor="isExisting" className="text-xs text-slate-700 select-none">
                Existing Zscaler customer (Evaluate as expansion opportunity rather than new-logo)
              </label>
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <div className="pt-4 border-t border-slate-100 flex items-center justify-end gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-100"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting || !companyName.trim()}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-sky-600 text-white hover:bg-sky-700 disabled:opacity-50 shadow-sm"
              >
                {isSubmitting ? "Starting Research..." : "Run Intelligence Pipeline"}
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-4 pt-4 text-xs">
            {/* Progress Header */}
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-800">
                Pipeline Progress: {activeRun.current_step}
              </span>
              <span className="font-mono font-bold text-sky-700">{activeRun.progress_pct}%</span>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div
                className="bg-sky-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${activeRun.progress_pct}%` }}
              ></div>
            </div>

            {/* Terminal Logs View */}
            <div className="bg-slate-900 rounded-lg p-3.5 font-mono text-[11px] text-slate-200 h-48 overflow-y-auto space-y-1">
              <div className="text-slate-400 flex items-center gap-1.5 pb-1 border-b border-slate-800 mb-2">
                <Terminal className="w-3.5 h-3.5" />
                <span>AccountIQ Execution Stream</span>
              </div>
              {activeRun.logs.map((log, idx) => (
                <div key={idx} className="leading-relaxed">
                  {log}
                </div>
              ))}
              {activeRun.status === "RUNNING" && (
                <div className="text-sky-400 animate-pulse">Running step...</div>
              )}
            </div>

            {/* Completion or Error State */}
            {activeRun.status === "COMPLETED" || activeRun.status === "PARTIALLY_COMPLETED" ? (
              <div className="pt-2 flex items-center justify-between">
                <div className="flex items-center gap-1.5 font-semibold">
                  <CheckCircle2 className={`w-4 h-4 ${activeRun.status === "COMPLETED" ? "text-emerald-700" : "text-amber-600"}`} />
                  <span className={activeRun.status === "COMPLETED" ? "text-emerald-800" : "text-amber-800"}>
                    {activeRun.status === "COMPLETED"
                      ? "Dossier generated successfully!"
                      : "Dossier generated (undisclosed public metrics flagged as UNKNOWN)"}
                  </span>
                </div>
                <button
                  onClick={handleFinish}
                  className="px-4 py-2 text-xs font-bold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 shadow-sm inline-flex items-center gap-1.5"
                >
                  <span>Open Account Intelligence</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            ) : activeRun.status === "FAILED" ? (
              <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs space-y-1">
                <div className="font-semibold flex items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>Research pipeline could not be completed</span>
                </div>
                <div className="text-[11px] text-rose-700 pl-5">
                  {activeRun.error_message || "The research pipeline encountered an error. Please verify the entity name and check backend logs."}
                </div>
              </div>
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
};
