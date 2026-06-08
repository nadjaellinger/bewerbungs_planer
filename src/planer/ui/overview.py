from nicegui import ui

from planer.models.application import Application
from planer.ui.styles import Theme
from planer.ui.components.header import render_header
from planer.ui.components.stats_bar import render_stats
from planer.ui.components.card_view import render_cards
from planer.ui.components.table_view import render_table


class Overview:
    def __init__(self, logger):
        self.logger = logger

    def render(self, applications: list[Application]) -> None:
        ui.dark_mode(value=True)
        ui.query('body').style(f'background:{Theme.PAGE}; color:{Theme.TEXT}; margin:0')
        ui.add_css(Theme.GLOBAL_CSS)

        render_header()
        render_stats(applications)
        self._toolbar_and_content(applications)

    def _toolbar_and_content(self, applications: list[Application]) -> None:
        mode = {'view': 'cards'}

        with ui.row().classes('items-center justify-between w-full').style(
            f'padding:10px 28px 8px; border-bottom:1px solid {Theme.BORDER}'
        ):
            ui.label(f'{len(applications)} Bewerbung(en)').style(
                f'color:{Theme.TEXT_MUTED}; font-size:0.78rem'
            )
            with ui.row().classes('gap-1 items-center'):
                btn_c = (
                    ui.button(icon='grid_view', on_click=lambda: _switch('cards'))
                    .props('flat round dense')
                    .style(f'color:{Theme.INDIGO}')
                    .tooltip('Kachelansicht')
                )
                btn_t = (
                    ui.button(icon='table_rows', on_click=lambda: _switch('table'))
                    .props('flat round dense')
                    .style(f'color:{Theme.TEXT_MUTED}')
                    .tooltip('Tabellenansicht')
                )

        @ui.refreshable
        def content() -> None:
            if mode['view'] == 'cards':
                render_cards(applications)
            else:
                render_table(applications)

        def _switch(v: str) -> None:
            mode['view'] = v
            btn_c.style(f'color:{Theme.INDIGO if v == "cards" else Theme.TEXT_MUTED}')
            btn_t.style(f'color:{Theme.INDIGO if v == "table" else Theme.TEXT_MUTED}')
            content.refresh()

        content()

