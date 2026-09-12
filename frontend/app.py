import streamlit as st

from auth import require_authentication
from database import get_dataset_counts
from pipeline_runner import run_pipeline_live
from components import (
    show_dashboard_header,
    show_dataset_overview,
    show_live_pipeline,
    show_pipeline_result,
)
from styles import apply_styles


st.set_page_config(
    page_title="E-Commerce ETL Dashboard",
    page_icon="📊",
    layout="wide"
)

apply_styles()
require_authentication()

show_dashboard_header()

st.markdown('<span class="status-pill">● System ready</span>', unsafe_allow_html=True)

try:
    counts = get_dataset_counts()
except Exception as error:
    print(f"Database connection failed: {error}")
    st.warning(
        "The dashboard is online, but the PostgreSQL database is not reachable yet. "
        "Check the deployment database settings, then refresh this page."
    )
    counts = None

if counts:
    show_dataset_overview(counts)


st.divider()

st.subheader("Pipeline")


if st.button("Run ETL Pipeline", type="primary"):

    status_slot = st.empty()
    metrics_slot = st.empty()
    log_slot = st.empty()

    for snapshot in run_pipeline_live():
        if snapshot["running"]:
            show_live_pipeline(snapshot, status_slot, metrics_slot, log_slot)

    result = {
        "success": snapshot["returncode"] == 0,
        "output": snapshot["output"],
        "error": snapshot["output"] if snapshot["returncode"] != 0 else "",
        "runtime": snapshot["runtime"],
    }

    show_pipeline_result(result)