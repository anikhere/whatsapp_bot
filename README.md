# 🤖 Flavors Kitchen WhatsApp Bot

AI-powered WhatsApp bot helping small restaurants take orders and generate business analytics.

## 📋 Problem Statement
Small restaurants use WhatsApp for orders but have:
- ❌ No order tracking
- ❌ No sales analytics
- ❌ No customer insights
- ❌ Manual order processing

## 💡 Solution
Automated WhatsApp bot that:
- ✅ Takes orders via natural conversation
- ✅ Stores data in database (coming Day 2-3)
- ✅ Generates business analytics (coming Day 4-5)
- ✅ Provides actionable insights

## 🎯 Real Client
Built for **Flavors Kitchen** - a local restaurant in Godhra, Gujarat.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Messaging**: Twilio WhatsApp API
- **Database**: PostgreSQL (coming soon)
- **Analytics**: Streamlit (coming soon)
- **Deployment**: ngrok (dev), Render/Railway (production - coming soon)

---

## ✅ Progress Tracker

### Day 1 - Bot Foundation ✅ COMPLETE
- [x] Project structure setup
- [x] Twilio WhatsApp sandbox integration
- [x] Flask webhook handling messages
- [x] Intelligent response logic:
  - Greetings & help
  - Menu display
  - Catering inquiries
  - Order confirmations
- [x] Tested successfully with real WhatsApp messages

**Demo:** Bot processes orders like "2 momos and 1 thali" and confirms receipt.

### Day 2-3 - Database & Order Parsing (IN PROGRESS)
- [ ] PostgreSQL database setup
- [ ] Order parsing with NLP/regex
- [ ] Store orders with customer info & timestamps
- [ ] Query orders via bot commands

### Day 4-5 - Analytics Dashboard
- [ ] Streamlit dashboard
- [ ] Daily revenue charts
- [ ] Popular items analysis
- [ ] Peak hours heatmap
- [ ] Customer frequency tracking

### Day 6-7 - Real Business Testing
- [ ] Deploy for restaurant owner
- [ ] Collect real orders for 3-5 days
- [ ] Gather feedback
- [ ] Iterate on UX

### Day 8-10 - Production & Polish
- [ ] Deploy to production (Render/Railway)
- [ ] Automated daily reports
- [ ] Documentation & video demo
- [ ] Blog post about learnings

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Twilio account (free trial)
- ngrok account (free)

### Installation
```bash
# Clone repository
git clone https://github.com/anikhere/whatsapp-business-bot.git
cd whatsapp-business-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Twilio credentials
```

### Running the Bot
```bash
# Terminal 1: Start Flask
python src/app.py

# Terminal 2: Start ngrok
ngrok http 5000

# Copy ngrok URL and configure in Twilio Sandbox Settings:
# https://YOUR-NGROK-URL.ngrok-free.app/webhook
```

### Testing

Send WhatsApp messages to Twilio sandbox number:
- "hello" → Get welcome message
- "menu" → See full menu
- "2 momos" → Place order
- "catering" → Get catering info

---

## 📝 Day 1 Learnings

### What Worked Well:
- Twilio WhatsApp API is straightforward to integrate
- Flask webhooks are perfect for this use case
- Natural language keywords work better than rigid commands

### Challenges Faced:
- **ngrok URLs expire**: Need to update Twilio webhook after every restart
- **Sandbox limitations**: 24-hour session windows, can't customize branding
- **Path issues in PowerShell**: Folder names with spaces broke commands (use quotes!)

### Key Insights:
- Real client problems > tutorial datasets
- Building for your uncle's restaurant = portfolio gold
- Small businesses genuinely need this solution

---

## 🎬 Demo

**WhatsApp Conversation:**
```
User: hello
Bot: 👋 Welcome to Flavors Kitchen!
     Your friendly neighbourhood place for delicious meals...

User: menu
Bot: 📋 Flavors Kitchen Menu Categories:
     🍟 Snacks: Momos, Rolls, Samosa...

User: 2 momos and 1 veg thali
Bot: 🧾 Order Received at Flavors Kitchen!
     You ordered: 2 momos and 1 veg thali
     👍 Thank you! Your order is being processed.
```

---

## 📊 Planned Features

### v1.0 (Current)
- Basic order taking
- Menu display
- Order confirmations

### v2.0 (Week 2)
- Database storage
- Order history
- Customer analytics

### v3.0 (Week 3)
- Automated reports
- Inventory alerts
- Multi-restaurant support

---

## 🤝 Contributing

This is a learning project built in public. Feedback welcome!

---

## 📄 License

MIT

---

## 👨‍💻 Author

**Taha Anik**
- GitHub: [@anikhere](https://github.com/anikhere)
- LinkedIn: [Taha Anik](https://linkedin.com/in/taha-anik-56ba7531b)
- Building this as part of my journey to become an ML Engineer

---

## 🙏 Acknowledgments

- Built for **Flavors Kitchen** - real restaurant, real impact
- Inspired by the need to help small businesses leverage technology
- Part of my 10-day project sprint to land an ML internship

---

**⭐ Star this repo if you find it useful!**

**📹 Following the journey? Check out my [YouTube](#) for daily updates**