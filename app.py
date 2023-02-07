from flask import Flask, request, jsonify

app = Flask(__name__)

logs = []

@app.route('/', methods=['GET'])
def show_logs():
    return jsonify(logs)

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    data = request.get_json()
    logs.append(data)
    return "Webhook received."

if __name__ == '__main__':
    app.run()
