"""
SLRAI Streamlit Dashboard — developer testing interface.

Usage:
    .venv\\Scripts\\streamlit.exe run dashboard.py
"""

from __future__ import annotations

import json
import os

import requests
import streamlit as st

API_BASE_URL = os.environ.get("SLRAI_API_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="SLRAI Dev Dashboard",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── SESSION STATE ────────────────────────────────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "current_case_id" not in st.session_state:
    st.session_state.current_case_id = None
if "request_log" not in st.session_state:
    st.session_state.request_log = []


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def api_call(method: str, path: str, **kwargs) -> tuple[int, dict | str]:
    url = f"{API_BASE_URL}{path}"
    headers = kwargs.pop("headers", {})
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        resp = requests.request(method, url, headers=headers, timeout=30, **kwargs)
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        st.session_state.request_log.insert(
            0, {"method": method, "path": path, "status": resp.status_code}
        )
        if len(st.session_state.request_log) > 30:
            st.session_state.request_log = st.session_state.request_log[:30]
        return resp.status_code, body
    except requests.exceptions.ConnectionError:
        return 0, {"error": "Connection refused — is the API server running?"}
    except Exception as exc:
        return 0, {"error": str(exc)}


def show_response(status: int, body: dict | str) -> None:
    if status == 0:
        st.error(f"Connection error: {body}")
    elif status < 300:
        st.success(f"HTTP {status}")
        st.json(body)
    elif status < 500:
        st.warning(f"HTTP {status}")
        st.json(body)
    else:
        st.error(f"HTTP {status}")
        st.json(body)


def require_auth() -> bool:
    if not st.session_state.token:
        st.warning("Not authenticated — log in first using the Auth tab.")
        return False
    return True


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("⚖ SLRAI")
    st.caption("Dev Testing Dashboard")
    st.divider()

    if st.session_state.token:
        user = st.session_state.user_info or {}
        st.success(f"Authenticated")
        st.caption(f"**{user.get('email', 'Unknown')}** ({user.get('role', '')})")
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user_info = None
            st.rerun()
    else:
        st.info("Not logged in")

    st.divider()

    manual_token = st.text_input("Manual Token Override", type="password", key="manual_token_input")
    if manual_token and st.button("Apply Token"):
        st.session_state.token = manual_token
        st.rerun()

    st.divider()

    override_url = st.text_input("API URL Override", value=API_BASE_URL, key="url_override")
    if override_url != API_BASE_URL:
        API_BASE_URL = override_url

    if st.session_state.current_case_id:
        st.divider()
        st.caption("Active Case")
        st.code(st.session_state.current_case_id, language=None)
        if st.button("Clear Active Case"):
            st.session_state.current_case_id = None
            st.rerun()

    st.divider()
    st.caption("Request Log (last 30)")
    for entry in st.session_state.request_log[:10]:
        color = "🟢" if entry["status"] < 300 else ("🟡" if entry["status"] < 500 else "🔴")
        st.caption(f"{color} {entry['method']} {entry['path']} — {entry['status']}")


# ─── TABS ────────────────────────────────────────────────────────────────────

tabs = st.tabs(["Auth", "Cases", "Documents", "Workbench", "Results", "Report", "Health"])

# ─────────────────────────────────────────────────────────────────────────────
# AUTH TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[0]:
    st.header("Authentication")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_pass  = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="btn_login"):
            status, body = api_call("POST", "/auth/login", json={"email": login_email, "password": login_pass})
            if status == 200:
                st.session_state.token = body.get("access_token")
                # Fetch user info
                _, me_body = api_call("GET", "/auth/me")
                if isinstance(me_body, dict):
                    st.session_state.user_info = me_body
                st.rerun()
            else:
                show_response(status, body)

    with col2:
        st.subheader("Register New Bank")
        reg_bank_name  = st.text_input("Bank Name", key="reg_bank_name")
        reg_bank_code  = st.text_input("Short Code", key="reg_bank_code")
        reg_email      = st.text_input("Admin Email", key="reg_email")
        reg_pass       = st.text_input("Admin Password", type="password", key="reg_pass")
        if st.button("Register", key="btn_register"):
            status, body = api_call("POST", "/auth/register", json={
                "bank_name": reg_bank_name,
                "bank_short_code": reg_bank_code,
                "admin_email": reg_email,
                "admin_password": reg_pass,
            })
            show_response(status, body)

    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Create User")
        cu_email = st.text_input("Email", key="cu_email")
        cu_pass  = st.text_input("Password", type="password", key="cu_pass")
        cu_role  = st.selectbox("Role", ["BANK_OFFICER", "BANK_ADMIN"], key="cu_role")
        if st.button("Create User", key="btn_cu"):
            status, body = api_call("POST", "/auth/users", json={
                "email": cu_email,
                "password": cu_pass,
                "role": cu_role,
            })
            show_response(status, body)

    with col4:
        st.subheader("Token Actions")
        if st.button("Refresh Token", key="btn_refresh"):
            status, body = api_call("POST", "/auth/refresh")
            if status == 200:
                st.session_state.token = body.get("access_token")
                st.success("Token refreshed.")
            else:
                show_response(status, body)

        if st.button("Whoami", key="btn_whoami"):
            status, body = api_call("GET", "/auth/me")
            show_response(status, body)


# ─────────────────────────────────────────────────────────────────────────────
# CASES TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[1]:
    st.header("Cases")
    if not st.session_state.token:
        st.warning("Log in first.")
    else:
        col_l, col_r = st.columns([1, 1])

        with col_l:
            st.subheader("Create Case")
            borrower = st.text_input("Borrower Name*", key="c_borrower")
            case_ref = st.text_input("Case Ref", key="c_ref")
            drt_num  = st.text_input("DRT Case Number", key="c_drt")
            drt_bench = st.text_input("DRT Bench", key="c_bench")
            prop_desc = st.text_area("Property Description", key="c_prop", height=60)
            loan_acc  = st.text_input("Loan Account Number", key="c_loan")
            principal = st.number_input("Principal Amount (₹)", min_value=0.0, step=10000.0, key="c_principal")

            if st.button("Create Case", key="btn_create_case"):
                payload = {"borrower_name": borrower}
                if case_ref:  payload["case_ref"] = case_ref
                if drt_num:   payload["drt_case_number"] = drt_num
                if drt_bench: payload["drt_bench"] = drt_bench
                if prop_desc: payload["property_description"] = prop_desc
                if loan_acc:  payload["loan_account_number"] = loan_acc
                if principal: payload["principal_amount"] = principal
                status, body = api_call("POST", "/cases", json=payload)
                show_response(status, body)
                if status == 201 and isinstance(body, dict):
                    st.session_state.current_case_id = body.get("id")

        with col_r:
            st.subheader("List Cases")
            list_status_filter = st.selectbox("Filter by Status", ["(all)", "DRAFT", "PROCESSING", "PENDING_HUMAN_REVIEW", "ANALYSING", "COMPLETE", "FAILED"], key="list_status")
            list_search = st.text_input("Search (borrower/ref/DRT)", key="list_search")
            list_page = st.number_input("Page", min_value=1, value=1, key="list_page")

            if st.button("List Cases", key="btn_list_cases"):
                params: dict = {"page": list_page, "page_size": 20}
                if list_status_filter != "(all)":
                    params["status"] = list_status_filter
                if list_search:
                    params["search"] = list_search
                status, body = api_call("GET", "/cases", params=params)
                show_response(status, body)

        st.divider()

        col_get, col_patch = st.columns(2)

        with col_get:
            st.subheader("Get / Select Case")
            get_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="get_case_id")
            if st.button("Get Case", key="btn_get_case"):
                status, body = api_call("GET", f"/cases/{get_case_id}")
                show_response(status, body)
                if status == 200:
                    st.session_state.current_case_id = get_case_id

        with col_patch:
            st.subheader("Update Case")
            patch_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="patch_case_id")
            patch_borrower = st.text_input("New Borrower Name", key="patch_borrower")
            if st.button("Update Case", key="btn_patch_case"):
                payload = {}
                if patch_borrower:
                    payload["borrower_name"] = patch_borrower
                status, body = api_call("PATCH", f"/cases/{patch_case_id}", json=payload)
                show_response(status, body)

        st.divider()
        col_pipe, col_resume = st.columns(2)

        with col_pipe:
            st.subheader("Pipeline Status")
            pipe_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="pipe_case_id")
            auto_refresh = st.checkbox("Auto-refresh every 5s", key="auto_refresh")
            if st.button("Get Pipeline Status", key="btn_pipe") or auto_refresh:
                status, body = api_call("GET", f"/cases/{pipe_case_id}/pipeline-status")
                show_response(status, body)
                if auto_refresh:
                    import time
                    time.sleep(5)
                    st.rerun()

        with col_resume:
            st.subheader("Resume Analysis (Chain B)")
            resume_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="resume_case_id")
            st.warning("This triggers Chain B. Only use after completing workbench review.")
            if st.button("Resume Analysis", key="btn_resume"):
                status, body = api_call("POST", f"/cases/{resume_case_id}/resume")
                show_response(status, body)

        st.divider()
        st.subheader("Delete Case (ADMIN)")
        del_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="del_case_id")
        if st.button("Delete Case", key="btn_del_case", type="primary"):
            status, body = api_call("DELETE", f"/cases/{del_case_id}")
            show_response(status, body)


# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENTS TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[2]:
    st.header("Documents")
    if not require_auth():
        pass
    else:
        doc_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="doc_case_id")

        st.subheader("Upload Document")
        uploaded = st.file_uploader("Choose PDF", type=["pdf"], key="doc_upload")
        doc_type = st.selectbox("Document Type", ["sa_petition", "demand_notice", "possession_notice", "valuation_report", "auction_notice", "other"], key="doc_type")

        if st.button("Upload", key="btn_upload_doc") and uploaded:
            status, body = api_call(
                "POST", f"/cases/{doc_case_id}/documents",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                data={"doc_type": doc_type},
            )
            show_response(status, body)

        st.subheader("List Documents")
        if st.button("List Documents", key="btn_list_docs"):
            status, body = api_call("GET", f"/cases/{doc_case_id}/documents")
            show_response(status, body)


# ─────────────────────────────────────────────────────────────────────────────
# WORKBENCH TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[3]:
    st.header("Workbench")
    if not require_auth():
        pass
    else:
        wb_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="wb_case_id")

        col_wb1, col_wb2 = st.columns(2)

        with col_wb1:
            if st.button("View Workbench (needs review)", key="btn_wb_view"):
                status, body = api_call("GET", f"/cases/{wb_case_id}/workbench")
                show_response(status, body)

            if st.button("All Facts", key="btn_wb_all"):
                status, body = api_call("GET", f"/cases/{wb_case_id}/workbench/all-facts")
                show_response(status, body)

        with col_wb2:
            st.subheader("Confirm / Correct Fact")
            cf_field = st.text_input("Field Name", key="cf_field")
            cf_value = st.text_input("Confirmed Value", key="cf_value")
            if st.button("Confirm Fact", key="btn_cf"):
                status, body = api_call("POST", f"/cases/{wb_case_id}/workbench/confirm",
                                        json={"field_name": cf_field, "confirmed_value": cf_value})
                show_response(status, body)

        st.subheader("Confirm All (triggers Chain B)")
        st.warning("This marks all facts as confirmed and fires Chain B automatically.")
        if st.button("Confirm All Facts", key="btn_confirm_all", type="primary"):
            status, body = api_call("POST", f"/cases/{wb_case_id}/workbench/confirm-all")
            show_response(status, body)


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[4]:
    st.header("Compliance Results")
    if not require_auth():
        pass
    else:
        res_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="res_case_id")

        col_r1, col_r2 = st.columns(2)

        with col_r1:
            if st.button("Compliance Results", key="btn_compliance"):
                status, body = api_call("GET", f"/cases/{res_case_id}/results/compliance")
                show_response(status, body)

            if st.button("Ground Scores", key="btn_grounds"):
                status, body = api_call("GET", f"/cases/{res_case_id}/results/grounds")
                show_response(status, body)

        with col_r2:
            if st.button("Judgments", key="btn_judgments"):
                status, body = api_call("GET", f"/cases/{res_case_id}/results/judgments")
                show_response(status, body)

            if st.button("Corpus Stats", key="btn_corpus"):
                status, body = api_call("GET", f"/cases/{res_case_id}/results/corpus-stats")
                show_response(status, body)


# ─────────────────────────────────────────────────────────────────────────────
# REPORT TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[5]:
    st.header("Report")
    if not require_auth():
        pass
    else:
        rpt_case_id = st.text_input("Case ID", value=st.session_state.current_case_id or "", key="rpt_case_id")

        if st.button("Generate Report", key="btn_gen_report", type="primary"):
            status, body = api_call("POST", f"/cases/{rpt_case_id}/reports/generate")
            show_response(status, body)

        if st.button("Get Latest Report (JSON)", key="btn_get_report"):
            status, body = api_call("GET", f"/cases/{rpt_case_id}/reports/latest")
            show_response(status, body)

        st.subheader("Download PDF")
        rpt_report_id = st.text_input("Report ID", key="rpt_report_id")
        if st.button("Get PDF URL", key="btn_pdf"):
            status, body = api_call("GET", f"/cases/{rpt_case_id}/reports/{rpt_report_id}/pdf")
            show_response(status, body)


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH TAB
# ─────────────────────────────────────────────────────────────────────────────

with tabs[6]:
    st.header("Health")

    if st.button("Ping /health", key="btn_health"):
        status, body = api_call("GET", "/health")
        show_response(status, body)

    if st.button("Ping API Root (/)", key="btn_root"):
        url = API_BASE_URL.replace("/api/v1", "")
        try:
            resp = requests.get(url, timeout=5)
            show_response(resp.status_code, resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text)
        except Exception as exc:
            st.error(str(exc))

    st.divider()
    st.subheader("Raw API Call")
    raw_method = st.selectbox("Method", ["GET", "POST", "PATCH", "DELETE"], key="raw_method")
    raw_path   = st.text_input("Path (e.g. /auth/me)", key="raw_path")
    raw_body   = st.text_area("JSON Body (optional)", key="raw_body", height=80)

    if st.button("Send", key="btn_raw"):
        kwargs: dict = {}
        if raw_body.strip():
            try:
                kwargs["json"] = json.loads(raw_body)
            except json.JSONDecodeError as exc:
                st.error(f"Invalid JSON: {exc}")
                kwargs = {}
        if kwargs is not None:
            status, body = api_call(raw_method, raw_path, **kwargs)
            show_response(status, body)
