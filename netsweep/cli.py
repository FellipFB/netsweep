import argparse
import sys
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from . import __version__
from .scanner import arp_scan, port_scan
from .reporter import gen_html_report, gen_csv_report

console = Console()


def print_banner():
    banner = """
╔══════════════════════════════════════╗
║           NetSweep v%s            ║
║     Scanner de Rede e Serviços       ║
╚══════════════════════════════════════╝
    """ % __version__
    console.print(Panel(banner, style="bold cyan", box=box.HEAVY))


def display_results(hosts_data):
    """Exibe resultados em formato de tabela no terminal."""
    if not hosts_data:
        console.print("[yellow]Nenhum dispositivo encontrado na rede.[/yellow]")
        return

    table = Table(title=f"Dispositivos Encontrados: {len(hosts_data)}", box=box.ROUNDED)
    table.add_column("IP", style="cyan")
    table.add_column("Hostname", style="green")
    table.add_column("MAC", style="yellow")
    table.add_column("Fabricante", style="magenta")
    table.add_column("Portas", justify="right", style="white")

    for host in hosts_data:
        port_count = len(host.get("ports", []))
        port_str = str(port_count) if port_count > 0 else "-"
        table.add_row(
            host["ip"],
            host.get("hostname", "-") or "-",
            host["mac"],
            host.get("vendor", "?"),
            port_str,
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="NetSweep - Scanner de Rede Local e Análise de Serviços",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  netsweep                        # Escaneia a rede 192.168.1.0/24 automaticamente
  netsweep 10.0.0.0/24           # Escaneia rede específica
  netsweep --ports 22,80,443     # Escaneia portas específicas
  netsweep --output html         # Gera relatório em HTML
  netsweep --output csv          # Gera relatório em CSV
        """
    )
    parser.add_argument("network", nargs="?", default="192.168.1.0/24",
                        help="Rede a ser escaneada (ex: 192.168.1.0/24)")
    parser.add_argument("--ports", type=str, default=None,
                        help="Portas a escanear, separadas por vírgula (ex: 22,80,443)")
    parser.add_argument("--output", type=str, default=None,
                        choices=["html", "csv", "both"],
                        help="Formato de saída do relatório")
    parser.add_argument("--no-color", action="store_true",
                        help="Desativa cores no terminal")
    parser.add_argument("-v", "--version", action="version",
                        version=f"NetSweep {__version__}")

    args = parser.parse_args()

    print_banner()

    if args.ports:
        try:
            port_list = [int(p.strip()) for p in args.ports.split(",")]
        except ValueError:
            console.print("[red]Erro: lista de portas inválida. Use números separados por vírgula.[/red]")
            sys.exit(1)
    else:
        port_list = None

    console.print(f"[bold]Escaneando rede:[/bold] {args.network}")
    with console.status("[bold green]Varredura ARP em andamento..."):
        hosts = arp_scan(args.network)

    if not hosts:
        console.print("[red]Nenhum dispositivo encontrado. Verifique a rede informada.[/red]")
        sys.exit(1)

    console.print(f"[green]Encontrados {len(hosts)} dispositivo(s). Iniciando varredura de portas...[/green]\n")

    for i, host in enumerate(hosts, 1):
        ip = host["ip"]
        with console.status(f"[bold blue]({i}/{len(hosts)}) Escaneando {ip}..."):
            open_ports = port_scan(ip, ports=port_list)
            host["ports"] = open_ports
        console.print(f"  {ip}: [green]{len(open_ports)} porta(s) aberta(s)[/green]")

    console.print("\n")
    display_results(hosts)

    if args.output in ("html", "both"):
        gen_html_report(hosts)
    if args.output in ("csv", "both"):
        gen_csv_report(hosts)
    if not args.output:
        console.print("\n[dim]Dica: use --output html ou --output csv para gerar relatório.[/dim]")

    console.print("\n[bold green]Scan concluído![/bold green]")
