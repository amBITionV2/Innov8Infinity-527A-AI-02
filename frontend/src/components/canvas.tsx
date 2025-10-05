"use client";

import { WorkflowCanvas } from "./workflow/workflow-canvas";
import { AnimatedCoral } from "./animated-coral";
import { useState } from "react";
import type { Project } from "@/contexts/AuthContext";
import { RunQueryAlertDialog } from "./ui/run-query-alert-dialog";
import { toast } from "sonner";
import { useAuth } from "@/contexts/AuthContext";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface CanvasProps {
  project: Project;
}

export function Canvas({ project }: CanvasProps) {
  const { user } = useAuth();

  // Convert workflowState to JSON string for WorkflowCanvas component
  const workflowJson = project.workflowState
    ? JSON.stringify(project.workflowState, null, 2)
    : undefined;

  const [exporting, setExporting] = useState(false);
  const [running, setRunning] = useState(false);
  const [showQueryDialog, setShowQueryDialog] = useState(false);
  const [workflowResult, setWorkflowResult] = useState<string | null>(null);
  const [showResultDialog, setShowResultDialog] = useState(false);

  const handleExport = async () => {
    console.log("Canvas - BUILD button clicked");
    
    if (!project.workflowState) {
      console.error("Canvas - No workflow state");
      toast.error("No workflow to export");
      return;
    }

    if (!user?.uid) {
      console.error("Canvas - User not authenticated");
      toast.error("User not authenticated");
      return;
    }

    try {
      setExporting(true);
      console.log("Canvas - Calling /api/export with:", {
        userId: user.uid,
        projectId: project.id,
        workflowState: project.workflowState,
      });
      
      const res = await fetch("/api/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workflowState: project.workflowState,
          userId: user.uid,
          projectId: project.id,
        }),
      });

      console.log("Canvas - Export API response status:", res.status);
      
      const data = await res.json().catch((err) => {
        console.error("Canvas - Failed to parse response JSON:", err);
        return {};
      });
      
      console.log("Canvas - Export API response data:", data);
      
      if (!res.ok) {
        console.error("Canvas - Export failed:", data);
        toast.error(data?.error || "Export failed");
        return;
      }

      console.log("Canvas - Export successful!");
      toast.success("Workflow built successfully");
    } catch (e: any) {
      console.error("Canvas - Export error:", e);
      toast.error(e?.message || "Export failed");
    } finally {
      setExporting(false);
    }
  };

  const handleRun = () => {
    setShowQueryDialog(true);
  };

  const handleQuerySubmit = async (query: string) => {
    console.log("Canvas - RUN button - Query submitted:", query);
    
    if (!user?.uid) {
      console.error("Canvas - RUN - User not authenticated");
      toast.error("User not authenticated");
      return;
    }

    try {
      setRunning(true);
      console.log("Canvas - RUN - Calling /api/deploy with:", {
        query,
        userId: user.uid,
        projectId: project.id,
      });
      
      const res = await fetch("/api/deploy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          userId: user.uid,
          projectId: project.id,
        }),
      });

      console.log("Canvas - RUN - Deploy API response status:", res.status);
      
      const data = await res.json().catch((err) => {
        console.error("Canvas - RUN - Failed to parse response:", err);
        return {};
      });
      
      console.log("Canvas - RUN - Deploy API response data:", data);
      
      if (!res.ok) {
        console.error("Canvas - RUN - Deploy failed:", data);
        toast.error(data?.error || "Run failed");
        return;
      }

      console.log("Canvas - RUN - Workflow started successfully!");
      
      // Extract and display the result
      const result = data?.data?.result || data?.result;
      if (result) {
        console.log("Canvas - RUN - Agent response:", result);
        setWorkflowResult(result);
        setShowResultDialog(true);
        toast.success("Workflow completed successfully!");
      } else {
        toast.success("Workflow started successfully");
      }
    } catch (e: any) {
      console.error("Canvas - RUN - Error:", e);
      toast.error(e?.message || "Run failed");
    } finally {
      setRunning(false);
      setShowQueryDialog(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-gray-50 h-screen">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold text-gray-900">
              Workflow Canvas
            </h2>
            <span className="text-sm text-gray-500">
              {project.workflowState
                ? "AI agents running on the Coral Protocol"
                : "No workflow created yet"}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleRun}
              disabled={running}
              className="relative px-4 py-[6px] bg-emerald-600 dark:bg-emerald-700 shadow-[0px_0px_0px_2.5px_rgba(255,255,255,0.08)_inset] dark:shadow-[0px_0px_0px_1px_rgba(255,255,255,0.15)_inset] overflow-hidden rounded-full flex justify-center items-center cursor-pointer hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div className="w-full h-full absolute left-0 top-0 bg-gradient-to-b from-[rgba(255,255,255,0)] to-[rgba(0,0,0,0.10)] mix-blend-multiply"></div>
              <span className="text-white text-[13px] font-medium leading-5 font-sans relative z-10">
                {running ? "Running..." : "Run"}
              </span>
            </button>
            <button
              type="button"
              onClick={handleExport}
              disabled={exporting}
              className="relative px-4 py-[6px] bg-slate-600 dark:bg-slate-700 shadow-[0px_0px_0px_2.5px_rgba(255,255,255,0.08)_inset] dark:shadow-[0px_0px_0px_1px_rgba(255,255,255,0.15)_inset] overflow-hidden rounded-full flex justify-center items-center cursor-pointer hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div className="w-full h-full absolute left-0 top-0 bg-gradient-to-b from-[rgba(255,255,255,0)] to-[rgba(0,0,0,0.10)] mix-blend-multiply"></div>
              <span className="text-white text-[13px] font-medium leading-5 font-sans relative z-10">
                {exporting ? "Building..." : "Build"}
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* Canvas Area */}
      <div className="flex-1 overflow-hidden">
        {project.workflowState ? (
          <WorkflowCanvas jsonContent={workflowJson} />
        ) : (
          <AnimatedCoral />
        )}
      </div>

      {/* Query Dialog */}
      <RunQueryAlertDialog
        open={showQueryDialog}
        onOpenChange={setShowQueryDialog}
        onSubmit={handleQuerySubmit}
      />

      {/* Result Dialog */}
      {showResultDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                🎉 Agent Response
              </h3>
              <button
                onClick={() => setShowResultDialog(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            <div className="px-6 py-4 overflow-y-auto flex-1">
              <div className="prose prose-sm max-w-none">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <p className="text-sm text-green-800 font-medium mb-1">
                    ✅ Workflow completed successfully!
                  </p>
                  <p className="text-xs text-green-600">
                    Your agent has processed the request and generated the following response.
                  </p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <div className="prose prose-sm max-w-none text-gray-800">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {workflowResult || ""}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            </div>
            <div className="px-6 py-4 border-t border-gray-200 flex justify-end gap-2">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(workflowResult || "");
                  toast.success("Copied to clipboard!");
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                📋 Copy
              </button>
              <button
                onClick={() => setShowResultDialog(false)}
                className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
