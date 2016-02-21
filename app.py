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

def check_auth():
    if('logged_in' in session):
        if(session['logged_in'] == False):
            return False;
        else:
            return True;

    return False;

@app.route('/')
def home_page():
    session['logged_in'] = False
    return render_template('index.html')

@app.route('/landing')
def landing():
    if('logged_in' in session):
        if(session['logged_in'] == False):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('main'))

    return redirect(url_for('login'))

@app.route('/login')
def login():
    session['logged_in'] = False
    return render_template('login.html');

@app.route('/register')
def register():
    return render_template('register.html');

@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    if (request.method == "POST"):
        user_username = request.form['inputUserName']
        user_name = request.form['inputFullName']
        user_email = request.form['inputEmail']
        user_password = request.form['inputPassword']
        user_type= request.form['inputType']
        user_accountNumber = request.form['inputAccountNumber']
    if(user_type == "organization"):
        user_frequency = "N/A";
        user_amount = "-1";
    else:
        user_frequency = request.form['inputFrequency']
        user_amount = request.form['inputAmount']
    
    # validate the received values  
    if not (user_username and user_name and user_email and user_password and 
        user_type):
        # check username uniqueness
        return render_template('register.html')  
    else:
        post = {"username":user_username, "name": user_name, "password":generate_password_hash(user_password)
        , "email":user_email, "type": user_type, "accountNumber" : user_accountNumber,
        "frequency" : user_frequency, "amount" : user_amount}
        firebase.put('/users', user_username, post)
        session['logged_in'] = True;
        session['username'] = user_username;
        return redirect(url_for('landing'))
	# return json.dumps({'status':'OK', 'redirect':url_for('main')})
    return "end of func";
    

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
                session['username'] = user_name;
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
    if('logged_in' in session):
        if(session['logged_in'] == False):
            return redirect(url_for('login'))
        else:
            return render_template('trackPayments.html')
    return redirect(url_for('login'))
'''
Login - Check auth 
Signup - Push data to Firebase
Landing - Display monthly amount
Track - All payments, merchants
Organization

'''
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
    app.run(debug=True)