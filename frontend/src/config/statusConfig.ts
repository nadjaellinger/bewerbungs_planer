import type { ApplicationStatus } from '../types/application'

// [badgeBg, badgeFg, stripColor, icon (lucide name), label]
type StatusStyle = {
  badgeBg: string
  badgeFg: string
  strip: string
  label: string
}

export const STATUS_STYLES: Record<ApplicationStatus, StatusStyle> = {
  APPLIED:              { badgeBg: '#1e1b4b', badgeFg: '#a5b4fc', strip: '#6366f1', label: 'Beworben' },
  INVITED_FIRST:        { badgeBg: '#451a03', badgeFg: '#fde68a', strip: '#f59e0b', label: 'Interview 1 – Eingeladen' },
  INTERVIEWED_FIRST:    { badgeBg: '#422006', badgeFg: '#fed7aa', strip: '#f59e0b', label: 'Warte auf Feedback' },
  INVITED_SECOND:       { badgeBg: '#451a03', badgeFg: '#fde68a', strip: '#f59e0b', label: 'Interview 2 – Eingeladen' },
  INTERVIEWED_SECOND:   { badgeBg: '#422006', badgeFg: '#fed7aa', strip: '#f59e0b', label: 'Warte auf Feedback' },
  INVITED_THIRD:        { badgeBg: '#451a03', badgeFg: '#fde68a', strip: '#f59e0b', label: 'Interview 3 – Eingeladen' },
  INTERVIEWED_THIRD:    { badgeBg: '#422006', badgeFg: '#fed7aa', strip: '#f59e0b', label: 'Warte auf Feedback' },
  OFFERED:              { badgeBg: '#042f2e', badgeFg: '#5eead4', strip: '#0d9488', label: 'Angebot erhalten' },
  REJECTED:             { badgeBg: '#450a0a', badgeFg: '#fca5a5', strip: '#ef4444', label: 'Abgelehnt' },
  ACCEPTED:             { badgeBg: '#052e16', badgeFg: '#86efac', strip: '#22c55e', label: 'Angenommen' },
  WITHDRAWN:            { badgeBg: '#1e293b', badgeFg: '#64748b', strip: '#475569', label: 'Zurückgezogen' },
}

export const ACTIVE_STATUSES: ApplicationStatus[] = [
  'APPLIED', 'INVITED_FIRST', 'INTERVIEWED_FIRST',
  'INVITED_SECOND', 'INTERVIEWED_SECOND',
  'INVITED_THIRD', 'INTERVIEWED_THIRD',
]
