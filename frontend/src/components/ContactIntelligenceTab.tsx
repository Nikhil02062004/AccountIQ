"use client";

import React, { useState } from "react";
import { AccountDetail, Contact } from "@/types";
import {
  Users, Search, Filter, ShieldCheck, ExternalLink,
  Trash2, Mail, Phone, Award, UserCheck, X
} from "lucide-react";
import { deleteContactRecord } from "@/lib/api";

interface ContactIntelligenceTabProps {
  account: AccountDetail;
  onRefreshAccount: () => void;
}

export const ContactIntelligenceTab: React.FC<ContactIntelligenceTabProps> = ({
  account,
  onRefreshAccount,
}) => {
  const [search, setSearch] = useState("");
  const [selectedDept, setSelectedDept] = useState("ALL");
  const [selectedRole, setSelectedRole] = useState("ALL");
  const [selectedInfluence, setSelectedInfluence] = useState("ALL");
  const [selectedReachability, setSelectedReachability] = useState("ALL");
  const [activeModalContact, setActiveModalContact] = useState<Contact | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // Filter contacts
  const filteredContacts = account.contacts.filter((c) => {
    const matchesSearch =
      search === "" ||
      c.full_name.toLowerCase().includes(search.toLowerCase()) ||
      c.current_title.toLowerCase().includes(search.toLowerCase()) ||
      c.department.toLowerCase().includes(search.toLowerCase());

    const matchesDept =
      selectedDept === "ALL" || c.department.toLowerCase().includes(selectedDept.toLowerCase());
    const matchesRole = selectedRole === "ALL" || c.buying_role === selectedRole;
    const matchesInfluence = selectedInfluence === "ALL" || c.influence_level === selectedInfluence;
    const matchesReach = selectedReachability === "ALL" || c.reachability_status === selectedReachability;

    return matchesSearch && matchesDept && matchesRole && matchesInfluence && matchesReach;
  });

  const handleDeleteContact = async (contactId: string) => {
    if (!confirm("Are you sure you want to permanently delete this contact record under GDPR/PDPA data subject erasure rights?")) {
      return;
    }
    try {
      setIsDeleting(true);
      await deleteContactRecord(contactId);
      setActiveModalContact(null);
      onRefreshAccount();
    } catch (e: any) {
      alert("Error deleting contact: " + e.message);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header and Controls */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5 text-sky-600" />
              <h2 className="text-base font-bold text-slate-900 tracking-tight">Enterprise Buying Committee Intelligence</h2>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Identified and verified {account.contacts.length} key stakeholders with transparent buying role hypotheses and public provenance.
            </p>
          </div>

          {/* Search Box */}
          <div className="relative w-full lg:w-72">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search by name, title, or dept..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 focus:bg-white"
            />
          </div>
        </div>

        {/* Filter Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4">
          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Department</label>
            <select
              value={selectedDept}
              onChange={(e) => setSelectedDept(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-300 rounded-md p-1.5"
            >
              <option value="ALL">All Departments</option>
              <option value="IT Leadership">IT Leadership</option>
              <option value="Cybersecurity">Cybersecurity</option>
              <option value="Executive Board">Executive Board</option>
              <option value="Procurement">Procurement</option>
              <option value="Digital Industries">Digital Industries</option>
              <option value="Software">Software</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Buying Role</label>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-300 rounded-md p-1.5"
            >
              <option value="ALL">All Buying Roles</option>
              <option value="CHAMPION">Champion</option>
              <option value="TECHNICAL_DECISION_MAKER">Technical Decision Maker</option>
              <option value="ECONOMIC_BUYER">Economic Buyer</option>
              <option value="BLOCKER">Blocker / Security Gatekeeper</option>
              <option value="PROCUREMENT_APPROVER">Procurement Approver</option>
              <option value="INFLUENCER">Influencer</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Influence Level</label>
            <select
              value={selectedInfluence}
              onChange={(e) => setSelectedInfluence(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-300 rounded-md p-1.5"
            >
              <option value="ALL">All Influence Levels</option>
              <option value="HIGH">High Influence</option>
              <option value="MEDIUM">Medium Influence</option>
              <option value="LOW">Low Influence</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] font-semibold text-slate-500 uppercase block mb-1">Reachability</label>
            <select
              value={selectedReachability}
              onChange={(e) => setSelectedReachability(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-300 rounded-md p-1.5"
            >
              <option value="ALL">All Reachability</option>
              <option value="PUBLIC_PROFILE_ONLY">Public Profile Only</option>
              <option value="VERIFIED_PUBLIC_CHANNEL">Verified Public Channel</option>
              <option value="UNKNOWN">Unknown</option>
            </select>
          </div>
        </div>
      </div>

      {/* Stakeholders Table */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                <th className="py-3 px-4">Stakeholder</th>
                <th className="py-3 px-4">Department &amp; Unit</th>
                <th className="py-3 px-4">Buying Role Hypothesis</th>
                <th className="py-3 px-4">Influence</th>
                <th className="py-3 px-4">Reachability Status</th>
                <th className="py-3 px-4">Relevance</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredContacts.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900 text-sm">{c.full_name}</div>
                    <div className="text-[11px] text-slate-600">{c.current_title}</div>
                    <div className="text-[10px] text-slate-400 mt-0.5">{c.geography || "Germany"}</div>
                  </td>

                  <td className="py-3.5 px-4">
                    <div className="font-medium text-slate-800">{c.department}</div>
                    {c.business_unit && <div className="text-[10px] text-slate-500">{c.business_unit}</div>}
                  </td>

                  <td className="py-3.5 px-4">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      c.buying_role === "CHAMPION"
                        ? "bg-emerald-100 text-emerald-800"
                        : c.buying_role === "TECHNICAL_DECISION_MAKER"
                        ? "bg-sky-100 text-sky-800"
                        : c.buying_role === "ECONOMIC_BUYER"
                        ? "bg-purple-100 text-purple-800"
                        : c.buying_role === "BLOCKER"
                        ? "bg-rose-100 text-rose-800"
                        : c.buying_role === "PROCUREMENT_APPROVER"
                        ? "bg-amber-100 text-amber-800"
                        : "bg-slate-100 text-slate-700"
                    }`}>
                      {c.buying_role.replace("_", " ")}
                    </span>
                  </td>

                  <td className="py-3.5 px-4">
                    <span className={`text-[11px] font-semibold ${
                      c.influence_level === "HIGH" ? "text-slate-900 font-bold" : "text-slate-500"
                    }`}>
                      {c.influence_level}
                    </span>
                  </td>

                  <td className="py-3.5 px-4">
                    <span className="inline-flex items-center gap-1 text-[11px] font-medium text-slate-600">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{c.reachability_status.replace("_", " ")}</span>
                    </span>
                  </td>

                  <td className="py-3.5 px-4">
                    <div className="font-mono font-bold text-sky-700 text-xs">
                      {c.relevance_score}/100
                    </div>
                  </td>

                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => setActiveModalContact(c)}
                      className="px-2.5 py-1 text-xs font-semibold rounded bg-sky-50 text-sky-700 hover:bg-sky-100 border border-sky-200 transition-colors"
                    >
                      Inspect Profile
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Stakeholder Details Drawer / Modal */}
      {activeModalContact && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
          <div className="bg-white rounded-xl shadow-xl border border-slate-200 max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between pb-4 border-b border-slate-100">
              <div>
                <span className="px-2.5 py-0.5 text-[10px] font-bold rounded-full bg-sky-100 text-sky-800 uppercase tracking-wide">
                  {activeModalContact.buying_role.replace("_", " ")}
                </span>
                <h3 className="text-xl font-bold text-slate-900 mt-1">{activeModalContact.full_name}</h3>
                <p className="text-xs text-slate-600">{activeModalContact.current_title}</p>
                <div className="text-xs text-slate-400 mt-0.5">{activeModalContact.department} • {activeModalContact.geography}</div>
              </div>
              <button
                onClick={() => setActiveModalContact(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 pt-4 text-xs">
              <div>
                <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Stated Priority &amp; Signal</div>
                <p className="text-slate-800 font-medium mt-1 leading-relaxed">{activeModalContact.stated_priority}</p>
              </div>

              {activeModalContact.quote_excerpt && (
                <div className="bg-slate-50 p-3 rounded-lg border-l-4 border-sky-500 italic text-slate-700">
                  "{activeModalContact.quote_excerpt}"
                </div>
              )}

              <div>
                <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Why This Topic Matters to Them</div>
                <p className="text-slate-700 mt-1 leading-relaxed">{activeModalContact.why_matters}</p>
              </div>

              <div className="bg-sky-50 p-3.5 rounded-lg border border-sky-100">
                <div className="font-bold text-sky-900 uppercase tracking-wide text-[10px]">Relevant Zscaler Value Proposition</div>
                <p className="text-sky-800 mt-1 leading-relaxed">{activeModalContact.zscaler_value_prop}</p>
              </div>

              <div>
                <div className="font-semibold text-slate-500 uppercase tracking-wide text-[10px]">Areas of Responsibility</div>
                <p className="text-slate-700 mt-1 leading-relaxed">{activeModalContact.areas_of_responsibility}</p>
              </div>

              {/* Public Reachability Links */}
              <div className="pt-3 border-t border-slate-100 flex flex-wrap gap-2">
                {activeModalContact.official_profile_url && (
                  <a
                    href={activeModalContact.official_profile_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 font-medium"
                  >
                    <span>Public Professional Profile</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
                {activeModalContact.official_bio_url && (
                  <a
                    href={activeModalContact.official_bio_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 font-medium"
                  >
                    <span>Official Corporate Bio</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>

              {/* Privacy Erasure Action */}
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-400">
                  Last verified: {activeModalContact.last_verified_date} | Provenance weight: {Math.round(activeModalContact.confidence * 100)}%
                </span>
                <button
                  onClick={() => handleDeleteContact(activeModalContact.id)}
                  disabled={isDeleting}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded text-rose-700 hover:bg-rose-50 border border-rose-200 text-xs font-semibold"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>{isDeleting ? "Deleting..." : "Erase Contact (GDPR/PDPA)"}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
