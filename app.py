from flask import Flask
from firebase import firebase
from werkzeug import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
capitalAPIkey = ''
capitalUserID = ''
capitalAPIURl = 'api.reimaginebanking.com/'
#firebase = firebase.FirebaseApplication('https://pennysum.firebaseIO.com', None)
#post = {"name": "Akash", "password":generate_password_hash("Hey")}
#print(firebase.put('/users', "Akash", post))
#autentication = firebase.Authentication('PASSWORD', 'akash22jain@gmail.com')
#firebase.authentication = authentication
@app.route('/')
def home_page():        
    return 'Hello world!'
'''
'''
@app.route('/login')
    #return render_template('login.html')

@app.route('/addUser', method=['POST'])
def add_user():
    user_name = request.form['inputName']
    user_email = request.form['inputEmail']
    user_password = request.form['inputPassword']
    user_type= request.form['inputType']
    user_payment_info = request.form['inputPaymentInfo']
    user_frequency = request.form['inputFrequency']
    user_amount = request.form['inputAmount']
    # validate the received values  
    if not (user_name and user_email and user_password and 
        user_type and user_payment_info and user_frequency and
        user_amount):       
        return json.dumps({'status':'ERROR', 'errorMessage':'Enter all fields!'})   
    else:
        post = {"name": user_name, "password":generate_password_hash(user_password)
        , "email":user_email, "type" = user_type, "paymentInfo" = user_payment_info,
        "frequency" = user_frequency, "amount" = user_amount}
        firebase.put('/users', user_email, post)
        return json.dumps({'status':'OK', 'redirect':url_for('schedule')})


@app.route('/checkAuth', method=['POST'])
def check_auth():
    
    user_email = request.form['inputEmail'] 
    user_password = request.form['inputPassword']   
    # validate the received values  
    if not (user_email and user_password):      
        return json.dumps({'status':'ERROR', 'errorMessage':'Enter all fields!'})   
    else:
    document = firebase.get('/users', user_email)
        if not document:
            return json.dumps({'status':'ERROR', 'errorMessage':"Email ID doesn't exist! Try again!"})
        elif check_password_hash(document["password"], user_password):
            return json.dumps({'status':'OK', 'redirect':url_for('schedule')})
        else:
            return json.dumps({'status':'ERROR', 'errorMessage':"Incorrect password! Try again!"})

@app.route('/homepage')
def user_home_page():
    return render_template('user_home_page.html')

@app.route('/trackPayments')
def track_payments():
    return render_template('track_payments.html')
'''
Login - Check auth 
Signup - Push data to Firebase
Landing - Display monthly amount
Track - All payments, merchants
Organization

'''
def get_monthly_amount():
    document = firebase.get('/users', user_email)
    return document["user_amount"]

def get_user_payments():
    document = firebase.get('/purchases', 1)
    listDoc = []
    merchantIDList = []
    for eachPurchase in document:
        date = time.strptime(eachPurchase["purchase_date"], "%Y-%m-%d");
        if(date == present)
            listDoc.append(eachPurchase)            
    return json.dumps([obj for obj in listDoc])

def get_merchant_by_id(id):
    document = firebase.get('/merchants', id)
    return document["name"]

def transfer_payment(senderId, receiverID, amount):
    senderDetails = firebase.get('/accounts', senderId)
    receiverDetails = firebase.get('/accounts', receiverID)
    

# user_detail_url = capitalAPIURl+'/accounts/{}?key={}'.format(capitalUserID, capitalAPIkey)
# response = requests.get(user_detail_url)

if __name__ == '__main__':
    app.run()