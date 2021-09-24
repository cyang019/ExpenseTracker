import os
from dotenv import load_dotenv
from application.app import create_app, db


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


app = create_app()
