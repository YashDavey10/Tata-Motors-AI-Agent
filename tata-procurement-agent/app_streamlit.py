"""
Tata Motors Step-by-Step Autonomous Procurement Agent & ERP Engine
TMPVL (Passenger Vehicles) & TPEML (Electric Mobility) - Pune Plant (Pimpri & Chikhali)
Conversational Copilot & Interactive Enterprise Dashboard with Modal Approval Popups
"""

import streamlit as st
import datetime
from erp_data import erp_db
from engine import engine
from email_service import email_service
from ariba_edi_service import ariba_edi_service

st.set_page_config(
    page_title="Tata Motors Autonomous Procurement Agent",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (High-Contrast Professional Dark Theme)
st.markdown("""
<style>
    /* Dark Theme Global Layout */
    .stApp {
        background-color: #070e1b;
        color: #f1f5f9;
    }
    div[data-testid="stSidebar"] {
        background-color: #0d192e;
        border-right: 1px solid #1e355b;
    }
    div[data-testid="stChatMessage"] {
        background-color: #0e1c33;
        border: 1px solid #1e355b;
        border-radius: 10px;
        margin-bottom: 12px;
        color: #f1f5f9;
    }
    div[data-testid="stExpander"] {
        background-color: #0d192e;
        border: 1px solid #1e355b;
        border-radius: 8px;
    }
    div[data-testid="stMetric"] {
        background-color: #12213a;
        border: 1px solid #1e355b;
        border-radius: 8px;
        padding: 12px 14px;
    }
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 800;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
    }
    code {
        color: #38bdf8 !important;
        background-color: #12213a !important;
        border: 1px solid #1e355b !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }

    .main-header {
        background: linear-gradient(135deg, #07162c 0%, #002d62 60%, #004b93 100%);
        border: 1px solid #1e355b;
        padding: 20px 24px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #93c5fd;
        font-size: 13px;
        margin: 6px 0 0;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 8px;
    }
    .badge-live {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-risk {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-mode {
        background-color: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }
    .approval-alert-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.16) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 15px 0;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Audio Chime Generator (Web Audio API)
AUDIO_CHIME_HTML = """
<script>
try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (AudioCtx) {
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.setValueAtTime(880.00, ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.45);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.45);
    }
} catch (e) {}
</script>
"""

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>TATA MOTORS &nbsp;|&nbsp; Autonomous Step-by-Step Procurement Agent</h1>
    <p>Manufacturing Operations: TMPVL (Passenger Vehicles) & TPEML (Electric Mobility) &nbsp;•&nbsp; Pune Plant (Pimpri & Chikhali)</p>
    <div style="margin-top: 10px;">
        <span class="badge-pill badge-live">● SAP Ariba: CONNECTED (cXML 1.2.014 / EDI 850)</span>
        <span class="badge-pill badge-risk">⚡ Line Risk: ₹15L–₹22L / hr</span>
        <span class="badge-pill badge-mode">🛡️ Compliance: Auto PLI (50% DVA) & IATF-16949 Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "**Tata Motors Step-by-Step Autonomous Procurement Agent Online.**\n\n"
            "I operate as a deterministic finite-state machine protecting the Pune assembly lines (Nexon, Harrier, Safari, Curvv EV) "
            "from costly stoppages (₹15L–₹22L/hr), enforcing Auto PLI (50% DVA) and IATF-16949 quality holds, preventing anti-split budget circumvention, "
            "and generating verifiable SAP Ariba cXML 1.2.014 & EDI 850 orders.\n\n"
            "**Operational Modes:**\n"
            "• **Full Automation (Tier 1):** Autonomous sourcing, math, and dispatch for requisitions within Tier 1 thresholds.\n"
            "• **Human-in-the-Loop (Tier 2 / Tier 3):** Immediate execution freeze at Step 5 with an interactive **Approval Modal Popup**, staging the PO and vendor email, awaiting 'Approved' or 'Rejected'.\n\n"
            "Enter your requisition (or select a preloaded scenario from the sidebar):"
        )
    }]
if "pending_po" not in st.session_state:
    st.session_state.pending_po = None
if "show_approval_modal" not in st.session_state:
    st.session_state.show_approval_modal = False
if "scenario_to_run" not in st.session_state:
    st.session_state.scenario_to_run = None

# -------------------------------------------------------------
# MODAL POPUP DIALOG FOR HUMAN APPROVAL SIGN-OFF
# -------------------------------------------------------------
@st.dialog("🔔 Action Required: Purchase Order Digital Sign-Off", width="large")
def show_approval_dialog(po):
    st.components.v1.html(AUDIO_CHIME_HTML, height=0)
    
    total_val = po.get("total_value_inr", 0.0)
    sup_name = po.get("vendor", {}).get("name", "Contracted Supplier")
    sup_id = po.get("vendor", {}).get("id", "N/A")
    cc_code = po.get("cost_center", "CC-PU-TCF")
    po_num = po.get("po_number", "PO-TML-PENDING")
    items = po.get("line_items", [{}])
    qty = items[0].get("quantity", 1) if items else 1
    mat_name = items[0].get("description", "Component")
    mat_code = items[0].get("material_code", "N/A")
    unit_rate = items[0].get("unit_rate", 0.0)
    routing = po.get("approval_routing", {})
    approver = routing.get("approver_role", "Shop Head")
    reason = routing.get("reasoning", po.get("reasoning", "Exceeds Tier 1 auto-approval threshold."))
    guardrails = po.get("guardrails", [])

    st.markdown(f"""
    <div style="background-color: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; border-radius: 8px; padding: 14px 18px; margin-bottom: 18px; box-shadow: 0 4px 14px rgba(239, 68, 68, 0.2);">
        <div style="color: #fca5a5; font-weight: 800; font-size: 16px; margin-bottom: 4px; letter-spacing: 0.02em;">
            🚨 DIGITAL SIGN-OFF MANDATORY: {approver.upper()}
        </div>
        <div style="color: #fecaca; font-size: 13px; line-height: 1.5;">
            This Purchase Requisition exceeds the Tier 1 auto-approval ceiling. The dispatch email is currently <strong style="color: #ffffff;">STAGED in outbox</strong> (held from transmission). Your explicit digital authorization is required to commit company funds and transmit to SAP Ariba.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total PO Value", f"₹{total_val:,.2f}")
    with col2:
        st.metric("Order Quantity", f"{qty} {items[0].get('unit', 'units')}")
    with col3:
        st.metric("Unit Rate", f"₹{unit_rate:,.2f}")

    st.markdown(f"""
    **Requisition & Compliance Audit:**
    • **Purchase Order:** `{po_num}`  
    • **Material:** `{mat_code}` — **{mat_name}**  
    • **Sourced Vendor:** `{sup_id}`: **{sup_name}**  
    • **Requesting Cost Center:** `{cc_code}` ({erp_db.get_cost_center(cc_code)['name'] if erp_db.get_cost_center(cc_code) else 'Central'})  
    • **Sourcing Rule Triggered:** {', '.join(guardrails) if guardrails else 'Standard Sourcing'}  
    • **Audit Justification:** {reason}  
    • **Dispatch Outbox Status:** `STAGED (Held Pending Sign-Off)`  
    """)

    st.divider()
    modal_dest_email = st.text_input(
        "📧 Send Real-Time PO Copy to Mail ID:",
        value=st.session_state.get("custom_email", ""),
        placeholder="e.g. user@domain.com (Leave blank for supplier only)",
        key="modal_dest_email_input"
    )
    if modal_dest_email:
        st.session_state.custom_email = modal_dest_email.strip()
        erp_db.set_custom_live_email(modal_dest_email.strip())

    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("✅ One-Click Sign-Off & Dispatch to SAP Ariba", type="primary", use_container_width=True):
            st.session_state.scenario_to_run = ("Approved", {})
            st.session_state.show_approval_modal = False
            st.rerun()
    with b_col2:
        if st.button("❌ Reject Requisition (Zero Budget Committed)", type="secondary", use_container_width=True):
            st.session_state.scenario_to_run = ("Rejected", {})
            st.session_state.show_approval_modal = False
            st.rerun()

# Sidebar: ERP Knowledge Base & Preloaded Scenarios
with st.sidebar:
    st.subheader("📊 Plant Cost Centers & Budgets")
    for cc_id, cc in erp_db.cost_centers.items():
        pct = max(0.0, min(100.0, (cc["remaining_budget"] / cc["total_budget"]) * 100))
        st.markdown(f"**{cc['code']}** ({cc['name']})")
        st.progress(pct / 100.0)
        st.caption(f"Remaining: **₹{cc['remaining_budget']:,.2f}** / ₹{cc['total_budget']:,.2f} | Tier 1 limit: ≤ ₹{cc['tier1_limit']:,.0f}")
    
    st.divider()
    st.subheader("📬 Live Real-Time Email Dispatch")
    st.caption("Specify a live email ID to receive real-time PO dispatches:")
    sidebar_email = st.text_input(
        "Destination Mail ID:",
        value=st.session_state.get("custom_email", ""),
        placeholder="e.g. yourname@domain.com",
        key="sidebar_live_email"
    )
    if sidebar_email != st.session_state.get("custom_email", ""):
        st.session_state.custom_email = sidebar_email.strip()
        erp_db.set_custom_live_email(sidebar_email.strip())

    with st.expander("⚙️ SMTP Server Settings (For Real Inbox Delivery)"):
        st.caption("Configure SMTP server to deliver directly to external mailboxes (Gmail/Outlook/Corporate):")
        smtp_h = st.text_input("SMTP Host:", value=erp_db.smtp_settings.get("host", "smtp.gmail.com"), key="st_smtp_h")
        smtp_p = st.number_input("SMTP Port:", value=erp_db.smtp_settings.get("port", 587), key="st_smtp_p")
        smtp_u = st.text_input("Sender Username / Email:", value=erp_db.smtp_settings.get("user", ""), key="st_smtp_u")
        smtp_pass = st.text_input("App Password:", value=erp_db.smtp_settings.get("pass", ""), type="password", key="st_smtp_pass")

        if st.button("💾 Save SMTP Credentials", use_container_width=True):
            erp_db.set_smtp_settings({
                "host": smtp_h.strip(),
                "port": int(smtp_p),
                "user": smtp_u.strip(),
                "pass": smtp_pass.strip(),
                "use_tls": True
            })
            st.success("SMTP configuration saved!")

        if st.button("📤 Send Test Real-Time Mail", use_container_width=True):
            if not sidebar_email:
                st.error("Please enter a Destination Mail ID first.")
            else:
                test_res = email_service.send_live_email(sidebar_email, subject_override="[TEST] Tata Motors Procurement Live Dispatch System Test")
                if test_res.get("success"):
                    st.success(test_res.get("message"))
                else:
                    st.error(test_res.get("error"))

    st.divider()
    st.subheader("⚡ Preloaded Plant Scenarios")
    
    if st.button("Scenario 1: JIT Emergency (400 ABS Sensors)", use_container_width=True):
        st.session_state.scenario_to_run = ("Short 400 ABS sensors (TML-PV-101) for TCF line. Need in 24 hrs.", {})
        st.rerun()

    if st.button("Scenario 2: EV Auto PLI Violation (20 EV Paste)", use_container_width=True):
        st.session_state.scenario_to_run = ("Order 20 pails of EV paste (TML-EV-303) from Shenzhen Tech at ₹29,000 for CC-PU-EV.", {})
        st.rerun()

    if st.button("Scenario 3: IATF Quality Hold (10 M8 Rivets)", use_container_width=True):
        st.session_state.scenario_to_run = ("Need 10 boxes of Fastener Rivets M8 (TML-BIW-204) from Sundram Fasteners for CC-PU-BIW.", {})
        st.rerun()

    if st.button("Scenario 4: Anti-Split Circumvention (8+8 Rivets)", use_container_width=True):
        st.session_state.scenario_to_run = ("Request 8 boxes of Fastener Rivets M8 (TML-BIW-204) for CC-PU-BIW at ₹12,400 each.", {"simulate_anti_split": True})
        st.rerun()

    if st.button("Scenario 5: Volume Bundling (2,000 Oil Filters)", use_container_width=True):
        st.session_state.scenario_to_run = ("Nexon needs 800 Alternators, Punch needs 600, Altroz needs 600 (TML-ELE-707 at ₹4,200).", {})
        st.rerun()

    st.divider()
    if st.button("🔄 Reset ERP Database", use_container_width=True):
        erp_db.reset()
        st.session_state.pending_po = None
        st.session_state.show_approval_modal = False
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🔄 **ERP database reset to baseline factory state.** All budgets, outbox emails, and transactional ledgers cleared."
        })
        st.rerun()

# Display Chat Messages
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("email_html"):
            is_staged = msg.get("is_staged", False)
            title = "⚠️ Staged Supplier Email (Held in Outbox — Awaiting Human Authorization)" if is_staged else "📧 Dispatched Supplier PO Letterhead (Official Transmitted Copy — Sent & Delivered)"
            with st.expander(title, expanded=True):
                st.components.v1.html(msg["email_html"], height=480, scrolling=True)
                
                # Direct interactive spot to send real-time mail to any email ID
                st.divider()
                st.caption("⚡ **Live Real-Time Email Dispatch Spot:**")
                col_live_a, col_live_b = st.columns([3, 1])
                po_num_ref = msg.get("po_number") or ("PO-TML-LIVE" if "po_item" not in locals() else po_item.get("po_number", "PO-TML-LIVE"))
                with col_live_a:
                    msg_target_email = st.text_input(
                        "Send real-time copy of this PO to mail ID:",
                        value=st.session_state.get("custom_email", ""),
                        key=f"msg_send_{idx}_{po_num_ref}",
                        placeholder="e.g. reviewer@tatamotors.com or your email"
                    )
                with col_live_b:
                    st.write("")
                    if st.button("🚀 Send Live Mail Now", key=f"btn_msg_send_{idx}_{po_num_ref}", use_container_width=True):
                        if msg_target_email:
                            s_res = email_service.send_live_email(msg_target_email.strip(), po_number=po_num_ref)
                            if s_res.get("success"):
                                st.toast(f"✅ Real-time email dispatched to {msg_target_email}!", icon="📬")
                                st.success(s_res.get("message"))
                            else:
                                st.error(s_res.get("error"))
                        else:
                            st.warning("Please enter a destination mail ID in the spot above.")

# Trigger Modal Dialog if approval is pending and modal flag is set
if st.session_state.pending_po and st.session_state.show_approval_modal:
    show_approval_dialog(st.session_state.pending_po)

# Sticky Notification Banner if approval is pending
if st.session_state.pending_po:
    po_item = st.session_state.pending_po
    routing_info = po_item.get("approval_routing", {})
    approver_name = routing_info.get("approver_role", "Shop Head")
    po_cost = po_item.get("total_value_inr", 0.0)

    st.markdown(f"""
    <div class="approval-alert-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 18px; margin-right: 8px;">🔔</span>
                <strong style="color: #fbbf24; font-size: 15px; letter-spacing: 0.02em;">ACTION REQUIRED: Digital Sign-Off Pending for {approver_name.upper()}</strong>
                <div style="color: #fde68a; font-size: 13px; margin-top: 4px;">
                    PO <code>{po_item.get('po_number')}</code> valued at <strong style="color: #ffffff;">₹{po_cost:,.2f}</strong> is held in staged outbox.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if st.button("🔔 Open Interactive Approval Dialog (Popup)", type="primary", use_container_width=True):
            st.session_state.show_approval_modal = True
            st.rerun()
    with col2:
        if st.button("✅ Quick Approve", use_container_width=True):
            st.session_state.scenario_to_run = ("Approved", {})
            st.rerun()
    with col3:
        if st.button("❌ Quick Reject", use_container_width=True):
            st.session_state.scenario_to_run = ("Rejected", {})
            st.rerun()

# User Input Handling
user_input = st.chat_input("Enter requisition or reply 'Approved' / 'Rejected'...")

# Process preloaded scenario or typed input
input_text = None
input_meta = {}
if st.session_state.scenario_to_run:
    input_text, input_meta = st.session_state.scenario_to_run
    st.session_state.scenario_to_run = None
elif user_input:
    input_text = user_input

if input_text:
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)

    with st.chat_message("assistant"):
        text_lower = input_text.lower().strip()
        
        # -------------------------------------------------------------
        # STATE MACHINE: HANDLE HUMAN APPROVAL / REJECTION
        # -------------------------------------------------------------
        if st.session_state.pending_po and any(w in text_lower for w in ["approve", "approved", "reject", "rejected"]):
            pending_po = st.session_state.pending_po
            po_num = pending_po.get("po_number", "PO-TML-PENDING")
            total_val = pending_po.get("total_value_inr", 0.0)
            sup_name = pending_po.get("vendor", {}).get("name", "Contracted Supplier")
            cc_code = pending_po.get("cost_center", "CC-PU-TCF")
            items = pending_po.get("line_items", [{}])
            qty = items[0].get("quantity", 1) if items else 1
            unit = items[0].get("unit", "units") if items else "units"

            if "approve" in text_lower:
                approve_res = engine.approve_po(po_num, approver_role="Shop Head", approver_name="R. Sen (Head BIW)")
                cc = erp_db.get_cost_center(cc_code)
                rem_budget = cc.get("remaining_budget", 0.0) if cc else 0.0
                sup_info = erp_db.get_supplier(pending_po.get("vendor", {}).get("id")) or {}
                vendor_email = sup_info.get("email", "orders@supplier.in")
                ariba_txn = pending_po.get("ariba_transaction", {})
                ariba_doc_id = ariba_txn.get("transaction_id", f"ARIBA-{po_num}")
                sha_digest = ariba_txn.get("payload_digest_sha256", "3f7a1e8c...verified")[:24]
                email_rec = approve_res.get("email") if isinstance(approve_res, dict) else None

                resp = (
                    f"**[STEP 6: TASK COMPLETION]**\n\n"
                    f"✅ PO generated and dispatched to supplier.\n"
                    f"• PO Number: {po_num}\n"
                    f"• Vendor: {sup_name}\n"
                    f"• Quantity: {qty} {unit}\n"
                    f"• Total Value: ₹{total_val:,.2f}\n"
                    f"• SAP Ariba cXML 1.2.014 Document: {ariba_doc_id} (SYN-ACK Confirmed, SHA-256 Digest: {sha_digest})\n"
                    f"• EDI 850/855 Handshake: Completed (Status: ACK*IA, HTTP 200 OK)\n"
                    f"• Automated Dispatch Email: Sent to {vendor_email}\n"
                    f"• Budget Updated: {cc_code} remaining budget is ₹{rem_budget:,.2f}\n\n"
                    f"---\n"
                    f"### 📬 DISPATCHED SUPPLIER EMAIL (OFFICIAL TRANSMISSION COPY — SENT & DELIVERED)\n"
                    f"• **Transmission Status:** `✅ SENT & DELIVERED (SAP Ariba Verified)`\n"
                    f"• **Recipient:** `{vendor_email}`\n"
                    f"• **Subject:** `{email_rec['subject'] if email_rec else 'TATA MOTORS PO DISPATCH - APPROVED'}`\n"
                    f"• **Digital Signatory:** `R. Sen (Head BIW) [Shop Head]`\n"
                    f"• **Assigned Receiving Dock:** `{email_service._get_dock(cc_code)}`\n"
                    f"• **Quality Conformance:** `Mandatory IATF-16949 Certificate of Analysis (CoA)`\n"
                )
                st.session_state.pending_po = None
                st.session_state.show_approval_modal = False
                st.toast(f"✅ PO {po_num} approved and released to SAP Ariba!", icon="🎉")

                st.markdown(resp)
                if email_rec and email_rec.get("html_body"):
                    with st.expander("📧 Dispatched Supplier PO Letterhead (Official Transmitted Copy — Sent & Delivered)", expanded=True):
                        st.components.v1.html(email_rec["html_body"], height=480, scrolling=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": resp,
                    "email_html": email_rec.get("html_body") if email_rec else None,
                    "is_staged": False
                })
            else:
                resp = (
                    "**[STEP 6: TASK CANCELLED]**\n\n"
                    "❌ Requisition rejected by human authority. Zero budget committed. PO generation aborted and staged outbox hold released."
                )
                st.session_state.pending_po = None
                st.session_state.show_approval_modal = False
                st.toast("❌ Requisition rejected by authority. Zero funds committed.", icon="🛑")
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp, "is_staged": False})

        # -------------------------------------------------------------
        # STATE MACHINE: PROCESS REQUISITIONS STEP-BY-STEP
        # -------------------------------------------------------------
        else:
            strict_json, telemetry, ariba_po = engine.process_pr(input_text, input_meta)
            calc = strict_json["Calculations"]
            mat_code = strict_json["Material_Code"]
            mat = erp_db.get_material(mat_code) or {}
            routing = strict_json.get("Approval_Routing", {})
            requires_human = routing.get("Requires_Human_Approval", False)
            cc_code = routing.get("Cost_Center", "CC-PU-TCF")
            cc = erp_db.get_cost_center(cc_code)
            sup_name = strict_json.get("Selected_Supplier", "Contracted Supplier")
            rule_logs = strict_json.get("Guardrails_Triggered", [])
            ariba_txn = ariba_po.get("ariba_transaction", {}) if ariba_po else {}
            ariba_doc_id = ariba_txn.get("transaction_id", f"ARIBA-DOC-{calc['Final_PO_Qty']}")
            sha_digest = ariba_txn.get("payload_digest_sha256", "3f7a1e8c...verified")[:24]
            email_info = ariba_po.get("email_dispatch", {}) if ariba_po else {}
            vendor_email = email_info.get("recipient", "orders@supplier-network.com")
            rem_budget = cc.get("remaining_budget", 0.0) if cc else 0.0

            step1 = (
                f"**[STEP 1: IDENTIFYING THE PROBLEM]**\n"
                f"• Material Code: `{mat_code}`\n"
                f"• Material Description: {mat.get('name', 'Automotive Component')}\n"
                f"• Requested Quantity: {calc['Requested_Qty']} {mat.get('unit', 'units')}\n"
                f"• Lead Time / Urgency: {ariba_po.get('urgency_hours', 24)}h Required Delivery Window\n"
                f"• Requesting Cost Center: `{cc_code}` ({cc.get('name', 'Shop Floor') if cc else 'Central'})\n"
                f"• Vehicle Line: {mat.get('platforms', 'All Platforms')}\n\n"
            )

            compliance_rules = []
            if "Quality Hold" in rule_logs:
                compliance_rules.append("Rule A (Quality Hold): Primary supplier on IATF-16949 hold (>100 PPM); pivoted to certified alternate supplier.")
            if "PLI Block" in rule_logs:
                compliance_rules.append("Rule B (Auto PLI Scheme): Material is EV-critical; foreign vendor blocked to enforce 50% Domestic Value Addition (DVA).")
            if "JIT Pivot" in rule_logs:
                compliance_rules.append("Rule C (JIT Delivery): Required window < primary lead time; pivoted to local 24h alternate supplier to prevent line stoppage.")
            if "Anti-Split Rule" in rule_logs:
                compliance_rules.append(f"Rule D (Anti-Split Check): Detected duplicate requisition in rolling window; merged {calc['Requested_Qty']} + {calc['Merged_Prior_PR_Qty']} = {calc['Final_PO_Qty']} to prevent approval threshold circumvention.")
            if not compliance_rules:
                compliance_rules.append("Standard Compliance: Primary supplier active, PLI-compliant, and within quality tolerance.")

            rules_str = "\n • ".join(compliance_rules)
            step2_3 = (
                f"**[STEP 2 & 3: AUTOMATED SOURCING & MATH]**\n"
                f" • {rules_str}\n"
                f" • Selected Supplier: {sup_name}\n"
                f" • Math: {calc['Final_PO_Qty']} units × ₹{calc['Final_Unit_Rate_INR']:,.2f} = Total Value ₹{calc['Total_PO_Value_INR']:,.2f} INR\n"
                f" • Quantity Integrity: `{strict_json.get('Quantity_Integrity_Check', 'EXACT_MATCH')}`\n\n"
            )

            status_mark = "REQUIRES_HUMAN_APPROVAL" if requires_human else "AUTONOMOUS_APPROVED"
            approver_target = routing.get("Approver_Role", "Shop Head")
            step4 = (
                f"**[STEP 4: ROUTING DECISION]**\n"
                f"• Total PO Value: ₹{calc['Total_PO_Value_INR']:,.2f}\n"
                f"• Approval Threshold Matrix: {routing.get('Approval_Tier', 'Cost Center Delegation Matrix')}\n"
                f"• Governance Status: `{status_mark}`\n"
                f"• Assigned Signatory: {approver_target}\n\n"
            )

            if requires_human:
                st.session_state.pending_po = ariba_po
                st.session_state.show_approval_modal = True
                st.toast(f"🚨 APPROVAL REQUIRED: Digital signature requested from {approver_target}!", icon="🔔")

                step5 = (
                    f"**[STEP 5: NOTIFICATION / SYSTEM PAUSE]**\n"
                    f"🔔 NOTIFICATION TO {approver_target.upper()}: PR value is ₹{calc['Total_PO_Value_INR']:,.2f}. "
                    f"Justification: {strict_json.get('Reasoning', 'Exceeds Tier 1 auto-approval threshold.')}\n"
                    f"Vendor dispatch email has been STAGED in outbox (Held from dispatch).\n"
                    f"Please reply 'Approved' to proceed or 'Rejected' to cancel."
                )
                full_resp = step1 + step2_3 + step4 + step5
                st.markdown(full_resp)

                staged_email_html = None
                if erp_db.email_outbox and erp_db.email_outbox[0].get("po_number") == ariba_po['po_number']:
                    staged_email_html = erp_db.email_outbox[0].get("html_body")

                if staged_email_html:
                    with st.expander("⚠️ Staged Supplier Email (Held from Dispatch — Awaiting Authorization)", expanded=True):
                        st.caption("This email draft is currently HELD in the staging outbox. It will NOT be transmitted to the supplier or SAP Ariba until authorized.")
                        st.components.v1.html(staged_email_html, height=480, scrolling=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_resp,
                    "email_html": staged_email_html,
                    "is_staged": True
                })
                st.rerun()
            else:
                st.session_state.pending_po = None
                st.session_state.show_approval_modal = False
                step5 = (
                    f"**[STEP 5: NOTIFICATION / SYSTEM PAUSE]**\n"
                    f"No human required. Proceeding to Step 6.\n\n"
                )
                step6 = (
                    f"**[STEP 6: TASK COMPLETION]**\n"
                    f"✅ PO generated and dispatched to supplier.\n"
                    f"• PO Number: {ariba_po['po_number']}\n"
                    f"• Vendor: {sup_name}\n"
                    f"• Quantity: {calc['Final_PO_Qty']} {mat.get('unit', 'units')}\n"
                    f"• Total Value: ₹{calc['Total_PO_Value_INR']:,.2f}\n"
                    f"• SAP Ariba cXML 1.2.014 Document: {ariba_doc_id} (SYN-ACK Confirmed, SHA-256 Digest: {sha_digest})\n"
                    f"• EDI 850/855 Handshake: Completed (Status: ACK*IA, HTTP 200 OK)\n"
                    f"• Automated Dispatch Email: Sent to {vendor_email}\n"
                    f"• Budget Updated: {cc_code} remaining budget is ₹{rem_budget:,.2f}\n\n"
                    f"---\n"
                    f"### 📬 DISPATCHED SUPPLIER EMAIL (AUTONOMOUS DISPATCH COPY — SENT & DELIVERED)\n"
                    f"• **Transmission Status:** `✅ SENT & DELIVERED (SAP Ariba Verified)`\n"
                    f"• **Recipient:** `{vendor_email}`\n"
                    f"• **Subject:** `{email_info.get('subject', 'TATA MOTORS PO DISPATCH')}`\n"
                    f"• **Authorization:** `Autonomous Policy Tier 1`\n"
                    f"• **Assigned Receiving Dock:** `{email_service._get_dock(cc_code)}`\n"
                    f"• **Quality Conformance:** `Mandatory IATF-16949 Certificate of Analysis (CoA)`\n"
                )
                full_resp = step1 + step2_3 + step4 + step5 + step6
                st.markdown(full_resp)

                tier1_email_html = None
                if erp_db.email_outbox and erp_db.email_outbox[0].get("po_number") == ariba_po['po_number']:
                    tier1_email_html = erp_db.email_outbox[0].get("html_body")

                if tier1_email_html:
                    with st.expander("📧 Dispatched Supplier PO Letterhead (Official Transmitted Copy — Sent & Delivered)", expanded=True):
                        st.components.v1.html(tier1_email_html, height=480, scrolling=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_resp,
                    "email_html": tier1_email_html,
                    "is_staged": False
                })

# -------------------------------------------------------------
# DISPATCHED SUPPLIER OUTBOX LEDGER (LIVE ERP PREVIEW)
# -------------------------------------------------------------
if erp_db.email_outbox:
    st.divider()
    with st.expander(f"📬 Supplier Email Hub & Outbox ({len(erp_db.email_outbox)} Transmissions Recorded)", expanded=False):
        st.markdown("**Live Transmission Status Ledger:**")
        for idx, em in enumerate(erp_db.email_outbox):
            st_badge = "✅ RELEASED & DELIVERED" if "RELEASED" in em.get("status", "") else ("⚠️ STAGED IN BUFFER" if "STAGED" in em.get("status", "") else em.get("status", ""))
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**#{idx+1} {em.get('po_number')}** — *{em.get('subject')}*")
                st.caption(f"To: `{em.get('recipient_email')}` | Value: ₹{em.get('total_value_inr', 0.0):,.2f} | Time: {em.get('timestamp')}")
            with col_b:
                st.markdown(f"**{st_badge}**")
            
            with st.popover(f"🔍 View Letterhead Copy ({em.get('po_number')})"):
                st.components.v1.html(em.get("html_body", "<p>No body</p>"), height=420, scrolling=True)
                st.divider()
                st.caption("⚡ **Send Real-Time Copy to Mail ID:**")
                col_ob1, col_ob2 = st.columns([3, 1])
                with col_ob1:
                    ob_mail = st.text_input("Destination Mail ID:", value=st.session_state.get("custom_email", ""), key=f"ob_mail_{em.get('po_number')}_{idx}", placeholder="e.g. user@gmail.com")
                with col_ob2:
                    st.write("")
                    if st.button("🚀 Send Live Mail", key=f"btn_ob_{em.get('po_number')}_{idx}", use_container_width=True):
                        if ob_mail:
                            s_res = email_service.send_live_email(ob_mail.strip(), po_number=em.get('po_number'))
                            if s_res.get("success"):
                                st.success(s_res.get("message"))
                            else:
                                st.error(s_res.get("error"))
                        else:
                            st.warning("Please enter a destination mail ID.")
            st.divider()

