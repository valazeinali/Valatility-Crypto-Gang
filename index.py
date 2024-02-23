from dash import Dash, page_container, dcc, clientside_callback, ClientsideFunction, Output, Input

class MainApplication:
    def __init__(self):
        self.__app = Dash(
            __name__,
            update_title="Loading...",
            use_pages=True,
        )
       ....


    @property
    def app(self):
        return self.__app


Application = MainApplication()
app = Application.app.server
