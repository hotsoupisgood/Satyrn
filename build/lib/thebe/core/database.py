import sqlite3, logging, dill, os, sys, time

import thebe.core.constants as Constant
from datetime import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        if col[0] == 'cells' or col[0] == 'local_scope' or col[0] == 'global_scope':
            d[col[0]] = dill.loads(row[idx])
        else:
            d[col[0]] = row[idx]
    return d
DATABASE = '%s/database.sqlite' % os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(DATABASE, check_same_thread=False)
conn.row_factory = dict_factory
c = conn.cursor()

def getLedger(target):
    '''
    Get the data objects, if they do not exist create them.
    '''
    c.execute('SELECT * FROM ledger WHERE name=?', (target,))
    fetched=c.fetchone()
    if bool(fetched):
        r=fetched
        return r['cells'], r['global_scope'], r['local_scope']
    else:
        createLedger(target)
        return getLedger(target)

def getExecutions(target):
    '''
    '''
    c.execute('SELECT executions FROM ledger WHERE name=?', (target,))
    return c.fetchone()['executions']

def getIsActive(target):
    '''
    '''
    c.execute('SELECT is_active FROM ledger WHERE name=?', (target,))
    return c.fetchone()['is_active']

def setIsActive(target):
    '''
    '''
    c.execute('UPDATE ledger SET is_active=? WHERE name=?', \
            (True, target))

def createLedger(target):
    '''
    '''
    logging.info('Adding\t%s\t to db...' % target)
    now=datetime.now().strftime('%a, %B, %d, %y')
    c.execute('INSERT INTO ledger (name, last_edit, created, cells, global_scope, local_scope, is_active) \
            VALUES (?,?,?,?,?,?,?)', (target, now, now, dill.dumps([]), dill.dumps({}), dill.dumps({}), False))

def setActive(target, active):
    c.execute('UPDATE ledger SET is_active=? WHERE name=?', (active, target))

def update(target, cells, globalScope, localScope, executions):
    '''
    '''
    localdump = {}
    try:
        localdump = dill.dumps(localScope)
    except AttributeError:
        logging.debug('Dill pickling the local scope, yields an error')
    c.execute('UPDATE ledger SET cells=?, global_scope=?, local_scope=?, executions=? WHERE name=?', \
            (dill.dumps(cells), dill.dumps(globalScope), dill.dumps(localdump), executions, target))
