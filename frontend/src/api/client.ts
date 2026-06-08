import type { Application } from '../types/application'

const BASE = '/api'

export async function fetchApplications(): Promise<Application[]> {
  const res = await fetch(`${BASE}/applications/`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}
