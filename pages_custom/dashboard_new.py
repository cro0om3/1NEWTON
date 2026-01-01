
import streamlit as st
import pandas as pd
from datetime import datetime
try:
    from utils import db as _db
except Exception:
    _db = None

# Apple-style icon grid for dashboard header
def _app_icon_grid():
    pass

# Apple Style Dashboard - Always visible structure


def _apply_dashboard_theme():
    # Use the app's global theme and styles — avoid page-specific heavy overrides
    # This keeps dashboard styling consistent with other pages.
    return
def _metric(title, value, subtitle=None):
    # Use the shared hero-card style from the global theme for consistent appearance
    st.markdown(
        f"""
        <div class="hero-card" style="text-align:center; padding:18px 20px;">
            <div style="font-size:28px;font-weight:700;color:var(--text-main);">{value}</div>
            <div style="font-size:18px;font-weight:500;color:var(--text-main);">{title}</div>
            <div style="font-size:15px;color:var(--accent);">{subtitle if subtitle else ""}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def dashboard_new_app():
    _apply_dashboard_theme()
    _app_icon_grid()
    # ربط البيانات مع Excel
    def _load_or_empty(path, columns):
        df = None
        if _db is not None:
            try:
                if path.endswith("records.xlsx"):
                    rows = _db.db_query(
                        "SELECT base_id, date, type, number, amount, client_name, phone, location, note FROM records ORDER BY date"
                    )
                    if rows:
                        df = pd.DataFrame(rows)
                        df.columns = [c.strip().lower() for c in df.columns]
                        if "date" in df.columns:
                            df["date"] = pd.to_datetime(df["date"], errors="coerce")
                        if "type" in df.columns:
                            df["type"] = df["type"].astype(str).str.lower()
                        if "amount" in df.columns:
                            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
                elif path.endswith("customers.xlsx"):
                    rows = _db.db_query(
                        "SELECT name, phone, email, address FROM customers ORDER BY id"
                    )
                    if rows:
                        df = pd.DataFrame(rows)
                        df = df.rename(columns={"name": "client_name", "address": "location"})
                        df.columns = [c.strip().lower() for c in df.columns]
            except Exception:
                df = None
        if df is None:
            try:
                df = pd.read_excel(path)
                df.columns = [c.strip().lower() for c in df.columns]
            except Exception:
                df = pd.DataFrame(columns=columns)
        for col in columns:
            if col not in df.columns:
                df[col] = None
        return df[columns]

    records = _load_or_empty(
        "data/records.xlsx",
        ["base_id", "date", "type", "number", "amount", "client_name", "phone", "location", "note"],
    )
    customers = _load_or_empty(
        "data/customers.xlsx",
        ["client_name", "phone", "location", "last_activity", "status"],
    )

    rec = records.copy()
    if not rec.empty and "date" in rec.columns:
        rec["date"] = pd.to_datetime(rec["date"], errors="coerce")

    total_q = int((rec["type"] == "q").sum()) if "type" in rec.columns else 0
    total_i = int((rec["type"] == "i").sum()) if "type" in rec.columns else 0
    total_r = int((rec["type"] == "r").sum()) if "type" in rec.columns else 0
    total_invoice_amount = float(rec.loc[rec.get("type","") == "i", "amount"].sum()) if "amount" in rec.columns else 0.0
    total_received = float(rec.loc[rec.get("type","") == "r", "amount"].sum()) if "amount" in rec.columns else 0.0
    remaining_balance = total_invoice_amount - total_received

    c1, c2, c3 = st.columns(3)
    with c1: _metric("Quotations", total_q, "Active proposals")
    with c2: _metric("Invoices", total_i, "Issued bills")
    with c3: _metric("Receipts", total_r, "Recorded payments")

    c4, c5, c6 = st.columns(3)
    with c4: _metric("Invoice Volume", f"AED {total_invoice_amount:,.0f}")
    with c5: _metric("Received", f"AED {total_received:,.0f}")
    with c6: _metric("Outstanding", f"AED {remaining_balance:,.0f}")

    st.markdown('<div class="section-title">Project Lifecycle Tracking</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
    # English Project Lifecycle Table with icons
    lifecycle_data = pd.DataFrame([
        {"Base ID": "20251116-002", "Client": "Fahad Ahmed Mohammed", "Phone": "5292932", "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": True, "Receipt": True, "Amount": 5639.93, "Balance": 5639.93, "Last Update": "2025-11-20 00:00:00"},
        {"Base ID": "20251116-004", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-16 00:00:00"},
        {"Base ID": "20251116-012", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-16 00:00:00"},
        {"Base ID": "20251117-003", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-17 00:00:00"},
        {"Base ID": "20251118-002", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-18 00:00:00"},
        {"Base ID": "20251119-002", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-19 00:00:00"},
        {"Base ID": "20251120-003", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-20 00:00:00"},
        {"Base ID": "20251120-005", "Client": None, "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": False, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-20 00:00:00"},
        {"Base ID": "20251120-007", "Client": "Fahad Ahmed", "Phone": None, "Location": "Abu Dhabi - Al Shamkha", "Quotation": True, "Invoice": True, "Receipt": False, "Amount": 0, "Balance": 0, "Last Update": "2025-11-20 00:00:00"},
    ])
    # تحويل القيم True/False إلى رموز
    for col in ["Quotation", "Invoice", "Receipt"]:
        lifecycle_data[col] = lifecycle_data[col].apply(lambda x: "<span style='font-size:22px;'>✅</span>" if x else "<span style='font-size:22px;'>❌</span>")
    # تنسيق المبلغ بدقتين عشريتين
    lifecycle_data["Amount"] = lifecycle_data["Amount"].apply(lambda x: f"{x:,.2f}")
    lifecycle_data["Balance"] = lifecycle_data["Balance"].apply(lambda x: f"{x:,.2f}")
    st.markdown(f"<div style='overflow-x:auto;'><table class='project-table'>{lifecycle_data.to_html(escape=False, index=False, classes='stTable')}</table></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    two1, two2 = st.columns(2)
    with two1:
        st.markdown('<div class="section-title">Latest Invoices</div>', unsafe_allow_html=True)
        st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
        if not rec.empty and "type" in rec.columns:
            last_10_invoices = (
                rec[rec["type"] == "i"]
                .sort_values("date", ascending=False, na_position="last")
                .head(10)[["date", "number", "client_name", "amount"]]
            )
            if not last_10_invoices.empty:
                d = last_10_invoices.copy()
                if "date" in d.columns:
                    d["date"] = pd.to_datetime(d["date"], errors="coerce").dt.strftime("%Y-%m-%d")
                st.table(d.rename(columns={"date": "Date", "number": "Invoice", "client_name": "Client", "amount": "Amount (AED)"}))
            else:
                st.write("No invoices yet.")
        else:
            st.write("No invoices yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with two2:
        st.markdown('<div class="section-title">Latest Receipts</div>', unsafe_allow_html=True)
        st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
        if not rec.empty and "type" in rec.columns:
            last_10_receipts = (
                rec[rec["type"] == "r"]
                .sort_values("date", ascending=False, na_position="last")
                .head(10)[["date", "number", "client_name", "amount"]]
            )
            if not last_10_receipts.empty:
                d = last_10_receipts.copy()
                if "date" in d.columns:
                    d["date"] = pd.to_datetime(d["date"], errors="coerce").dt.strftime("%Y-%m-%d")
                st.table(d.rename(columns={"date": "Date", "number": "Receipt", "client_name": "Client", "amount": "Amount (AED)"}))
            else:
                st.write("No receipts yet.")
        else:
            st.write("No receipts yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Customer Signals</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-wrap">', unsafe_allow_html=True)
    if not customers.empty:
        st.table(
            customers.rename(
                columns={
                    "client_name": "Client",
                    "phone": "Phone",
                    "location": "Location",
                    "last_activity": "Last Activity",
                    "status": "Stage",
                }
            )
        )
    else:
        st.write("No customer records yet.")
    st.markdown('</div>', unsafe_allow_html=True)
