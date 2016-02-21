import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from firebase import firebase
from werkzeug import generate_password_hash, check_password_hash
import json
import requests
import time, math
capitalMerchantID = '56c66be6a73e492741507624'
capitalAPIkey = 'b17c7f357d390d8a6a36badc619283a7'
capitalAccountID = '56c66be6a73e492741507c4b'
capitalAPIURl = 'http://api.reimaginebanking.com/'
firebase = firebase.FirebaseApplication('https://pennysum.firebaseIO.com', None)
'''
Login - Check auth 
Signup - Push data to Firebase
Landing - Display monthly amount
Track - All payments, merchants
Organization

'''


def main():
    #jsonObj =(get_firebase_entries())
    #print(jsonObj)
    #print(sample_entry())
    # print("test")
    # print(sample_paylist())
    # print(get_user_payments());
    make_firebase_entries('test_from_capital');
    #print(get_monthly_amount())
    # print(make_purchase())

def make_purchase(username, amount, merchID, accID):
    # amount = "8";
    merchantID = capitalMerchantID;
    accountID = capitalAccountID;
    dataPost = {
          "merchant_id":"56c66be6a73e492741507624",
          "medium": "balance",
          "purchase_date": "2016-02-21",
          "amount": float(amount),
          "status": "pending",
          "description": "string"
    }
    user_purchase_url = '{}accounts/{}/purchases?key={}'.format(capitalAPIURl, capitalAccountID, capitalAPIkey)
    resp = requests.post(user_purchase_url, json=dataPost)
    print(type(resp.status_code))
    if resp.status_code < 300:
        make_firebase_entries(username);

def sample_paylist():
    #user_payment_history_url = capitalAPIURl+'accounts/{}/purchases?key={}'.format(
        #capitalAccountID, capitalAPIKey)
    user_payment_history_url = 'http://api.reimaginebanking.com/accounts/56c66be6a73e492741507c4b/purchases?key=b17c7f357d390d8a6a36badc619283a7'
    document = requests.get(user_payment_history_url)
    print(document.text)
    return document

def get_firebase_entries(user_username):    
    return firebase.get('/users/'+user_username+'/donationHistory', None)

def sample_entry():
    customJSON = {'original': 1, 'extra':2,
            'date':'2016-03-12', 'merchant':'Hobo'}
    user_name = 'test'
    firebase.put('/users/'+user_name+'/donationHistory/2015-03-12', 'purch_id_3', customJSON)

def make_firebase_entries(user_name):
    user_payments = json.loads(get_user_payments())
    # print(json.dumps(user_payments))
    present = time.strftime('%Y-%m-%d');
    for eachPurchase in user_payments:
        fb_purchaseID = firebase.get('users/'+user_name+'/donationHistory/' + present, eachPurchase["_id"])
        if (fb_purchaseID == None):
            merchant_for_payment = get_merchant_by_id(eachPurchase["merchant_id"])
            amount = eachPurchase['amount']
            date = eachPurchase['purchase_date']
            pruchaseID = eachPurchase['_id']
            if(math.ceil(amount) - amount) <= 0.3:
                extra_amount = math.ceil(amount)-amount;
                customJSON = {'original': amount, 
                'extra':extra_amount,
                'date':date, 
                'merchant':merchant_for_payment}            
                resp = firebase.put('/users/'+user_name+'/donationHistory/'+date, pruchaseID, customJSON);
                print(resp)

def get_monthly_amount(user_username):
    document = firebase.get('/users', user_username)
    return document['amount']

def get_user_payments():
    user_payment_history_url = '{}accounts/{}/purchases?key={}'.format(capitalAPIURl,
        capitalAccountID, capitalAPIkey)
    document_get = requests.get(user_payment_history_url)
    document = json.loads(document_get.text)
    listDoc = []
    merchantIDList = []
    present = time.strftime('%Y-%m-%d');
    for eachPurchase in document:
        if(eachPurchase['purchase_date'] == present):
            listDoc.append(eachPurchase)
    return json.dumps([obj for obj in listDoc])


def get_merchant_by_id(merchantId):
    merchant_details_url = '{}merchants/{}?key={}'.format(capitalAPIURl, 
        merchantId, capitalAPIkey)
    document_get = requests.get(merchant_details_url)
    document = json.loads(document_get.text)
    return document['name'] 

def transfer_payment(senderID, receiverID, amount):
    dataPost = {'medium': 'balance',
  'payee_id': receiverID,
  'amount': amount,
  'transaction_date': time.strftime("%Y-%m-%d"),
  'status': 'pending',
  'description': 'Transfer to organization'
    }
    senderDetails = firebase.get('/accounts', senderId)
    receiverDetails = firebase.get('/accounts', receiverID)
    
    user_transfer_url = '{}accounts/{}/transfers?key={}'.format(capitalAPIURl, senderID, capitalAPIKey)
    response = requests.post(user_transfer_url, json = dataPos)

if __name__ == '__main__':
    main()
