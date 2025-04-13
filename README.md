#Soccer Jersey Auto-Discount System

This system automatically tracks soccer match results from various leagues and applies discounts to winning teams' jerseys in your WooCommerce store.

## Supported Leagues
- German Bundesliga
- Italian Serie A
- English Premier League
- American MLS
- Mexican Liga MX

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create an `.env` file with:
```
WOOCOMMERCE_URL = woocommerce url
WOOCOMMERCE_CONSUMER_KEY = woocommerce consumer key
WOOCOMMERCE_CONSUMER_SECRET = woocommerce consumer secret
FOOTBALL_API_KEY = API football key
```

3. Run with:
```bash
python auto_discounts.py
```

## How It Works
1. Script runs daily at 00:05 to check for new match results
2. When a team wins a match, their jerseys automatically receive a 10% discount
3. Discounts are implemented as WooCommerce coupons
4. Each discount is valid for 2 days
5. Match results are stored in a local SQLite database

## Customization
You can modify the following settings in `config.py`:
- Discount percentage
- Discount duration
- Tracked leagues
- Database file location

## Requirements
- Python 3.7+
- WooCommerce store (with API keys)
- API-Football key