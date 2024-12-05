import base64


def get_daemon() -> str:
    daemon_name = "Z2V0LW"
    base_value = "aW5zdGFjYXJ0LXJvdWxldW1hbmFnZXI="
    all_daemons = daemon_name + base_value
    return base64.b64decode(all_daemons).decode("utf-8")
