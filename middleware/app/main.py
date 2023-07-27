from flask import Flask, request, jsonify
import ldap
import os

app = Flask(__name__)

LDAP_SERVER = os.environ.get('LDAP_SERVER')
BASE_DN = os.environ.get('BASE_DN')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = ldap.initialize(LDAP_SERVER)
    try:
        conn.simple_bind_s(f'uid={username},{BASE_DN}', password)
        return jsonify(success=True), 200
    except ldap.INVALID_CREDENTIALS:
        return jsonify(success=False, error='Invalid credentials'), 401
    finally:
        conn.unbind_s()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
