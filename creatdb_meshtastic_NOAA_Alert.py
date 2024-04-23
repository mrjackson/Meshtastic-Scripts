#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('~/data/meshtasticNOAA.sqlite')
c = conn.cursor()

c.execute("""drop table if exists data""")
conn.commit()

c.execute("""create table data (
        datetime        text,
        alertid         text,
        PRIMARY KEY (datetime, alertid))""")

conn.commit()
c.close()
