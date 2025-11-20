# 🏌️ Automated Golf Deal Finder - Setup Guide

Complete guide to set up your automated golf deal finder with GitHub Actions and GitHub Pages.

## 🎯 What This Does

**Automated (Daily):**
1. GitHub Actions runs at 9 AM every day
2. Uses Anthropic API to search Golf Town & Golf Clearance Warehouse
3. Finds all deals, parses them, generates interactive dashboard
4. Publishes dashboard to your GitHub Pages site

**Manual (You):**
1. Visit your GitHub Pages site: `https://yourusername.github.io/golf-deals`
2. See all today's deals with checkboxes
3. Select deals you want to post
4. Click "Copy Selected for Reddit"
5. Paste into Reddit and post!

## 📋 Prerequisites

- GitHub account (free)
- Anthropic API key (get from https://console.anthropic.com)

## 🚀 Setup Instructions

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `golf-deals` (or whatever you want)
3. Description: "Automated Canadian golf deal finder"
4. **Make it PUBLIC** (required for free GitHub Pages)
5. ✅ Initialize with README
6. Click "Create repository"

### Step 2: Get Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up / Log in
3. Go to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)
6. **SAVE THIS** - you won't see it again!

### Step 3: Add API Key to GitHub

1. In your GitHub repo, go to **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Paste your API key
6. Click **Add secret**

### Step 4: Upload Project Files

You have two options:

**Option A: Git Command Line** (if you know Git)
```bash
git clone https://github.com/yourusername/golf-deals.git
cd golf-deals
# Copy all files from golf-deals-automation folder here
git add .
git commit -m "Initial setup"
git push
```

**Option B: GitHub Web Interface** (easier)
1. Download all files from `/golf-deals-automation/` folder
2. In your GitHub repo, click **Add file** → **Upload files**
3. Drag and drop ALL these files:
   - `.github/workflows/find-deals.yml`
   - `scripts/find_deals_with_api.py`
   - `scripts/generate_interactive_dashboard.py`
   - `README.md`
   - `requirements.txt` (create if needed)
4. Commit the files

### Step 5: Enable GitHub Pages

1. In your repo, go to **Settings** tab
2. Scroll to **Pages** section
3. Source: **Deploy from a branch**
4. Branch: Select `main` and `/docs` folder
5. Click **Save**
6. Wait 1-2 minutes
7. Your site will be live at: `https://yourusername.github.io/golf-deals/`

### Step 6: Run First Time

**Manual trigger to test:**
1. Go to **Actions** tab in your repo
2. Click **Find Golf Deals** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait 2-3 minutes
5. Check the **docs/** folder - you should see:
   - `index.html` (your dashboard)
   - `deals.json` (deal data)
   - `raw_deals.json` (search results)

### Step 7: Visit Your Dashboard!

Go to: `https://yourusername.github.io/golf-deals/`

You should see your interactive deal selector!

## 📅 How It Works Daily

**Automated Schedule:**
- Runs every day at 9 AM EST (2 PM UTC)
- Takes ~3-5 minutes to complete
- Automatically commits new deals
- GitHub Pages auto-updates

**Manual Trigger:**
- Go to Actions → Find Golf Deals → Run workflow
- Useful for testing or getting deals now

## 🎨 Using the Dashboard

### Selecting Deals

1. **View all deals** - sorted by discount %
2. **Filter** - by discount level or source
3. **Check boxes** next to deals you want
4. **Copy Selected for Reddit** - generates formatted posts
5. **Export to CSV** - download for your records

### Reddit Post Format

When you click "Copy Selected", it generates:

```
🔥 [Golf Clearance Warehouse] Women's FootJoy StaSof Glove - $7.95 (77% off!)

~~$35.00~~ **$7.95** - Save $27.05

[Link to deals page](https://www.golfclearancewarehouse.com/...)

Source: Golf Clearance Warehouse

---
```

Ready to paste directly into Reddit!

## 🔧 Customization

### Change Schedule

Edit `.github/workflows/find-deals.yml`:

```yaml
schedule:
  - cron: '0 14 * * *'  # 9 AM EST
  # Change to:
  - cron: '0 17 * * *'  # 12 PM EST
```

Use https://crontab.guru to help create cron expressions.

### Add More Sites

Edit `scripts/find_deals_with_api.py` and add:

```python
all_deals_text['new_site'] = self.search_for_deals(
    "newsite.com",
    "category",
    "site:newsite.com search query"
)
```

Then add parsing in `generate_interactive_dashboard.py`.

### Change Categories

Currently searches: shoes, gloves, clubs

To add balls, edit `find_deals_with_api.py`:

```python
all_deals_text['gcw_balls'] = self.search_for_deals(
    "golfclearancewarehouse.com",
    "golf balls",
    "site:golfclearancewarehouse.com golf balls price"
)
```

## 💰 Costs

**GitHub:**
- Free for public repos
- Free 2,000 Actions minutes/month
- This uses ~10 min/month
- Free GitHub Pages hosting

**Anthropic API:**
- Pay per use
- ~$0.01-0.02 per day
- ~$0.30-0.60 per month
- Set up billing alerts in console

**Total: ~$0.50/month**

## 🐛 Troubleshooting

### Dashboard not updating?

1. Check Actions tab for errors
2. Make sure API key is set correctly
3. Check if GitHub Pages is enabled

### No deals showing?

1. Check `docs/raw_deals.json` - is it populated?
2. API key might be invalid
3. Check Actions logs for errors

### API key not working?

1. Regenerate key in Anthropic console
2. Update GitHub secret
3. Re-run workflow

## 📝 Files Explanation

```
golf-deals/
├── .github/
│   └── workflows/
│       └── find-deals.yml          # Automation config
├── scripts/
│   ├── find_deals_with_api.py      # Searches for deals
│   └── generate_interactive_dashboard.py  # Creates HTML
├── docs/
│   ├── index.html                  # Your dashboard (generated)
│   ├── deals.json                  # Deal data (generated)
│   └── raw_deals.json              # Search results (generated)
└── README.md                       # This file
```

## 🎯 Next Steps

1. ✅ Set up GitHub repo
2. ✅ Add API key
3. ✅ Enable GitHub Pages
4. ✅ Run first workflow
5. ✅ Visit your dashboard
6. 🎉 Start posting deals!

## 💡 Tips

- Check dashboard every morning after 9 AM
- Focus on 50%+ deals for Reddit
- Use CSV export to track what you've posted
- Customize filters to your preferences

## 🤝 Questions?

If something isn't working, check:
1. Actions tab for error logs
2. GitHub Pages deployment status
3. API key is correct in Secrets

---

**Ready to find deals automatically? Follow the steps above!** 🏌️⛳
