from flask import Flask, request, render_template

app = Flask(__name__)

logs = []

@app.route('/', methods=['GET'])
def show_logs():
    return render_template('index.html', logs=logs)

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    print(request.json)
    data = request.get_json()
    logs.append(data)
    return "Webhook received."

if __name__ == '__main__':
    app.run()
