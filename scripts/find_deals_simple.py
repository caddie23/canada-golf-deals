#!/usr/bin/env python3
"""
Simplified Golf Deal Finder - Direct Scraping
No API needed - directly fetches and parses deal pages
"""

import json
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

class SimpleDealFinder:
    """Directly scrapes golf deal sites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.all_deals = []
    
    def fetch_page(self, url):
        """Fetch a page and return text"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""
    
    def parse_gcw_deals(self, text, url):
        """Parse Golf Clearance Warehouse format"""
        deals = []
        pattern = r'([^·]+?)·\s*Our Price[:\s]*\$([0-9,]+\.?\d*)\s*·\s*Sale Price[:\s]*\$([0-9,]+\.?\d*)\s*·\s*You save \$([0-9,]+\.?\d*)'
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                product_name = match.group(1).strip()
                # Clean up product name
                product_name = re.sub(r'(Deal of the Day Price:|You save.*)', '', product_name).strip()
                
                original_price = float(match.group(2).replace(',', ''))
                sale_price = float(match.group(3).replace(',', ''))
                savings = float(match.group(4).replace(',', ''))
                discount_pct = (savings / original_price * 100) if original_price > 0 else 0
                
                if product_name and original_price > 0:
                    deals.append({
                        'product_name': product_name,
                        'original_price': original_price,
                        'sale_price': sale_price,
                        'savings': savings,
                        'discount_pct': round(discount_pct, 1),
                        'url': url,
                        'source': 'Golf Clearance Warehouse'
                    })
            except:
                pass
        
        return deals
    
    def parse_golf_town_deals(self, text, url):
        """Parse Golf Town format"""
        deals = []
        pattern = r'([^·]+?)·\s*\$([0-9,]+\.?\d*)\s+\$([0-9,]+\.?\d*)\s+\((\d+)%\s+off\)'
        
        for match in re.finditer(pattern, text):
            try:
                product_name = match.group(1).strip()
                product_name = re.sub(r'(Clearance|Final Sale|Waterproof)', '', product_name).strip()
                
                original_price = float(match.group(2).replace(',', ''))
                sale_price = float(match.group(3).replace(',', ''))
                discount_pct = int(match.group(4))
                savings = original_price - sale_price
                
                if product_name and original_price > 0:
                    deals.append({
                        'product_name': product_name,
                        'original_price': original_price,
                        'sale_price': sale_price,
                        'savings': savings,
                        'discount_pct': discount_pct,
                        'url': url,
                        'source': 'Golf Town'
                    })
            except:
                pass
        
        return deals
    
    def scrape_gcw_category(self, url, category_name):
        """Scrape Golf Clearance Warehouse category"""
        print(f"  Scraping GCW {category_name}...")
        html = self.fetch_page(url)
        if html:
            deals = self.parse_gcw_deals(html, url)
            print(f"    Found {len(deals)} deals")
            return deals
        return []
    
    def scrape_golf_town_category(self, url, category_name):
        """Scrape Golf Town category"""
        print(f"  Scraping Golf Town {category_name}...")
        html = self.fetch_page(url)
        if html:
            deals = self.parse_golf_town_deals(html, url)
            print(f"    Found {len(deals)} deals")
            return deals
        return []
    
    def find_all_deals(self):
        """Scrape all sites and categories"""
        print("🔍 Starting deal search...")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_deals = []
        
        # Golf Clearance Warehouse
        print("Searching Golf Clearance Warehouse...")
        
        gcw_urls = [
            ("https://www.golfclearancewarehouse.com/golf-shoes-s/11.htm", "Shoes"),
            ("https://www.golfclearancewarehouse.com/category-s/99.htm", "Gloves"),
            ("https://www.golfclearancewarehouse.com/discount-golf-clubs-canada-s/656.htm", "Clubs"),
            ("https://www.golfclearancewarehouse.com/golf-bags-s/1.htm", "Bags"),
        ]
        
        for url, name in gcw_urls:
            deals = self.scrape_gcw_category(url, name)
            all_deals.extend(deals)
        
        # Golf Town
        print("\nSearching Golf Town...")
        
        gt_urls = [
            ("https://www.golftown.com/en-CA/sale/clearance/clubs/", "Clubs"),
            ("https://www.golftown.com/en-CA/sale/clearance/shoes/", "Shoes"),
            ("https://www.golftown.com/en-CA/sale/clearance/golf-gloves/", "Gloves"),
        ]
        
        for url, name in gt_urls:
            deals = self.scrape_golf_town_category(url, name)
            all_deals.extend(deals)
        
        print(f"\n✅ Deal search complete! Found {len(all_deals)} total deals")
        
        # Save deals
        timestamp = datetime.now().isoformat()
        output = {
            'timestamp': timestamp,
            'total_deals': len(all_deals),
            'deals': all_deals
        }
        
        with open('docs/raw_deals.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"📁 Deals saved to docs/raw_deals.json")
        
        return all_deals

def main():
    """Main function"""
    finder = SimpleDealFinder()
    deals = finder.find_all_deals()
    
    print("\n" + "="*60)
    print(f"Found {len(deals)} deals:")
    print(f"  🔥 {len([d for d in deals if d['discount_pct'] >= 50])} excellent (50%+ off)")
    print(f"  🔥 {len([d for d in deals if 30 <= d['discount_pct'] < 50])} great (30-49% off)")
    print("="*60)

if __name__ == "__main__":
    main()
