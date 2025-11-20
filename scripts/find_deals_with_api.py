#!/usr/bin/env python3
"""
Automated Golf Deal Finder - Uses Anthropic API with web search
Runs daily via GitHub Actions to find deals from multiple sites
"""

import os
import json
import requests
from datetime import datetime

class AnthropicDealFinder:
    """Uses Anthropic API with web search to find golf deals"""
    
    def __init__(self):
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    
    def search_for_deals(self, site, category, search_query):
        """Use Claude with web search to find deals"""
        
        prompt = f"""Search {site} for {category} deals using this query: {search_query}

Extract ALL deals you find in this exact format:
Product Name · Price Info · Savings Info

Return ONLY the raw deal text, no explanations or commentary."""

        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4096,
            "tools": [{
                "type": "web_search_tool",
                "name": "web_search"
            }],
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract text from response
            if 'content' in data and len(data['content']) > 0:
                return data['content'][0].get('text', '')
            
            return ""
            
        except Exception as e:
            print(f"Error searching {site}: {e}")
            return ""
    
    def find_all_deals(self):
        """Search all sites and categories"""
        
        all_deals_text = {
            'gcw_shoes': "",
            'gcw_gloves': "",
            'gcw_clubs': "",
            'golf_town_clubs': "",
            'golf_town_shoes': "",
            'golf_town_gloves': ""
        }
        
        print("🔍 Starting automated deal search...")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Golf Clearance Warehouse searches
        print("Searching Golf Clearance Warehouse...")
        
        all_deals_text['gcw_shoes'] = self.search_for_deals(
            "golfclearancewarehouse.com",
            "golf shoes",
            "site:golfclearancewarehouse.com golf shoes price sale"
        )
        
        all_deals_text['gcw_gloves'] = self.search_for_deals(
            "golfclearancewarehouse.com", 
            "golf gloves",
            "site:golfclearancewarehouse.com golf gloves price sale"
        )
        
        all_deals_text['gcw_clubs'] = self.search_for_deals(
            "golfclearancewarehouse.com",
            "golf clubs",
            "site:golfclearancewarehouse.com golf clubs clearance price"
        )
        
        # Golf Town searches
        print("Searching Golf Town...")
        
        all_deals_text['golf_town_clubs'] = self.search_for_deals(
            "golftown.com",
            "clubs",
            "site:golftown.com clearance clubs price off"
        )
        
        all_deals_text['golf_town_shoes'] = self.search_for_deals(
            "golftown.com",
            "shoes", 
            "site:golftown.com clearance golf shoes price off"
        )
        
        all_deals_text['golf_town_gloves'] = self.search_for_deals(
            "golftown.com",
            "gloves",
            "site:golftown.com clearance golf gloves price off"
        )
        
        # Save raw search results
        timestamp = datetime.now().isoformat()
        output = {
            'timestamp': timestamp,
            'deals': all_deals_text
        }
        
        with open('docs/raw_deals.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("\n✅ Deal search complete!")
        print(f"📁 Raw results saved to docs/raw_deals.json")
        
        return all_deals_text

def main():
    """Main function"""
    finder = AnthropicDealFinder()
    deals = finder.find_all_deals()
    
    print("\n" + "="*60)
    print("Next: Run generate_interactive_dashboard.py to process deals")
    print("="*60)

if __name__ == "__main__":
    main()
