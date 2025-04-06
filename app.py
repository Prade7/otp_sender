from flask import Flask, request, jsonify
from db import get_connection
from otp_sender import send_otp_with_provider

app = Flask(__name__)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    phone = data.get("phone")
    count = data.get("count", 1)

    if not phone or not isinstance(count, int) or count <= 0:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Insert request entry
    cur.execute("""
        INSERT INTO otp_request (phone_number, otp_count)
        VALUES (%s, %s)
        RETURNING id
    """, (phone, count))
    request_id = cur.fetchone()[0]

    # Get random `count` providers with headers and payload_template as TEXT
    cur.execute("""
        SELECT id, name, url, headers::TEXT, payload_template::TEXT
        FROM provider_config
        ORDER BY RANDOM()
        LIMIT %s
    """, (count,))
    providers = cur.fetchall()

    if len(providers) < count:
        conn.close()
        return jsonify({
            "error": f"Only {len(providers)} providers available, but {count} requested."
        }), 400

    used_providers = []
    for row in providers:
        provider = {
            "id": row[0],
            "name": row[1],
            "url": row[2],
            "headers": row[3],  # TEXT
            "payload_template": row[4]  # TEXT
        }

        result = send_otp_with_provider(phone, provider)

        cur.execute("""
            INSERT INTO otp_log (request_id, provider_id, status_code, response_text, error_message)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            request_id,
            provider["id"],
            result["status_code"],
            result["response_text"],
            result["error_message"]
        ))

        used_providers.append({
            "provider_id": provider["id"],
            "name": provider["name"],
            "status_code": result["status_code"]
        })

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"{count} request(s) sent (or attempted) to {phone}",
        "request_id": request_id,
        "providers_used": used_providers
    })


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
