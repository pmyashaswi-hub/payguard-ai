"""
PayGuard AI - Database Viewer & Inspector Component.
Renders interactive database table explorer allowing users to inspect raw SQLite tables directly in the browser UI.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "payguard_bank.db")

def render_db_inspector():
    """Renders interactive Database Viewer page."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 26px; font-weight: 800; color: #0B1D33; margin: 0 0 6px 0; letter-spacing: -0.02em;">
            🗄️ Database Inspector
        </h1>
        <div style="color: #6B7280; font-size: 14px;">
            Inspect raw tables, registered user records, beneficiaries, and transaction logs stored inside <code>payguard_bank.db</code>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not os.path.exists(DB_PATH):
        st.error(f"Database file not found at: `{DB_PATH}`")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch Table List
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        tables = [r[0] for r in cursor.fetchall()]
        
        if not tables:
            st.warning("No database tables found.")
            conn.close()
            return

        # Metrics Bar
        m1, m2, m3 = st.columns(3)
        with m1:
            u_count = pd.read_sql_query("SELECT COUNT(*) as count FROM users", conn).iloc[0]['count']
            st.metric(label="Registered Users", value=u_count)
        with m2:
            t_count = pd.read_sql_query("SELECT COUNT(*) as count FROM transactions", conn).iloc[0]['count']
            st.metric(label="Stored Transactions", value=t_count)
        with m3:
            b_count = pd.read_sql_query("SELECT COUNT(*) as count FROM beneficiaries", conn).iloc[0]['count']
            st.metric(label="Saved Beneficiaries", value=b_count)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Table Selection Tabs
        selected_table = st.selectbox("Select Database Table to Inspect", options=tables, index=0)

        # Query Selected Table Data
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
        conn.close()

        st.markdown(f"### 📋 `{selected_table}` Table Records (`{len(df)}` rows)")
        
        # Interactive Search Filter
        search = st.text_input("🔍 Filter rows...", placeholder="Type to search any field...")
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            df_filtered = df[mask]
        else:
            df_filtered = df

        # Display Table
        st.dataframe(df_filtered, use_container_width=True)

        # Raw SQL Query Sandbox
        with st.expander("⚡ Run Custom SQL Query Sandbox"):
            query = st.text_area("SQL Query", value=f"SELECT * FROM {selected_table} LIMIT 10")
            if st.button("Execute Query", type="primary"):
                try:
                    c = sqlite3.connect(DB_PATH)
                    res_df = pd.read_sql_query(query, c)
                    c.close()
                    st.dataframe(res_df, use_container_width=True)
                except Exception as e:
                    st.error(f"SQL Execution Error: {e}")

    except Exception as ex:
        st.error(f"Failed to access database: {ex}")
