# --- automation.py ---
import streamlit as st

def automation_controls():
    st.header("⚙️ Automation Settings")

    trigger = st.selectbox("When to trigger?", ["On Connect", "After X Minutes", "On Disconnect"])
    action = st.selectbox("Action", ["Send SMS", "Send Email", "Webhook Call"])
    content = st.text_area("Message Content", "Thanks for connecting to Free WiFi!")
    
    if st.button("Save Rule"):
        st.success(f"Rule saved: {trigger} → {action}")
        # Save rule to config DB or file (for future expansion)
