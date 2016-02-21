import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from firebase import firebase
from werkzeug import generate_password_hash, check_password_hash
import json
import requests

capitalAPIkey = 'b17c7f357d390d8a6a36badc619283a7'
capitalAccountID = ''
capitalAPIURl = 'api.reimaginebanking.com/'
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
    print(sample_entry())
    #print(get_monthly_amount())

def get_firebase_entries(user_username):    
    return firebase.get('/users/'+user_username+'/donationHistory', None)

def sample_entry():
    customJSON = {'original': 1, 'extra':'2',
            'date':'2016-03-12', 'merchant':'Hobo'}
    user_name = 'test'
    firebase.put('/users/'+user_name+'/donationHistory/2015-03-12', 'purch_id_3', customJSON)

def make_firebase_entries():
    user_payments = get_user_payments()
    listUpdated = []
    for eachPurchase in user_payments:
        merchant_for_payment = get_merchant_by_id(eachPurchase['merchant_id'])
        amount = eachPurchase['amount']
        date = eachPurchase['purchase_date']
        pruchaseID = eachPurchase['_id']
        if(math.ceil(amount)-amount) > 0.4:
            extra_amount = math.ceil(amount)-amount;
            customJSON = {'original': amount, 
            'extra':extra_amount,
            'date':date, 
            'merchant':merchant_for_payment}            
            firebase.put('/users/'+user_name+'/donationHistory/'+date, pruchaseID, customJSON)                

def get_monthly_amount():
    user_username = 'ajain34'
    document = firebase.get('/users', user_username)
    return document['amount']

def get_user_payments():
    user_payment_history_url = 'accounts/{}/purchases?key={}'.format(
        capitalAccountID, capitalAPIKey)
    document = requests.get(user_payment_history_url)
    #document = firebase.get('/purchases', 1)
    listDoc = []
    merchantIDList = []
    for eachPurchase in document:
        date = time.strptime(eachPurchase['purchase_date'], '%Y-%m-%d');
        if(date == present):
            listDoc.append(eachPurchase)            
    return json.dumps([obj for obj in listDoc])

def get_merchant_by_id(merchantId):
    merchant_details_url = 'merchants/{}?key={}'.format(
        merchantOd, capitalAPIKey)
    #document = firebase.get('/merchants', id)
    document = requests.get(merchant_details_url)
    if document['category'] == 'Restaurant':
        return document['name']
    return None 

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
    user_transfer_url = capitalAPIURL+'accounts/{}/transfers?key={}'.format(senderID, capitalAPIKey)
    response = requests.post(user_transfer_url, body = dataPos)
