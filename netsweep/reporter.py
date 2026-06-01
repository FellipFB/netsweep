import csv
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path


def gen_html_report(hosts_data: List[Dict], output_path: str = "netsweep_report.html"):
    """Gera relatório HTML bonito com Bootstrap inline."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    host_rows = ""
    port_sections = ""

    for host in hosts_data:
        ip = host.get("ip", "?")
        mac = host.get("mac", "?")
        hostname = host.get("hostname", "-") or "-"
        vendor = host.get("vendor", "?")
        ports = host.get("ports", [])

        status_color = "#28a745"

        host_rows += f"""
        <tr>
            <td>{ip}</td>
            <td>{hostname}</td>
            <td>{mac}</td>
            <td>{vendor}</td>
            <td><span style="color:{status_color};">● Online</span></td>
        </tr>"""

        if ports:
            port_rows = ""
            for p in ports:
                port_rows += f"""
                <tr>
                    <td>{p['port']}</td>
                    <td>{p['state']}</td>
                    <td>{p['service']}</td>
                </tr>"""

            port_sections += f"""
            <div class="card mt-3">
                <div class="card-header"><strong>{ip}</strong> - Portas Abertas ({len(ports)})</div>
                <div class="card-body p-0">
                    <table class="table table-sm mb-0">
                        <thead class="thead-light">
                            <tr><th>Porta</th><th>Estado</th><th>Serviço</th></tr>
                        </thead>
                        <tbody>
                            {port_rows}
                        </tbody>
                    </table>
                </div>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetSweep Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background: #f5f5f5; }}
        .container {{ margin-top: 30px; }}
        .badge-online {{ background: #28a745; color: #fff; }}
    </style>
</head>
<body>
<div class="container">
    <h1 class="mb-2">NetSweep Report</h1>
    <p class="text-muted">Gerado em {now} | {len(hosts_data)} dispositivo(s) encontrado(s)</p>

    <div class="card">
        <div class="card-header"><strong>Dispositivos na Rede</strong></div>
        <div class="card-body p-0">
            <table class="table table-striped mb-0">
                <thead class="thead-dark">
                    <tr><th>IP</th><th>Hostname</th><th>MAC</th><th>Fabricante</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {host_rows}
                </tbody>
            </table>
        </div>
    </div>

    {port_sections}

    <footer class="text-center text-muted mt-4 mb-4">
        <small>NetSweep v0.1.0 - Relatório automático</small>
    </footer>
</div>
</body>
</html>"""

    path = Path(output_path)
    path.write_text(html, encoding="utf-8")
    print(f"[+] Relatório HTML salvo: {path.resolve()}")


def gen_csv_report(hosts_data: List[Dict], output_path: str = "netsweep_report.csv"):
    """Gera relatório CSV simples."""
    path = Path(output_path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Hostname", "MAC", "Fabricante", "Portas Abertas"])
        for host in hosts_data:
            ports_str = "; ".join([f"{p['port']}/{p['service']}" for p in host.get("ports", [])])
            writer.writerow([
                host.get("ip", ""),
                host.get("hostname", ""),
                host.get("mac", ""),
                host.get("vendor", ""),
                ports_str,
            ])
    print(f"[+] Relatório CSV salvo: {path.resolve()}")
