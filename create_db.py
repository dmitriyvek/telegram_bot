import sqlite3
from sys import argv
from subprocess import call


CSV_ACCOUNTS_DATA = './info/accounts_data.csv'
CSV_ACCOUNTS_BOTS_INFO_DATA = './info/accounts_bots_info_data.csv'

db = sqlite3.connect('accounts.db')
cur = db.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id            INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number          TEXT NOT NULL,
        api_id                TEXT,
        api_hash              TEXT,
        two_step_verification BOOLEAN DEFAULT 0 NOT NULL CHECK (two_step_verification in (0, 1))
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts_bots_info (
        account_id                      INTEGER NOT NULL,
        vipserf_setup                   BOOLEAN DEFAULT 0 NOT NULL CHECK (vipserf_setup in (0, 1)),
        vipserf_initial_post_watch_farm BOOLEAN DEFAULT 0 NOT NULL CHECK ((vipserf_initial_post_watch_farm in (0, 1)) and (not (vipserf_setup == 0 and vipserf_initial_post_watch_farm == 1))),
        FOREIGN KEY (account_id)
            REFERENCES accounts (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
    )
""")

db.commit()


if argv[1] == '-csv':
    call(
        ["sqlite3", "accounts.db", ".mode csv", f".import {CSV_ACCOUNTS_DATA} accounts",
         f".import {CSV_ACCOUNTS_BOTS_INFO_DATA} accounts_bots_info"])
