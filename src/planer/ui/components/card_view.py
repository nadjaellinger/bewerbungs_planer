from nicegui import ui
from planer.models.application import Application
from planer.ui.styles import Theme
from planer.ui import status_config


def render_cards(applications: list[Application]) -> None:
    with ui.element('div').style('padding:14px 28px 28px'):
        if not applications:
            _empty_state()
            return
        with ui.element('div').style(
            'display:grid; '
            'grid-template-columns:repeat(auto-fill, minmax(265px, 1fr)); '
            'gap:11px'
        ):
            for app in applications:
                _card(app)


def _card(app: Application) -> None:
    badge_bg, badge_fg, strip, icon, label = status_config.get(app.status)
    latest = app.history[-1][0].strftime('%d.%m.%Y') if app.history else None

    with ui.element('div').style(Theme.card()).classes('bp-card'):
        # coloured top strip
        ui.element('div').style(f'height:3px; background:{strip}')
        with ui.element('div').style('padding:11px 13px 13px'):
            # company + status badge
            with ui.row().classes('items-start justify-between gap-2 flex-nowrap'):
                with ui.column().classes('gap-0 flex-1 min-w-0'):
                    ui.label(app.company).style(
                        f'color:{Theme.TEXT}; font-weight:700; font-size:0.93rem; '
                        'overflow:hidden; text-overflow:ellipsis; white-space:nowrap'
                    )
                    ui.label(app.position).style(
                        f'color:{Theme.TEXT_SUB}; font-size:0.77rem; '
                        'overflow:hidden; text-overflow:ellipsis; white-space:nowrap'
                    )
                with ui.row().style(
                    f'background:{badge_bg}; color:{badge_fg}; '
                    'padding:2px 7px; border-radius:999px; '
                    'font-size:0.67rem; font-weight:600; '
                    'align-items:center; gap:3px; white-space:nowrap; flex-shrink:0'
                ):
                    ui.icon(icon).style('font-size:0.8rem')
                    ui.label(label)

            ui.element('div').style(f'height:1px; background:{Theme.BORDER}; margin:8px 0')

            with ui.column().classes('gap-1'):
                if latest:
                    _detail('event', f'Letzte Aktivität: {latest}', Theme.TEXT_SUB)
                if app.source:
                    _detail('source', f'Quelle: {app.source}', Theme.TEXT_SUB)
                if app.requires_motivation_letter:
                    _detail('description', 'Motivationsschreiben erforderlich', Theme.AMBER, Theme.AMBER)
                if app.comments:
                    _detail('chat_bubble_outline', app.comments, Theme.TEXT_MUTED)
                if app.url:
                    with ui.element('div').style('margin-top:5px'):
                        ui.link('Stellenanzeige ↗', target=app.url, new_tab=True).style(
                            f'color:{Theme.INDIGO}; font-size:0.72rem; text-decoration:none'
                        )


def _detail(icon: str, text: str, text_color: str, icon_color: str = '') -> None:
    ic = icon_color or Theme.TEXT_MUTED
    with ui.row().classes('items-center gap-2'):
        ui.icon(icon).style(f'color:{ic}; font-size:0.83rem; flex-shrink:0')
        ui.label(text).style(
            f'color:{text_color}; font-size:0.75rem; '
            'overflow:hidden; text-overflow:ellipsis; white-space:nowrap'
        )


def _empty_state() -> None:
    with ui.element('div').style(
        'display:flex; flex-direction:column; align-items:center; padding:60px 0'
    ):
        ui.icon('inbox').style(f'color:{Theme.TEXT_MUTED}; font-size:3.5rem; margin-bottom:8px')
        ui.label('Keine Bewerbungen vorhanden').style(f'color:{Theme.TEXT_MUTED}; font-size:0.95rem')
