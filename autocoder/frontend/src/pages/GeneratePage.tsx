import React from 'react'
import { useGenerationStore, useUIStore } from '@/store'
import { useExecutionLogs, useSharedMemory } from '@/hooks/useGeneration'
import {
  PromptInput,
  ProjectSpecDisplay,
  ExecutionLogs,
  AgentStatus,
  GenerationStatus,
} from '@/components'

/**
 * Generate Page - Main generation interface
 */
export default function GeneratePage() {
  const store = useGenerationStore()
  const { logs } = useExecutionLogs(50)
  const { memory } = useSharedMemory()

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      {/* Input and Spec */}
      <div className="lg:col-span-1 space-y-4">
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Describe Your Project</h2>
          <PromptInput />
        </div>

        {store.projectSpec && (
          <div>
            <h2 className="text-lg font-semibold text-white mb-4">Project Specification</h2>
            <ProjectSpecDisplay spec={store.projectSpec} />
          </div>
        )}
      </div>

      {/* Status and Logs */}
      <div className="lg:col-span-2 space-y-4">
        <GenerationStatus status={store.status} currentStage={store.currentStage} error={store.error} />

        <div className="grid grid-cols-1 gap-4">
          <div className="h-96">
            <ExecutionLogs logs={logs} />
          </div>

          {memory?.agents_status && <AgentStatus agentsStatus={memory.agents_status} />}
        </div>

        {store.projectDir && (
          <div className="bg-green-900 border border-green-700 rounded-lg p-4">
            <p className="text-green-200">
              <strong>Project generated at:</strong> {store.projectDir}
            </p>
            <p className="text-green-300 text-sm mt-2">
              Follow the README.md for setup and deployment instructions.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
