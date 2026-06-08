from nicegui import ui
from planer.models.application import Application
from planer.ui.styles import Theme
from planer.ui import status_config


def render_table(applications: list[Application]) -> None:
    with ui.element('div').style('padding:14px 28px 28px'):
        if not applications:
            _empty_state()
            return

        columns = [
            {'name': 'company',  'label': 'Firma',            'field': 'company',  'sortable': True,  'align': 'left'},
            {'name': 'position', 'label': 'Stelle',            'field': 'position', 'sortable': True,  'align': 'left'},
            {'name': 'status',   'label': 'Status',            'field': 'status',   'sortable': True,  'align': 'left'},
            {'name': 'source',   'label': 'Quelle',            'field': 'source',   'sortable': True,  'align': 'left'},
            {'name': 'date',     'label': 'Letzte Aktivität',  'field': 'date',     'sortable': True,  'align': 'left'},
            {'name': 'letter',   'label': 'Motiv.',            'field': 'letter',   'sortable': False, 'align': 'center'},
        ]

        rows = []
        for app in applications:
            badge_bg, badge_fg, _, _, label = status_config.get(app.status)
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
            .props('flat dark separator=none')
            .classes('bp-table w-full')
        )

        table.add_slot('body-cell-company', r'''
            <q-td :props="props">
                <span style="font-weight:600; color:#f1f5f9">{{ props.value }}</span>
                <a v-if="props.row.url" :href="props.row.url" target="_blank"
                   style="margin-left:6px; color:#818cf8; font-size:0.75rem; text-decoration:none">↗</a>
            </q-td>
        ''')

        table.add_slot('body-cell-status', r'''
            <q-td :props="props">
                <span :style="`background:${props.row.badge_bg}; color:${props.row.badge_fg};
                    padding:2px 9px; border-radius:999px; font-size:0.69rem; font-weight:600`">
                    {{ props.value }}
                </span>
            </q-td>
        ''')

        table.add_slot('body-cell-letter', r'''
            <q-td :props="props" style="text-align:center">
                <q-icon v-if="props.row.letter" name="check_circle"
                        style="color:#86efac; font-size:1rem" />
                <span v-else style="color:#334155">–</span>
            </q-td>
        ''')


def _empty_state() -> None:
    with ui.element('div').style(
        'display:flex; flex-direction:column; align-items:center; padding:60px 0'
    ):
        ui.icon('inbox').style(f'color:{Theme.TEXT_MUTED}; font-size:3.5rem; margin-bottom:8px')
        ui.label('Keine Bewerbungen vorhanden').style(f'color:{Theme.TEXT_MUTED}; font-size:0.95rem')
