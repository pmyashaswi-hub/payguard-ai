"""
PayGuard AI - Root Application Launcher.
Executes the Streamlit Banking Application when running:
  streamlit run app.py
"""

import os
import sys

# Ensure root directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from frontend.streamlit_app import main

if __name__ == "__main__":
    main()
