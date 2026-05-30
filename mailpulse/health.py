#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MailPulse-Server Health Check Module
Provides health checking for SMTP, IMAP, and POP3 servers
"""

import socket
import ssl
import time
from typing import Dict, Any, Optional
import re


def _connect_server(
    server: str,
    port: int,
    timeout: int,
    use_ssl: bool = False,
    starttls: bool = False
) -> Dict[str, Any]:
    """
    Generic server connection test.
    
    Args:
        server: Server hostname or IP
        port: Server port
        timeout: Connection timeout in seconds
        use_ssl: Whether to use SSL/TLS
        starttls: Whether to use STARTTLS (for SMTP)
    
    Returns:
        Dict with connection results
    """
    result = {
        "status": "unhealthy",
        "response_time": None,
        "banner": None,
        "tls": False,
        "message": ""
    }
    
    start_time = time.time()
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Wrap with SSL if needed
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=server)
        
        # Connect
        sock.connect((server, port))
        
        # Calculate response time
        result["response_time"] = round((time.time() - start_time) * 1000, 2)
        
        # Receive banner
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            result["banner"] = banner
        except:
            result["banner"] = "No banner received"
        
        # Check for STARTTLS support (SMTP)
        if starttls:
            try:
                sock.send(b"EHLO localhost\r\n")
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                if "STARTTLS" in response:
                    result["tls"] = True
            except:
                pass
        
        result["status"] = "healthy"
        result["message"] = "Connection successful"
        result["tls"] = use_ssl or result["tls"]
        
        sock.close()
        
    except socket.timeout:
        result["message"] = f"Connection timed out after {timeout}s"
        result["response_time"] = timeout * 1000
    except socket.gaierror:
        result["message"] = f"DNS resolution failed for {server}"
    except ConnectionRefusedError:
        result["message"] = f"Connection refused by {server}:{port}"
    except Exception as e:
        result["message"] = f"Connection error: {str(e)}"
    
    return result


def check_smtp_health(
    server: str,
    port: int = 25,
    timeout: int = 10,
    use_tls: bool = False
) -> Dict[str, Any]:
    """
    Check SMTP server health.
    
    Args:
        server: SMTP server hostname or IP
        port: SMTP port (default: 25)
        timeout: Connection timeout in seconds
        use_tls: Whether to use TLS
    
    Returns:
        Dict with health check results
    """
    result = _connect_server(server, port, timeout, use_ssl=use_tls, starttls=(port == 587))
    
    # Additional SMTP-specific checks
    if result["status"] == "healthy" and result.get("banner"):
        banner = result["banner"].lower()
        if "smtp" not in banner and "esmtp" not in banner and "mail" not in banner:
            result["status"] = "warning"
            result["message"] = "Connected but banner doesn't look like SMTP"
    
    return result


def check_imap_health(
    server: str,
    port: int = 143,
    timeout: int = 10,
    use_ssl: bool = False
) -> Dict[str, Any]:
    """
    Check IMAP server health.
    
    Args:
        server: IMAP server hostname or IP
        port: IMAP port (default: 143)
        timeout: Connection timeout in seconds
        use_ssl: Whether to use SSL
    
    Returns:
        Dict with health check results
    """
    result = _connect_server(server, port, timeout, use_ssl=use_ssl)
    
    # Additional IMAP-specific checks
    if result["status"] == "healthy" and result.get("banner"):
        banner = result["banner"].lower()
        if "imap" not in banner and "ok" not in banner:
            result["status"] = "warning"
            result["message"] = "Connected but banner doesn't look like IMAP"
    
    return result


def check_pop3_health(
    server: str,
    port: int = 110,
    timeout: int = 10,
    use_ssl: bool = False
) -> Dict[str, Any]:
    """
    Check POP3 server health.
    
    Args:
        server: POP3 server hostname or IP
        port: POP3 port (default: 110)
        timeout: Connection timeout in seconds
        use_ssl: Whether to use SSL
    
    Returns:
        Dict with health check results
    """
    result = _connect_server(server, port, timeout, use_ssl=use_ssl)
    
    # Additional POP3-specific checks
    if result["status"] == "healthy" and result.get("banner"):
        banner = result["banner"].lower()
        if "pop3" not in banner and "+ok" not in banner:
            result["status"] = "warning"
            result["message"] = "Connected but banner doesn't look like POP3"
    
    return result


def check_all_protocols(
    server: str,
    timeout: int = 10
) -> Dict[str, Dict[str, Any]]:
    """
    Check all common email protocols for a server.
    
    Args:
        server: Server hostname or IP
        timeout: Connection timeout in seconds
    
    Returns:
        Dict with results for each protocol
    """
    return {
        "smtp_25": check_smtp_health(server, 25, timeout),
        "smtp_587": check_smtp_health(server, 587, timeout, use_tls=True),
        "smtp_465": check_smtp_health(server, 465, timeout, use_tls=True),
        "imap_143": check_imap_health(server, 143, timeout),
        "imap_993": check_imap_health(server, 993, timeout, use_ssl=True),
        "pop3_110": check_pop3_health(server, 110, timeout),
        "pop3_995": check_pop3_health(server, 995, timeout, use_ssl=True),
    }
