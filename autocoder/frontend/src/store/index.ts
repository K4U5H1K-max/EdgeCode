import { create } from 'zustand'

/**
 * Global application state management using Zustand
 */

interface GenerationState {
  projectId: string | null
  projectSpec: any | null
  status: 'idle' | 'generating' | 'completed' | 'error'
  currentStage: string
  logs: any[]
  error: string | null
  projectDir: string | null
}

interface GenerationStore extends GenerationState {
  startGeneration: (projectId: string, spec: any) => void
  updateStatus: (status: string, stage: string) => void
  addLog: (log: any) => void
  setError: (error: string) => void
  setProjectDir: (dir: string) => void
  reset: () => void
}

export const useGenerationStore = create<GenerationStore>((set) => ({
  projectId: null,
  projectSpec: null,
  status: 'idle',
  currentStage: '',
  logs: [],
  error: null,
  projectDir: null,

  startGeneration: (projectId, spec) =>
    set({
      projectId,
      projectSpec: spec,
      status: 'generating',
      logs: [],
      error: null,
    }),

  updateStatus: (status, stage) =>
    set({
      status: status as any,
      currentStage: stage,
    }),

  addLog: (log) =>
    set((state) => ({
      logs: [...state.logs, log],
    })),

  setError: (error) =>
    set({
      status: 'error',
      error,
    }),

  setProjectDir: (dir) =>
    set({
      projectDir: dir,
    }),

  reset: () =>
    set({
      projectId: null,
      projectSpec: null,
      status: 'idle',
      currentStage: '',
      logs: [],
      error: null,
      projectDir: null,
    }),
}))

// Memory state
interface MemoryState {
  memory: any | null
  loading: boolean
  error: string | null
}

interface MemoryStore extends MemoryState {
  setMemory: (memory: any) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useMemoryStore = create<MemoryStore>((set) => ({
  memory: null,
  loading: false,
  error: null,

  setMemory: (memory) => set({ memory }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}))

// UI state
interface UIState {
  sidebarOpen: boolean
  theme: 'light' | 'dark'
  activeTab: string
}

interface UIStore extends UIState {
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
  setActiveTab: (tab: string) => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  theme: 'dark',
  activeTab: 'generate',

  toggleSidebar: () =>
    set((state) => ({
      sidebarOpen: !state.sidebarOpen,
    })),

  setTheme: (theme) => set({ theme }),
  setActiveTab: (tab) => set({ activeTab: tab }),
}))
