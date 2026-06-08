from nicegui import ui

from planer.models.application import Application
from planer.enums.application_status import ApplicationStatus
from planer.ui.styles import Theme

# (badge_bg, badge_fg, strip_color, icon, label_de)
_STATUS: dict[ApplicationStatus, tuple[str, str, str, str, str]] = {
    ApplicationStatus.APPLIED:              ("#172554", "#93c5fd", "#3b82f6", "send",           "Beworben"),
    ApplicationStatus.INVITED_FIRST:        ("#451a03", "#fde68a", "#f59e0b", "calendar_today", "Interview 1 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_FIRST:    ("#422006", "#fef08a", "#eab308", "hourglass_empty","Warte auf Feedback"),
    ApplicationStatus.INVITED_SECOND:       ("#451a03", "#fcd34d", "#f59e0b", "event",          "Interview 2 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_SECOND:   ("#422006", "#fef3c7", "#eab308", "hourglass_top",  "Warte auf Feedback"),
    ApplicationStatus.INVITED_THIRD:        ("#431407", "#fdba74", "#f97316", "event_repeat",   "Interview 3 – Eingeladen"),
    ApplicationStatus.INTERVIEWED_THIRD:    ("#431407", "#fed7aa", "#f97316", "pending",        "Warte auf Feedback"),
    ApplicationStatus.OFFERED:              ("#022c22", "#6ee7b7", "#10b981", "celebration",    "Angebot erhalten"),
    ApplicationStatus.REJECTED:             ("#450a0a", "#fca5a5", "#ef4444", "cancel",         "Abgelehnt"),
    ApplicationStatus.ACCEPTED:             ("#022c22", "#34d399", "#059669", "check_circle",   "Angenommen"),
    ApplicationStatus.WITHDRAWN:            ("#1e293b", "#64748b", "#475569", "undo",           "Zurückgezogen"),
}

_ACTIVE: set[ApplicationStatus] = {
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
        ui.dark_mode(value=True)
        ui.query('body').style(f'background:{Theme.PAGE}; color:{Theme.TEXT}')
        self._render_header()
        self._render_stats(applications)
        self._render_toolbar_and_content(applications)

    # ── Header ────────────────────────────────────────────────────────────────
    def _render_header(self) -> None:
        with ui.element('div').style(
            f'background:{Theme.HEADER_GRADIENT}; padding:20px 32px 22px; margin-bottom:20px'
        ):
            with ui.row().classes('items-center gap-3'):
                ui.icon('work').style('color:#a5b4fc; font-size:2.5rem')
                with ui.column().classes('gap-0'):
                    ui.label('Bewerbungsplaner').style(
                        f'color:{Theme.TEXT}; font-size:1.6rem; font-weight:700; line-height:1.2'
                    )
                    ui.label('Deine aktuelle Bewerbungsübersicht').style(
                        'color:#a5b4fc; font-size:0.85rem'
                    )

    # ── Stats ─────────────────────────────────────────────────────────────────
    def _render_stats(self, applications: list[Application]) -> None:
        total    = len(applications)
        active   = sum(1 for a in applications if a.status in _ACTIVE)
        offers   = sum(1 for a in applications if a.status == ApplicationStatus.OFFERED)
        accepted = sum(1 for a in applications if a.status == ApplicationStatus.ACCEPTED)
        rejected = sum(1 for a in applications if a.status == ApplicationStatus.REJECTED)

        with ui.row().classes('flex-wrap gap-3 px-8 mb-5'):
            self._stat_tile('Gesamt',     str(total),    'layers',       *Theme.STAT['total'])
            self._stat_tile('Aktiv',      str(active),   'trending_up',  *Theme.STAT['active'])
            self._stat_tile('Angebote',   str(offers),   'celebration',  *Theme.STAT['offers'])
            self._stat_tile('Angenommen', str(accepted), 'check_circle', *Theme.STAT['accepted'])
            self._stat_tile('Abgelehnt',  str(rejected), 'cancel',       *Theme.STAT['rejected'])

    def _stat_tile(self, label: str, value: str, icon: str, bg: str, icon_color: str) -> None:
        with ui.element('div').style(
            f'background:{bg}; border:1px solid {Theme.BORDER}; '
            'border-radius:12px; padding:12px 18px; min-width:120px; '
            'display:flex; align-items:center; gap:12px'
        ):
            ui.icon(icon).style(f'color:{icon_color}; font-size:1.8rem')
            with ui.column().classes('gap-0'):
                ui.label(value).style(
                    f'color:{Theme.TEXT}; font-size:1.5rem; font-weight:700; line-height:1'
                )
                ui.label(label).style(
                    f'color:{Theme.TEXT_SUB}; font-size:0.7rem; '
                    'text-transform:uppercase; letter-spacing:0.05em'
                )

    # ── Toolbar + Content ─────────────────────────────────────────────────────
    def _render_toolbar_and_content(self, applications: list[Application]) -> None:
        mode = {'view': 'cards'}

        @ui.refreshable
        def content() -> None:
            if mode['view'] == 'cards':
                self._render_cards(applications)
            else:
                self._render_table(applications)

        with ui.row().classes('px-8 mb-3 items-center justify-between w-full'):
            ui.label(f'{len(applications)} Bewerbung(en)').style(
                f'color:{Theme.TEXT_MUTED}; font-size:0.82rem'
            )
            with ui.row().classes('gap-1 items-center'):
                btn_c = (
                    ui.button(icon='grid_view', on_click=lambda: switch('cards'))
                    .props('flat round dense')
                    .style(f'color:{Theme.INDIGO}')
                    .tooltip('Kachelansicht')
                )
                btn_t = (
                    ui.button(icon='table_rows', on_click=lambda: switch('table'))
                    .props('flat round dense')
                    .style(f'color:{Theme.TEXT_MUTED}')
                    .tooltip('Tabellenansicht')
                )

        def switch(v: str) -> None:
            mode['view'] = v
            btn_c.style(f'color:{Theme.INDIGO if v == "cards" else Theme.TEXT_MUTED}')
            btn_t.style(f'color:{Theme.INDIGO if v == "table" else Theme.TEXT_MUTED}')
            content.refresh()

        content()

    # ── Card view ─────────────────────────────────────────────────────────────
    def _render_cards(self, applications: list[Application]) -> None:
        with ui.element('div').classes('px-8 pb-10'):
            if not applications:
                self._empty_state()
                return
            with ui.element('div').style(
                'display:grid; '
                'grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); '
                'gap:14px'
            ):
                for app in applications:
                    self._card(app)

    def _card(self, app: Application) -> None:
        badge_bg, badge_fg, strip, icon, label = _STATUS.get(
            app.status, ('#1e293b', '#94a3b8', '#475569', 'help', app.status.value)
        )
        latest = app.history[-1][0].strftime('%d.%m.%Y') if app.history else None

        with ui.element('div').style(Theme.card()).classes(
            'transition-all duration-200 hover:brightness-110'
        ):
            # colour strip
            ui.element('div').style(f'height:3px; background:{strip}')
            with ui.element('div').style('padding:12px 14px 14px'):
                # company + badge row
                with ui.row().classes('items-start justify-between gap-2 flex-nowrap mb-1'):
                    with ui.column().classes('gap-0 flex-1 min-w-0'):
                        ui.label(app.company).style(
                            f'color:{Theme.TEXT}; font-weight:700; font-size:1rem; '
                            'overflow:hidden; text-overflow:ellipsis; white-space:nowrap'
                        )
                        ui.label(app.position).style(
                            f'color:{Theme.TEXT_SUB}; font-size:0.8rem; '
                            'overflow:hidden; text-overflow:ellipsis; white-space:nowrap'
                        )
                    with ui.row().style(
                        f'background:{badge_bg}; color:{badge_fg}; '
                        'padding:2px 8px; border-radius:999px; '
                        'font-size:0.7rem; font-weight:600; '
                        'align-items:center; gap:3px; white-space:nowrap; flex-shrink:0'
                    ):
                        ui.icon(icon).style('font-size:0.85rem')
                        ui.label(label)

                ui.element('div').style(
                    f'height:1px; background:{Theme.BORDER}; margin:8px 0'
                )

                # details
                with ui.column().classes('gap-1'):
                    if latest:
                        self._detail_row('event', f'Letzte Aktivität: {latest}', Theme.TEXT_SUB)
                    if app.source:
                        self._detail_row('source', f'Quelle: {app.source}', Theme.TEXT_SUB)
                    if app.requires_motivation_letter:
                        self._detail_row(
                            'description', 'Motivationsschreiben', Theme.AMBER, Theme.AMBER
                        )
                    if app.comments:
                        self._detail_row(
                            'chat_bubble_outline', app.comments, Theme.TEXT_MUTED
                        )
                    if app.url:
                        with ui.element('div').style('margin-top:4px'):
                            ui.link('Stellenanzeige ↗', target=app.url, new_tab=True).style(
                                f'color:{Theme.INDIGO}; font-size:0.75rem; text-decoration:none'
                            )

    @staticmethod
    def _detail_row(icon: str, text: str, text_color: str, icon_color: str = '') -> None:
        ic = icon_color if icon_color else Theme.TEXT_MUTED
        with ui.row().classes('items-start gap-2'):
            ui.icon(icon).style(
                f'color:{ic}; font-size:0.9rem; margin-top:1px; flex-shrink:0'
            )
            ui.label(text).style(
                f'color:{text_color}; font-size:0.78rem; '
                'display:-webkit-box; -webkit-line-clamp:1; '
                '-webkit-box-orient:vertical; overflow:hidden'
            )

    # ── Table view ────────────────────────────────────────────────────────────
    def _render_table(self, applications: list[Application]) -> None:
        with ui.element('div').classes('px-8 pb-10'):
            if not applications:
                self._empty_state()
                return

            columns = [
                {'name': 'company',  'label': 'Firma',            'field': 'company',  'sortable': True,  'align': 'left'},
                {'name': 'position', 'label': 'Stelle',            'field': 'position', 'sortable': True,  'align': 'left'},
                {'name': 'status',   'label': 'Status',            'field': 'status',   'sortable': True,  'align': 'left'},
                {'name': 'source',   'label': 'Quelle',            'field': 'source',   'sortable': True,  'align': 'left'},
                {'name': 'date',     'label': 'Letzte Aktivität',  'field': 'date',     'sortable': True,  'align': 'left'},
                {'name': 'letter',   'label': 'Motivationsschr.',  'field': 'letter',   'sortable': False, 'align': 'center'},
            ]

            rows = []
            for app in applications:
                badge_bg, badge_fg, _, _, label = _STATUS.get(
                    app.status, ('#1e293b', '#94a3b8', '', '', app.status.value)
                )
                rows.append({
                    'id':       app.id,
                    'company':  app.company,
                    'position': app.position,
                    'status':   label,
                    'badge_bg': badge_bg,
                    'badge_fg': badge_fg,
                    'source':   app.source or '–',
                    'date':     app.history[-1][0].strftime('%d.%m.%Y') if app.history else '–',
                    'letter':   'ja' if app.requires_motivation_letter else '',
                    'url':      app.url or '',
                })

            table = (
                ui.table(columns=columns, rows=rows, row_key='id')
                .props('flat bordered dark separator=cell')
                .classes('w-full')
            )

            table.add_slot('body-cell-status', r'''
                <q-td :props="props">
                    <span :style="`background:${props.row.badge_bg}; color:${props.row.badge_fg};
                        padding:2px 10px; border-radius:999px; font-size:0.72rem; font-weight:600`">
                        {{ props.value }}
                    </span>
                </q-td>
            ''')

            table.add_slot('body-cell-company', r'''
                <q-td :props="props">
                    <span style="font-weight:600">{{ props.value }}</span>
                    <a v-if="props.row.url" :href="props.row.url" target="_blank"
                       style="margin-left:6px; color:#818cf8; font-size:0.75rem; text-decoration:none">↗</a>
                </q-td>
            ''')

            table.add_slot('body-cell-letter', r'''
                <q-td :props="props" style="text-align:center">
                    <q-icon v-if="props.row.letter" name="check_circle"
                            style="color:#34d399; font-size:1.1rem" />
                    <span v-else style="color:#475569">–</span>
                </q-td>
            ''')

    # ── Empty state ───────────────────────────────────────────────────────────
    @staticmethod
    def _empty_state() -> None:
        with ui.element('div').style(
            'display:flex; flex-direction:column; align-items:center; padding:80px 0'
        ):
            ui.icon('inbox').style(
                f'color:{Theme.TEXT_MUTED}; font-size:4rem; margin-bottom:8px'
            )
            ui.label('Keine Bewerbungen vorhanden').style(
                f'color:{Theme.TEXT_MUTED}; font-size:1rem'
            )
