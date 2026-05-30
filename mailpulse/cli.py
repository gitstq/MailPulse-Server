#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MailPulse-Server CLI Entry Point
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .health import check_smtp_health, check_imap_health, check_pop3_health
from .security import check_spf, check_dkim, check_dmarc
from .diagnostics import diagnose_domain, analyze_mx_records
from .version import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="mailpulse-server")
def main():
    """
    🔥 MailPulse-Server - Lightweight Email Server Health Monitoring CLI
    
    A powerful tool for monitoring and diagnosing email server health,
    security configurations, and delivery performance.
    
    \b
    Examples:
        mailpulse health smtp://mail.example.com:587
        mailpulse security example.com --full
        mailpulse diagnose example.com
    """
    pass


@main.command()
@click.argument('server', required=True)
@click.option('--port', default=25, help='SMTP port (default: 25)')
@click.option('--timeout', default=10, help='Connection timeout in seconds')
@click.option('--tls', is_flag=True, help='Use TLS/SSL connection')
def smtp(server, port, timeout, tls):
    """
    🔌 Check SMTP server health status.
    
    \b
    Example:
        mailpulse smtp mail.example.com --port 587 --tls
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Checking SMTP server {server}:{port}...", total=None)
        result = check_smtp_health(server, port, timeout, tls)
    
    _display_health_result("SMTP", server, port, result)


@main.command()
@click.argument('server', required=True)
@click.option('--port', default=143, help='IMAP port (default: 143)')
@click.option('--timeout', default=10, help='Connection timeout in seconds')
@click.option('--ssl', 'use_ssl', is_flag=True, help='Use SSL connection')
def imap(server, port, timeout, use_ssl):
    """
    📥 Check IMAP server health status.
    
    \b
    Example:
        mailpulse imap mail.example.com --port 993 --ssl
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Checking IMAP server {server}:{port}...", total=None)
        result = check_imap_health(server, port, timeout, use_ssl)
    
    _display_health_result("IMAP", server, port, result)


@main.command()
@click.argument('server', required=True)
@click.option('--port', default=110, help='POP3 port (default: 110)')
@click.option('--timeout', default=10, help='Connection timeout in seconds')
@click.option('--ssl', 'use_ssl', is_flag=True, help='Use SSL connection')
def pop3(server, port, timeout, use_ssl):
    """
    📬 Check POP3 server health status.
    
    \b
    Example:
        mailpulse pop3 mail.example.com --port 995 --ssl
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Checking POP3 server {server}:{port}...", total=None)
        result = check_pop3_health(server, port, timeout, use_ssl)
    
    _display_health_result("POP3", server, port, result)


@main.command()
@click.argument('domain', required=True)
@click.option('--full', is_flag=True, help='Run full security audit')
def security(domain, full):
    """
    🛡️ Check email security configurations (SPF, DKIM, DMARC).
    
    \b
    Example:
        mailpulse security example.com --full
    """
    console.print(Panel(f"🔒 Security Audit for [bold]{domain}[/bold]", style="blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Analyzing security records for {domain}...", total=None)
        
        spf_result = check_spf(domain)
        dkim_result = check_dkim(domain) if full else {"status": "skipped", "message": "Use --full to check DKIM"}
        dmarc_result = check_dmarc(domain)
    
    table = Table(title="Security Configuration Results")
    table.add_column("Record Type", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details")
    
    # SPF
    spf_status = "✅ PASS" if spf_result.get("valid") else "❌ FAIL"
    spf_style = "green" if spf_result.get("valid") else "red"
    table.add_row("SPF", f"[{spf_style}]{spf_status}[/{spf_style}]", spf_result.get("message", ""))
    
    # DKIM
    if full:
        dkim_status = "✅ PASS" if dkim_result.get("valid") else "❌ FAIL"
        dkim_style = "green" if dkim_result.get("valid") else "red"
        table.add_row("DKIM", f"[{dkim_style}]{dkim_status}[/{dkim_style}]", dkim_result.get("message", ""))
    else:
        table.add_row("DKIM", "[yellow]⏭️ SKIPPED[/yellow]", "Use --full to check")
    
    # DMARC
    dmarc_status = "✅ PASS" if dmarc_result.get("valid") else "❌ FAIL"
    dmarc_style = "green" if dmarc_result.get("valid") else "red"
    table.add_row("DMARC", f"[{dmarc_style}]{dmarc_status}[/{dmarc_style}]", dmarc_result.get("message", ""))
    
    console.print(table)


@main.command()
@click.argument('domain', required=True)
def diagnose(domain):
    """
    🔍 Run comprehensive email diagnostics for a domain.
    
    \b
    Example:
        mailpulse diagnose example.com
    """
    console.print(Panel(f"🔍 Comprehensive Diagnostics for [bold]{domain}[/bold]", style="blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Running diagnostics for {domain}...", total=None)
        result = diagnose_domain(domain)
    
    # MX Records
    console.print("\n[bold cyan]📧 MX Records:[/bold cyan]")
    if result.get("mx_records"):
        mx_table = Table()
        mx_table.add_column("Priority", style="yellow")
        mx_table.add_column("Server", style="green")
        mx_table.add_column("IP", style="blue")
        for mx in result["mx_records"]:
            mx_table.add_row(str(mx.get("priority", "N/A")), mx.get("server", "N/A"), mx.get("ip", "N/A"))
        console.print(mx_table)
    else:
        console.print("[red]No MX records found[/red]")
    
    # Security Summary
    console.print("\n[bold cyan]🔒 Security Summary:[/bold cyan]")
    sec_table = Table()
    sec_table.add_column("Check", style="yellow")
    sec_table.add_column("Status", style="bold")
    for check, status in result.get("security", {}).items():
        status_str = "✅ PASS" if status else "❌ FAIL"
        style = "green" if status else "red"
        sec_table.add_row(check.upper(), f"[{style}]{status_str}[/{style}]")
    console.print(sec_table)
    
    # Recommendations
    if result.get("recommendations"):
        console.print("\n[bold cyan]💡 Recommendations:[/bold cyan]")
        for rec in result["recommendations"]:
            console.print(f"  • {rec}")


@main.command()
@click.argument('domain', required=True)
def mx(domain):
    """
    📊 Analyze MX records for a domain.
    
    \b
    Example:
        mailpulse mx example.com
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Analyzing MX records for {domain}...", total=None)
        result = analyze_mx_records(domain)
    
    console.print(Panel(f"📊 MX Record Analysis for [bold]{domain}[/bold]", style="blue"))
    
    if result.get("records"):
        table = Table()
        table.add_column("Priority", style="yellow")
        table.add_column("Server", style="green")
        table.add_column("IP Address", style="blue")
        table.add_column("TTL", style="magenta")
        
        for record in result["records"]:
            table.add_row(
                str(record.get("priority", "N/A")),
                record.get("server", "N/A"),
                record.get("ip", "N/A"),
                str(record.get("ttl", "N/A"))
            )
        console.print(table)
        
        console.print(f"\n[bold]Total MX Records:[/bold] {len(result['records'])}")
        if result.get("warnings"):
            console.print("\n[bold yellow]⚠️ Warnings:[/bold yellow]")
            for warning in result["warnings"]:
                console.print(f"  • {warning}")
    else:
        console.print("[red]No MX records found for this domain[/red]")


def _display_health_result(protocol: str, server: str, port: int, result: dict):
    """Display health check result in a formatted table."""
    status = result.get("status", "unknown")
    response_time = result.get("response_time", "N/A")
    
    if status == "healthy":
        status_display = "[green]✅ HEALTHY[/green]"
    elif status == "warning":
        status_display = "[yellow]⚠️ WARNING[/yellow]"
    else:
        status_display = "[red]❌ UNHEALTHY[/red]"
    
    table = Table(title=f"{protocol} Health Check Results")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="bold")
    
    table.add_row("Server", server)
    table.add_row("Port", str(port))
    table.add_row("Status", status_display)
    table.add_row("Response Time", f"{response_time}ms" if isinstance(response_time, (int, float)) else response_time)
    
    if result.get("banner"):
        table.add_row("Banner", result["banner"][:50] + "..." if len(result["banner"]) > 50 else result["banner"])
    
    if result.get("tls"):
        table.add_row("TLS", "[green]✅ Supported[/green]" if result["tls"] else "[red]❌ Not Supported[/red]")
    
    if result.get("message"):
        table.add_row("Message", result["message"])
    
    console.print(table)


if __name__ == "__main__":
    main()
