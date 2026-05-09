import axios from 'axios'

const API_BASE = '/api'

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Generate a new project from prompt
 */
export async function generateProject(prompt: string) {
  try {
    const response = await apiClient.post('/generate', { prompt })
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * Get shared memory state
 */
export async function getMemory() {
  try {
    const response = await apiClient.get('/memory')
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * Get generation status
 */
export async function getStatus() {
  try {
    const response = await apiClient.get('/status')
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * Get execution logs
 */
export async function getLogs(limit: number = 50) {
  try {
    const response = await apiClient.get('/logs', { params: { limit } })
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * Reset memory
 */
export async function resetMemory() {
  try {
    const response = await apiClient.post('/reset')
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * List generated projects
 */
export async function listProjects() {
  try {
    const response = await apiClient.get('/projects')
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * List files in a project path
 */
export async function listProjectFiles(projectId: string, path = '') {
  try {
    const response = await apiClient.get(`/projects/${projectId}/files`, { params: { path } })
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

/**
 * Get file content
 */
export async function getProjectFile(projectId: string, path: string) {
  try {
    const response = await apiClient.get(`/projects/${projectId}/file`, { params: { path } })
    return response.data
  } catch (error: any) {
    throw error.response?.data || error.message
  }
}

export default apiClient
