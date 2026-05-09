import React from 'react'
import { Menu, X, Settings, Zap } from 'lucide-react'
import { useUIStore } from '@/store'

/**
 * Navigation Bar Component
 */
export function Navbar() {
  const { sidebarOpen, toggleSidebar } = useUIStore()

  return (
    <nav className="bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
      <div className="px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-400 hover:text-white"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          <div className="flex items-center gap-2">
            <Zap className="w-6 h-6 text-blue-500" />
            <h1 className="text-xl font-bold text-white">AutoCoder</h1>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-400 hover:text-white">
            <Settings className="w-5 h-5" />
          </button>
        </div>
      </div>
    </nav>
  )
}

/**
 * Sidebar Component
 */
export function Sidebar() {
  const { sidebarOpen, activeTab, setActiveTab } = useUIStore()

  if (!sidebarOpen) return null

  const tabs = [
    { id: 'generate', label: 'Generate Project' },
    { id: 'memory', label: 'Shared Memory' },
    { id: 'history', label: 'Project Status' },
  ]

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-[calc(100vh-60px)]">
      <div className="p-4 flex-1 space-y-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`w-full text-left px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="p-4 border-t border-slate-800">
        <p className="text-xs text-slate-400">
          AutoCoder v1.0.0 • GenAI-powered code generation
        </p>
      </div>
    </aside>
  )
}
