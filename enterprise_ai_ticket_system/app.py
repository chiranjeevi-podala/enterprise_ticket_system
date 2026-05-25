import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Enterprise AI ITSM Copilot", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("tickets.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue TEXT,
    category TEXT,
    priority TEXT,
    solution TEXT,
    time TEXT
)
""")
conn.commit()

# ---------------- KNOWLEDGE BASE ----------------
knowledge_base = {
    "vpn": "Restart VPN, check network adapter, reconnect to corporate network.",
    "password": "Reset password via company portal or contact IT admin.",
    "server": "Server issue detected. DevOps team is notified immediately.",
    "email": "Check Outlook configuration and mail server status.",
    "slow": "Clear cache, close background apps, check system RAM usage.",
    "login": "Verify credentials or reset password using SSO portal."
}

# ---------------- AI ENGINE ----------------
def classify(issue):
    issue = issue.lower()

    if "server" in issue:
        return "Critical Issue", "Critical"

    elif "vpn" in issue or "network" in issue:
        return "Network Issue", "High"

    elif "password" in issue or "login" in issue:
        return "Access Issue", "Medium"

    elif "slow" in issue:
        return "Performance Issue", "Medium"

    else:
        return "General Issue", "Low"


def get_solution(issue):
    issue = issue.lower()

    for key in knowledge_base:
        if key in issue:
            return knowledge_base[key]

    return "AI is analyzing the issue. Support team will respond shortly."


def save_ticket(issue, category, priority, solution):
    c.execute(
        "INSERT INTO tickets (issue, category, priority, solution, time) VALUES (?, ?, ?, ?, ?)",
        (issue, category, priority, solution, str(datetime.now()))
    )
    conn.commit()

# ---------------- UI ----------------
st.title("🏢 Enterprise AI ITSM Copilot (Final Product Level)")

tab1, tab2 = st.tabs(["🧾 Create Ticket", "📊 Dashboard"])

# ---------------- TAB 1 ----------------
with tab1:
    issue = st.text_area("Enter your IT issue")

    if st.button("🚀 Process Ticket"):

        category, priority = classify(issue)
        solution = get_solution(issue)

        save_ticket(issue, category, priority, solution)

        st.success("Ticket Created Successfully!")

        st.subheader("🎯 AI Analysis")
        st.write("Category:", category)
        st.write("Priority:", priority)

        st.subheader("💡 AI Suggested Solution")
        st.info(solution)

        st.subheader("🤖 Auto Response")
        st.write(
            f"Your ticket has been classified as **{category}** "
            f"with **{priority} priority**. Suggested fix: {solution}"
        )

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("📊 Ticket Analytics")

    c.execute("SELECT category, priority FROM tickets")
    data = c.fetchall()

    if data:
        categories = {}
        priorities = {}

        for cat, pri in data:
            categories[cat] = categories.get(cat, 0) + 1
            priorities[pri] = priorities.get(pri, 0) + 1

        st.write("### Category Distribution")
        st.bar_chart(categories)

        st.write("### Priority Distribution")
        st.bar_chart(priorities)

    else:
        st.info("No tickets available yet.")