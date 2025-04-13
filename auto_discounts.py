import sqlite3
import requests
import schedule
import time
from datetime import datetime, timedelta
import pytz
from woocommerce import API
from config import *

class SoccerDiscountManager:
    def __init__(self):
        self.wcapi = API(
            url=WOOCOMMERCE_URL,
            consumer_key=WOOCOMMERCE_CONSUMER_KEY,
            consumer_secret=WOOCOMMERCE_CONSUMER_SECRET,
            version="wc/v3"
        )
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing match results"""
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS match_results
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     league TEXT,
                     home_team TEXT,
                     away_team TEXT,
                     home_score INTEGER,
                     away_score INTEGER,
                     match_date TEXT,
                     discount_applied BOOLEAN DEFAULT 0)''')
        conn.commit()
        conn.close()

    def fetch_match_results(self):
        """Fetch match results from API-Football for all tracked leagues"""
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': FOOTBALL_API_KEY
        }
        
        for league_name, league_id in LEAGUES.items():
            url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures"
            params = {
                'league': league_id,
                'season': datetime.now().year,
                'last': '1'
            }
            
            try:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                
                if data['response']:
                    for match in data['response']:
                        self.process_match_result(league_name, match)
            except Exception as e:
                print(f"Error fetching results for {league_name}: {str(e)}")

    def process_match_result(self, league, match):
        """Process a single match result and store it in the database"""
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        home_score = match['goals']['home']
        away_score = match['goals']['away']
        match_date = match['fixture']['date']
        
        #determine winner
        winner = None
        if home_score > away_score:
            winner = home_team
        elif away_score > home_score:
            winner = away_team
            
        if winner:
            conn = sqlite3.connect(DATABASE_FILE)
            c = conn.cursor()
            c.execute('''INSERT INTO match_results 
                        (league, home_team, away_team, home_score, away_score, match_date)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (league, home_team, away_team, home_score, away_score, match_date))
            conn.commit()
            conn.close()
            
            #apply discount for winner's jerseys
            self.apply_discount(winner)

    def apply_discount(self, team_name):
        """Apply discount to winning team's jerseys in WooCommerce"""
        #search for products containing team name
        products = self.wcapi.get("products", params={
            'search': team_name,
            'category': 'jerseys'
        }).json()
        
        for product in products:
            #create a coupon
            coupon_data = {
                'code': f"{team_name.lower().replace(' ', '-')}-winner",
                'discount_type': 'percent',
                'amount': str(DISCOUNT_PERCENTAGE),
                'individual_use': True,
                'product_ids': [product['id']],
                'date_expires': (datetime.now() + timedelta(days=DISCOUNT_DURATION_DAYS)).isoformat(),
                'usage_limit': 100,
                'description': f"Automatic discount for {team_name} winning their match!"
            }
            
            try:
                self.wcapi.post("coupons", coupon_data)
                print(f"Created discount coupon for {team_name}")
            except Exception as e:
                print(f"Error creating coupon for {team_name}: {str(e)}")

    def run(self):
        """Main execution loop"""
        print("Starting Soccer Discount Manager...")
        self.fetch_match_results()
        
        #schedule daily checks
        schedule.every().day.at("00:05").do(self.fetch_match_results)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    manager = SoccerDiscountManager()
    manager.run() 