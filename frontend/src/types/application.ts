// Spiegelt planer/models/application.py und planer/enums/application_status.py

export type ApplicationStatus =
  | 'APPLIED'
  | 'INVITED_FIRST'
  | 'INTERVIEWED_FIRST'
  | 'INVITED_SECOND'
  | 'INTERVIEWED_SECOND'
  | 'INVITED_THIRD'
  | 'INTERVIEWED_THIRD'
  | 'OFFERED'
  | 'REJECTED'
  | 'ACCEPTED'
  | 'WITHDRAWN'

export interface Application {
  id: number
  company: string
  position: string
  url: string | null
  status: ApplicationStatus
  source: string | null
  history: [string, ApplicationStatus][]  // [ISO-date, status]
  comments: string | null
  requires_motivation_letter: boolean
}
