import sys
import json
import re

def analyze_url(url):
    score = 0
    reasons = []

    # 1. Check for IP address in URL
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'
        r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'
    )
    if ip_pattern.search(url):
        score += 3
        reasons.append("URL contains an IP address.")

    # 2. Check URL length
    if len(url) > 75:
        score += 2
        reasons.append("URL is unusually long.")
    elif len(url) > 54:
        score += 1
        reasons.append("URL is somewhat long.")

    # 3. Check for @ symbol
    if "@" in url:
        score += 3
        reasons.append("URL contains an '@' symbol, often used to hide the real domain.")

    # 4. Check for double slash (//) outside of protocol
    if url.find("//", 7) > -1:
        score += 2
        reasons.append("URL contains a double slash after the protocol, which can be suspicious.")

    # 5. Check for common suspicious keywords in domain or path
    suspicious_keywords = ["login", "verify", "update", "secure", "account", "bank", "free", "admin", "billing"]
    url_lower = url.lower()
    found_keywords = [kw for kw in suspicious_keywords if kw in url_lower]
    if found_keywords:
        score += len(found_keywords)
        reasons.append(f"URL contains suspicious keywords: {', '.join(found_keywords)}.")

    # 6. Check for hyphen in domain
    try:
        # Very basic domain extraction
        domain = url.split("://")[-1].split("/")[0]
        if "-" in domain:
            score += 1
            reasons.append("Domain contains a hyphen, common in phishing domains.")
        
        # 7. Check for excessive subdomains
        if domain.count(".") > 3:
            score += 2
            reasons.append("Domain has an excessive number of subdomains.")
    except Exception:
        pass

    # Determine classification based on score
    classification = "Safe"
    if score >= 5:
        classification = "Phishing"
    elif score >= 2:
        classification = "Suspicious"

    return {
        "url": url,
        "score": score,
        "classification": classification,
        "reasons": reasons
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No URL provided"}))
        sys.exit(1)

    input_url = sys.argv[1]
    result = analyze_url(input_url)
    print(json.dumps(result))
