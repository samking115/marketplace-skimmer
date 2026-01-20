# Facebook Marketplace Skimmer

A Python tool that scans Facebook Marketplace for undervalued items by comparing prices to sold eBay listings. The tool identifies potential resale opportunities and sends notifications about the best deals.

## Features

- 🔍 **Facebook Marketplace Scraping**: Automatically scan listings in your location
- 💰 **eBay Price Comparison**: Compare prices against recently sold eBay listings
- 📊 **Value Analysis**: Calculate discount percentages and profit potential
- 🎯 **Smart Filtering**: Configurable threshold for undervalued items
- 📧 **Notifications**: Console output and optional email alerts
- ⚙️ **Customizable**: JSON configuration for search parameters and preferences

## How It Works

1. **Scrape Marketplace**: The tool fetches listings from Facebook Marketplace based on your location and search criteria
2. **Find Comparables**: For each item, it searches eBay for recently sold listings of the same or similar items
3. **Analyze Value**: Compares the marketplace price to eBay averages and calculates discount percentage
4. **Identify Opportunities**: Filters items that are undervalued by your configured threshold (default: 30%)
5. **Notify You**: Sends notifications about the best opportunities ranked by profit potential

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/samking115/marketplace-skimmer.git
cd marketplace-skimmer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings in `config.json` (see Configuration section below)

## Usage

Run the skimmer:
```bash
python main.py
```

The tool will:
1. Scan Facebook Marketplace in your configured location
2. Compare prices to eBay sold listings
3. Display undervalued items in the console
4. Optionally send email notifications

### Sample Output

```
================================================================================
                    FACEBOOK MARKETPLACE SKIMMER
               Find Undervalued Items for Resale
================================================================================

[INFO] Configuration loaded from config.json
[INFO] Initializing components...
[INFO] Undervalued threshold: 30%
[INFO] Minimum eBay samples: 3

────────────────────────────────────────────────────────────────────────────────
STEP 1: Scraping Facebook Marketplace
────────────────────────────────────────────────────────────────────────────────
[INFO] Scraping Facebook Marketplace in Seattle, WA
[INFO] Found 1 marketplace items

────────────────────────────────────────────────────────────────────────────────
STEP 2: Analyzing Items Against eBay Sold Listings
────────────────────────────────────────────────────────────────────────────────

[1/1] Analyzing: iPhone 13 Pro 128GB - Excellent Condition
     Price: $450.00
[INFO] Found 4 sold listings
[✓] UNDERVALUED: 'iPhone 13 Pro 128GB - Excellent Condition'
    Marketplace: $450.00 | eBay Avg: $647.50
    Discount: 30.5% | Potential Profit: $197.50

────────────────────────────────────────────────────────────────────────────────
STEP 4: Sending Notifications
────────────────────────────────────────────────────────────────────────────────

================================================================================
Found 1 undervalued item(s)!
================================================================================

🔥 OPPORTUNITY #1 - Confidence: HIGH
────────────────────────────────────────────────────────────────────────────────
Title:       iPhone 13 Pro 128GB - Excellent Condition
Location:    Seattle, WA
URL:         https://facebook.com/marketplace/item/sample1

PRICING:
  Marketplace Price:  $450.00
  eBay Average:       $647.50
  eBay Median:        $647.50
  eBay Range:         $625.00 - $675.00

VALUE ANALYSIS:
  Discount:           30.5% below average
  Potential Profit:   $197.50
  eBay Samples:       4 sold listings
```

## Configuration

Edit `config.json` to customize the skimmer:

### Location Settings
```json
"location": {
  "city": "Seattle",
  "state": "WA",
  "radius_miles": 25,
  "zip_code": "98101"
}
```

### Search Parameters
```json
"search": {
  "categories": ["electronics", "furniture", "collectibles"],
  "keywords": [],
  "min_price": 0,
  "max_price": 1000,
  "max_listings_per_run": 50
}
```

### Analysis Settings
```json
"analysis": {
  "undervalued_threshold_percent": 30,
  "min_ebay_sold_samples": 3,
  "price_comparison_days": 90
}
```

### Notification Settings
```json
"notifications": {
  "console": true,
  "email": false,
  "email_address": "your-email@example.com",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_username": "your-email@example.com",
  "smtp_password": "your-app-password"
}
```

## Important Notes

### Facebook Marketplace Scraping

⚠️ **Authentication Required**: Facebook Marketplace requires authentication and uses heavy JavaScript rendering. The current implementation includes a demonstration structure but requires additional setup:

1. **Selenium/Playwright**: Install browser automation tools for dynamic content
2. **Authentication**: Handle Facebook login (consider using session cookies)
3. **Rate Limiting**: Implement proper delays to avoid detection
4. **CAPTCHA Handling**: May need to handle CAPTCHA challenges

To implement full scraping:
- Use Selenium WebDriver or Playwright for browser automation
- Store session cookies for authentication persistence
- Implement proper error handling and retry logic
- Respect Facebook's terms of service and rate limits

### eBay Scraping

The tool scrapes eBay's public sold listings pages. For production use:
- Consider using eBay's official Finding API (requires API key)
- Implement caching to reduce repeated queries
- Add more sophisticated matching algorithms
- Handle pagination for more comprehensive data

## Project Structure

```
marketplace-skimmer/
├── main.py                  # Main application entry point
├── marketplace_scraper.py   # Facebook Marketplace scraping logic
├── ebay_scraper.py          # eBay sold listings scraper
├── value_analyzer.py        # Price comparison and value analysis
├── notifier.py              # Notification system (console/email)
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Dependencies

- `requests`: HTTP library for web scraping
- `beautifulsoup4`: HTML parsing and extraction
- `selenium`: Browser automation (for dynamic content)
- `python-dotenv`: Environment variable management
- `Pillow`: Image processing capabilities

## Roadmap

- [ ] Full Facebook Marketplace scraper implementation with authentication
- [ ] Image-based similarity matching using computer vision
- [ ] Machine learning for better value prediction
- [ ] Database storage for historical tracking
- [ ] Web dashboard for monitoring
- [ ] Automated bidding/messaging integration
- [ ] Support for additional marketplaces (OfferUp, Craigslist, etc.)
- [ ] Mobile app notifications

## Legal and Ethical Considerations

- **Terms of Service**: Ensure your usage complies with Facebook and eBay's terms of service
- **Rate Limiting**: Respect website rate limits and implement appropriate delays
- **Privacy**: Don't collect or store personal information from listings
- **Fair Use**: Use this tool for personal research and deal-finding only
- **Robots.txt**: Respect website robots.txt directives

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and personal use only. The authors are not responsible for any misuse or violations of third-party terms of service. Always ensure your use complies with applicable laws and website terms of service.