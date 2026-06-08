from nicegui import ui
from planer.ui.styles import Theme


def render_header() -> None:
    with ui.element('div').style(
        f'background:{Theme.HEADER_GRADIENT}; '
        'padding:15px 28px 17px; '
        f'border-bottom:1px solid {Theme.BORDER}'
    ):
        with ui.row().classes('items-center gap-3'):
            ui.icon('work').style('color:#a5b4fc; font-size:1.9rem')
            with ui.column().classes('gap-0'):
                ui.label('Bewerbungsplaner').style(
                    f'color:{Theme.TEXT}; font-size:1.35rem; font-weight:700; line-height:1.25'
                )
                ui.label('Deine Bewerbungsübersicht').style(
                    'color:#a5b4fc; font-size:0.78rem'
                )
