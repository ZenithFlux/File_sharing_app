from dotenv import load_dotenv
import os
import string
import random

def generate_env():
    os.environ['SECRET_KEY'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))
    os.environ['UPLOAD_FOLDER'] = 'uploads'
    os.environ['DEBUG'] = '0'
    os.environ['TESTING'] = '0'
    with open('.env', 'w') as f:
        f.write(f"SECRET_KEY={os.environ['SECRET_KEY']}\n"
                +f"UPLOAD_FOLDER={os.environ['UPLOAD_FOLDER']}\n"
                +f"DEBUG={os.environ['DEBUG']}\n"
                +f"TESTING={os.environ['TESTING']}")

load_dotenv(".env")

class Config:
    try:
        SECRET_KEY = os.environ['SECRET_KEY']
        UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
        DEBUG = int(os.environ['DEBUG'])
        TESTING = int(os.environ['TESTING'])
        
    except Exception:
        print('Generated new .env')
        generate_env()
        SECRET_KEY = os.environ['SECRET_KEY']
        UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
        DEBUG = int(os.environ['DEBUG'])
        TESTING = int(os.environ['TESTING'])