import hmac
import os

import streamlit as st


def require_authentication():
    expected_username = os.getenv("DASHBOARD_USERNAME")
    expected_password = os.getenv("DASHBOARD_PASSWORD")

    if not expected_username or not expected_password:
        st.error("Dashboard authentication is not configured.")
        st.stop()

    if st.session_state.get("authenticated"):
        return

    st.subheader("Sign in")
    with st.form("dashboard_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")

    if submitted:
        valid_username = hmac.compare_digest(username, expected_username)
        valid_password = hmac.compare_digest(password, expected_password)
        if valid_username and valid_password:
            st.session_state.authenticated = True
            st.rerun()
        st.error("Invalid username or password.")

    st.stop()