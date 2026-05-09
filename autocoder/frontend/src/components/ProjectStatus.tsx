import React, { useEffect, useState } from 'react'
import { listProjects, listProjectFiles, getProjectFile } from '@/utils/api'
// simple buttons used inline
 
type FileItem = {
  name: string
  path: string
  is_dir: boolean
}

export default function ProjectStatus() {
  const [projects, setProjects] = useState<Array<any>>([])
  const [selectedProject, setSelectedProject] = useState<string | null>(null)
  const [items, setItems] = useState<FileItem[]>([])
  const [selectedFilePath, setSelectedFilePath] = useState<string | null>(null)
  const [fileContent, setFileContent] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadProjects()
  }, [])

  async function loadProjects() {
    try {
      const res = await listProjects()
      setProjects(res.projects || [])
      if (res.projects && res.projects.length > 0) {
        setSelectedProject(res.projects[0].project_id)
        loadFiles(res.projects[0].project_id, '')
      }
    } catch (err) {
      console.error('Failed to load projects', err)
    }
  }

  async function loadFiles(projectId: string, path = '') {
    setLoading(true)
    try {
      const res = await listProjectFiles(projectId, path)
      setItems(res.items || [])
      setSelectedFilePath(null)
      setFileContent(null)
    } catch (err) {
      console.error('Failed to list files', err)
    } finally {
      setLoading(false)
    }
  }

  async function openFile(path: string) {
    if (!selectedProject) return
    setLoading(true)
    try {
      const res = await getProjectFile(selectedProject, path)
      setSelectedFilePath(res.path)
      setFileContent(res.content)
    } catch (err) {
      console.error('Failed to open file', err)
      setFileContent('// Failed to load file')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-[70vh] gap-4">
      {/* Left: project list + file tree */}
      <div className="w-80 bg-slate-900 border border-slate-800 p-3 rounded">
        <h3 className="text-sm text-slate-300 mb-2">Projects</h3>
        <div className="space-y-2 max-h-40 overflow-auto">
          {projects.map((p) => (
            <button
              key={p.project_id}
              className={`w-full text-left px-2 py-1 rounded ${
                selectedProject === p.project_id ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'
              }`}
              onClick={() => {
                setSelectedProject(p.project_id)
                loadFiles(p.project_id, '')
              }}
            >
              {p.name}
            </button>
          ))}
        </div>

        <div className="mt-4">
          <h4 className="text-xs text-slate-400">Files</h4>
          <div className="mt-2 space-y-1 max-h-[42vh] overflow-auto">
            {loading && <div className="text-xs text-slate-400">Loading...</div>}
            {!loading && items.length === 0 && <div className="text-xs text-slate-400">No files</div>}
            {!loading &&
              items.map((it) => (
                <div key={it.path} className="flex items-center justify-between">
                  <button
                    className="text-sm text-left text-slate-200 hover:text-white px-2 py-1 w-full"
                    onClick={() => (it.is_dir ? loadFiles(selectedProject || '', it.path) : openFile(it.path))}
                  >
                    {it.is_dir ? '📁 ' + it.name : '📄 ' + it.name}
                  </button>
                </div>
              ))}
          </div>
        </div>
      </div>

      {/* Center: file viewer */}
      <div className="flex-1 bg-slate-900 border border-slate-800 p-4 rounded flex flex-col">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="text-sm text-slate-300">{selectedFilePath || 'No file selected'}</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => window.location.reload()}
              className="px-3 py-1 bg-blue-600 text-white rounded text-sm"
            >
              Generate project
            </button>
            <button
              onClick={() => window.alert('Open shared memory tab')}
              className="px-3 py-1 bg-slate-700 text-slate-200 rounded text-sm"
            >
              Shared memory
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-auto bg-slate-950 p-3 rounded">
          {selectedFilePath ? (
            <pre className="whitespace-pre-wrap text-sm font-mono text-slate-100">{fileContent}</pre>
          ) : (
            <div className="text-slate-400">Select a file to view its contents</div>
          )}
        </div>
      </div>
    </div>
  )
}
