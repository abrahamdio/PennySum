import os, json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from methods import *
from firebase import firebase
from werkzeug import generate_password_hash, check_password_hash
import time
import requests

app = Flask(__name__)
SECRET_KEY = 'this should be a secret key';
capitalAPIkey = 'b17c7f357d390d8a6a36badc619283a7'
capitalAPIURl = 'http://api.reimaginebanking.com/'
capitalOrgID = '56c66be6a73e492741507c48'
#autentication = firebase.Authentication('PASSWORD', 'akash22jain@gmail.com')
#firebase.authentication = authentication
firebase = firebase.FirebaseApplication('https://pennysum.firebaseIO.com', None)

@app.route('/')
def home_page():
    session['logged_in'] = False
    return render_template('index.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/demo')
def demo():
    if('logged_in' in session):
        if(session['logged_in'] == False):
            return redirect(url_for('login'))
        else:
            accountID = firebase.get('users/' + session['username'], "accountNumber");
            return render_template('demo.html', accountID=accountID, orgBalance=get_balance(capitalOrgID), currBalance=get_balance(accountID))
    return redirect(url_for('login'))

def get_balance(accID):
    user_balance_url = '{}accounts/{}?key={}'.format(capitalAPIURl, accID, capitalAPIkey)
    print(user_balance_url)
    document_get = requests.get(user_balance_url)
    if(document_get):
        document = json.loads(document_get.text)
        return document['balance'];
    return -1;

@app.route('/landing')
def landing():
    if('logged_in' in session):
        if(session['logged_in'] == False):
            return redirect(url_for('login'))
        else:
            freq = firebase.get('users/'+session['username'],'frequency')
            amount = firebase.get('users/'+session['username'],'amount')
            return render_template('landing.html', name=session['username'], freq=freq, amount=amount)

    return redirect(url_for('login'))

@app.route('/login')
def login():
    if('logged_in' in session):
        if(session['logged_in'] == False):
            return render_template('login.html');
        else:
            return redirect(url_for('landing'));
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
        post = {'username':user_username, 'name': user_name, 'password':generate_password_hash(user_password)
        , 'email':user_email, 'type': user_type, 'accountNumber' : user_accountNumber,
        'frequency' : user_frequency, 'amount' : user_amount}
        firebase.put('/users', user_username, post)
        session['logged_in'] = True;
        session['username'] = user_username;
        session['cust_id'] = user_accountNumber;
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
            elif check_password_hash(document["password"], user_password):
                session['logged_in'] = True;
                session['username'] = user_name;
                session['cust_id'] = '56c66be6a73e492741507c4b'
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
            present = time.strftime('%Y-%m-%d');
            current_username = session['username']
            current_id = session['cust_id']
            total = firebase.get('users/' + current_username + '/donationHistory/' + present, "Total")
            # donationHistory = get_user_payments(current_id);
            donationHistory = get_firebase_entries(current_username);
            # users = firebase.get('/users', None, params={'print': 'pretty'});
            # users = json.dumps(users)
            return render_template('trackPayments.html', donationHistory=donationHistory, total=total)
    return redirect(url_for('login'))

@app.route('/firebase')
def firebaseTest():
    users = firebase.get('/users', None, params={'print': 'pretty'});
    print users;
    return json.dumps(users);

@app.route('/makePurchase', methods=['POST'])
def makePurchase():
    amount = request.form["inputAmount"];
    merchantID = request.form["inputMerchant"];
    accountID = request.form["inputAccount"];
    make_purchase(session['username'], amount, merchantID, accountID)
    return "purchase";

@app.route('/makeTransfer', methods=['POST'])
def makeTransfer_1():
    present = time.strftime('%Y-%m-%d');
    amount = firebase.get('/users/' + session['username'] + '/donationHistory/' + present, 'Total')
    orgID = request.form["inputOrg"];
    accountID = request.form["inputAccount"];
    if(make_transfer(session['username'], accountID, orgID, amount)):
        return "transfer " + str(amount)
    else:
        return "failed to transfer"
# @app.route('/get_user_payments', methods=['GET'])
# def get_user_payments(currentID):
#     user_payment_history_url = '{}accounts/{}/purchases?key={}'.format(capitalAPIURl,
#         currentID, capitalAPIkey)
#     print(user_payment_history_url)
#     document_get = requests.get(user_payment_history_url)
#     document = json.loads(document_get.text)
#     # print (document)
#     # document = firebase.get('/purchases', 1)
#     listDoc = []
#     # merchantIDList = []
#     present = current
#     for eachPurchase in document:
#         print(eachPurchase);
#         date = time.strptime(eachPurchase['purchase_date'], '%Y-%m-%d');
#         if(date == present):
#         listDoc.append(eachPurchase)
#     return json.loads(document_get.text)          
#     # return json.dumps([obj for obj in listDoc])


'''
Login - Check auth 
Signup - Push data to Firebase
Landing - Display monthly amount
Track - All payments, merchants
Organization

'''
def get_firebase_entries(user_username):
    entry = firebase.get('/users/'+user_username+'/donationHistory', None);
    return entry

if __name__ == '__main__':
    app.secret_key=os.urandom(12)
    app.run(debug=True)