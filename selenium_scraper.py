"""
Advanced Facebook Marketplace Scraper with Selenium

This module demonstrates how to implement full Facebook Marketplace scraping
using Selenium for dynamic content and authentication.

REQUIREMENTS:
1. Install selenium and webdriver-manager:
   pip install selenium webdriver-manager

2. For production use, you'll need to:
   - Handle Facebook authentication (login with cookies or credentials)
   - Implement proper error handling and retries
   - Add rate limiting and delays to avoid detection
   - Handle CAPTCHA challenges
   - Respect Facebook's Terms of Service

IMPORTANT: This is a demonstration template only. Facebook's Terms of Service
may restrict automated access. Use responsibly and ensure compliance.
"""
from typing import List, Dict, Optional
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumMarketplaceScraper:
    """
    Advanced marketplace scraper using Selenium.
    
    NOTE: This is a template/demonstration. Facebook's structure changes frequently
    and may require updates to selectors and logic.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.location = config['location']
        self.search_params = config['search']
        self.driver = None
        
    def _init_driver(self):
        """Initialize Selenium WebDriver."""
        try:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in background
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={self.config["scraping"]["user_agent"]}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            print("[INFO] Selenium WebDriver initialized")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize WebDriver: {e}")
            print("[INFO] Make sure to install: pip install selenium webdriver-manager")
            raise
    
    def _login_to_facebook(self, email: str, password: str):
        """
        Login to Facebook.
        
        WARNING: Storing credentials in plain text is insecure.
        In production, use environment variables or secure credential storage.
        Consider using saved session cookies instead.
        """
        try:
            self.driver.get("https://www.facebook.com/login")
            time.sleep(2)
            
            # Find and fill email
            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys(email)
            
            # Find and fill password
            password_input = self.driver.find_element(By.ID, "pass")
            password_input.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            
            time.sleep(5)  # Wait for login to complete
            
            print("[INFO] Logged into Facebook")
            
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            raise
    
    def scrape_marketplace(self, max_items: int = 50) -> List[Dict]:
        """
        Scrape Facebook Marketplace listings.
        
        Args:
            max_items: Maximum number of items to scrape
            
        Returns:
            List of marketplace listings
        """
        if not self.driver:
            self._init_driver()
        
        listings = []
        
        try:
            # Build marketplace URL
            # Format: https://www.facebook.com/marketplace/{location}/search
            # Add parameters for category, price range, etc.
            
            base_url = "https://www.facebook.com/marketplace/seattle/search"
            params = []
            
            if self.search_params['min_price'] > 0:
                params.append(f"minPrice={self.search_params['min_price']}")
            if self.search_params['max_price'] > 0:
                params.append(f"maxPrice={self.search_params['max_price']}")
            
            url = base_url + ("?" + "&".join(params) if params else "")
            
            print(f"[INFO] Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(3)  # Additional wait for dynamic content
            
            # Scroll to load more items
            self._scroll_page(times=5)
            
            # Find listing elements
            # NOTE: Facebook's HTML structure changes frequently
            # You'll need to inspect the page and update selectors
            listing_elements = self.driver.find_elements(
                By.CSS_SELECTOR, 
                'div[data-testid="marketplace-search-result"]'  # Example selector
            )
            
            print(f"[INFO] Found {len(listing_elements)} listing elements")
            
            for element in listing_elements[:max_items]:
                try:
                    listing = self._parse_listing_element(element)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    print(f"[WARN] Error parsing listing: {e}")
                    continue
            
        except TimeoutException:
            print("[ERROR] Timeout waiting for page to load")
        except Exception as e:
            print(f"[ERROR] Scraping failed: {e}")
        finally:
            # Keep driver open for potential reuse
            pass
        
        return listings
    
    def _scroll_page(self, times: int = 3):
        """Scroll page to load more dynamic content."""
        for i in range(times):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
    
    def _parse_listing_element(self, element) -> Optional[Dict]:
        """
        Parse a single listing element.
        
        NOTE: Selectors will need to be updated based on Facebook's current structure.
        """
        try:
            # Example parsing logic - needs to be updated for current Facebook structure
            title = element.find_element(By.CSS_SELECTOR, 'span.listing-title').text
            price_text = element.find_element(By.CSS_SELECTOR, 'span.listing-price').text
            
            # Parse price
            price = float(price_text.replace('$', '').replace(',', ''))
            
            # Get URL
            link = element.find_element(By.TAG_NAME, 'a')
            url = link.get_attribute('href')
            
            # Get image
            img = element.find_element(By.TAG_NAME, 'img')
            image_url = img.get_attribute('src')
            
            listing = {
                'id': url.split('/')[-1],
                'title': title,
                'price': price,
                'url': url,
                'images': [image_url],
                'location': f"{self.location['city']}, {self.location['state']}",
                'description': '',  # Would need to visit detail page
                'posted_date': '',
                'seller': ''
            }
            
            return listing
            
        except NoSuchElementException:
            return None
        except Exception as e:
            print(f"[WARN] Error parsing element: {e}")
            return None
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("[INFO] WebDriver closed")


# Example usage (commented out - requires actual credentials)
"""
if __name__ == '__main__':
    import json
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    scraper = SeleniumMarketplaceScraper(config)
    
    # Login (use environment variables in production!)
    # scraper._login_to_facebook('your-email@example.com', 'your-password')
    
    # Scrape
    listings = scraper.scrape_marketplace(max_items=20)
    
    print(f"\nFound {len(listings)} listings:")
    for listing in listings:
        print(f"  - {listing['title']}: ${listing['price']}")
    
    scraper.close()
"""
