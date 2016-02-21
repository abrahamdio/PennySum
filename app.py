import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from firebase import firebase
from werkzeug import generate_password_hash, check_password_hash

import requests

app = Flask(__name__)
SECRET_KEY = 'this should be a secret key';
capitalAPIkey = 'b17c7f357d390d8a6a36badc619283a7'
capitalAccountID = ''
capitalAPIURl = 'api.reimaginebanking.com/'
firebase = firebase.FirebaseApplication('https://pennysum.firebaseIO.com', None)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html');

@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    print("inside add_user");
    print(request);
	# return "hello world";
	# print("add user");
	
    user_username = request.form['inputUserName']
    # user_name = request.form['inputName']
    # user_email = request.form['inputEmail']
    user_password = request.form['inputPassword']
    print(user_email)
    print(user_password)
    # user_type= request.form['inputType']
    # user_payment_info = request.form['inputPaymentInfo']
    # user_frequency = request.form['inputFrequency']
    # user_amount = request.form['inputAmount']
    # # validate the received values  
    # if not (user_username and user_name and user_email and user_password and 
    #     user_type and user_payment_info and user_frequency and
    #     user_amount):       
    #     return json.dumps({'status':'ERROR', 'errorMessage':'Enter all fields!'})   
    # else:
    #     post = {"username":user_username, "name": user_name, "password":generate_password_hash(user_password)
    #     , "email":user_email, "type": user_type, "paymentInfo" : user_payment_info,
    #     "frequency" : user_frequency, "amount" : user_amount}
    #     firebase.put('/users', user_email, post)
	# return json.dumps({'status':'OK', 'redirect':url_for('main')})
    return render_template('main.html')
    

@app.route('/checkAuth', methods=['GET', 'POST'])
def check_auth():
    user_name = request.form['inputUsername'] 
    user_password = request.form['inputPassword']   
    if request.method == 'POST':
        print(user_name)
        print(user_password)
        # validate the received values  
        if not (user_name and user_password):
            print("empty fields")      
            return json.dumps({'status':'ERROR', 'errorMessage':'Enter all fields!'})   
        else:
            document = firebase.get('/users', user_name)
            if not document:
                return "Error Username"
                # return json.dumps({'status':'ERROR', 'errorMessage':"Email ID doesn't exist! Try again!"})
            # elif check_password_hash(document["password"], user_password):
            elif user_password == document["password"]:
                session['logged_in'] = True;
                return redirect(url_for('landing'))
                #return json.dumps({'status':'OK', 'redirect':url_for('main')})
            else:
                return "Error Credentials"
                #return json.dumps({'status':'ERROR', 'errorMessage':"Incorrect password! Try again!"})



@app.route('/homepage')
def user_home_page():
    return render_template('user_home_page.html')

@app.route('/trackPayments')
def track_payments():
    if session['logged_in']:

        return render_template('trackPayments.html')            
'''
Login - Check auth 
Signup - Push data to Firebase
Landing - Display monthly amount
Track - All payments, merchants
Organization

'''
def get_firebase_entries():
    firebase.get('/donationHistory')

def make_firebase_entries():
    user_payments = get_user_payments()
    listUpdated = []
    for eachPurchase in user_payments:
        merchant_for_payment = get_merchant_by_id(eachPurchase["merchant_id"])
        amount = eachPurchase["amount"]
        date = eachPurchase["purchase_date"]
        if(math.ceil(amount)-amount) > 0.4:
            extra_amount = math.ceil(amount)-amount;
            customJSON = {"original": amount, "extra":extra_amount,
            "date":date, "merchant":merchant_for_payment}
            firebase.put('/donationHistory/'+date, ctr, customJSON)                

def get_monthly_amount():
    document = firebase.get('/users', user_username)
    return document["user_amount"]

def get_user_payments():
    user_payment_history_url = 'accounts/{}/purchases?key={}'.format(
        capitalAccountID, capitalAPIKey)
    document = requests.get(user_payment_history_url)
    #document = firebase.get('/purchases', 1)
    listDoc = []
    merchantIDList = []
    for eachPurchase in document:
        date = time.strptime(eachPurchase["purchase_date"], "%Y-%m-%d");
        if(date == present):
            listDoc.append(eachPurchase)            
    return json.dumps([obj for obj in listDoc])

def get_merchant_by_id(merchantId):
    merchant_details_url = 'merchants/{}?key={}'.format(
        merchantOd, capitalAPIKey)
    #document = firebase.get('/merchants', id)
    document = requests.get(merchant_details_url)
    if document["category"] == "Restaurant":
        return document["name"]
    return None 

def transfer_payment(senderID, receiverID, amount):
    dataPost = {
  "medium": "balance",
  "payee_id": reeiverID,
  "amount": amount,
  "transaction_date": time.strftime("%Y-%m-%d"),
  "status": "pending",
  "description": "Transfer to organization"
    }
    senderDetails = firebase.get('/accounts', senderId)
    receiverDetails = firebase.get('/accounts', receiverID)
    user_transfer_url = capitalAPIURL+"accounts/{}/transfers?key={}".format(senderID, capitalAPIKey)
    response = requests.post(user_transfer_url, body = dataPos)
# user_detail_url = capitalAPIURl+'/accounts/{}?key={}'.format(capitalAccountID, capitalAPIkey)
# response = requests.get(user_detail_url)

if __name__ == '__main__':
    app.secret_key=os.urandom(12)
    app.run()