import sqlite3

def init_db():

    conn = sqlite3.connect("civic_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        location TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_report(issue, location):

    conn = sqlite3.connect("civic_reports.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reports(issue, location, status) VALUES (?, ?, ?)",
        (issue, location, "Pending")
    )

    complaint_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return complaint_id