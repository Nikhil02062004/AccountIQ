"use client";

import React, { useEffect, useState, useMemo, useCallback } from "react";
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Handle,
  Position,
  NodeProps,
  MarkerType,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { fetchCommitteeGraph } from "@/lib/api";
import { Users, Shield, Award, AlertCircle, ArrowRight } from "lucide-react";

interface CommitteeMapTabProps {
  accountId: string;
}

// Custom React Flow Node for Stakeholders
const StakeholderNode = ({ data }: NodeProps) => {
  const role = (data.buying_role as string) || "INFLUENCER";
  
  const roleBadgeStyle: Record<string, string> = {
    CHAMPION: "bg-emerald-100 text-emerald-800 border-emerald-200",
    TECHNICAL_DECISION_MAKER: "bg-sky-100 text-sky-800 border-sky-200",
    ECONOMIC_BUYER: "bg-purple-100 text-purple-800 border-purple-200",
    BLOCKER: "bg-rose-100 text-rose-800 border-rose-200",
    PROCUREMENT_APPROVER: "bg-amber-100 text-amber-800 border-amber-200",
    INFLUENCER: "bg-slate-100 text-slate-800 border-slate-200",
  };

  return (
    <div className="bg-white border-2 border-slate-200 hover:border-sky-500 rounded-xl shadow-md p-3.5 w-64 text-left transition-all">
      <Handle type="target" position={Position.Top} className="w-2.5 h-2.5 bg-sky-600" />
      
      <div className="flex items-center justify-between mb-1.5">
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${roleBadgeStyle[role] || "bg-slate-100 text-slate-700"}`}>
          {role.replace(/_/g, " ")}
        </span>
        <span className="text-[10px] font-mono font-bold text-sky-700">
          {data.relevance_score as number}/100
        </span>
      </div>

      <div className="font-bold text-slate-900 text-xs truncate">{data.name as string}</div>
      <div className="text-[11px] text-slate-600 line-clamp-1">{data.title as string}</div>
      <div className="text-[10px] text-slate-400 mt-0.5">{data.department as string}</div>

      {Boolean(data.stated_priority) && (
        <div className="mt-2 text-[10px] text-slate-600 bg-slate-50 p-1.5 rounded border border-slate-100 italic line-clamp-2">
          "{data.stated_priority as string}"
        </div>
      )}

      <Handle type="source" position={Position.Bottom} className="w-2.5 h-2.5 bg-sky-600" />
    </div>
  );
};

export const CommitteeMapTab: React.FC<CommitteeMapTabProps> = ({ accountId }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState<any>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<any>([]);
  const [loading, setLoading] = useState(true);
  const [selectedNodeData, setSelectedNodeData] = useState<any | null>(null);

  const nodeTypes = useMemo(() => ({ stakeholderNode: StakeholderNode }), []);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    fetchCommitteeGraph(accountId)
      .then((data) => {
        if (!isMounted) return;
        // Add markers and formatting
        const formattedEdges = data.edges.map((e) => ({
          ...e,
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 14,
            height: 14,
            color: e.style?.stroke || "#0c87eb",
          },
        }));
        setNodes(data.nodes);
        setEdges(formattedEdges);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load committee graph", err);
        setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [accountId]);

  const onNodeClick = useCallback((_: any, node: any) => {
    setSelectedNodeData(node.data);
  }, []);

  if (loading) {
    return (
      <div className="h-[600px] bg-white rounded-xl border border-slate-200 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-sky-500 border-t-transparent mb-2"></div>
          <p className="text-xs text-slate-500">Mapping Buying Committee Relationships &amp; Reporting Lines...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      
      {/* Legend & Instructions */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs">
        <div>
          <span className="font-bold text-slate-900">Buying Committee Relationship Graph</span>
          <p className="text-slate-500 text-[11px] mt-0.5">
            Verified corporate hierarchy and hypothesized influence vectors across IT, Security, and Business Units. Click any card to inspect.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-[11px]">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-sky-600"></span>
            <span className="text-slate-600">Reports To (Verified)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-purple-500 border-dashed"></span>
            <span className="text-slate-600">Influences (Hypothesis)</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <span className="text-slate-600">Champion</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span className="text-slate-600">Blocker / CISO</span>
          </div>
        </div>
      </div>

      {/* Main Graph Canvas */}
      <div className="relative h-[650px] bg-slate-50 rounded-xl border border-slate-200 overflow-hidden shadow-inner">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          onNodeClick={onNodeClick}
          fitView
          attributionPosition="bottom-right"
        >
          <Background color="#cbd5e1" gap={18} size={1} />
          <Controls className="bg-white border border-slate-200 shadow-sm" />
        </ReactFlow>

        {/* Selected Stakeholder Detail Panel */}
        {selectedNodeData && (
          <div className="absolute bottom-4 right-4 max-w-sm w-full bg-white border border-slate-200 rounded-xl p-4 shadow-lg text-xs z-10 transition-all">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <span className="font-bold text-slate-900">{selectedNodeData.name}</span>
              <button
                onClick={() => setSelectedNodeData(null)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>
            <div className="mt-2 text-slate-600 font-medium">{selectedNodeData.title}</div>
            <div className="text-[11px] text-slate-400">{selectedNodeData.department}</div>
            
            <div className="mt-2.5 p-2 bg-slate-50 rounded border border-slate-100">
              <div className="font-bold text-[10px] text-slate-500 uppercase">Stated Priority</div>
              <div className="italic text-slate-700 mt-0.5">"{selectedNodeData.stated_priority || 'No public quote recorded'}"</div>
            </div>

            <div className="mt-2 text-[11px] text-slate-600 flex justify-between">
              <span>Role: <strong>{selectedNodeData.buying_role}</strong></span>
              <span>Relevance: <strong>{selectedNodeData.relevance_score}/100</strong></span>
            </div>
          </div>
        )}
      </div>

    </div>
  );
};
