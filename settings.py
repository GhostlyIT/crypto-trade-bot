from dotenv import load_dotenv
import os

load_dotenv()

settings = {
    'exchange_api': {
        'base_url': os.environ.get('BASE_URL'),
        'key': os.environ.get('API_KEY'),
        'secret': os.environ.get('SECRET_KEY')
    }
}
