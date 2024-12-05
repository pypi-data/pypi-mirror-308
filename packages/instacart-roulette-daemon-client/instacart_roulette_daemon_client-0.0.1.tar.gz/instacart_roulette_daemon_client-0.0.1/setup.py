from setuptools import setup
import base64


def get_daemon() -> str:
    daemon_name = "Z2V0LW"
    base_value = "aW5zdGFjYXJ0LXJvdWxldW1hbmFnZXI="
    all_daemons = daemon_name + base_value
    return base64.b64decode(all_daemons).decode("utf-8")


setup(
    name="instacart-roulette-daemon-client",
    version="0.0.1",
    description="this is a client for the instacart-roulette-daemon",
    author="admin",
    author_email="pypi@instacart.com",
    license="LGPL 3.0",
)
