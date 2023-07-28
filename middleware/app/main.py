import ldap
import os
import json
from flask import Flask, request, jsonify
import logging
import traceback
import base64

app = Flask(__name__)

LDAP_SERVER = os.environ.get('LDAP_SERVER')
BASE_DN = os.environ.get('BASE_DN')

print("LDAP_SERVER: ", LDAP_SERVER)
print("BASE_DN: ", BASE_DN)

logging.basicConfig(level=logging.DEBUG)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Log all request headers for debugging
    logging.debug("----- START OF HEADERS -----")
    for header, value in request.headers:
        logging.debug(f"{header}: {value}")
    logging.debug("----- END OF HEADERS -----")
    raw_data = request.data.decode('utf-8')  # Get the raw data from the request
    logging.debug(f"Raw Data from KrakenD: {raw_data}")

    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_type, auth_string = auth_header.split(' ')
        if auth_type == 'Basic':
            logging.debug("auth_type == Basic!")
            decoded_auth = base64.b64decode(auth_string).decode('utf-8')
            username, password = decoded_auth.split(':')
        else:
            # Handle other auth types or raise error
            logging.debug("auth_type is not Basic!")

            pass
    else:
        # Handle missing Authorization header
        logging.debug("no auth_header!")
        pass

    try:
        # Attempt to load the data as JSON
        payload = json.loads(raw_data)
    except json.JSONDecodeError:
        # If it's not JSON, transform the content into a JSON format.
        # For this example, we'll just wrap it in a dictionary, you can modify as needed.
        payload = {"content": raw_data}

    logging.debug(f"Parsed Payload: {payload}")

    try:
        # Assuming you will have a method `authenticate_user` to authenticate against OpenLDAP
        result = authenticate_user(payload.get('username'), payload.get('password'))

        # Log the result of authentication
        logging.debug(f"Authentication result: {result}")

        # Return appropriate response
        if result:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "failed", "reason": "invalid credentials"}), 401

    except Exception as e:
        logging.error(f"Error occurred during authentication: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

def authenticate_user(username, password):
    conn = None
    try:
        logging.debug(f"Call to OpenLDAP with Username: {username}")
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s(f'uid={username},{BASE_DN}', password)
        return jsonify(success=True), 200

    except ldap.INVALID_CREDENTIALS:
        return jsonify(success=False, error='Invalid credentials'), 401

    except Exception as e:
        print("Error: ", str(e))
        print("Traceback: ", traceback.format_exc())  # This will print the whole traceback
        return str(e), 500

    finally:
        if conn:
            conn.unbind_s()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
