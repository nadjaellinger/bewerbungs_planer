from nicegui import ui

from planer.models.application import Application
from planer.enums.application_status import ApplicationStatus

# Status badge style: (tailwind-classes, material-icon, german label)
_STATUS_STYLE: dict[ApplicationStatus, tuple[str, str, str]] = {
    ApplicationStatus.APPLIED:              ("bg-blue-100 text-blue-800",       "send",             "Beworben"),
    ApplicationStatus.INVITED_FIRST:        ("bg-amber-100 text-amber-800",     "calendar_today",   "Interview 1 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_FIRST:    ("bg-yellow-100 text-yellow-700",   "hourglass_empty",  "Warte auf Rückmeldung"),
    ApplicationStatus.INVITED_SECOND:       ("bg-amber-200 text-amber-900",     "event",            "Interview 2 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_SECOND:   ("bg-yellow-200 text-yellow-800",   "hourglass_top",    "Warte auf Rückmeldung"),
    ApplicationStatus.INVITED_THIRD:        ("bg-orange-200 text-orange-900",   "event_repeat",     "Interview 3 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_THIRD:    ("bg-orange-100 text-orange-800",   "pending",          "Warte auf Rückmeldung"),
    ApplicationStatus.OFFERED:              ("bg-green-100 text-green-800",     "celebration",      "Angebot erhalten"),
    ApplicationStatus.REJECTED:             ("bg-red-100 text-red-700",         "cancel",           "Abgelehnt"),
    ApplicationStatus.ACCEPTED:             ("bg-emerald-100 text-emerald-800", "check_circle",     "Angenommen"),
    ApplicationStatus.WITHDRAWN:            ("bg-gray-100 text-gray-500",       "undo",             "Zurückgezogen"),
}

_ACTIVE_STATUSES = {
    ApplicationStatus.APPLIED,
    ApplicationStatus.INVITED_FIRST,
    ApplicationStatus.INTERVIEWED_FIRST,
    ApplicationStatus.INVITED_SECOND,
    ApplicationStatus.INTERVIEWED_SECOND,
    ApplicationStatus.INVITED_THIRD,
    ApplicationStatus.INTERVIEWED_THIRD,
}


class Overview:
    def __init__(self, logger):
        self.logger = logger

    def render(self, applications: list[Application]) -> None:
        ui.query("body").style("background: #f1f5f9")
        self._render_header()
        self._render_stats(applications)
        self._render_cards(applications)

    # ------------------------------------------------------------------ header
    def _render_header(self) -> None:
        with ui.element("div").classes(
            "w-full bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6 mb-6 shadow-md"
        ):
            with ui.row().classes("items-center gap-3"):
                ui.icon("work").classes("text-white text-4xl")
                with ui.column().classes("gap-0"):
                    ui.label("Bewerbungsplaner").classes("text-3xl font-bold text-white leading-tight")
                    ui.label("Deine aktuelle Bewerbungsübersicht").classes("text-blue-100 text-sm")

    # ------------------------------------------------------------------- stats
    def _render_stats(self, applications: list[Application]) -> None:
        total    = len(applications)
        active   = sum(1 for a in applications if a.status in _ACTIVE_STATUSES)
        offers   = sum(1 for a in applications if a.status == ApplicationStatus.OFFERED)
        accepted = sum(1 for a in applications if a.status == ApplicationStatus.ACCEPTED)
        rejected = sum(1 for a in applications if a.status == ApplicationStatus.REJECTED)

        with ui.row().classes("flex-wrap gap-4 px-8 mb-6"):
            self._stat_card("Gesamt",     str(total),    "layers",        "#3b82f6", "#eff6ff")
            self._stat_card("Aktiv",      str(active),   "trending_up",   "#6366f1", "#eef2ff")
            self._stat_card("Angebote",   str(offers),   "celebration",   "#22c55e", "#f0fdf4")
            self._stat_card("Angenommen", str(accepted), "check_circle",  "#10b981", "#ecfdf5")
            self._stat_card("Abgelehnt",  str(rejected), "cancel",        "#ef4444", "#fef2f2")

    def _stat_card(self, label: str, value: str, icon: str, icon_color: str, bg: str) -> None:
        with ui.element("div").style(
            f"background:{bg}; min-width:140px;"
        ).classes("flex items-center gap-3 px-5 py-4 rounded-xl border border-white shadow-sm"):
            ui.icon(icon).style(f"color:{icon_color}; font-size:2rem")
            with ui.column().classes("gap-0"):
                ui.label(value).classes("text-2xl font-bold text-gray-800 leading-tight")
                ui.label(label).classes("text-xs text-gray-500 uppercase tracking-wide")

    # ------------------------------------------------------------------- cards
    def _render_cards(self, applications: list[Application]) -> None:
        with ui.element("div").classes("px-8 pb-10"):
            if not applications:
                with ui.element("div").classes("flex flex-col items-center py-20 text-gray-400"):
                    ui.icon("inbox").classes("text-7xl mb-3")
                    ui.label("Keine Bewerbungen vorhanden").classes("text-lg")
                return

            with ui.element("div").classes(
                "grid grid-cols-1 gap-4"
                " sm:grid-cols-2 xl:grid-cols-3"
            ):
                for app in applications:
                    self._application_card(app)

    def _application_card(self, app: Application) -> None:
        badge_cls, icon_name, status_label = _STATUS_STYLE.get(
            app.status, ("bg-gray-100 text-gray-600", "help_outline", app.status.value)
        )
        latest_date = app.history[-1][0].strftime("%d.%m.%Y") if app.history else None

        with ui.card().classes(
            "w-full hover:shadow-xl transition-shadow duration-200"
            " border border-gray-100 rounded-2xl overflow-hidden"
        ).style("background: white"):

            # ---- coloured top strip based on status
            strip_color = self._strip_color(app.status)
            ui.element("div").style(
                f"height:4px; background:{strip_color}; margin:-16px -16px 12px -16px"
            )

            # ---- company + position + badge row
            with ui.row().classes("items-start justify-between gap-2 flex-nowrap"):
                with ui.column().classes("gap-0 flex-1 min-w-0"):
                    ui.label(app.company).classes(
                        "text-lg font-bold text-gray-800 leading-tight"
                    ).style("overflow:hidden; text-overflow:ellipsis; white-space:nowrap")
                    ui.label(app.position).classes("text-sm text-gray-500").style(
                        "overflow:hidden; text-overflow:ellipsis; white-space:nowrap"
                    )

                # status badge
                with ui.row().classes(
                    f"items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold"
                    f" whitespace-nowrap shrink-0 {badge_cls}"
                ):
                    ui.icon(icon_name).style("font-size:0.9rem")
                    ui.label(status_label)

            ui.separator().classes("my-3")

            # ---- detail rows
            with ui.column().classes("gap-1"):
                if latest_date:
                    self._detail_row("event", f"Letzte Aktivität: {latest_date}", "text-gray-600")
                if app.source:
                    self._detail_row("source", f"Quelle: {app.source}", "text-gray-600")
                if app.requires_motivation_letter:
                    self._detail_row(
                        "description",
                        "Motivationsschreiben erforderlich",
                        "text-amber-700",
                        icon_color="#f59e0b",
                    )
                if app.comments:
                    self._detail_row("chat_bubble_outline", app.comments, "text-gray-500 text-xs italic")

            # ---- footer link
            if app.url:
                ui.separator().classes("mt-3 mb-2")
                with ui.row().classes("justify-end"):
                    ui.link("Stellenanzeige öffnen ↗", target=app.url, new_tab=True).classes(
                        "text-xs text-blue-600 hover:text-blue-800 font-medium"
                    )

    @staticmethod
    def _detail_row(icon: str, text: str, text_cls: str, icon_color: str = "#9ca3af") -> None:
        with ui.row().classes("items-start gap-2"):
            ui.icon(icon).style(f"color:{icon_color}; font-size:1rem; margin-top:1px")
            ui.label(text).classes(f"text-sm {text_cls}").style(
                "display:-webkit-box; -webkit-line-clamp:2;"
                " -webkit-box-orient:vertical; overflow:hidden"
            )

    @staticmethod
    def _strip_color(status: ApplicationStatus) -> str:
        mapping = {
            ApplicationStatus.APPLIED:              "#3b82f6",
            ApplicationStatus.INVITED_FIRST:        "#f59e0b",
            ApplicationStatus.INTERVIEWED_FIRST:    "#eab308",
            ApplicationStatus.INVITED_SECOND:       "#f59e0b",
            ApplicationStatus.INTERVIEWED_SECOND:   "#eab308",
            ApplicationStatus.INVITED_THIRD:        "#f97316",
            ApplicationStatus.INTERVIEWED_THIRD:    "#f97316",
            ApplicationStatus.OFFERED:              "#22c55e",
            ApplicationStatus.REJECTED:             "#ef4444",
            ApplicationStatus.ACCEPTED:             "#10b981",
            ApplicationStatus.WITHDRAWN:            "#9ca3af",
        }
        return mapping.get(status, "#9ca3af")
