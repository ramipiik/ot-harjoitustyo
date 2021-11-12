from sqlite3.dbapi2 import SQLITE_DROP_VIEW
from ui.text_ui import start
from services.flow import flow

portfolio=start()
flow(portfolio)