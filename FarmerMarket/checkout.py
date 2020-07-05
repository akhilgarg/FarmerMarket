import json
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app,  resources={r"/*": {"origins": "*"}})
api = Api(app)


discount_dict = {"AP1": "APPL", "CH1": "CHMK", "OM1": "APOM", "CF1": "BOGO"}
item_price = {}
with open("item_price.json") as f:
    item_price = json.load(f)
    f.close()


def get_bill_data(result):
    """
    :param result:
    :return: dict having item_details and total alon with promo
    example:  {"item_details": [{"item":"milk", "promo": "APPL", "price": 234}], "total": 500}
    """
    bill_data = {"item_details": [], "total": 0}

    for item_code, item_qty in result.items():
        if discount_dict.get(item_code):
            promo = discount_dict[item_code]
            if promo == 'APPL':
                for i in range(item_qty):
                    bill_data["item_details"].append({"item": "AP1", "price": 6.00})
                    if item_qty >= 3:
                        bill_data["item_details"].append({"promo": "APPL", "price": -1.50})

            elif promo == 'CHMK':
                bill_data["item_details"].append({"item": "CH1", "price": 3.11})
                # if milk already selected by buyer then don't give extra. However give it free but only one.
                if not result.get("MK1"):
                    bill_data["item_details"].append({"item": "MK1", "price": 4.75})
                bill_data["item_details"].append({"promo": "CHMK", "price": -4.75})
                # as limit is 1 so no promo for more than one qty
                for i in range(item_qty-1):
                    bill_data["item_details"].append({"item": "CH1", "price": 3.11})
            elif promo == 'APOM':
                for i in range(item_qty):
                    bill_data["item_details"].append({"item": "OM1", "price": 3.69})
                    # for less than 3 apples bag this offers appplicable for 50% discount otherwise price discount of 1.50 already applied.
                    if result.get("AP1") and result["AP1"] < 3 and (i+1) <= result["AP1"]:
                        bill_data["item_details"].append({"promo": "APOM", "price": -3.00})
            elif promo == "BOGO":
                for i in range(item_qty):
                    bill_data["item_details"].append({"item": "CF1", "price": 11.23})
                for i in range(item_qty//2):
                    bill_data["item_details"].append({"promo": "BOGO", "price": -11.23})
        else:
            for i in range(item_qty):
                bill_data["item_details"].append({"item": item_code, "price": item_price[item_code]["price"]})


    # calculate the total prices
    for bd in  bill_data["item_details"]:
        print(bd)
        bill_data["total"] = bill_data["total"] + bd["price"]
    print(f"total: {bill_data['total']}")
    return bill_data


@app.route('/', methods = ['POST', 'GET'])
def checkout():
    if request.method == 'GET':
        # return render_template("checkout_form.html")
        result = {}
        bill_data = {}
    if request.method == 'POST':
        result = request.form
        result_dict = {k:int(v) for k, v in result.items() if int(v)>0}
        bill_data = get_bill_data(result_dict)

    # fetch item price data
    item_price = {}
    with open("item_price.json") as f:
        item_price = json.load(f)
        f.close()
    return render_template("checkout_form.html", item_price=item_price, result=result, bill_data=bill_data)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')