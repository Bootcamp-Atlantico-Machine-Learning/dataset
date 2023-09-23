from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials,storage
from google.cloud import storage
from google.oauth2 import service_account

config = {
  "apiKey": "AIzaSyDci14vP0nqfyDyDymcFTG0CgZyAJLhPvg",
  "authDomain": "cancertumorbootcampdosboots.firebaseapp.com",
  "projectId": "cancertumorbootcampdosboots",
  "storageBucket": "cancertumorbootcampdosboots.appspot.com",
  "messagingSenderId": "1025730251750",
  "appId": "1:1025730251750:web:bfcd620d8dcfa2ad502427",
  "measurementId": "G-HTJRM0LT10"
}


cred = credentials.Certificate("backend\cancertumorbootcampdosboots-8d42b3f35964.json")

firebase = firebase_admin.initialize_app(cred)
storage.Client(credentials=credentials).bucket(firebase_admin.storage.bucket().name).blob('file.png').download_to_filename('image.png')