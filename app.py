from pathlib import Path
import pandas as pd
import streamlit as st
BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "auth.log"
REPORT_FILE = BASE_DIR / "security_report.csv"
st.set_page_config(page_title="CyberShield AI", page_icon=":shield:", layout="wide")
st.title("CyberShield AI")
st.subheader("Security Log Monitoring Dashboard")
st.caption("Analyze authentication events and review security alerts.")
if not LOG_FILE.exists():
    st.error("auth.log was not found Generate the logs first.")
    st.stop()
logs = pd.read_csv(LOG_FILE)
required_columns = {"timestamp", "ip", "status"}
if not required_columns.issubset(logs.columns):
    st.error("the log file does not have the expected columns")
    st.stop()
total_events = len(logs)
successful_logins = int((logs["status"] == "SUCCESS").sum())
failed_logins = int((logs["status"] == "FAILED").sum())
col1, col2, col3 = st.columns(3)
col1.metric("Total Events", total_events)
col2.metric("Successful Logins", successful_logins)
col3.metric("Failed Logins", failed_logins)
st.divider()
st.subheader("Authentication Events Overview")
status_counts = (logs["status"].value_counts().reindex(["SUCCESS", "FAILED"], fill_value=0))
st.bar_chart(status_counts)
st.subheader("Security Alerts")
if REPORT_FILE.exists():
    alerts = pd.read_csv(REPORT_FILE)
    if alerts.empty:
        st.success("No security alerts found.")
    else:
        st.warning(f"{len(alerts)} suspicious IP addresses detected.")
        st.dataframe(alerts, use_container_width=True)
    report_data = REPORT_FILE.read_bytes()
    st.download_button(
        label="Download Security Report",
        data=report_data,
        file_name="security_report.csv",
        mime="text/csv",
    )
else:
    st.info("No security report found. Run analyze_logs.py first.")
with st.expander("View all authentication events"):
    st.dataframe(logs, use_container_width=True)
st.caption("CyberShield AI | Educational security monitoring project.")