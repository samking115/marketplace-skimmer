#!/usr/bin/env python3
"""
Facebook Marketplace Skimmer - Main Application

This application scans Facebook Marketplace for items, compares their prices
to sold eBay listings, and identifies undervalued items for potential resale.
"""
import json
import sys
import os
from typing import List, Dict
from marketplace_scraper import MarketplaceScraper
from ebay_scraper import EbayScraper
from value_analyzer import ValueAnalyzer
from notifier import Notifier


def load_config(config_path: str = 'config.json') -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"[INFO] Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        print(f"[ERROR] Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in configuration file: {e}")
        sys.exit(1)


def print_header():
    """Print application header."""
    print("\n" + "="*80)
    print(" "*20 + "FACEBOOK MARKETPLACE SKIMMER")
    print(" "*15 + "Find Undervalued Items for Resale")
    print("="*80 + "\n")


def print_summary(total_items: int, undervalued_count: int):
    """Print execution summary."""
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(f"Total items analyzed:     {total_items}")
    print(f"Undervalued items found:  {undervalued_count}")
    if total_items > 0:
        percentage = (undervalued_count / total_items) * 100
        print(f"Success rate:             {percentage:.1f}%")
    print("="*80 + "\n")


def main():
    """Main application logic."""
    # Print header
    print_header()
    
    # Load configuration
    config = load_config()
    
    # Initialize components
    print("[INFO] Initializing components...")
    marketplace_scraper = MarketplaceScraper(config)
    ebay_scraper = EbayScraper(config)
    value_analyzer = ValueAnalyzer(config)
    notifier = Notifier(config)
    
    print(f"[INFO] Undervalued threshold: {config['analysis']['undervalued_threshold_percent']}%")
    print(f"[INFO] Minimum eBay samples: {config['analysis']['min_ebay_sold_samples']}")
    print()
    
    # Step 1: Scrape Facebook Marketplace
    print("─" * 80)
    print("STEP 1: Scraping Facebook Marketplace")
    print("─" * 80)
    marketplace_items = marketplace_scraper.scrape_marketplace()
    print(f"[INFO] Found {len(marketplace_items)} marketplace items\n")
    
    if not marketplace_items:
        print("[WARN] No marketplace items found. Exiting.")
        return
    
    # Step 2: Analyze each item
    print("─" * 80)
    print("STEP 2: Analyzing Items Against eBay Sold Listings")
    print("─" * 80)
    
    analyses = []
    for i, item in enumerate(marketplace_items, 1):
        print(f"\n[{i}/{len(marketplace_items)}] Analyzing: {item['title']}")
        print(f"     Price: ${item['price']:.2f}")
        
        # Search eBay for sold listings
        ebay_listings = ebay_scraper.search_sold_listings(item['title'])
        
        # Calculate price statistics
        ebay_stats = ebay_scraper.calculate_average_price(ebay_listings)
        
        # Analyze value
        analysis = value_analyzer.analyze_item(item, ebay_stats)
        analyses.append(analysis)
    
    # Step 3: Rank opportunities
    print("\n" + "─" * 80)
    print("STEP 3: Ranking Opportunities")
    print("─" * 80)
    opportunities = value_analyzer.rank_opportunities(analyses)
    
    if opportunities:
        print(f"[INFO] Found {len(opportunities)} undervalued items")
        for i, opp in enumerate(opportunities, 1):
            print(f"  {i}. {opp['marketplace_item']['title']} - ${opp['potential_profit']:.2f} profit potential")
    else:
        print("[INFO] No undervalued items found")
    
    # Step 4: Send notifications
    print("\n" + "─" * 80)
    print("STEP 4: Sending Notifications")
    print("─" * 80)
    notifier.notify(opportunities)
    
    # Print summary
    print_summary(len(marketplace_items), len(opportunities))
    
    print("[INFO] Skimmer execution completed!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Execution interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
