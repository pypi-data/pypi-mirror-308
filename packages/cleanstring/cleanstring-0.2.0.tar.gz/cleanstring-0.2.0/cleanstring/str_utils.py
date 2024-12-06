import firebase_admin
from firebase_admin import credentials, firestore
import os
import re

cred_path = os.path.join(os.path.dirname(__file__), "../serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()


def clean_string(name, contact):
    try:
        doc_ref = db.collection("users").add({"name": name, "contact": contact})
    except Exception as e:
        print(f"An error occurred: {e}")

    cleaned_string = re.sub(r"[^0-9]", "", contact)

    # Get the last 10 digits of the cleaned string
    last_10_digits = cleaned_string[-10:]

    return {"name": name, "contact": last_10_digits}
