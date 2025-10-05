"use client";

import { Sparkles, ListChecks } from "lucide-react";
import { cls } from "../../lib/utils";

export type WorkflowMode = "ai" | "detailed";

interface WorkflowModeSelectorProps {
  mode: WorkflowMode;
  onModeChange: (mode: WorkflowMode) => void;
}

export function WorkflowModeSelector({
  mode,
  onModeChange,
}: WorkflowModeSelectorProps) {
  return (
    <div className="w-full flex flex-col items-center px-4 pt-4 pb-2">
      <div className="w-full max-w-3xl">
        <div className="flex items-center gap-2 p-1 bg-zinc-100 dark:bg-zinc-900 rounded-xl">
          <button
            onClick={() => onModeChange("ai")}
            className={cls(
              "flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200",
              mode === "ai"
                ? "bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm"
                : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white"
            )}
          >
            <Sparkles className="h-4 w-4" />
            <span>Let AI Decide</span>
          </button>
          <button
            onClick={() => onModeChange("detailed")}
            className={cls(
              "flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-medium text-sm transition-all duration-200",
              mode === "detailed"
                ? "bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white shadow-sm"
                : "text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white"
            )}
          >
            <ListChecks className="h-4 w-4" />
            <span>Detailed Setup</span>
          </button>
        </div>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-2 text-center">
          {mode === "ai" ? (
            <>
              <Sparkles className="h-3 w-3 inline mr-1" />
              AI will auto-build your workflow with smart defaults
            </>
          ) : (
            <>
              <ListChecks className="h-3 w-3 inline mr-1" />
              Step-by-step guidance for complete control
            </>
          )}
        </p>
      </div>
    </div>
  );
}

