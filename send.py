import requests
import json

url = "http://127.0.0.1:5000/webhook"
# url = "https://geekydevelopers.pythonanywhere.com/webhook"
# data = { 'name': 'Vaibhav Ji2', 
#          'Just Testing': 'Hello World' }
data = {'event_id': '630927a2-17a6-5872-a4cf-6dd7a516e943', 'event_type': 'orders.notification', 'event_time': 1677938990000, 'resource_href': 'https://api.uber.com/v2/eats/order/e67189cc-c759-4f21-8bf2-423a3f29415f', 'meta': {'user_id': '3012e635-19f2-4f52-8c01-819db9c08762', 'resource_id': 'e67189cc-c759-4f21-8bf2-423a3f29415f', 'status': 'pos'}, 'webhook_meta': {'client_id': 'oyT5zxkN_4a1_c8KhSyvB34SzeelmhPx', 'webhook_config_id': 'eats-restaurant-order-experience.order-webhooks', 'webhook_msg_timestamp': 1677938990, 'webhook_msg_uuid': 'ce307a0d-ffa7-5341-a7d0-d7836226639f'}}
r = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})