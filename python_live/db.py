from pony.orm import *
from pony.options import CUT_TRACEBACK
CUT_TRACEBACK = False
set_sql_debug(True)
db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
class Ledger(db.Entity):
    datetime=Required(str)
    cells=Set('Cell')
class Cell(db.Entity):
    location=Required(int)
    code=Required(str)
    hashId=Required(str)
    datetime=Required(str)
    changed=Required(bool)
    owner=Required(Ledger)
def create():
    db.generate_mapping(create_tables=True)
@db_session
def add_cell(location, code, hashId, datetime, changed):
    Cell(location=location, code=code, hashId=hashId, datetime=datetime, changed=changed)
@db_session
def get_ledger():
    return select(c for c in Cell)[-1]
@db_session
def add_cells(datetime, cells):
    cellsList=[]
    for c in cells:
        cellsList.append(Cell(location=c['location'], code=c['code'], hashId=c['hashId'], datetime=c['datetime'], changed=c['changed']))
    flish()
    Ledger(datetime=datetime, cells=cellsList)
