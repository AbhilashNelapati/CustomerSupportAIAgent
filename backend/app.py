from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
import re

app = FastAPI(title="QuickKart Support AI Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_message: str
    customer_name: str | None = None

class ChatResponse(BaseModel):
    reply: str
    customer_name: str | None = None

# Regex patterns for parsing
ORDER_ID_PATTERN = re.compile(r"#(\d+)")
NAME_PATTERN = re.compile(r"i am (\w+)|my name is (\w+)|this is (\w+)", re.I)

def generate_ai_response(user_message: str, customer_name: str | None) -> tuple[str, str | None]:
    """Generate AI response based on user message and context"""
    lower_msg = user_message.lower()

    # Extract and remember customer name
    name_match = NAME_PATTERN.search(user_message)
    if name_match and not customer_name:
        customer_name = next(filter(None, name_match.groups()))

    # Extract or generate order ID
    order_match = ORDER_ID_PATTERN.search(user_message)
    order_id = order_match.group(1) if order_match else str(random.randint(10000, 99999))

    # Telugu greeting response
    if any(term in lower_msg for term in ["namaste", "వన్నక్కం", "వన్‌నక్కం", "నమస్తే"]):
        reply = f"నమస్తే {customer_name or 'garu'} 😊 QuickKart Support AI ఇక్కడ! మీ order గురించి ఏమైనా సమస్య ఉందా?"
        return reply, customer_name

    # Order tracking
    if any(keyword in lower_msg for keyword in ["track", "order", "delivery", "#"]):
        eta = datetime.now() + timedelta(minutes=random.randint(30, 240))
        reply = (
            f"I've checked your order #{order_id} 📦\n\n"
            f"Status: Out for delivery\n"
            f"ETA: {eta.strftime('%I:%M %p')} today\n"
            f"Location: 2.5 km away\n\n"
            f"Your delivery partner will call you 10 minutes before arrival. "
            f"Track live: quickkart.in/track/{order_id}"
        )
        return reply, customer_name

    # Late/delayed delivery
    if any(keyword in lower_msg for keyword in ["late", "delay", "slow"]):
        reply = (
            f"I understand late deliveries can be frustrating {customer_name or 'Sir/Madam'} 😊\n\n"
            "• Checked with delivery partner - minor traffic delay\n"
            "• Your order is now priority flagged\n"
            "• Expected within next 30 minutes\n"
            "• ₹50 courtesy credit added to your account\n\n"
            "I'll personally monitor this delivery. Is there anything else I can help with?"
        )
        return reply, customer_name

    # Wrong/damaged items
    if any(keyword in lower_msg for keyword in ["wrong", "damaged", "broken", "different"]):
        ticket_id = random.randint(1000, 9999)
        reply = (
            "I sincerely apologize for this inconvenience!\n\n"
            "✅ Immediate replacement initiated\n"
            "✅ New order will arrive within 2 hours\n"
            "✅ Return pickup scheduled for damaged item\n"
            "✅ No additional charges\n\n"
            f"Ticket #TK{ticket_id} created. You'll receive SMS updates. "
            "Anything else I can assist with?"
        )
        return reply, customer_name

    # Refund requests
    if any(keyword in lower_msg for keyword in ["refund", "money back", "cancel"]):
        amount = random.randint(200, 700)
        refund_id = random.randint(10000, 99999)
        reply = (
            "I'll process your refund request immediately!\n\n"
            f"• Refund amount: ₹{amount}\n"
            "• Processing time: 3-5 business days\n"
            "• Refund to original payment method\n"
            "• Confirmation SMS sent\n\n"
            f"Refund ID: RF{refund_id}\n\n"
            "Is there anything specific that went wrong? Your feedback helps us improve."
        )
        return reply, customer_name

    # Escalation requests
    if any(keyword in lower_msg for keyword in ["manager", "senior", "escalate", "complaint"]):
        escalation_id = random.randint(1000, 9999)
        reply = (
            "I understand you'd like to speak with a senior executive.\n\n"
            f"✅ Escalation ticket created: ES{escalation_id}\n"
            "✅ Priority callback scheduled within 1 hour\n"
            "✅ Senior Manager: Priya Sharma will contact you\n"
            "✅ Direct line: +91-80-4567-8900\n\n"
            "You'll receive a confirmation call shortly. "
            "Is there anything urgent I can help with right now?"
        )
        return reply, customer_name

    # General help
    if any(keyword in lower_msg for keyword in ["help", "support", "problem"]):
        reply = (
            "I'm here to help! Here are the most common things I can assist with:\n\n"
            "📦 Order tracking & delivery status\n"
            "🔄 Returns, refunds & exchanges\n"
            "⏱️ Delivery time updates\n"
            "🛒 Order modifications\n"
            "💳 Payment & billing queries\n"
            "📱 App & website support\n\n"
            "What specific issue are you facing today?"
        )
        return reply, customer_name

    # Payment issues
    if any(keyword in lower_msg for keyword in ["payment", "charged", "money", "amount"]):
        amount = random.randint(200, 1000)
        reference = random.randint(100000, 999999)
        reply = (
            "I can help you with payment concerns!\n\n"
            "For your security, I can see only the last 4 digits of your payment method.\n\n"
            f"• Recent transaction: ₹{amount}\n"
            "• Status: Processed successfully\n"
            f"• Reference: PAY{reference}\n\n"
            "If you see any unauthorized charges, I can initiate a dispute right away. "
            "What specific payment issue are you experiencing?"
        )
        return reply, customer_name

    # Default responses
    default_responses = [
        "Thank you for contacting QuickKart! I'm here to help with any delivery, order, or service questions you might have 😊",
        "I'd be happy to assist you! Could you please share your order number or describe the issue you're experiencing?",
        "Great question! Let me help you with that. For faster service, you can also share your order ID if this is about a specific delivery.",
        "I'm here to make sure you have the best QuickKart experience! What can I help you with today?"
    ]
    
    return random.choice(default_responses), customer_name

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint that processes user messages and returns AI responses"""
    reply, updated_name = generate_ai_response(request.user_message, request.customer_name)
    return ChatResponse(reply=reply, customer_name=updated_name)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "QuickKart Support AI Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)