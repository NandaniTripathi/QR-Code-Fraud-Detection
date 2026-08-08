from dataset.database import get_connection


def save_scan(
    filename,
    payload_type,
    decoded_url,
    risk_score,
    risk_level
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO scans(
            filename,
            payload_type,
            decoded_url,
            risk_score,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            filename,
            payload_type,
            decoded_url,
            risk_score,
            risk_level
        )
    )

    conn.commit()

    conn.close()

def get_scan_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            filename,
            payload_type,
            decoded_url,
            risk_score,
            risk_level,
            scanned_at
        FROM scans
        ORDER BY scanned_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
