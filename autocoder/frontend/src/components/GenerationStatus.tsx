import React from 'react'
import { AlertCircle, CheckCircle, Loader, XCircle } from 'lucide-react'

interface LogEntry {
  timestamp: string
  agent: string
  message: string
  level: 'info' | 'error' | 'warning' | 'success'
}

/**
 * Execution Logs Display Component
 */
export function ExecutionLogs({ logs = [] }: { logs: LogEntry[] }) {
  const getLogIcon = (level: string) => {
    switch (level) {
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />
      case 'warning':
        return <AlertCircle className="w-4 h-4 text-yellow-500" />
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      default:
        return <Loader className="w-4 h-4 text-blue-500 animate-spin" />
    }
  }

  const getLogColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'text-red-400'
      case 'warning':
        return 'text-yellow-400'
      case 'success':
        return 'text-green-400'
      default:
        return 'text-slate-300'
    }
  }

  return (
    <div className="h-full flex flex-col bg-slate-900 rounded-lg border border-slate-700">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-700 flex justify-between items-center">
        <h3 className="font-semibold text-white">Execution Logs</h3>
      </div>

      {/* Logs */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-sm">
        {logs.length === 0 ? (
          <div className="text-slate-400 text-center py-8">No logs yet...</div>
        ) : (
          logs.map((log, idx) => (
            <div key={idx} className="flex gap-2 items-start">
              <div className="flex-shrink-0">{getLogIcon(log.level)}</div>
              <div className="flex-1 min-w-0">
                <div className="flex gap-2 text-xs">
                  <span className="text-slate-500">{log.timestamp}</span>
                  <span className="text-slate-400">[{log.agent}]</span>
                </div>
                <p className={`text-xs mt-1 ${getLogColor(log.level)} break-words`}>
                  {log.message}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

/**
 * Agent Status Component
 */
export function AgentStatus({ agentsStatus = {} }: { agentsStatus: any }) {
  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-white mb-3">Agent Status</h3>
      {Object.entries(agentsStatus).map(([agent, status]: [string, any]) => (
        <div key={agent} className="flex items-center justify-between p-3 bg-slate-800 rounded border border-slate-700">
          <span className="text-sm text-white">{agent}</span>
          <div className="flex items-center gap-2">
            <span
              className={`text-xs px-2 py-1 rounded ${
                status.status === 'completed'
                  ? 'bg-green-900 text-green-200'
                  : status.status === 'error'
                  ? 'bg-red-900 text-red-200'
                  : status.status === 'in_progress'
                  ? 'bg-blue-900 text-blue-200'
                  : 'bg-slate-700 text-slate-300'
              }`}
            >
              {status.status}
            </span>
            {status.status === 'in_progress' && <Loader className="w-4 h-4 animate-spin text-blue-500" />}
          </div>
        </div>
      ))}
    </div>
  )
}

/**
 * Generation Status Component
 */
export function GenerationStatus({
  status,
  currentStage,
  error,
}: {
  status: string
  currentStage: string
  error: string | null
}) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
      <div className="flex items-center gap-3 mb-3">
        {status === 'generating' ? (
          <Loader className="w-5 h-5 text-blue-500 animate-spin" />
        ) : status === 'completed' ? (
          <CheckCircle className="w-5 h-5 text-green-500" />
        ) : status === 'error' ? (
          <XCircle className="w-5 h-5 text-red-500" />
        ) : (
          <AlertCircle className="w-5 h-5 text-slate-400" />
        )}
        <div>
          <h3 className="font-semibold text-white">
            {status === 'generating' && 'Generating Project...'}
            {status === 'completed' && 'Project Generated!'}
            {status === 'error' && 'Generation Failed'}
            {status === 'idle' && 'Ready to Generate'}
          </h3>
          {currentStage && <p className="text-sm text-slate-400">{currentStage}</p>}
        </div>
      </div>

      {error && (
        <div className="mt-3 p-3 bg-red-900 border border-red-700 rounded text-red-200 text-sm">
          {error}
        </div>
      )}
    </div>
  )
}
