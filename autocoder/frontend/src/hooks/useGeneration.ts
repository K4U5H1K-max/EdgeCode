import { useGenerationStore } from '@/store'
import { useEffect, useState } from 'react'

/**
 * Hook for polling generation status
 */
export function useGenerationStatus() {
  const [isPolling, setIsPolling] = useState(false)
  const store = useGenerationStore()

  useEffect(() => {
    if (!isPolling || store.status !== 'generating') {
      return
    }

    const interval = setInterval(async () => {
      try {
        const response = await fetch('/api/status')
        const status = await response.json()

        if (status.status === 'completed') {
          store.updateStatus('completed', 'Project generation complete')
          setIsPolling(false)
        } else {
          store.updateStatus(status.status, status.status)
        }
      } catch (error) {
        console.error('Failed to fetch status:', error)
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [isPolling, store.status])

  return { isPolling, setIsPolling }
}

/**
 * Hook for polling execution logs
 */
export function useExecutionLogs(limit: number = 50) {
  const [logs, setLogs] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const generationStatus = useGenerationStore((state) => state.status)

  const fetchLogs = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/logs?limit=${limit}`)
      const data = await response.json()
      setLogs(data.logs || [])
      setError(null)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (generationStatus !== 'generating') {
      return
    }

    const interval = setInterval(fetchLogs, 2000)
    fetchLogs() // Initial fetch

    return () => clearInterval(interval)
  }, [limit, generationStatus])

  return { logs, loading, error, refetch: fetchLogs }
}

/**
 * Hook for polling shared memory
 */
export function useSharedMemory() {
  const [memory, setMemory] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const generationStatus = useGenerationStore((state) => state.status)

  const fetchMemory = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/memory')
      const data = await response.json()
      setMemory(data)
      setError(null)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (generationStatus === 'generating') {
      const interval = setInterval(fetchMemory, 3000)
      fetchMemory() // Initial fetch

      return () => clearInterval(interval)
    }

    fetchMemory()
  }, [generationStatus])

  return { memory, loading, error, refetch: fetchMemory }
}
