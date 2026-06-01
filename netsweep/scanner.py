import asyncio
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict, Optional

from scapy.all import ARP, Ether, srp
from rich.progress import Progress, SpinnerColumn, TextColumn

from .utils import resolve_hostname, get_mac_vendor

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
                993, 995, 1433, 1521, 2049, 3306, 3389, 5432, 5900, 5901,
                6379, 8080, 8443, 9090, 27017, 27018]


def arp_scan(network: str) -> List[Dict]:
    """Varre a rede usando ARP e retorna lista de dispositivos encontrados."""
    hosts = []
    try:
        net = ipaddress.ip_network(network, strict=False)
        broadcast = "255.255.255.255"
        arp_request = ARP(pdst=str(net))
        ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether_frame / arp_request

        result = srp(packet, timeout=3, verbose=0)[0]

        for sent, received in result:
            mac = received.hwsrc
            ip = received.psrc
            hostname = resolve_hostname(ip)
            vendor = get_mac_vendor(mac)
            hosts.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "vendor": vendor,
            })

        hosts.sort(key=lambda h: [int(o) for o in h["ip"].split(".")])

    except Exception as e:
        print(f"[!] Erro no ARP scan: {e}")

    return hosts


def _scan_port(ip: str, port: int, timeout: float = 1.0) -> Optional[Dict]:
    """Escaneia uma porta específica e retorna informações do serviço."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = socket.getservbyport(port, "tcp") if port <= 65535 else "unknown"
            sock.close()
            return {"port": port, "state": "open", "service": service}
        sock.close()
    except:
        pass
    return None


def port_scan(ip: str, ports: List[int] = None, max_workers: int = 100) -> List[Dict]:
    """Escaneia portas abertas em um IP usando ThreadPoolExecutor."""
    if ports is None:
        ports = COMMON_PORTS

    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_scan_port, ip, port): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)

    open_ports.sort(key=lambda p: p["port"])
    return open_ports
