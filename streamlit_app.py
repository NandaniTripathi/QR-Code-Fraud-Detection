import streamlit as st
import requests
import pandas as pd

from dataset.operations import get_scan_history


# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="QR Shield",
    page_icon="🛡️",
    layout="wide"
)


# =====================================
# Load Custom CSS
# =====================================

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# =====================================
# Header
# =====================================

st.markdown("""
<div class="main-title">
    QR Shield
</div>

<div class="subtitle">
    AI Powered QR Code Security Scanner
</div>
""", unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# =====================================
# Upload Section
# =====================================

left_space, center, right_space = st.columns([1, 2, 1])

with center:

    st.markdown("""
    <div class="section-title">
        Upload QR Code
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )



# =====================================
# Upload Section
# =====================================

if uploaded_file is not None:

    preview_col, result_col = st.columns([1, 2])

    # ---------------------------------
    # QR Preview
    # ---------------------------------

    with preview_col:

        st.markdown("""
        <div class="card-title">
            QR Preview
        </div>
        """, unsafe_allow_html=True)

        st.image(
            uploaded_file,
            use_container_width=True
        )

    # ---------------------------------
    # Scan Button
    # ---------------------------------

    with result_col:

        analyze = st.button(
            "Analyze QR Code",
            use_container_width=True
        )

        if analyze:

            progress = st.progress(0)

            progress.progress(10)

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            progress.progress(40)

            response = requests.post(
                "http://127.0.0.1:5000/scan",
                files=files
            )

            progress.progress(100)

            if response.status_code == 200:

                result = response.json()

                st.success("Analysis completed successfully.")


                # -----------------------------

                # URL

                # -----------------------------

                # =====================================
                # Payload Information
                # =====================================

                st.subheader("Payload Information")

                payload_type = result["payload_type"]

                payload_col1, payload_col2 = st.columns([1, 3])

                with payload_col1:
                    st.metric(
                        "Payload Type",
                        payload_type
                    )

                with payload_col2:
                    st.code(result["payload_data"])

                # Show button only for URL payloads
                if payload_type == "URL":

                    st.link_button(
                        "Open Website",
                        result["decoded_url"],
                        use_container_width=True
                    )

                st.divider()

                # Continue with URL-specific analysis
                if payload_type == "URL":

                # -----------------------------

                # Metrics

                # -----------------------------

                    score_col, level_col, age_col = st.columns(3)



                    score_col.metric(

                        "Risk Score",

                        f"{result['risk_score']}/100"

                    )



                    age = result.get("domain_age_days")



                    if age is not None:

                       age_col.metric(

                          "Domain Age",

                           f"{age} days"

                        )



                    level = result["risk_level"]



                    if level == "Low":

                       level_col.success("LOW")

                    elif level == "Medium":

                        level_col.warning("MEDIUM")

                    else:

                        level_col.error("HIGH")



                # Risk Progress Bar

                    st.progress(result["risk_score"] / 100)



                    st.divider()



                # -----------------------------

                # Threat Indicators

                # -----------------------------

                    st.subheader("Threat Indicators")

                    if result["reasons"]:

                        for reason in result["reasons"]:

                            st.markdown(f"- {reason}")

                    else:

                        st.info("No suspicious indicators were detected.")

                    st.divider()



                # -----------------------------
                # VirusTotal
                # -----------------------------
                    st.subheader("VirusTotal Results")

                    vt = result["virustotal"]

                    c1, c2, c3 = st.columns(3)

                    c1.metric("Malicious", vt["malicious"])
                    c2.metric("Suspicious", vt["suspicious"])
                    c3.metric("Harmless", vt["harmless"])

                    st.divider()

                # -----------------------------
# Downloadable File Scan
# -----------------------------
                    st.subheader("Downloadable File Scan")

                    file_scan = result["file_scan"]

                    if file_scan["success"]:

                        malicious_col, suspicious_col, harmless_col = st.columns(3)

                        malicious_col.metric(
                            "Malicious",
                            file_scan["malicious"]
                    )

                        suspicious_col.metric(
                            "Suspicious",
                            file_scan["suspicious"]
               )

                        harmless_col.metric(
                            "Harmless",
                            file_scan["harmless"]
      )

                    else:

                        st.info(file_scan["reason"])

                    st.divider()    


# -----------------------------
# IP Geolocation
# -----------------------------
                    st.subheader("IP Geolocation")

                    ip = result["ip_information"]

                    if ip["success"]:

                       left, right = st.columns(2)

                       with left:
                    
                            st.metric("IP Address", ip["ip"])
                            st.metric("Country", ip["country"])
                            st.metric("City", ip["city"])

                       with right:
                            st.metric("ISP", ip["isp"])
                            st.metric("Organization", ip["org"])
                            st.metric("ASN", ip["asn"])

                    else:
                        st.warning(ip["reason"])

                    st.divider()


# -----------------------------
# Hosting Provider
# -----------------------------
                    st.subheader("Hosting Provider")

                    host = result["hosting_provider"]

                    provider_col, class_col = st.columns(2)

                    provider_col.metric("Provider", host["provider"])
                    class_col.metric("Classification", host["risk"])

                    st.divider()


# -----------------------------
# Recommendation
# -----------------------------
                    st.subheader("Recommendation")

                    if result["risk_score"] < 40:

                        st.success(
                            "This QR Code appears safe."
                        )

                    elif result["risk_score"] < 70:

                        st.warning(
                            "Be cautious before opening this URL."
                        )

                    else:

                        st.error(
                           "High Risk! Avoid opening this QR Code."
                       )



                else:

                    st.info("This QR code does not contain a website.")

                    payload_type = result["payload_type"]

                    if payload_type == "WiFi":
                       st.success("WiFi Configuration QR Code detected.")

                    elif payload_type == "vCard":
                       st.success("Contact Card detected.")

                    elif payload_type == "Email":
                       st.success("Email QR Code detected.")

                    elif payload_type == "SMS":
                       st.success("SMS QR Code detected.")

                    elif payload_type == "Phone":
                       st.success("Phone Number QR Code detected.")

                    elif payload_type == "Location":
                       st.success("Location QR Code detected.")

                    elif payload_type == "UPI Payment":
                       st.success("UPI Payment QR Code detected.")

                    else:
                       st.success("Plain Text QR Code detected.")




# -----------------------------
# Scan History
# -----------------------------

st.markdown("---")
st.subheader("Scan History")

history = get_scan_history()

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

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No scan history available.")
# -----------------------------

# Footer

# -----------------------------

st.markdown("---")

st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "QR Shield • AI Powered QR Code Security Scanner"
    "</p>",
    unsafe_allow_html=True
)

