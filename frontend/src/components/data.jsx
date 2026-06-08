// data.jsx — status metadata + sample applications for Bewerbungsplaner
import { useState, useEffect } from 'react'

// ApplicationStatus enum -> German label, short code, color role, pipeline stage
const STATUS_META = {
  APPLIED:            { label: "Beworben",                      short: "BEWORBEN",   role: "neutral", stage: 1, group: "active" },
  INVITED_FIRST:      { label: "1. Gespräch · eingeladen",      short: "1.GESPR ▸",  role: "invite",  stage: 2, group: "active" },
  INTERVIEWED_FIRST:  { label: "1. Gespräch · warte auf Feedback", short: "1.GESPR ⧖", role: "wait",  stage: 3, group: "active" },
  INVITED_SECOND:     { label: "2. Gespräch · eingeladen",      short: "2.GESPR ▸",  role: "invite",  stage: 4, group: "active" },
  INTERVIEWED_SECOND: { label: "2. Gespräch · warte auf Feedback", short: "2.GESPR ⧖", role: "wait",  stage: 5, group: "active" },
  INVITED_THIRD:      { label: "3. Gespräch · eingeladen",      short: "3.GESPR ▸",  role: "invite",  stage: 6, group: "active" },
  INTERVIEWED_THIRD:  { label: "3. Gespräch · warte auf Feedback", short: "3.GESPR ⧖", role: "wait",  stage: 7, group: "active" },
  OFFERED:            { label: "Angebot erhalten",              short: "ANGEBOT",    role: "offer",   stage: 8, group: "won" },
  ACCEPTED:           { label: "Angenommen",                    short: "ANGENOMMEN", role: "accept",  stage: 9, group: "won" },
  REJECTED:           { label: "Abgelehnt",                     short: "ABGELEHNT",  role: "reject",  stage: 0, group: "closed" },
  WITHDRAWN:          { label: "Zurückgezogen",                 short: "ZURÜCKGEZ.", role: "muted",   stage: 0, group: "closed" },
};

const STATUS_ORDER = Object.keys(STATUS_META);

const STATUS_BY_VALUE = {
  "Applied": "APPLIED",
  "Invited to first interview": "INVITED_FIRST",
  "Waiting for feedback after first interview": "INTERVIEWED_FIRST",
  "Invited to second interview": "INVITED_SECOND",
  "Waiting for feedback after second interview": "INTERVIEWED_SECOND",
  "Invited to third interview": "INVITED_THIRD",
  "Waiting for feedback after third interview": "INTERVIEWED_THIRD",
  "Offered": "OFFERED",
  "Rejected": "REJECTED",
  "Accepted": "ACCEPTED",
  "Withdrawn": "WITHDRAWN",
};

// role -> CSS custom prop holding the hue color (defined in theme)
const ROLE_COLOR = {
  neutral: "var(--c-dim)",
  invite:  "var(--c-cyan)",
  wait:    "var(--c-amber)",
  offer:   "var(--c-green)",
  accept:  "var(--c-green)",
  reject:  "var(--c-red)",
  muted:   "var(--c-mute)",
};

function statusColor(status) {
  const m = STATUS_META[status];
  return m ? ROLE_COLOR[m.role] : "var(--c-dim)";
}

// helper to build a history list
function H(...pairs) {
  // pairs: [ "2026-04-01", "APPLIED" ], ...
  return pairs.map(([d, s]) => [d, s]);
}

const SAMPLE_APPLICATIONS = [
  {
    id: 1, company: "Helios Systems", position: "Backend Engineer (Python)",
    url: "https://helios-systems.example/careers/be-py",
    status: "INTERVIEWED_SECOND", source: "LinkedIn",
    history: H(["2026-03-12","APPLIED"],["2026-03-20","INVITED_FIRST"],["2026-03-28","INTERVIEWED_FIRST"],["2026-04-08","INVITED_SECOND"],["2026-04-16","INTERVIEWED_SECOND"]),
    comments: "Team wirkte sehr stark. Zweites Gespräch lief gut — Tech-Lead fragt nach Referenzen.",
    requires_motivation_letter: false,
  },
  {
    id: 2, company: "Nordlicht GmbH", position: "Data Engineer",
    url: "https://nordlicht.example/jobs/data-eng",
    status: "OFFERED", source: "Empfehlung",
    history: H(["2026-02-28","APPLIED"],["2026-03-06","INVITED_FIRST"],["2026-03-13","INTERVIEWED_FIRST"],["2026-03-21","OFFERED"]),
    comments: "Angebot: 72k + Bonus. Frist bis 20.04. Verhandeln?",
    requires_motivation_letter: true,
  },
  {
    id: 3, company: "Brightloop", position: "Full-Stack Developer",
    url: "https://brightloop.example/careers",
    status: "APPLIED", source: "Stepstone",
    history: H(["2026-04-02","APPLIED"]),
    comments: null,
    requires_motivation_letter: false,
  },
  {
    id: 4, company: "Veridian Labs", position: "ML Engineer",
    url: "https://veridian.example/join/ml",
    status: "REJECTED", source: "Firmenwebsite",
    history: H(["2026-02-10","APPLIED"],["2026-02-18","INVITED_FIRST"],["2026-02-25","INTERVIEWED_FIRST"],["2026-03-05","REJECTED"]),
    comments: "Absage nach erstem Gespräch — zu wenig Erfahrung mit PyTorch genannt.",
    requires_motivation_letter: true,
  },
  {
    id: 5, company: "Kestrel Analytics", position: "Platform Engineer",
    url: null,
    status: "INVITED_FIRST", source: "Xing",
    history: H(["2026-04-05","APPLIED"],["2026-04-14","INVITED_FIRST"]),
    comments: "Erstes Gespräch am 22.04 um 14:00, remote.",
    requires_motivation_letter: false,
  },
  {
    id: 6, company: "Aurora Cloud", position: "Site Reliability Engineer",
    url: "https://auroracloud.example/sre",
    status: "INTERVIEWED_THIRD", source: "LinkedIn",
    history: H(["2026-01-20","APPLIED"],["2026-01-29","INVITED_FIRST"],["2026-02-05","INTERVIEWED_FIRST"],["2026-02-14","INVITED_SECOND"],["2026-02-22","INTERVIEWED_SECOND"],["2026-03-04","INVITED_THIRD"],["2026-03-12","INTERVIEWED_THIRD"]),
    comments: "Finale Runde mit VP Eng. Sehr lange Pipeline.",
    requires_motivation_letter: false,
  },
  {
    id: 7, company: "Mosaik Studio", position: "Frontend Engineer",
    url: "https://mosaik.example/jobs/fe",
    status: "ACCEPTED", source: "Empfehlung",
    history: H(["2025-12-01","APPLIED"],["2025-12-09","INVITED_FIRST"],["2025-12-16","INTERVIEWED_FIRST"],["2025-12-22","OFFERED"],["2026-01-04","ACCEPTED"]),
    comments: "Angenommen! Start 01.03. (Als Vergleichsreferenz behalten.)",
    requires_motivation_letter: false,
  },
  {
    id: 8, company: "Tessellate AI", position: "Research Engineer",
    url: "https://tessellate.example/careers/re",
    status: "WITHDRAWN", source: "Firmenwebsite",
    history: H(["2026-02-15","APPLIED"],["2026-02-24","INVITED_FIRST"],["2026-03-02","WITHDRAWN"]),
    comments: "Zurückgezogen — Standort passt nicht (kein Remote).",
    requires_motivation_letter: true,
  },
  {
    id: 9, company: "Polaris Fintech", position: "Backend Engineer",
    url: "https://polaris.example/jobs",
    status: "INVITED_SECOND", source: "Stepstone",
    history: H(["2026-03-18","APPLIED"],["2026-03-25","INVITED_FIRST"],["2026-04-01","INTERVIEWED_FIRST"],["2026-04-10","INVITED_SECOND"]),
    comments: "Pair-Programming-Runde am 24.04.",
    requires_motivation_letter: false,
  },
  {
    id: 10, company: "Grünwald Energy", position: "Software Engineer (IoT)",
    url: null,
    status: "INTERVIEWED_FIRST", source: "Jobmesse",
    history: H(["2026-03-30","APPLIED"],["2026-04-09","INVITED_FIRST"],["2026-04-15","INTERVIEWED_FIRST"]),
    comments: "Nette Leute auf der Messe getroffen. Warte auf Rückmeldung.",
    requires_motivation_letter: true,
  },
  {
    id: 11, company: "Cobalt & Co.", position: "DevOps Engineer",
    url: "https://cobalt.example/careers/devops",
    status: "APPLIED", source: "LinkedIn",
    history: H(["2026-04-11","APPLIED"]),
    comments: null,
    requires_motivation_letter: false,
  },
  {
    id: 12, company: "Lumen Robotics", position: "Embedded Software Engineer",
    url: "https://lumen-robotics.example/jobs/embedded",
    status: "REJECTED", source: "Xing",
    history: H(["2026-01-08","APPLIED"],["2026-01-30","REJECTED"]),
    comments: "Standardabsage, keine Begründung.",
    requires_motivation_letter: false,
  },
];

export { STATUS_META, STATUS_ORDER, ROLE_COLOR, statusColor, SAMPLE_APPLICATIONS }

function normalizeStatus(status) {
  if (STATUS_META[status]) return status;
  return STATUS_BY_VALUE[status] || "APPLIED";
}

function normalizeApp(a) {
  return {
    ...a,
    status: normalizeStatus(a.status),
    history: (a.history || []).map(([d, s]) => [d, normalizeStatus(s)]),
  };
}

// Hook: Daten von der FastAPI laden, mit Fallback auf SAMPLE_APPLICATIONS
export function useApplications() {
  const [apps, setApps] = useState(() => SAMPLE_APPLICATIONS.map(a => ({ ...a })))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    fetch('/api/applications/')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() })
      .then(data => {
        // API liefert history als [[iso-string, status], ...]
        setApps(data.map(normalizeApp))
        setError(null)
      })
      .catch(err => {
        console.warn('API nicht erreichbar, nutze Beispieldaten:', err.message)
        setError(err.message)
      })
      .finally(() => setLoading(false))
  }, [])

  return { apps, setApps, loading, error }
};
