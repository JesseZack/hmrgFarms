import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('hmrg-farms-firebase-adminsdk.json')

firebase_admin.initialize_app(cred)


