import os
from dotenv import load_dotenv

#load environment variables
load_dotenv()

#woocommerce API stuff
WOOCOMMERCE_URL = os.getenv('WOOCOMMERCE_URL')
WOOCOMMERCE_CONSUMER_KEY = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
WOOCOMMERCE_CONSUMER_SECRET = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')

#API-Football credentials
FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')

#league to track (API-Football IDs)
LEAGUES = {
    #bundesliga
    'german': 78,
    #serie A
    'italian': 135,
    #EPL
    'english': 39,
    #MLS
    'american': 253,
    #ligma MX
    'mexican': 262,
}

#discount settings
DISCOUNT_PERCENTAGE = 10
DISCOUNT_DURATION_DAYS = 2

#database settings
DATABASE_FILE = 'match_results.db' 