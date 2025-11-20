# ⛳ Automated Golf Deal Finder

Automatically finds and aggregates golf deals from Canadian retailers every day.

## 🎯 Features

- 🤖 **Fully Automated** - Runs daily via GitHub Actions
- 🎨 **Interactive Dashboard** - Select deals with checkboxes
- 📋 **Reddit-Ready** - One-click copy formatted posts
- 💾 **CSV Export** - Download for tracking
- 🔥 **Multi-Site** - Golf Clearance Warehouse + Golf Town
- 💰 **Free Hosting** - GitHub Pages (no server costs!)

## 🚀 Live Dashboard

Visit: **https://yourusername.github.io/golf-deals/** (update with your username)

Last updated: Automatically every day at 9 AM EST

## 📊 Current Stats

- **Sites Monitored:** 2 (Golf Clearance Warehouse, Golf Town)
- **Categories:** Shoes, Gloves, Clubs
- **Average Deals:** 30-50 per day
- **Best Discounts:** Up to 80% off

## 🛠️ Setup

See [SETUP.md](SETUP.md) for complete instructions.

**Quick Start:**
1. Fork this repo
2. Add `ANTHROPIC_API_KEY` to Secrets
3. Enable GitHub Pages (Settings → Pages → `/docs`)
4. Run workflow manually to test
5. Visit your dashboard!

## 📱 How to Use

1. **Visit dashboard** - Opens automatically updated page
2. **Browse deals** - All sorted by discount %
3. **Select favorites** - Check boxes next to deals you want
4. **Copy for Reddit** - Click button to copy formatted posts
5. **Post to Reddit** - Paste and submit!

## 🎨 Dashboard Features

- ✅ Interactive checkboxes
- 🔍 Filter by discount % or source
- 📋 One-click Reddit post copy
- 💾 CSV export
- 📊 Live statistics
- 🎯 Quality indicators (Excellent/Great/Good)

## 🤖 Automation

- **Schedule:** Daily at 9 AM EST
- **Duration:** ~3 minutes
- **Cost:** ~$0.50/month (Anthropic API)
- **Manual Trigger:** Available anytime

## 📦 Tech Stack

- **GitHub Actions** - Automation
- **GitHub Pages** - Free hosting
- **Anthropic Claude API** - Web searching
- **Python** - Scraping & parsing
- **Vanilla JS** - Interactive dashboard

## 🔧 Customization

### Add More Sites
Edit `scripts/find_deals_with_api.py`:
```python
all_deals_text['new_site'] = self.search_for_deals(...)
```

### Change Schedule
Edit `.github/workflows/find-deals.yml`:
```yaml
cron: '0 14 * * *'  # Change time
```

### Add Categories
Add new search queries in `find_deals_with_api.py`

## 📈 Roadmap

- [ ] Add more Canadian golf retailers
- [ ] Price history tracking
- [ ] Email notifications for hot deals
- [ ] Direct Reddit posting (via API)
- [ ] Mobile-optimized dashboard
- [ ] Deal quality scoring algorithm

## 💰 Costs

- GitHub: **Free** (public repo)
- GitHub Actions: **Free** (2000 min/month, uses ~10)
- GitHub Pages: **Free** (unlimited)
- Anthropic API: **~$0.50/month**

**Total: $0.50/month** 🎉

## 🤝 Contributing

Feel free to:
- Add more retailers
- Improve parsers
- Enhance dashboard
- Submit issues/PRs

## 📝 License

MIT License - Free to use and modify!

## 🙏 Acknowledgments

- Golf Clearance Warehouse
- Golf Town
- Anthropic Claude API

---

**Happy Deal Hunting!** 🏌️⛳

[View Setup Guide](SETUP.md) | [Report Issue](../../issues)
