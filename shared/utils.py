
import requests
from bs4 import BeautifulSoup
import tldextract
import socket
import logging

def calculate_url_features(url):
    # Initialize feature dictionary
    features = {
        "IsDomainIP": 0.0,
        "NoOfAmpersandInURL": 0.0,
        "TLDLegitimateProb": 0.0,
        "TLDLength": 0.0,
        "LargestLineLength": 0.0,
        "Robots": 0.0,
        "NoOfURLRedirect": 0.0,
        "NoOfPopup": 0.0,
        "HasExternalFormSubmit": 0.0,
        "HasHiddenFields": 0.0,
        "HasPasswordField": 0.0,
        "Bank": 0.0,
        "Pay": 0.0,
        "Crypto": 0.0,
        "NoOfiFrame": 0.0,
        "NoOfEmptyRef": 0.0
    }

    try:
        # Extract domain info
        domain_info = tldextract.extract(url)
        
        # Check if domain is an IP address
        try:
            socket.inet_aton(domain_info.domain)
            features["IsDomainIP"] = 1.0
        except socket.error:
            features["IsDomainIP"] = 0.0

        # Count ampersands in URL
        features["NoOfAmpersandInURL"] = url.count('&')

        # Calculate TLD Legitimacy (based on common TLDs as a simple heuristic)
        common_tlds = {'com', 'org', 'net', 'edu', 'gov'}
        features["TLDLegitimateProb"] = 1.0 if domain_info.suffix in common_tlds else 0.5

        # Calculate TLD length
        features["TLDLength"] = len(domain_info.suffix)

        # Request the webpage content
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        html_content = response.text

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Calculate largest line length
        lines = html_content.splitlines()
        features["LargestLineLength"] = max(len(line) for line in lines)

        # Check for robots.txt
        robots_url = f"{domain_info.domain}/robots.txt"
        try:
            robots_response = requests.get(robots_url, timeout=3)
            features["Robots"] = 1.0 if robots_response.status_code == 200 else 0.0
        except requests.RequestException:
            features["Robots"] = 0.0

        # Check for redirects
        features["NoOfURLRedirect"] = len(response.history)

        # Count popups (heuristic by checking for "onclick" with window.open)
        features["NoOfPopup"] = len(soup.find_all(lambda tag: tag.has_attr('onclick') and 'window.open' in tag['onclick']))

        # Check for external form submissions
        forms = soup.find_all('form')
        features["HasExternalFormSubmit"] = 1.0 if any(form.get('action', '').startswith('http') and not form.get('action', '').startswith(url) for form in forms) else 0.0

        # Check for hidden fields
        features["HasHiddenFields"] = 1.0 if soup.find_all(attrs={"type": "hidden"}) else 0.0

        # Check for password fields
        features["HasPasswordField"] = 1.0 if soup.find_all(attrs={"type": "password"}) else 0.0

        # Check for keywords in text content
        text_content = soup.get_text().lower()
        features["Bank"] = 1.0 if "bank" in text_content else 0.0
        features["Pay"] = 1.0 if "pay" in text_content else 0.0
        features["Crypto"] = 1.0 if "crypto" in text_content else 0.0

        # Count iframes
        features["NoOfiFrame"] = len(soup.find_all('iframe'))

        # Count empty references (links with href="#", href="javascript:void(0)", etc.)
        features["NoOfEmptyRef"] = len(soup.find_all(href=lambda href: href in {"#", "javascript:void(0);"}))

    except Exception as e:
        logging.error(f"An error occurred while processing the URL: {e}")
    
    return features