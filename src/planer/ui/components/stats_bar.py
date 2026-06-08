from nicegui import ui
from planer.models.application import Application
from planer.enums.application_status import ApplicationStatus
from planer.ui.styles import Theme
from planer.ui import status_config


def render_stats(applications: list[Application]) -> None:
    total    = len(applications)
    active   = sum(1 for a in applications if a.status in status_config.ACTIVE)
    offers   = sum(1 for a in applications if a.status == ApplicationStatus.OFFERED)
    accepted = sum(1 for a in applications if a.status == ApplicationStatus.ACCEPTED)
    rejected = sum(1 for a in applications if a.status == ApplicationStatus.REJECTED)

    with ui.row().classes('flex-wrap gap-3').style('padding:14px 28px 6px'):
        _tile('Gesamt',     str(total),    'layers',       *Theme.STAT['total'])
        _tile('Aktiv',      str(active),   'trending_up',  *Theme.STAT['active'])
        _tile('Angebote',   str(offers),   'celebration',  *Theme.STAT['offers'])
        _tile('Angenommen', str(accepted), 'check_circle', *Theme.STAT['accepted'])
        _tile('Abgelehnt',  str(rejected), 'cancel',       *Theme.STAT['rejected'])


def _tile(label: str, value: str, icon: str, bg: str, icon_color: str) -> None:
    with ui.element('div').style(
        f'background:{bg}; border:1px solid {Theme.BORDER}; '
        'border-radius:10px; padding:9px 15px; min-width:105px; '
        'display:flex; align-items:center; gap:10px'
    ):
        ui.icon(icon).style(f'color:{icon_color}; font-size:1.55rem')
        with ui.column().classes('gap-0'):
            ui.label(value).style(
                f'color:{Theme.TEXT}; font-size:1.3rem; font-weight:700; line-height:1.1'
            )
            ui.label(label).style(
                f'color:{Theme.TEXT_SUB}; font-size:0.67rem; '
                'text-transform:uppercase; letter-spacing:0.05em'
            )
