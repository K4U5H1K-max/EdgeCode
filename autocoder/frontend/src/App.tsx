import './styles/globals.css'
import React from 'react'
import { useUIStore } from './store'
import { Navbar, Sidebar } from './components'
import { GeneratePage, MemoryPage } from './pages'
import ProjectStatus from './components/ProjectStatus'

export function App() {
  const { activeTab, sidebarOpen } = useUIStore()

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Navbar */}
      <Navbar />

      <div className="flex">
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <main
          className={`flex-1 p-6 transition-all ${
            sidebarOpen ? 'lg:ml-0' : 'ml-0'
          }`}
        >
          {activeTab === 'generate' && <GeneratePage />}
          {activeTab === 'memory' && <MemoryPage />}
          {activeTab === 'history' && <ProjectStatus />}
        </main>
      </div>
    </div>
  )
}

export default App
