import requests
import json

def send_otp_with_provider(phone, provider_row):
    try:
        # Convert headers from JSON text to dict
        headers = json.loads(provider_row["headers"])

        # Replace placeholder in payload_template and convert to dict
        payload_template_str = provider_row["payload_template"].replace("{mobile_number}", phone)
        payload = json.loads(payload_template_str)

        print("Headers:", headers)
        print("Payload:", payload)

        # Send POST request
        response = requests.post(provider_row["url"], headers=headers, json=payload)

        return {
            "status_code": response.status_code,
            "response_text": response.text,
            "error_message": None
        }

    except Exception as e:
        print("Error:", e)
        return {
            "status_code": None,
            "response_text": None,
            "error_message": str(e)
        }
