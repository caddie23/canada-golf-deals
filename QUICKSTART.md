# 🚀 Quick Start - Golf Deal Finder Automation

## What You're Getting

A **fully automated system** that:
1. ✅ Searches Golf Town & Golf Clearance Warehouse **daily at 9 AM**
2. ✅ Finds all deals (shoes, gloves, clubs)
3. ✅ Creates an **interactive dashboard** with checkboxes
4. ✅ Lets you **select deals** and copy formatted Reddit posts
5. ✅ Hosts everything **free on GitHub Pages**

## Cost: $0.50/month
- GitHub: Free
- Hosting: Free  
- API: ~$0.50/month

## 5-Minute Setup

### 1. Get Anthropic API Key
- Go to https://console.anthropic.com
- Create account → Get API key
- Save it somewhere

### 2. Create GitHub Repo
- Go to https://github.com/new
- Name: `golf-deals` 
- Make it **PUBLIC**
- Create it

### 3. Upload Files
**All the files you need are in the `/golf-deals-automation/` folder:**

```
golf-deals-automation/
├── .github/workflows/find-deals.yml    ← Automation
├── scripts/
│   ├── find_deals_with_api.py          ← Searcher
│   └── generate_interactive_dashboard.py ← Dashboard maker
├── docs/index.html                     ← Demo dashboard
├── SETUP.md                            ← Full instructions
├── README.md                           ← Repo docs
└── requirements.txt                    ← Dependencies
```

**Upload these to your GitHub repo:**
- Click "Add file" → "Upload files"
- Drag the ENTIRE folder
- Commit

### 4. Add API Key
- Repo Settings → Secrets → Actions
- New secret: `ANTHROPIC_API_KEY`
- Paste your key
- Save

### 5. Enable GitHub Pages
- Repo Settings → Pages
- Source: Deploy from branch
- Branch: `main`, Folder: `/docs`
- Save
- Your site: `https://yourusername.github.io/golf-deals/`

### 6. Run It!
- Go to Actions tab
- Click "Find Golf Deals"
- Click "Run workflow"
- Wait 3 minutes
- Visit your dashboard!

## Daily Workflow

**Morning (Automatic):**
- 9:00 AM: GitHub Actions runs
- 9:03 AM: Dashboard updates
- You get fresh deals!

**Afternoon (You):**
1. Visit `yourusername.github.io/golf-deals`
2. See all deals sorted by discount
3. Check boxes next to deals you like
4. Click "Copy Selected for Reddit"
5. Paste in Reddit
6. Done! (2 minutes total)

## What the Dashboard Looks Like

```
┌──────────────────────────────────────────────┐
│  ⛳ Golf Deals - Deal Selector                │
│  Last updated: Nov 20, 2025 at 9:00 AM       │
├──────────────────────────────────────────────┤
│  [Select All] [Copy for Reddit] [Export]    │
│                                 3 selected    │
├──────────────────────────────────────────────┤
│  Stats: 30 deals | Avg 52% off | Best 78%   │
├──────────────────────────────────────────────┤
│  Filter: [50%+ only ▼] [All sources ▼]      │
├──────────────────────────────────────────────┤
│  ☑ Women's FootJoy Glove - $7.95 (77% off)  │
│     🔥 EXCELLENT | Golf Clearance Warehouse  │
│                                               │
│  ☐ TaylorMade Driver - $279 (53% off)       │
│     🔥 GREAT | Golf Town                     │
│                                               │
│  ☑ Adidas Shoes - $39.95 (73% off)          │
│     🔥 EXCELLENT | Golf Clearance Warehouse  │
└──────────────────────────────────────────────┘
```

## Features

### ✅ Interactive Selection
- Checkboxes next to each deal
- Select All / Deselect All
- Filter by discount or source
- Real-time selection count

### 📋 Reddit Post Generator
Click "Copy Selected" and get:

```markdown
🔥 [Golf Clearance Warehouse] Women's FootJoy Glove - $7.95 (77% off!)

~~$35.00~~ **$7.95** - Save $27.05

[Link to deals page](https://...)

Source: Golf Clearance Warehouse
---
```

### 💾 Export to CSV
Download selected deals for tracking what you've posted.

### 🔍 Smart Filters
- Show only 50%+ deals
- Filter by Golf Town or GCW
- Sort by discount percentage

## Need Help?

**Check:**
1. `SETUP.md` - Full detailed instructions
2. `README.md` - Project overview
3. Actions tab - See if workflow ran
4. GitHub Pages settings - Make sure it's enabled

**Common Issues:**
- Dashboard not showing? Enable GitHub Pages in Settings
- No deals? Check API key is correct in Secrets
- Workflow failing? Check Actions tab for error logs

## What Happens Daily

```
9:00 AM EST
└─> GitHub Actions starts
    ├─> Searches Golf Clearance Warehouse (3 categories)
    ├─> Searches Golf Town (3 categories)  
    ├─> Parses all deals (~30-50 found)
    ├─> Generates new dashboard
    └─> Commits to repo → GitHub Pages updates

9:03 AM EST  
└─> Dashboard live at yourusername.github.io/golf-deals
    └─> You can now select & post deals!
```

## Customization Later

Want to add more?
- **More sites:** Edit `find_deals_with_api.py`
- **More categories:** Add searches (balls, bags, etc)
- **Different time:** Edit cron schedule
- **Email alerts:** Add notification step

## Next Steps

1. ✅ Follow the 5-minute setup above
2. ✅ Test with manual workflow run
3. ✅ Visit your dashboard
4. ✅ Select some deals
5. ✅ Post to Reddit!
6. 🎉 Enjoy automated deal finding!

---

**Questions?** Read `SETUP.md` for detailed step-by-step instructions.

**Ready to automate your deal hunting?** Let's go! 🏌️
