import socket
import subprocess
import sys
from pathlib import Path


def resolve_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return ""


def get_mac_vendor(mac: str) -> str:
    """Retorna o fabricante com base nos primeiros 3 bytes (OUI) do MAC."""
    oui = mac.upper().replace(":", "")[:6]
    oui_db = {
        "000C29": "VMware",
        "005056": "VMware",
        "001C42": "Parallels",
        "00155D": "Hyper-V",
        "00037F": "Microsoft (Xbox)",
        "080027": "Oracle VirtualBox",
        "001DD8": "Cisco",
        "F8E903": "Intel",
        "C8D719": "Apple",
        "B8A3D0": "Dell",
        "001132": "Samsung",
        "4C3275": "HP",
        "DCA632": "TP-Link",
        "A8F94E": "LG",
    }
    return oui_db.get(oui, "Desconhecido")


def colorize(text: str, color: str) -> str:
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"
