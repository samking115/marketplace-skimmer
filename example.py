#!/usr/bin/env python3
"""
Example usage script for the Marketplace Skimmer.

This demonstrates how to use the skimmer with custom marketplace listings.
Modify the sample_listings list to test with your own data.
"""
import json
from marketplace_scraper import MarketplaceScraper
from ebay_scraper import EbayScraper
from value_analyzer import ValueAnalyzer
from notifier import Notifier


def load_config():
    """Load configuration."""
    with open('config.json', 'r') as f:
        return json.load(f)


def main():
    """Example usage with custom data."""
    print("\n" + "="*80)
    print(" "*20 + "MARKETPLACE SKIMMER - EXAMPLE")
    print("="*80 + "\n")
    
    # Load config
    config = load_config()
    
    # Initialize components
    ebay_scraper = EbayScraper(config)
    value_analyzer = ValueAnalyzer(config)
    notifier = Notifier(config)
    
    # Define sample marketplace listings to analyze
    # Modify this list to test with your own items
    sample_listings = [
        {
            'id': 'fb_1',
            'title': 'iPhone 13 Pro 128GB',
            'description': 'Great condition, includes box and charger',
            'price': 450.00,
            'location': 'Seattle, WA',
            'url': 'https://facebook.com/marketplace/item/sample1',
            'images': [],
            'posted_date': '2024-01-15',
            'seller': 'Sample Seller'
        },
        {
            'id': 'fb_2',
            'title': 'Sony PlayStation 5 Console',
            'description': 'Barely used, like new condition with all accessories',
            'price': 350.00,
            'location': 'Seattle, WA',
            'url': 'https://facebook.com/marketplace/item/sample2',
            'images': [],
            'posted_date': '2024-01-16',
            'seller': 'Sample Seller 2'
        },
        {
            'id': 'fb_3',
            'title': 'MacBook Air M1 2020',
            'description': 'Excellent condition, 8GB RAM, 256GB SSD',
            'price': 600.00,
            'location': 'Seattle, WA',
            'url': 'https://facebook.com/marketplace/item/sample3',
            'images': [],
            'posted_date': '2024-01-17',
            'seller': 'Sample Seller 3'
        }
    ]
    
    print(f"[INFO] Analyzing {len(sample_listings)} sample listings...\n")
    
    # Analyze each item
    analyses = []
    for i, item in enumerate(sample_listings, 1):
        print(f"\n[{i}/{len(sample_listings)}] Analyzing: {item['title']}")
        print(f"     Marketplace Price: ${item['price']:.2f}")
        
        # Search eBay (will use sample data if no internet)
        ebay_listings = ebay_scraper.search_sold_listings(item['title'])
        ebay_stats = ebay_scraper.calculate_average_price(ebay_listings)
        
        # Analyze
        analysis = value_analyzer.analyze_item(item, ebay_stats)
        analyses.append(analysis)
    
    # Get opportunities
    opportunities = value_analyzer.rank_opportunities(analyses)
    
    # Notify
    print("\n" + "─" * 80)
    notifier.notify(opportunities)
    
    # Summary
    print("\n" + "="*80)
    print(f"SUMMARY: Found {len(opportunities)} undervalued items out of {len(sample_listings)} analyzed")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
