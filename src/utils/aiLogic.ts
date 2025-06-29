interface AIResponse {
  reply: string;
  customerName?: string;
}

// Regex patterns for parsing
const ORDER_ID_PATTERN = /#(\d+)/;
const NAME_PATTERN = /i am (\w+)|my name is (\w+)|this is (\w+)/i;

export function generateAIResponse(userMessage: string, customerName?: string): AIResponse {
  const lowerMsg = userMessage.toLowerCase();

  // Extract and remember customer name
  const nameMatch = NAME_PATTERN.exec(userMessage);
  if (nameMatch && !customerName) {
    customerName = nameMatch[1] || nameMatch[2] || nameMatch[3];
  }

  // Extract or generate order ID
  const orderMatch = ORDER_ID_PATTERN.exec(userMessage);
  const orderId = orderMatch ? orderMatch[1] : Math.floor(Math.random() * 90000 + 10000).toString();

  // Telugu greeting response
  if (['namaste', 'వన్నక్కం', 'వన్‌నక్కం', 'నమస్తే'].some(term => lowerMsg.includes(term))) {
    return {
      reply: `నమస్తే ${customerName || 'garu'} 😊 QuickKart Support AI ఇక్కడ! మీ order గురించి ఏమైనా సమస్య ఉందా?`,
      customerName
    };
  }

  // Order tracking
  if (['track', 'order', 'delivery', '#'].some(keyword => lowerMsg.includes(keyword))) {
    const eta = new Date(Date.now() + Math.random() * 240 * 60000 + 30 * 60000);
    return {
      reply: `I've checked your order #${orderId} 📦\n\nStatus: Out for delivery\nETA: ${eta.toLocaleTimeString()} today\nLocation: 2.5 km away\n\nYour delivery partner will call you 10 minutes before arrival. Track live: quickkart.in/track/${orderId}`,
      customerName
    };
  }

  // Late/delayed delivery
  if (['late', 'delay', 'slow'].some(keyword => lowerMsg.includes(keyword))) {
    return {
      reply: `I understand late deliveries can be frustrating ${customerName || 'Sir/Madam'} 😊\n\n• Checked with delivery partner - minor traffic delay\n• Your order is now priority flagged\n• Expected within next 30 minutes\n• ₹50 courtesy credit added to your account\n\nI'll personally monitor this delivery. Is there anything else I can help with?`,
      customerName
    };
  }

  // Wrong/damaged items
  if (['wrong', 'damaged', 'broken', 'different'].some(keyword => lowerMsg.includes(keyword))) {
    const ticketId = Math.floor(Math.random() * 9000 + 1000);
    return {
      reply: `I sincerely apologize for this inconvenience!\n\n✅ Immediate replacement initiated\n✅ New order will arrive within 2 hours\n✅ Return pickup scheduled for damaged item\n✅ No additional charges\n\nTicket #TK${ticketId} created. You'll receive SMS updates. Anything else I can assist with?`,
      customerName
    };
  }

  // Refund requests
  if (['refund', 'money back', 'cancel'].some(keyword => lowerMsg.includes(keyword))) {
    const amount = Math.floor(Math.random() * 500 + 200);
    const refundId = Math.floor(Math.random() * 90000 + 10000);
    return {
      reply: `I'll process your refund request immediately!\n\n• Refund amount: ₹${amount}\n• Processing time: 3-5 business days\n• Refund to original payment method\n• Confirmation SMS sent\n\nRefund ID: RF${refundId}\n\nIs there anything specific that went wrong? Your feedback helps us improve.`,
      customerName
    };
  }

  // Escalation requests
  if (['manager', 'senior', 'escalate', 'complaint'].some(keyword => lowerMsg.includes(keyword))) {
    const escalationId = Math.floor(Math.random() * 9000 + 1000);
    return {
      reply: `I understand you'd like to speak with a senior executive.\n\n✅ Escalation ticket created: ES${escalationId}\n✅ Priority callback scheduled within 1 hour\n✅ Senior Manager: Priya Sharma will contact you\n✅ Direct line: +91-80-4567-8900\n\nYou'll receive a confirmation call shortly. Is there anything urgent I can help with right now?`,
      customerName
    };
  }

  // General help
  if (['help', 'support', 'problem'].some(keyword => lowerMsg.includes(keyword))) {
    return {
      reply: `I'm here to help! Here are the most common things I can assist with:\n\n📦 Order tracking & delivery status\n🔄 Returns, refunds & exchanges\n⏱️ Delivery time updates\n🛒 Order modifications\n💳 Payment & billing queries\n📱 App & website support\n\nWhat specific issue are you facing today?`,
      customerName
    };
  }

  // Payment issues
  if (['payment', 'charged', 'money', 'amount'].some(keyword => lowerMsg.includes(keyword))) {
    const amount = Math.floor(Math.random() * 800 + 200);
    const reference = Math.floor(Math.random() * 900000 + 100000);
    return {
      reply: `I can help you with payment concerns!\n\nFor your security, I can see only the last 4 digits of your payment method.\n\n• Recent transaction: ₹${amount}\n• Status: Processed successfully\n• Reference: PAY${reference}\n\nIf you see any unauthorized charges, I can initiate a dispute right away. What specific payment issue are you experiencing?`,
      customerName
    };
  }

  // Default responses
  const defaultResponses = [
    "Thank you for contacting QuickKart! I'm here to help with any delivery, order, or service questions you might have 😊",
    "I'd be happy to assist you! Could you please share your order number or describe the issue you're experiencing?",
    "Great question! Let me help you with that. For faster service, you can also share your order ID if this is about a specific delivery.",
    "I'm here to make sure you have the best QuickKart experience! What can I help you with today?"
  ];
  
  return {
    reply: defaultResponses[Math.floor(Math.random() * defaultResponses.length)],
    customerName
  };
}