from flask import Flask, request, render_template, jsonify
import requests
import json
import time

app = Flask(__name__)

logs = []
orderids = []
accepted_order_ids = []
cancelled_order_ids = []
event_ids = []

def order_create(order_details_dict):
    print("Creating order in Yelo Admin dashboard")
    url_for_creatingorder_in_yelo = "https://api.yelo.red/open/admin/order/create"
    payload = {
        "api_key": "13c080cdcfa5f5c18f07fecbabdd2dfd",
        "payment_method": 8,
        "job_description": "Deliver on time!",
        "customer_address": "Uber Eats Pickup",
        "customer_username": "Uber eats Pickup",
        "customer_email": "test@email.com",
        "customer_phone": "9898981122",
        "job_date_time": "2023-02-17T19:50Z",
        "job_latitude": 53.344486,
        "job_longitude": -6.249278,
        "products": [
            {
                "product_id": 106151222,
                "unit_price": 1.0,
                "quantity": 1,
                "total_price": 1.0
            }
        ],
        # vendor_id : Customer Id
        "vendor_id": 6179792,
        "is_scheduled": 0,
        "amount": 1.0,
        "delivery_charge": 0,
        "currency_id": 2,
        "store_id": 1478982,
        "self_pickup": 0,
        "checkout_template": [],
        "tip": 0,
        "subtotal_amount": 1.0
    }
    headers = {'Content-Type': 'application/json'}
    # Disable using a proxy server
    proxies = None
    response_from_yelo = requests.post(url_for_creatingorder_in_yelo, headers=headers, data=json.dumps(payload), proxies=proxies)
    logs.append(response_from_yelo.text)
    print(response_from_yelo.text)
    # converting the JSON string to a dictionary
    response_from_yelo_dict = response_from_yelo.json()
    if response_from_yelo_dict['status'] == 200:
        logs.append("Order created successfully in Yelo Admin dashboard")
    else:
        logs.append("Error creating order in Yelo Admin dashboard")
    return response_from_yelo_dict['status']

@app.route('/', methods=['GET'])
def show_logs():
    # return jsonify({'logs': logs})
    # data_logs = jsonify(logs)
    return render_template('index.html', logs=logs,orderids=accepted_order_ids,cancelids=cancelled_order_ids )

# @app.route('/logs', methods=['GET'])
# def get_logs():
#     return jsonify(logs)

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    order_id = request.form['order_id']
    # code to cancel the order
    url_for_canceling = f"https://api.uber.com/v1/eats/orders/{order_id}/cancel"
    payload = json.dumps({
        "reason": "RESTAURANT_TOO_BUSY"
        })
    headers = {
        'Authorization': 'Bearer IA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAGMAAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAYAAAABwAAAAEAAAAEAAAAJpc6ayHdJWQf4hoZm43JJM8AAAAARsFh6kcGdGs2c90S-ChgMeEppVUX8gonUck9NRDTDohUbBm4-JaiU14FB3HYVYcUofNtHZDKTQNzp4JDAAAALx_xIu-Ww_YEqeZ9yQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU',
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url_for_canceling, headers=headers, data=payload)
    print(response.text)
    logs.append(f"Order with id {order_id} Cancelled in Uber eats")
    cancelled_order_ids.append(order_id)
    accepted_order_ids.remove(order_id)
    print(response)
    return jsonify({'status': 'success'})


@app.route('/webhook', methods=['POST'])
def receive_webhook():
    # Cleaning previous logs
    # logs.clear()
    print(request.json)
    # fetching new logs in json format
    data = request.get_json()
    event_id = data['event_id']
    if event_id not in event_ids: # append order id only if it's not already in the logs
        event_ids.append(event_id)
        logs.append("==> New Notification")
        # Appending new notification log details into 
        logs.append(data)


    # Fetching order id & order url from json
    order_id = data['resource_href'].split('/')[-1] # extract order id from resource_href
    if order_id not in orderids: # append order id only if it's not already in the logs
        orderids.append(order_id)
        order_url = data['resource_href']
        print(order_url)
        # Passing token key required for fetching order details
        header_for_orderdetails = {
            "Authorization": "Bearer IA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAGMAAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAYAAAABwAAAAEAAAAEAAAABTSUv4t_LMAnZAkgTLzFx08AAAAR57gBPmSovBdJlbU1zwFF4J73cXar4IvcRpfVO69oleqoFQguHK_hsV_K--Ln50IUDGXnwOXaSoKmAeUDAAAAPErgzqsqrBuLmoleSQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU"
            }
        # Sending http request to get order details
        order_details = requests.get(order_url, headers=header_for_orderdetails)
        print(order_details.text)
        logs.append("==>order Details")
        

        # converting the JSON string to a dictionary
        order_details_dict = order_details.json()
        uber_eats_order_id = order_details_dict['id']
        display_id = order_details_dict['display_id']
        current_state = order_details_dict['current_state']
        logs.append(f"==> Order Description: {current_state}")
        logs.append(order_details.text)
        store_id = order_details_dict['store']['id']
        store_name = order_details_dict['store']['name']
        eater_first_name = order_details_dict['eater']['first_name']
        eater_phone = order_details_dict['eater']['phone']
        eater_phone_code = order_details_dict['eater']['phone_code']
        eater_last_name = order_details_dict['eater']['last_name']
        cart_items = order_details_dict['cart']['items']
        # Adding New Order Products id
        logs.append("order Product Details")
        if cart_items:
            logs.append({"order Items": cart_items})
        else:
            logs.append("No order items found")
        
        
        # fetching Payment Details
        payment_total_amount = order_details_dict['payment']['charges']['total']['amount']
        payment_total_currency = order_details_dict['payment']['charges']['total']['currency_code']
        placed_at = order_details_dict['placed_at']
        estimated_ready_for_pickup_at = order_details_dict['estimated_ready_for_pickup_at']
        delivery_type = order_details_dict['type']
        packaging_should_include = order_details_dict['packaging']['disposable_items']['should_include']
        eaters = order_details_dict['eaters']
        brand = order_details_dict['brand']

        # Creating order in Yelo
        
        logs.append("creating order in yelo Admin dashboard")
        order_creation_response = order_create(order_details_dict)
        #Accepting order on uber eats as well
        print(order_creation_response)
        logs.append("Accepting order in Uber eats dashboard")
        logs.append(f"Uber EATS ORDER ID : {uber_eats_order_id}")
        if(order_creation_response==200):
            logs.append("Accepting order in Uber eats dashboard")
            url_for_accepting_order = f"https://api.uber.com/v1/eats/orders/{uber_eats_order_id}/accept_pos_order"
            payload = json.dumps({
                "reason": "Order has been accepted."
                })
            headers = {
                'Authorization': 'Bearer IA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAGMAAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAYAAAABwAAAAEAAAAEAAAAGAwc0DNkTtzn9Z63gqV4lw8AAAALUdzcAghm_TwDzEcHzseRmt0_-2KH74BIz2suyl-ws14E_ScGqfJwoEHGUlUohRnTgYitFhvufNBSDFqDAAAAMPjXSIk12pHHYvfrCQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU',
                'Content-Type': 'application/json',
                }
            
            response_for_acceptingUbereats = requests.post( url_for_accepting_order, headers=headers, data=payload)
            print(response_for_acceptingUbereats)
            print(response_for_acceptingUbereats.text)
            accepted_order_ids.append(uber_eats_order_id)
            if(response_for_acceptingUbereats==204):
                logs.append("Order Accepted Succesully in Uber eats")
            # show_logs()
    return "Webhook received."

if __name__ == '__main__':
    app.run(debug=True)
