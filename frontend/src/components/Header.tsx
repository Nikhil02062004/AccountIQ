"use client";

import React from "react";
import { AccountSummary } from "@/types";
import { ShieldCheck, PlusCircle, FileText, CheckCircle2, Building2, ExternalLink } from "lucide-react";

interface HeaderProps {
  accounts: AccountSummary[];
  selectedAccountId: string;
  onSelectAccount: (id: string) => void;
  onOpenNewResearch: () => void;
  onOpenQualityReport: () => void;
  onExportReport: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  accounts,
  selectedAccountId,
  onSelectAccount,
  onOpenNewResearch,
  onOpenQualityReport,
  onExportReport,
}) => {
  const currentAccount = accounts.find((a) => a.id === selectedAccountId);

  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          
          {/* Logo & Product Brand */}
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-sky-600 flex items-center justify-center text-white shadow-sm font-black text-lg tracking-wider">
              IQ
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-900 text-lg tracking-tight">AccountIQ</span>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-100 text-sky-800 border border-sky-200">
                  Enterprise Intelligence
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Evidence-Driven Account & Contact Intelligence for Zscaler Sales
              </p>
            </div>
          </div>

          {/* Account Selector & Controls */}
          <div className="flex flex-wrap items-center gap-2.5 w-full sm:w-auto">
            {/* Account Dropdown */}
            <div className="relative flex-1 sm:w-64">
              <select
                value={selectedAccountId}
                onChange={(e) => onSelectAccount(e.target.value)}
                className="w-full appearance-none bg-slate-50 border border-slate-300 text-slate-800 text-sm font-semibold rounded-lg px-3 py-2 pr-8 hover:border-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:bg-white"
              >
                {accounts.map((acc) => (
                  <option key={acc.id} value={acc.id}>
                    {acc.name} ({acc.is_existing_customer ? "Existing / Expansion" : "Prospect"})
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2.5 text-slate-500 text-xs">
                ▼
              </div>
            </div>

            {/* Quality Report CTA */}
            <button
              onClick={onOpenQualityReport}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 shadow-sm"
              title="Audit Data Quality & Claim Provenance"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Data Quality</span>
            </button>

            {/* Export HTML/PDF Report CTA */}
            <button
              onClick={onExportReport}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 shadow-sm"
              title="Print or Export Complete Sales Dossier"
            >
              <FileText className="w-3.5 h-3.5 text-sky-600" />
              <span>Export Report</span>
            </button>

            {/* Research New Account CTA */}
            <button
              onClick={onOpenNewResearch}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg bg-sky-600 text-white hover:bg-sky-700 shadow-sm transition-colors"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Research Account</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
