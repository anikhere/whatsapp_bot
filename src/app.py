from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from db import get_db     # <-- ADD THIS


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint for Twilio WhatsApp messages.
    """
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    # SAVE MESSAGE INTO DATABASE
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO whatsapp_messages (sender, message)
            VALUES (%s, %s)
        """, (sender, incoming_msg))
        conn.commit()
        cur.close()
        conn.close()
        print("💾 Message saved to DB")
    except Exception as e:
        print("❌ DB Error:", e)

    
    
    print(f"📩 Received from {sender}: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()

    text = incoming_msg.lower()

    # GREETING
    if any(word in text for word in ['hi', 'hello', 'hey', 'namaste', 'hii']):
        msg.body(
            "👋 Welcome to **Flavors Kitchen!**\n"
            "Your friendly neighbourhood place for delicious meals, snacks, diet food, and catering orders.\n\n"
            "How can I assist you today?\n\n"
            "You can ask for:\n"
            "• 🍽️ Meals Menu\n"
            "• 🍟 Snacks\n"
            "• 🥗 Diet Food\n"
            "• 🎉 Catering Orders\n\n"
            "Or simply type your order (example: *2 plate momos and 1 veg thali*)."
        )

    # HELP
    elif any(word in text for word in ['help', 'how', 'use', 'guide']):
        msg.body(
            "🛟 **Here’s how I can help you at Flavors Kitchen:**\n\n"
            "👉 *Place an order:* Just type what you want.\n"
            "   _Example:_ 2 paneer rolls and 1 diet bowl\n\n"
            "👉 *See menu categories:* Send 'menu'\n"
            "👉 *Ask catering details:* Send 'catering'\n"
            "👉 *Track order:* (Coming soon!)\n"
            "👉 *Know today’s specials:* Send 'specials'\n\n"
            "I'm here to make your ordering experience smooth and easy. 😊"
        )

    # MENU
    elif any(word in text for word in ['menu', 'items', 'food']):
        msg.body(
            "📋 **Flavors Kitchen Menu Categories:**\n\n"
            "🍟 *Snacks:* Momos, Rolls, Samosa, Fries, Sandwiches\n"
            "🥗 *Diet Food:* Oats Bowl, Sprouts, Salad Box, Low-Calorie Meals\n"
            "🍽️ *Meals:* Veg Thali, Chicken Thali, Biryani, Dal Rice, Roti Sabzi\n"
            "🎉 *Catering:* Bulk orders for parties, office events, and family gatherings\n\n"
            "Tell me what you'd like to order. 😊"
        )

    # CATERING
    elif "cater" in text or "party" in text or "bulk" in text:
        msg.body(
            "🎉 **Flavors Kitchen Catering Service**\n\n"
            "We provide catering for:\n"
            "• Birthday Parties\n"
            "• Office Events\n"
            "• Home Gatherings\n"
            "• Special Occasions\n\n"
            "🍱 *Price Range:* Custom based on quantity\n"
            "📦 *Minimum Order:* 10 plates\n\n"
            "Please tell me:\n"
            "• Number of people\n"
            "• Veg / Non-veg preference\n"
            "• Event date\n\n"
            "I'll help you with the perfect catering plan!"
        )

    # TODAYS SPECIALS
    elif "special" in text or "today" in text:
        msg.body(
            "⭐ **Today's Specials at Flavors Kitchen:**\n\n"
            "🍛 Special Veg Thali – ₹99\n"
            "🔥 Paneer Tikka Roll – ₹79\n"
            "🥗 Diet Protein Bowl – ₹89\n"
            "🍗 Chicken Masala Meal – ₹149\n\n"
            "Want to order anything from specials?"
        )

    # EMPTY MESSAGE
    elif not incoming_msg:
        msg.body(
            "👋 Hello! Welcome to **Flavors Kitchen.**\n"
            "Please type your order or send 'menu' to explore options."
        )

    # DEFAULT: Treat any text as an order
    else:
        msg.body(
            f"🧾 **Order Received at Flavors Kitchen!**\n\n"
            f"You ordered: *{incoming_msg}*\n\n"
            "👍 Thank you! Your order is being processed.\n"
            "🔄 (Order tracking and database integration coming soon!)"
        )
    
    print(f"📤 Sending reply...")
    return str(resp)


@app.route('/test', methods=['GET'])
def test():
    return {
        "status": "running",
        "message": "Flavors Kitchen Bot is alive! 🤖",
        "webhook_url": "/webhook"
    }

@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Flavors Kitchen WhatsApp Bot</h1>
    <p>Bot is running! ✅</p>
    <p>Webhook endpoint: <code>/webhook</code></p>
    """

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
