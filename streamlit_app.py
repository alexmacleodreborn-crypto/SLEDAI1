import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st


st.title("🧠 A7DO — World Cage & Experiment Runner")

st.markdown("""
This app is **Observer-led**.  
A7DO only learns through **authorised schedules** (events), never direct story belief.
""")

st.info("Use the Pages menu: 0_World_Cage → 1_World_Profile → 3_Run_Experiment → 2_Observer")