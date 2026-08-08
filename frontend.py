import streamlit as st
import requests
import pandas as pd

from dataset.operations import get_scan_history


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="QR Shield",
    page_icon="QR",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================================================
# SESSION STATE
# ======================================================

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "scan_error" not in st.session_state:
    st.session_state.scan_error = None


# ======================================================
# LOAD CSS
# ======================================================

def load_css():
    try:
        with open("assets/styles.css", encoding="utf-8") as css:
            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css()


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown(
        """
        <div class="section-title">
            QR Shield
        </div>

        <div class="section-subtitle">
            AI Powered Threat Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Capabilities")

    st.markdown(
        """
        - QR Code Decoding
        - Payload Detection
        - URL Risk Analysis
        - VirusTotal Integration
        - WHOIS Lookup
        - IP Intelligence
        - Hosting Detection
        - File Download Analysis
        - Scan History
        """
    )

    st.divider()

    st.caption(
        "QR Security Analysis Platform"
    )


# ======================================================
# HEADER
# ======================================================

st.markdown(
    """
    <div class="main-title">
        QR Shield
    </div>

    <div class="subtitle">
        AI Powered QR Threat Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

st.write(
    "Upload a QR code image to perform security analysis, "
    "payload detection and threat intelligence checks."
)

st.write("")


# ======================================================
# UPLOAD AREA
# ======================================================

left_space, upload_col, right_space = st.columns([1, 2, 1])

with upload_col:

    st.markdown("### Upload QR Code")

    uploaded_file = st.file_uploader(
        "",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )


# ======================================================
# MAIN ANALYSIS
# ======================================================

if uploaded_file is not None:

    preview_col, result_col = st.columns([1, 2])

    # --------------------------------------------------
    # QR PREVIEW
    # --------------------------------------------------

    with preview_col:

        st.image(
            uploaded_file,
            use_container_width=True
        )

    # --------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------

    with result_col:

        st.write("")
        st.write("")

        analyze = st.button(
            "Analyze QR Code",
            use_container_width=True,
            type="primary"
        )

        if analyze:

            st.session_state.scan_result = None
            st.session_state.scan_error = None

            try:

                with st.spinner("Analyzing QR Code..."):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }

                    response = requests.post(
                        "http://127.0.0.1:5000/scan",
                        files=files,
                        timeout=60
                    )

                # ------------------------------------------
                # SUCCESS
                # ------------------------------------------

                if response.status_code == 200:

                    st.session_state.scan_result = response.json()

                # ------------------------------------------
                # BACKEND ERROR
                # ------------------------------------------

                else:

                    try:
                        error_data = response.json()
                    except Exception:
                        error_data = response.text

                    st.session_state.scan_error = {
                        "status": response.status_code,
                        "message": error_data
                    }

            except requests.exceptions.ConnectionError:

                st.session_state.scan_error = {
                    "status": "Connection Error",
                    "message": (
                        "Could not connect to the Flask backend. "
                        "Make sure python app.py is running."
                    )
                }

            except requests.exceptions.Timeout:

                st.session_state.scan_error = {
                    "status": "Timeout",
                    "message": (
                        "The backend took too long to respond."
                    )
                }

            except Exception as e:

                st.session_state.scan_error = {
                    "status": "Unexpected Error",
                    "message": str(e)
                }


# ======================================================
# DISPLAY BACKEND ERROR
# ======================================================

if st.session_state.scan_error is not None:

    error = st.session_state.scan_error

    st.error(
        f"Analysis failed — {error['status']}"
    )

    st.code(
        str(error["message"])
    )


# ======================================================
# DISPLAY RESULTS
# ======================================================

result = st.session_state.scan_result

if result is not None:

    st.success(
        "Analysis completed successfully."
    )

    st.divider()

    # ==================================================
    # PAYLOAD INFORMATION
    # ==================================================

    st.markdown("## Payload Information")

    payload_col1, payload_col2 = st.columns([1, 3])

    with payload_col1:

        st.markdown("**Type**")

        st.info(
            result.get("payload_type", "Unknown")
        )

    with payload_col2:

        st.markdown("**Content**")

        st.code(
            result.get("payload_data", "No payload data available.")
        )

    payload_type = result.get(
        "payload_type",
        ""
    )

    if payload_type == "URL":

        decoded_url = result.get(
            "decoded_url"
        )

        if decoded_url:

            st.link_button(
                "Open Website",
                decoded_url
            )

    st.divider()

    # ==================================================
    # URL ANALYSIS
    # ==================================================

    if payload_type == "URL":

        # --------------------------------------------------
        # RISK OVERVIEW
        # --------------------------------------------------

        st.markdown("## Risk Overview")

        c1, c2, c3 = st.columns(3)

        risk_score = result.get(
            "risk_score",
            0
        )

        risk_level = result.get(
            "risk_level",
            "Unknown"
        )

        domain_age = result.get(
            "domain_age_days"
        )

        with c1:

            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )

        with c2:

            st.metric(
                "Risk Level",
                risk_level
            )

        with c3:

            if domain_age is None:

                st.metric(
                    "Domain Age",
                    "N/A"
                )

            else:

                st.metric(
                    "Domain Age",
                    f"{domain_age} days"
                )

        st.progress(
            min(max(float(risk_score) / 100, 0), 1)
        )

        st.divider()

        # --------------------------------------------------
        # THREAT INDICATORS
        # --------------------------------------------------

        st.markdown("## Threat Indicators")

        reasons = result.get(
            "reasons",
            []
        )

        if reasons:

            for reason in reasons:

                st.markdown(
                    f"- {reason}"
                )

        else:

            st.success(
                "No suspicious indicators were detected."
            )

        st.divider()

        # --------------------------------------------------
        # VIRUSTOTAL
        # --------------------------------------------------

        st.markdown("## VirusTotal Analysis")

        vt = result.get(
            "virustotal",
            {}
        )

        vt1, vt2, vt3 = st.columns(3)

        with vt1:

            st.metric(
                "Malicious",
                vt.get("malicious", 0)
            )

        with vt2:

            st.metric(
                "Suspicious",
                vt.get("suspicious", 0)
            )

        with vt3:

            st.metric(
                "Harmless",
                vt.get("harmless", 0)
            )

        st.divider()

        # --------------------------------------------------
        # DOWNLOADABLE FILE SCAN
        # --------------------------------------------------

        st.markdown("## Downloadable File Scan")

        file_scan = result.get(
            "file_scan",
            {}
        )

        if file_scan.get("success"):

            f1, f2, f3 = st.columns(3)

            with f1:

                st.metric(
                    "Malicious",
                    file_scan.get("malicious", 0)
                )

            with f2:

                st.metric(
                    "Suspicious",
                    file_scan.get("suspicious", 0)
                )

            with f3:

                st.metric(
                    "Harmless",
                    file_scan.get("harmless", 0)
                )

        else:

            st.info(
                file_scan.get(
                    "reason",
                    "No downloadable file detected."
                )
            )

        st.divider()

        # --------------------------------------------------
        # IP INTELLIGENCE
        # --------------------------------------------------

        st.markdown("## IP Intelligence")

        ip = result.get(
            "ip_information",
            {}
        )

        if ip.get("success"):

            ip_left, ip_right = st.columns(2)

            with ip_left:

                st.metric(
                    "IP Address",
                    ip.get("ip", "N/A")
                )

                st.metric(
                    "Country",
                    ip.get("country", "N/A")
                )

                st.metric(
                    "City",
                    ip.get("city", "N/A")
                )

            with ip_right:

                st.metric(
                    "ISP",
                    ip.get("isp", "N/A")
                )

                st.metric(
                    "Organization",
                    ip.get("org", "N/A")
                )

                st.metric(
                    "ASN",
                    ip.get("asn", "N/A")
                )

        else:

            st.info(
                ip.get(
                    "reason",
                    "IP intelligence unavailable."
                )
            )

        st.divider()

        # --------------------------------------------------
        # HOSTING PROVIDER
        # --------------------------------------------------

        st.markdown("## Hosting Provider")

        host = result.get(
            "hosting_provider",
            {}
        )

        hp1, hp2 = st.columns(2)

        with hp1:

            st.metric(
                "Provider",
                host.get(
                    "provider",
                    "N/A"
                )
            )

        with hp2:

            st.metric(
                "Classification",
                host.get(
                    "risk",
                    "N/A"
                )
            )

        st.divider()

        # --------------------------------------------------
        # RECOMMENDATION
        # --------------------------------------------------

        st.markdown("## Recommendation")

        if risk_score < 40:

            st.success(
                "This QR code appears safe to access."
            )

        elif risk_score < 70:

            st.warning(
                "Proceed with caution before opening this QR code."
            )

        else:

            st.error(
                "High-risk QR code detected. Do not open it."
            )

    # ==================================================
    # NON-URL PAYLOAD
    # ==================================================

    else:

        st.info(
            "This QR code does not contain a URL."
        )

        payload_messages = {

            "WiFi":
                "WiFi configuration detected.",

            "vCard":
                "Contact card detected.",

            "Email":
                "Email payload detected.",

            "SMS":
                "SMS payload detected.",

            "Phone":
                "Phone number detected.",

            "Location":
                "Location payload detected.",

            "UPI Payment":
                "UPI payment request detected."
        }

        st.success(
            payload_messages.get(
                payload_type,
                "Plain text payload detected."
            )
        )


# ======================================================
# SCAN HISTORY
# ======================================================

st.divider()

st.markdown("## Scan History")

try:

    history = get_scan_history()

except Exception as e:

    history = []

    st.error(
        f"Could not load scan history: {e}"
    )


if history:

    df = pd.DataFrame(
        history,
        columns=[
            "Filename",
            "Payload Type",
            "Decoded URL",
            "Risk Score",
            "Risk Level",
            "Scanned At"
        ]
    )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    search = st.text_input(
        "Search History",
        placeholder="Search filename, URL or payload..."
    )

    if search:

        search_lower = search.lower()

        mask = (
            df["Filename"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower, na=False)
            |
            df["Decoded URL"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower, na=False)
            |
            df["Payload Type"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower, na=False)
        )

        df = df[mask]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # DOWNLOAD HISTORY
    # --------------------------------------------------

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Scan History",
        csv,
        "scan_history.csv",
        "text/csv",
        use_container_width=True
    )

else:

    st.info(
        "No scan history available."
    )


# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px;
        color:#6B7280;
        font-size:14px;
    ">
        <b>QR Shield</b><br>
        AI Powered QR Threat Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)