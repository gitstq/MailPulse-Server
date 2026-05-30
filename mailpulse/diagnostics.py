#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MailPulse-Server Diagnostics Module
Provides comprehensive email diagnostics for domains
"""

import dns.resolver
import socket
from typing import Dict, Any, List, Optional
from .security import check_spf, check_dkim, check_dmarc
from .health import check_smtp_health


def analyze_mx_records(domain: str) -> Dict[str, Any]:
    """
    Analyze MX records for a domain.
    
    Args:
        domain: Domain to analyze
    
    Returns:
        Dict with MX record analysis
    """
    result = {
        "records": [],
        "warnings": [],
        "count": 0
    }
    
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        
        for rdata in answers:
            mx_server = str(rdata.exchange).rstrip('.')
            priority = rdata.preference
            
            # Resolve IP address
            ip_address = None
            try:
                ip_address = socket.gethostbyname(mx_server)
            except:
                ip_address = "Unable to resolve"
            
            result["records"].append({
                "priority": priority,
                "server": mx_server,
                "ip": ip_address,
                "ttl": answers.rrset.ttl
            })
        
        # Sort by priority
        result["records"].sort(key=lambda x: x["priority"])
        result["count"] = len(result["records"])
        
        # Generate warnings
        if result["count"] == 0:
            result["warnings"].append("No MX records found - domain cannot receive email")
        elif result["count"] == 1:
            result["warnings"].append("Only one MX record - no redundancy")
        
        # Check for backup MX
        priorities = [r["priority"] for r in result["records"]]
        if len(set(priorities)) == 1 and len(priorities) > 1:
            result["warnings"].append("All MX records have same priority - consider using different priorities for load balancing")
        
    except dns.resolver.NXDOMAIN:
        result["warnings"].append(f"Domain {domain} does not exist")
    except dns.resolver.NoAnswer:
        result["warnings"].append("No MX records found")
    except Exception as e:
        result["warnings"].append(f"Error analyzing MX records: {str(e)}")
    
    return result


def diagnose_domain(domain: str) -> Dict[str, Any]:
    """
    Run comprehensive diagnostics for a domain.
    
    Args:
        domain: Domain to diagnose
    
    Returns:
        Dict with comprehensive diagnostic results
    """
    result = {
        "domain": domain,
        "mx_records": [],
        "security": {},
        "connectivity": {},
        "recommendations": []
    }
    
    # Analyze MX records
    mx_analysis = analyze_mx_records(domain)
    result["mx_records"] = mx_analysis["records"]
    
    # Security checks
    spf_result = check_spf(domain)
    dkim_result = check_dkim(domain)
    dmarc_result = check_dmarc(domain)
    
    result["security"] = {
        "spf": spf_result["valid"],
        "dkim": dkim_result["valid"],
        "dmarc": dmarc_result["valid"]
    }
    
    # Check connectivity to mail servers
    if result["mx_records"]:
        primary_mx = result["mx_records"][0]["server"]
        result["connectivity"] = {
            "smtp_25": check_smtp_health(primary_mx, 25, 5),
            "smtp_587": check_smtp_health(primary_mx, 587, 5),
            "smtp_465": check_smtp_health(primary_mx, 465, 5, use_tls=True)
        }
    
    # Generate recommendations
    if not spf_result["valid"]:
        result["recommendations"].append("Add an SPF record to prevent email spoofing")
    elif spf_result.get("all_qualifier") != "hardfail":
        result["recommendations"].append("Consider using '-all' (hardfail) in your SPF record for stronger protection")
    
    if not dkim_result["valid"]:
        result["recommendations"].append("Configure DKIM signing for outgoing emails")
    
    if not dmarc_result["valid"]:
        result["recommendations"].append("Add a DMARC record to enable email authentication reporting")
    elif dmarc_result.get("policy") != "reject":
        result["recommendations"].append("Consider setting DMARC policy to 'reject' for maximum protection")
    
    if len(result["mx_records"]) < 2:
        result["recommendations"].append("Add backup MX records for redundancy")
    
    # Check for open ports
    if result.get("connectivity"):
        smtp_25 = result["connectivity"].get("smtp_25", {})
        if smtp_25.get("status") != "healthy":
            result["recommendations"].append(f"Primary mail server may not be accepting connections on port 25")
    
    return result


def check_blacklist(domain: str) -> Dict[str, Any]:
    """
    Check if domain or its mail servers are blacklisted.
    
    Args:
        domain: Domain to check
    
    Returns:
        Dict with blacklist check results
    """
    result = {
        "domain": domain,
        "blacklists_checked": [],
        "listed": [],
        "clean": []
    }
    
    # Common DNSBLs (DNS-based Blackhole Lists)
    blacklists = [
        "zen.spamhaus.org",
        "bl.spamcop.net",
        "dnsbl.sorbs.net",
        "b.barracudacentral.org"
    ]
    
    # Get mail server IPs
    mx_analysis = analyze_mx_records(domain)
    ips_to_check = []
    
    for mx in mx_analysis.get("records", []):
        ip = mx.get("ip")
        if ip and ip != "Unable to resolve":
            ips_to_check.append(ip)
    
    for ip in ips_to_check:
        reversed_ip = '.'.join(reversed(ip.split('.')))
        
        for blacklist in blacklists:
            result["blacklists_checked"].append(blacklist)
            query = f"{reversed_ip}.{blacklist}"
            
            try:
                dns.resolver.resolve(query, 'A')
                result["listed"].append({
                    "ip": ip,
                    "blacklist": blacklist
                })
            except dns.resolver.NXDOMAIN:
                result["clean"].append({
                    "ip": ip,
                    "blacklist": blacklist
                })
            except:
                pass
    
    return result


def check_dns_propagation(domain: str) -> Dict[str, Any]:
    """
    Check DNS propagation for email-related records.
    
    Args:
        domain: Domain to check
    
    Returns:
        Dict with DNS propagation status
    """
    result = {
        "domain": domain,
        "records": {}
    }
    
    record_types = ['MX', 'TXT', 'A', 'AAAA']
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            result["records"][record_type] = {
                "status": "found",
                "count": len(answers),
                "values": [str(rdata) for rdata in answers]
            }
        except dns.resolver.NXDOMAIN:
            result["records"][record_type] = {"status": "domain_not_found", "count": 0}
        except dns.resolver.NoAnswer:
            result["records"][record_type] = {"status": "no_records", "count": 0}
        except Exception as e:
            result["records"][record_type] = {"status": "error", "message": str(e)}
    
    return result
