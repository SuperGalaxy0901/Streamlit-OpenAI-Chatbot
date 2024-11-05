import requests
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

def get_remote_ip() -> str:
    """Get remote ip."""
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

def get_country_name(ip_address: str) -> str:
    """Get country name from IP address using ipapi service."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        return data.get("country", "Unknown")
    except Exception as e:
        return "Unknown"

def get_remote_country() -> str:
    """Get remote country"""
    ip_address = get_remote_ip()
    country = get_country_name(ip_address)
    return country