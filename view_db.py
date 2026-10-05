"""
PayGuard AI - Terminal Database Viewer Utility.
Prints all database tables and records directly to the terminal console.
Usage: python view_db.py
"""

import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "payguard_bank.db")

def print_table(title, rows, columns):
    print(f"\n==================================================================")
    print(f"  {title.upper()} (Total Records: {len(rows)})")
    print(f"==================================================================")
    if not rows:
        print("  [No records found]")
        return
    
    # Print Column Names
    header = " | ".join(columns)
    print(header)
    print("-" * len(header))
    
    # Print Row Data
    for row in rows:
        row_str = []
        for col in columns:
            val = str(row[col])
            if len(val) > 30:
                val = val[:27] + "..."
            row_str.append(val)
        print(" | ".join(row_str))

def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get Table List
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r['name'] for r in cursor.fetchall() if r['name'] != 'sqlite_sequence']

    for tbl in tables:
        cursor.execute(f"SELECT * FROM {tbl}")
        rows = cursor.fetchall()
        cols = [description[0] for description in cursor.description]
        print_table(tbl, rows, cols)

    conn.close()

if __name__ == "__main__":
    main()
