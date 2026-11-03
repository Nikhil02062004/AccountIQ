"use client";

import React, { useState, useEffect } from "react";
import { Header } from "@/components/Header";
import { OverviewTab } from "@/components/OverviewTab";
import { AccountIntelligenceTab } from "@/components/AccountIntelligenceTab";
import { ContactIntelligenceTab } from "@/components/ContactIntelligenceTab";
import { CommitteeMapTab } from "@/components/CommitteeMapTab";
import { RecommendedWayInTab } from "@/components/RecommendedWayInTab";
import { EvidenceExplorerTab } from "@/components/EvidenceExplorerTab";
import { NewResearchModal } from "@/components/NewResearchModal";
import { QualityReportModal } from "@/components/QualityReportModal";
import { fetchAccounts, fetchAccountDetail } from "@/lib/api";
import { AccountSummary, AccountDetail } from "@/types";
import {
  LayoutDashboard, Building2, Users, Network,
  Compass, FileSearch, ShieldCheck, Printer
} from "lucide-react";

export default function Home() {
  const [accounts, setAccounts] = useState<AccountSummary[]>([]);
  const [selectedAccountId, setSelectedAccountId] = useState<string>("siemens-ag");
  const [accountDetail, setAccountDetail] = useState<AccountDetail | null>(null);
  const [activeTab, setActiveTab] = useState<string>("overview");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Modals
  const [isNewResearchOpen, setIsNewResearchOpen] = useState(false);
  const [isQualityReportOpen, setIsQualityReportOpen] = useState(false);

  // Initial accounts fetch
  const loadAccounts = async () => {
    try {
      const accList = await fetchAccounts();
      setAccounts(accList);
      if (accList.length > 0 && !accList.some((a) => a.id === selectedAccountId)) {
        setSelectedAccountId(accList[0].id);
      }
    } catch (err: any) {
      console.error("Error loading accounts:", err);
      setError("Unable to connect to AccountIQ backend. Please ensure the backend server is running on port 8000.");
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  // Fetch account details when selectedAccountId changes
  const loadAccountDetail = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const detail = await fetchAccountDetail(id);
      setAccountDetail(detail);
    } catch (err: any) {
      console.error(`Error loading account ${id}:`, err);
      setError(`Failed to retrieve dossier for account ${id}.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedAccountId) {
      loadAccountDetail(selectedAccountId);
    }
  }, [selectedAccountId]);

  const handleAccountCreated = async (newAccountId: string) => {
    await loadAccounts();
    setSelectedAccountId(newAccountId);
    setActiveTab("overview");
  };

  const handleExportReport = () => {
    const exportUrl = `http://127.0.0.1:8000/api/accounts/${selectedAccountId}/export-report`;
    window.open(exportUrl, "_blank");
  };

  const navTabs = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "account-intelligence", label: "Account Intelligence", icon: Building2 },
    { id: "contact-intelligence", label: "Contact Intelligence", icon: Users },
    { id: "buying-committee", label: "Buying Committee Map", icon: Network },
    { id: "recommended-way-in", label: "Recommended Way In", icon: Compass, highlighted: true },
    { id: "evidence-explorer", label: "Evidence Explorer", icon: FileSearch },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      
      {/* Top Navigation & Account Bar */}
      <Header
        accounts={accounts}
        selectedAccountId={selectedAccountId}
        onSelectAccount={(id) => setSelectedAccountId(id)}
        onOpenNewResearch={() => setIsNewResearchOpen(true)}
        onOpenQualityReport={() => setIsQualityReportOpen(true)}
        onExportReport={handleExportReport}
      />

      {/* Screen Tabs Bar */}
      <div className="bg-white border-b border-slate-200 sticky top-[65px] z-30 shadow-2xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-1 sm:space-x-4 overflow-x-auto py-2.5 scrollbar-none" aria-label="Tabs">
            {navTabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                    isActive
                      ? tab.highlighted
                        ? "bg-sky-600 text-white shadow-xs"
                        : "bg-slate-900 text-white shadow-xs"
                      : tab.highlighted
                      ? "text-sky-700 bg-sky-50 hover:bg-sky-100"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                  {tab.highlighted && (
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading ? (
          <div className="h-96 flex flex-col items-center justify-center">
            <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-sky-500 border-t-transparent mb-3"></div>
            <p className="text-sm font-medium text-slate-600">Retrieving Account &amp; Contact Intelligence Dossier...</p>
          </div>
        ) : error ? (
          <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center max-w-lg mx-auto">
            <h3 className="text-sm font-bold text-rose-800">Connection Error</h3>
            <p className="text-xs text-rose-700 mt-2">{error}</p>
            <button
              onClick={() => loadAccountDetail(selectedAccountId)}
              className="mt-4 px-4 py-2 text-xs font-semibold bg-rose-600 text-white rounded-lg hover:bg-rose-700 shadow-sm"
            >
              Retry Connection
            </button>
          </div>
        ) : accountDetail ? (
          <div>
            {activeTab === "overview" && (
              <OverviewTab
                account={accountDetail}
                onNavigateToTab={(tab) => setActiveTab(tab)}
              />
            )}
            {activeTab === "account-intelligence" && (
              <AccountIntelligenceTab account={accountDetail} />
            )}
            {activeTab === "contact-intelligence" && (
              <ContactIntelligenceTab
                account={accountDetail}
                onRefreshAccount={() => loadAccountDetail(selectedAccountId)}
              />
            )}
            {activeTab === "buying-committee" && (
              <CommitteeMapTab accountId={accountDetail.id} />
            )}
            {activeTab === "recommended-way-in" && (
              <RecommendedWayInTab
                account={accountDetail}
                onNavigateToTab={(tab) => setActiveTab(tab)}
              />
            )}
            {activeTab === "evidence-explorer" && (
              <EvidenceExplorerTab accountId={accountDetail.id} />
            )}
          </div>
        ) : null}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-4 text-xs text-slate-500 text-center">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            AccountIQ — Enterprise Intelligence Platform POC | Built for Zscaler Sales Teams
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <span>Main Account: <strong>Siemens AG (Expansion)</strong></span>
            <span>•</span>
            <span>0% Data Fabrication</span>
            <span>•</span>
            <span>GDPR/PDPA Compliant</span>
          </div>
        </div>
      </footer>

      {/* Modals */}
      <NewResearchModal
        isOpen={isNewResearchOpen}
        onClose={() => setIsNewResearchOpen(false)}
        onAccountCreated={handleAccountCreated}
      />

      <QualityReportModal
        accountId={selectedAccountId}
        isOpen={isQualityReportOpen}
        onClose={() => setIsQualityReportOpen(false)}
      />

    </div>
  );
}
