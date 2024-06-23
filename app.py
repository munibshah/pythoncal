from flask import Flask, request, jsonify
import datetime
import time
from threading import Thread

app = Flask(__name__)

def wait_and_print(target_time):
    """ Waits until the target time and prints it. """
    now = datetime.datetime.utcnow()
    wait_seconds = (target_time - now).total_seconds()
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    print(f"Time reached: {target_time.isoformat()}Z")

@app.route('/webhook', methods=['POST'])
def webhook():
    """ Receives a webhook and processes the time. """
    data = request.get_json()
    start_time_str = data.get('startTime', '')
    
    if not start_time_str:
        return jsonify({'error': 'startTime not provided'}), 400
    
    # Parse the start time and subtract 5 minutes
    start_time = datetime.datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
    target_time = start_time - datetime.timedelta(minutes=5)
    
    # Start a thread to wait until the target time
    Thread(target=wait_and_print, args=(target_time,)).start()

    return jsonify({'message': 'Webhook received and processing started'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)
