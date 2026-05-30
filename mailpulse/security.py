#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MailPulse-Server Security Check Module
Provides security configuration checking for SPF, DKIM, and DMARC
"""

import dns.resolver
from typing import Dict, Any, List, Optional
import re


def check_spf(domain: str) -> Dict[str, Any]:
    """
    Check SPF (Sender Policy Framework) record for a domain.
    
    Args:
        domain: Domain to check
    
    Returns:
        Dict with SPF check results
    """
    result = {
        "valid": False,
        "message": "",
        "record": None,
        "mechanisms": [],
        "all_qualifier": None
    }
    
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        
        for rdata in answers:
            txt_record = str(rdata).strip('"')
            if txt_record.startswith('v=spf1'):
                result["record"] = txt_record
                result["mechanisms"] = _parse_spf_mechanisms(txt_record)
                
                # Check for 'all' qualifier
                if ' -all' in txt_record:
                    result["all_qualifier"] = "hardfail"
                    result["valid"] = True
                    result["message"] = "SPF record found with hardfail (-all)"
                elif ' ~all' in txt_record:
                    result["all_qualifier"] = "softfail"
                    result["valid"] = True
                    result["message"] = "SPF record found with softfail (~all)"
                elif ' +all' in txt_record:
                    result["all_qualifier"] = "pass"
                    result["valid"] = False
                    result["message"] = "SPF record allows all senders (+all) - NOT RECOMMENDED"
                elif ' ?all' in txt_record:
                    result["all_qualifier"] = "neutral"
                    result["valid"] = True
                    result["message"] = "SPF record found with neutral (?all)"
                else:
                    result["valid"] = True
                    result["message"] = "SPF record found but no explicit 'all' mechanism"
                
                return result
        
        result["message"] = "No SPF record found"
        
    except dns.resolver.NXDOMAIN:
        result["message"] = f"Domain {domain} does not exist"
    except dns.resolver.NoAnswer:
        result["message"] = "No TXT records found"
    except Exception as e:
        result["message"] = f"Error checking SPF: {str(e)}"
    
    return result


def check_dkim(domain: str, selector: str = "default") -> Dict[str, Any]:
    """
    Check DKIM (DomainKeys Identified Mail) record for a domain.
    
    Args:
        domain: Domain to check
        selector: DKIM selector (default: "default")
    
    Returns:
        Dict with DKIM check results
    """
    result = {
        "valid": False,
        "message": "",
        "record": None,
        "key_type": None,
        "key_size": None
    }
    
    dkim_domain = f"{selector}._domainkey.{domain}"
    
    try:
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        
        for rdata in answers:
            txt_record = str(rdata).strip('"')
            if 'v=DKIM1' in txt_record or 'k=' in txt_record:
                result["record"] = txt_record
                
                # Parse key type
                k_match = re.search(r'k=(\w+)', txt_record)
                if k_match:
                    result["key_type"] = k_match.group(1)
                
                # Parse public key and estimate size
                p_match = re.search(r'p=([A-Za-z0-9+/=]+)', txt_record)
                if p_match:
                    public_key = p_match.group(1)
                    # Estimate key size based on base64 length
                    key_bytes = len(public_key) * 3 // 4
                    if key_bytes < 200:
                        result["key_size"] = "512-bit (WEAK)"
                        result["message"] = "DKIM key is too weak (512-bit)"
                    elif key_bytes < 350:
                        result["key_size"] = "1024-bit"
                        result["message"] = "DKIM record found with 1024-bit key"
                        result["valid"] = True
                    else:
                        result["key_size"] = "2048-bit or higher"
                        result["message"] = "DKIM record found with strong key"
                        result["valid"] = True
                
                return result
        
        result["message"] = f"No DKIM record found for selector '{selector}'"
        
    except dns.resolver.NXDOMAIN:
        result["message"] = f"No DKIM record found for selector '{selector}'"
    except Exception as e:
        result["message"] = f"Error checking DKIM: {str(e)}"
    
    return result


def check_dmarc(domain: str) -> Dict[str, Any]:
    """
    Check DMARC (Domain-based Message Authentication, Reporting, and Conformance) record.
    
    Args:
        domain: Domain to check
    
    Returns:
        Dict with DMARC check results
    """
    result = {
        "valid": False,
        "message": "",
        "record": None,
        "policy": None,
        "subdomain_policy": None,
        "pct": None,
        "rua": None,
        "ruf": None
    }
    
    dmarc_domain = f"_dmarc.{domain}"
    
    try:
        answers = dns.resolver.resolve(dmarc_domain, 'TXT')
        
        for rdata in answers:
            txt_record = str(rdata).strip('"')
            if txt_record.startswith('v=DMARC1'):
                result["record"] = txt_record
                
                # Parse policy
                p_match = re.search(r'p=(\w+)', txt_record)
                if p_match:
                    result["policy"] = p_match.group(1)
                    if result["policy"] == "reject":
                        result["valid"] = True
                        result["message"] = "DMARC policy set to reject (recommended)"
                    elif result["policy"] == "quarantine":
                        result["valid"] = True
                        result["message"] = "DMARC policy set to quarantine"
                    elif result["policy"] == "none":
                        result["valid"] = True
                        result["message"] = "DMARC policy set to none (monitoring only)"
                
                # Parse subdomain policy
                sp_match = re.search(r'sp=(\w+)', txt_record)
                if sp_match:
                    result["subdomain_policy"] = sp_match.group(1)
                
                # Parse percentage
                pct_match = re.search(r'pct=(\d+)', txt_record)
                if pct_match:
                    result["pct"] = int(pct_match.group(1))
                
                # Parse aggregate report URI
                rua_match = re.search(r'rua=mailto:([^\s;]+)', txt_record)
                if rua_match:
                    result["rua"] = rua_match.group(1)
                
                # Parse forensic report URI
                ruf_match = re.search(r'ruf=mailto:([^\s;]+)', txt_record)
                if ruf_match:
                    result["ruf"] = ruf_match.group(1)
                
                return result
        
        result["message"] = "No DMARC record found"
        
    except dns.resolver.NXDOMAIN:
        result["message"] = "No DMARC record found"
    except Exception as e:
        result["message"] = f"Error checking DMARC: {str(e)}"
    
    return result


def _parse_spf_mechanisms(spf_record: str) -> List[str]:
    """
    Parse SPF mechanisms from a record.
    
    Args:
        spf_record: SPF record string
    
    Returns:
        List of mechanisms
    """
    mechanisms = []
    parts = spf_record.split()
    
    for part in parts[1:]:  # Skip v=spf1
        if part.startswith(('ip4:', 'ip6:', 'a:', 'mx:', 'include:', 'exists:', 'all')):
            mechanisms.append(part)
    
    return mechanisms


def check_all_security(domain: str) -> Dict[str, Dict[str, Any]]:
    """
    Check all email security configurations for a domain.
    
    Args:
        domain: Domain to check
    
    Returns:
        Dict with results for each security check
    """
    return {
        "spf": check_spf(domain),
        "dkim": check_dkim(domain),
        "dmarc": check_dmarc(domain)
    }


def get_security_score(domain: str) -> Dict[str, Any]:
    """
    Calculate an overall security score for a domain's email configuration.
    
    Args:
        domain: Domain to check
    
    Returns:
        Dict with security score and details
    """
    spf = check_spf(domain)
    dkim = check_dkim(domain)
    dmarc = check_dmarc(domain)
    
    score = 0
    max_score = 100
    
    # SPF scoring (30 points)
    if spf["valid"]:
        score += 20
        if spf["all_qualifier"] == "hardfail":
            score += 10
    
    # DKIM scoring (30 points)
    if dkim["valid"]:
        score += 20
        if dkim["key_size"] and "2048" in dkim["key_size"]:
            score += 10
        elif dkim["key_size"] and "1024" in dkim["key_size"]:
            score += 5
    
    # DMARC scoring (40 points)
    if dmarc["valid"]:
        score += 20
        if dmarc["policy"] == "reject":
            score += 20
        elif dmarc["policy"] == "quarantine":
            score += 15
        elif dmarc["policy"] == "none":
            score += 5
        
        if dmarc["rua"]:
            score += 5
        if dmarc["ruf"]:
            score += 5
    
    # Cap at max
    score = min(score, max_score)
    
    return {
        "score": score,
        "max_score": max_score,
        "grade": _get_grade(score),
        "spf": spf,
        "dkim": dkim,
        "dmarc": dmarc
    }


def _get_grade(score: int) -> str:
    """Convert score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
