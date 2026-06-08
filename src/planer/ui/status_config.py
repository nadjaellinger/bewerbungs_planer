from planer.enums.application_status import ApplicationStatus

# (badge_bg, badge_fg, strip_color, icon, label_de)
# Palette: Indigo = Beworben | Amber = Interview-Phasen
#          Teal = Angebot | Green = Angenommen | Red = Abgelehnt | Gray = Zurückgezogen
STATUS: dict[ApplicationStatus, tuple[str, str, str, str, str]] = {
    ApplicationStatus.APPLIED:              ("#1e1b4b", "#a5b4fc", "#6366f1", "send",           "Beworben"),
    ApplicationStatus.INVITED_FIRST:        ("#451a03", "#fde68a", "#f59e0b", "calendar_today", "Interview 1 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_FIRST:    ("#422006", "#fed7aa", "#f59e0b", "hourglass_empty", "Warte auf Feedback"),
    ApplicationStatus.INVITED_SECOND:       ("#451a03", "#fde68a", "#f59e0b", "event",           "Interview 2 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_SECOND:   ("#422006", "#fed7aa", "#f59e0b", "hourglass_top",   "Warte auf Feedback"),
    ApplicationStatus.INVITED_THIRD:        ("#451a03", "#fde68a", "#f59e0b", "event_repeat",    "Interview 3 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_THIRD:    ("#422006", "#fed7aa", "#f59e0b", "pending",         "Warte auf Feedback"),
    ApplicationStatus.OFFERED:              ("#042f2e", "#5eead4", "#0d9488", "celebration",     "Angebot erhalten"),
    ApplicationStatus.REJECTED:             ("#450a0a", "#fca5a5", "#ef4444", "cancel",          "Abgelehnt"),
    ApplicationStatus.ACCEPTED:             ("#052e16", "#86efac", "#22c55e", "check_circle",    "Angenommen"),
    ApplicationStatus.WITHDRAWN:            ("#1e293b", "#64748b", "#475569", "undo",            "Zurückgezogen"),
}

ACTIVE: set[ApplicationStatus] = {
    ApplicationStatus.APPLIED,
    ApplicationStatus.INVITED_FIRST,
    ApplicationStatus.INTERVIEWED_FIRST,
    ApplicationStatus.INVITED_SECOND,
    ApplicationStatus.INTERVIEWED_SECOND,
    ApplicationStatus.INVITED_THIRD,
    ApplicationStatus.INTERVIEWED_THIRD,
}

_FALLBACK: tuple[str, str, str, str, str] = ("#1e293b", "#94a3b8", "#475569", "help", "Unbekannt")


def get(status: ApplicationStatus) -> tuple[str, str, str, str, str]:
    return STATUS.get(status, _FALLBACK)
