#!/usr/bin/env python3
"""
Generate Interactive Dashboard
Creates an HTML page with checkboxes to select deals for posting
"""

import json
import sys
import os
from datetime import datetime

# Add parent directory to path to import parsers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def parse_gcw_deals(text, url):
    """Parse Golf Clearance Warehouse format"""
    import re
    deals = []
    
    pattern = r'([^·]+?)·\s*Our Price[:\s]*\$([0-9,]+\.?\d*)\s*·\s*Sale Price[:\s]*\$([0-9,]+\.?\d*)\s*·\s*You save \$([0-9,]+\.?\d*)'
    
    for match in re.finditer(pattern, text):
        try:
            product_name = match.group(1).strip()
            original_price = float(match.group(2).replace(',', ''))
            sale_price = float(match.group(3).replace(',', ''))
            savings = float(match.group(4).replace(',', ''))
            discount_pct = (savings / original_price * 100) if original_price > 0 else 0
            
            if product_name:
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

def parse_golf_town_deals(text, url):
    """Parse Golf Town format"""
    import re
    deals = []
    
    pattern = r'([^·]+?)·\s*\$([0-9,]+\.?\d*)\s+\$([0-9,]+\.?\d*)\s+\((\d+)%\s+off\)'
    
    for match in re.finditer(pattern, text):
        try:
            product_name = match.group(1).strip()
            original_price = float(match.group(2).replace(',', ''))
            sale_price = float(match.group(3).replace(',', ''))
            discount_pct = int(match.group(4))
            savings = original_price - sale_price
            
            if product_name:
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

def generate_dashboard(deals):
    """Generate interactive HTML dashboard"""
    
    # Sort by discount percentage
    sorted_deals = sorted(deals, key=lambda x: x['discount_pct'], reverse=True)
    
    # Calculate stats
    total_deals = len(deals)
    avg_discount = sum(d['discount_pct'] for d in deals) / len(deals) if deals else 0
    max_discount = max(d['discount_pct'] for d in deals) if deals else 0
    total_savings = sum(d['savings'] for d in deals)
    excellent_deals = len([d for d in deals if d['discount_pct'] >= 50])
    great_deals = len([d for d in deals if 30 <= d['discount_pct'] < 50])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golf Deals - Deal Selector</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .header .timestamp {{ opacity: 0.9; font-size: 0.9em; }}
        
        .controls {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1em;
            transition: all 0.2s;
        }}
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        .btn-primary:hover {{ background: #5568d3; }}
        .btn-success {{
            background: #48bb78;
            color: white;
        }}
        .btn-success:hover {{ background: #38a169; }}
        .btn-secondary {{
            background: #718096;
            color: white;
        }}
        .btn-secondary:hover {{ background: #4a5568; }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{ color: #666; font-size: 0.9em; margin-bottom: 8px; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        
        .filters {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .filters select {{
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            margin-right: 10px;
        }}
        
        .deal-card {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            display: flex;
            gap: 20px;
            align-items: center;
            transition: all 0.2s;
        }}
        .deal-card:hover {{ box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
        .deal-card.selected {{ background: #f0f4ff; border-left-color: #48bb78; }}
        .deal-card.excellent {{ border-left-color: #f56565; }}
        .deal-card.great {{ border-left-color: #ed8936; }}
        .deal-card.good {{ border-left-color: #48bb78; }}
        
        .deal-checkbox {{
            width: 24px;
            height: 24px;
            cursor: pointer;
        }}
        
        .deal-info {{ flex: 1; }}
        .deal-info h3 {{ color: #2d3748; margin-bottom: 10px; font-size: 1.2em; }}
        .deal-prices {{
            display: flex;
            gap: 15px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}
        .price-tag {{
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: 600;
        }}
        .original-price {{
            background: #fed7d7;
            color: #c53030;
            text-decoration: line-through;
        }}
        .sale-price {{
            background: #c6f6d5;
            color: #22543d;
            font-size: 1.2em;
        }}
        .savings {{
            background: #bee3f8;
            color: #2c5282;
        }}
        .deal-source {{
            font-size: 0.85em;
            color: #718096;
            margin-top: 5px;
        }}
        .deal-quality {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        .quality-excellent {{ background: #fed7d7; color: #c53030; }}
        .quality-great {{ background: #feebc8; color: #c05621; }}
        .quality-good {{ background: #c6f6d5; color: #22543d; }}
        .quality-fair {{ background: #bee3f8; color: #2c5282; }}
        
        .deal-actions {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .deal-actions .btn {{
            padding: 8px 16px;
            font-size: 0.9em;
            white-space: nowrap;
        }}
        
        .selection-summary {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            min-width: 250px;
            display: none;
        }}
        .selection-summary.active {{ display: block; }}
        .selection-summary h3 {{ margin-bottom: 15px; color: #2d3748; }}
        .selection-count {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #48bb78;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: none;
            animation: slideIn 0.3s ease;
        }}
        .notification.show {{ display: block; }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        #copyOutput {{
            display: none;
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            max-height: 400px;
            overflow-y: auto;
        }}
        #copyOutput pre {{
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⛳ Golf Deals - Deal Selector</h1>
        <div class="timestamp">Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</div>
    </div>
    
    <div class="controls">
        <button class="btn btn-primary" onclick="selectAll()">Select All</button>
        <button class="btn btn-secondary" onclick="deselectAll()">Deselect All</button>
        <button class="btn btn-success" onclick="copySelectedDeals()">📋 Copy Selected for Reddit</button>
        <button class="btn btn-secondary" onclick="exportToCSV()">💾 Export to CSV</button>
        <span style="margin-left: auto; font-weight: 600; color: #718096;">
            <span id="selectedCount">0</span> deals selected
        </span>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>Total Deals</h3>
            <div class="value">{total_deals}</div>
        </div>
        <div class="stat-card">
            <h3>Avg Discount</h3>
            <div class="value">{avg_discount:.1f}%</div>
        </div>
        <div class="stat-card">
            <h3>Best Deal</h3>
            <div class="value">{max_discount:.0f}%</div>
        </div>
        <div class="stat-card">
            <h3>Total Savings</h3>
            <div class="value">${total_savings:.0f}</div>
        </div>
    </div>
    
    <div class="filters">
        <select id="qualityFilter" onchange="filterDeals()">
            <option value="all">All Quality Levels</option>
            <option value="50">🔥 50%+ off only</option>
            <option value="30">30%+ off only</option>
            <option value="20">20%+ off only</option>
        </select>
        
        <select id="sourceFilter" onchange="filterDeals()">
            <option value="all">All Sources</option>
            <option value="Golf Clearance Warehouse">Golf Clearance Warehouse</option>
            <option value="Golf Town">Golf Town</option>
        </select>
    </div>
    
    <div id="copyOutput">
        <h3>📋 Reddit Posts (Ready to Copy)</h3>
        <pre id="copyText"></pre>
        <button class="btn btn-primary" onclick="copyToClipboard()">Copy to Clipboard</button>
    </div>
    
    <div id="dealsContainer">
'''
    
    # Add deal cards
    for i, deal in enumerate(sorted_deals):
        quality = 'excellent' if deal['discount_pct'] >= 50 else 'great' if deal['discount_pct'] >= 30 else 'good' if deal['discount_pct'] >= 20 else 'fair'
        quality_label = '🔥 EXCELLENT' if deal['discount_pct'] >= 50 else '🔥 GREAT' if deal['discount_pct'] >= 30 else 'Good' if deal['discount_pct'] >= 20 else 'Fair'
        
        html += f'''
        <div class="deal-card {quality}" data-discount="{deal['discount_pct']}" data-source="{deal['source']}" data-index="{i}">
            <input type="checkbox" class="deal-checkbox" onchange="updateSelection()">
            <div class="deal-info">
                <h3>{deal['product_name']}</h3>
                <div class="deal-prices">
                    <span class="price-tag original-price">${deal['original_price']:.2f}</span>
                    <span class="price-tag sale-price">${deal['sale_price']:.2f}</span>
                    <span class="price-tag savings">Save ${deal['savings']:.2f} ({deal['discount_pct']:.0f}% off)</span>
                </div>
                <span class="deal-quality quality-{quality}">{quality_label}</span>
                <div class="deal-source">Source: {deal['source']}</div>
            </div>
            <div class="deal-actions">
                <a href="{deal['url']}" target="_blank" class="btn btn-secondary">View Category</a>
            </div>
        </div>
'''
    
    html += '''
    </div>
    
    <div id="notification" class="notification"></div>
    
    <script>
        const deals = ''' + json.dumps(sorted_deals) + ''';
        
        function updateSelection() {
            const checkboxes = document.querySelectorAll('.deal-checkbox');
            const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
            document.getElementById('selectedCount').textContent = selectedCount;
            
            // Update card appearance
            checkboxes.forEach((cb, index) => {
                const card = cb.closest('.deal-card');
                if (cb.checked) {
                    card.classList.add('selected');
                } else {
                    card.classList.remove('selected');
                }
            });
        }
        
        function selectAll() {
            document.querySelectorAll('.deal-checkbox:not([style*="display: none"])').forEach(cb => {
                const card = cb.closest('.deal-card');
                if (card.style.display !== 'none') {
                    cb.checked = true;
                }
            });
            updateSelection();
        }
        
        function deselectAll() {
            document.querySelectorAll('.deal-checkbox').forEach(cb => cb.checked = false);
            updateSelection();
        }
        
        function filterDeals() {
            const qualityFilter = document.getElementById('qualityFilter').value;
            const sourceFilter = document.getElementById('sourceFilter').value;
            
            document.querySelectorAll('.deal-card').forEach(card => {
                const discount = parseFloat(card.dataset.discount);
                const source = card.dataset.source;
                
                let show = true;
                
                if (qualityFilter !== 'all' && discount < parseFloat(qualityFilter)) {
                    show = false;
                }
                
                if (sourceFilter !== 'all' && source !== sourceFilter) {
                    show = false;
                }
                
                card.style.display = show ? 'flex' : 'none';
            });
        }
        
        function copySelectedDeals() {
            const checkboxes = document.querySelectorAll('.deal-checkbox');
            const selectedDeals = [];
            
            checkboxes.forEach((cb, index) => {
                if (cb.checked) {
                    selectedDeals.push(deals[parseInt(cb.closest('.deal-card').dataset.index)]);
                }
            });
            
            if (selectedDeals.length === 0) {
                showNotification('Please select at least one deal!', 'error');
                return;
            }
            
            let redditText = '';
            selectedDeals.forEach(deal => {
                redditText += formatRedditPost(deal) + '\\n\\n---\\n\\n';
            });
            
            document.getElementById('copyText').textContent = redditText;
            document.getElementById('copyOutput').style.display = 'block';
            document.getElementById('copyOutput').scrollIntoView({ behavior: 'smooth' });
        }
        
        function formatRedditPost(deal) {
            const qualityEmoji = deal.discount_pct >= 50 ? '🔥' : deal.discount_pct >= 30 ? '🔥' : '⛳';
            
            return `**${qualityEmoji} [${deal.source}] ${deal.product_name} - $${deal.sale_price.toFixed(2)} (${deal.discount_pct.toFixed(0)}% off!)**

~~$${deal.original_price.toFixed(2)}~~ **$${deal.sale_price.toFixed(2)}** - Save $${deal.savings.toFixed(2)}

[Link to deals page](${deal.url})

Source: ${deal.source}`;
        }
        
        function copyToClipboard() {
            const text = document.getElementById('copyText').textContent;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('✅ Copied to clipboard!');
            });
        }
        
        function exportToCSV() {
            const checkboxes = document.querySelectorAll('.deal-checkbox');
            const selectedDeals = [];
            
            checkboxes.forEach((cb, index) => {
                if (cb.checked) {
                    selectedDeals.push(deals[parseInt(cb.closest('.deal-card').dataset.index)]);
                }
            });
            
            if (selectedDeals.length === 0) {
                showNotification('Please select at least one deal!', 'error');
                return;
            }
            
            let csv = 'Product,Original Price,Sale Price,Savings,Discount %,Source,URL\\n';
            selectedDeals.forEach(deal => {
                csv += `"${deal.product_name}",${deal.original_price},${deal.sale_price},${deal.savings},${deal.discount_pct},"${deal.source}","${deal.url}"\\n`;
            });
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'golf-deals-' + new Date().toISOString().split('T')[0] + '.csv';
            a.click();
            
            showNotification('✅ CSV exported!');
        }
        
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.background = type === 'error' ? '#f56565' : '#48bb78';
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
    </script>
</body>
</html>
'''
    
    return html

def main():
    """Main function"""
    print("🎨 Generating interactive dashboard...")
    
    # Load raw deals
    try:
        with open('docs/raw_deals.json', 'r') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: docs/raw_deals.json not found")
        print("Run find_deals_simple.py first!")
        sys.exit(1)
    
    # Deals are already parsed in the new format
    all_deals = raw_data.get('deals', [])
    
    print(f"✅ Loaded {len(all_deals)} deals from raw_deals.json")
    
    # Generate dashboard
    html = generate_dashboard(all_deals)
    
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Save deals JSON
    with open('docs/deals.json', 'w') as f:
        json.dump(all_deals, f, indent=2)
    
    print("✅ Interactive dashboard generated: docs/index.html")
    print(f"📊 Found {len(all_deals)} deals")
    print(f"🔥 {len([d for d in all_deals if d['discount_pct'] >= 50])} excellent deals (50%+ off)")

if __name__ == "__main__":
    main()
