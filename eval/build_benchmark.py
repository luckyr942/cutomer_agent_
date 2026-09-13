# Golden Benchmark Dataset Generator (150 Hand-Labelled / Structured Samples)
# Fulfills Hiver assignment requirement for 150-250 benchmark samples.

import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import BENCHMARK_SET_PATH

# 150 Labeled Benchmark Samples
BENCHMARK_SAMPLES = [
    # --- 1. DELIVERY DELAY (35 Samples) ---
    {"customer_text": "My package was supposed to arrive yesterday but tracking has not updated. Where is order #12345?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Where is my shipment? It has been stuck in transit for 5 days.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "My tracking number says delivered but I haven't received my box.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Order #99214 status says out for delivery since 8 AM, still not here.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Why is my package delayed? Delivery date keeps changing.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "trackin says packeg delivrd yesterday but i havnt recived anything yet", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Item not received yet. Order ID: 44210", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "My package is lost in transit. Who do I contact?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Estimated delivery was 2 days ago, still no package.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Can you check the delivery status of my parcel?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Where is my package? Carrier says pending.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "I ordered 3 days ago with expedited shipping and it hasn't shipped yet.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "My package is arriving late, need an update ASAP.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Order 10928 tracking link is broken and delivery is delayed.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Package marked delivered to porch but nothing is outside.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Shipment delayed by carrier due to weather. Any revised ETA?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Haven't received dispatch email for my purchase yesterday.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Where is my order? Paid extra for 1-day delivery.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Tracking shows returned to sender by mistake.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "My package is stuck at sorting facility for 4 days.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Can I change my delivery address while package is in transit?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Order #55123 delivery failed attempt notice received.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Parcel status hasn't updated since Monday.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "When will my order ship out?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "My delivery was rescheduled without notifying me.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Package delivered to wrong address down the street.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Still waiting on my package from last week's sale.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Item says delivered to receptionist but we don't have one.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Tracking number 9912048201 shows no scan records.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Why is my order taking so long to deliver?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Package lost by courier, need replacement shipped.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Delivered label added but box never arrived.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Order processing delayed over 48 hours.", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Is there a delay on shipments to NYC this week?", "ground_truth_intent": "delivery_delay", "should_escalate": False},
    {"customer_text": "Where is my gift order #77123?", "ground_truth_intent": "delivery_delay", "should_escalate": False},

    # --- 2. PAYMENT ISSUE (35 Samples - High Risk -> Escalate) ---
    {"customer_text": "I was charged twice for my subscription this month! $14.99 deducted two times.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "My payment got stucked i din't recieved refund yet", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Why did you charge my credit card again without permission?", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "I requested a refund 10 days ago and money is still not in my bank.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Double deduction on order #44123, fix this immediately.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "why u chargd me again i already canceld my subscrip last mnth", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Payment failed but money was deducted from my account.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Charged $49.99 for a order I cancelled.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Where is my refund for returned order #88123?", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Billing error on my latest invoice, overcharged by $20.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "I see an unfamiliar charge from your site on my statement.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Promo code didn't apply and I was charged full price.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Refund status says processed but bank hasn't credited it.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Incorrect charge on my monthly membership fee.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "My card was charged 3 times for one transaction error.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Need urgent refund for damaged return item.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Subscription renewed automatically after I opted out.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Payment decline error but bank shows pending charge.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Overcharged tax on my non-taxable order.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Gift card balance deducted but order failed.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Unauthorized charge of $99 on my account statement.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Why was I charged a restocking fee on defective item?", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Refund issued to expired debit card, need it redirected.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Charged twice for shipping fees on single order.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Money debited from wallet but order status is unconfirmed.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Cancel charge on my account immediately.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Billing system error charged me twice.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Still waiting on $35 refund from last month.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Card charged without OTP confirmation.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "I was double billed for my Prime renewal.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Subscription fee charged after free trial cancelled.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Where is my store credit refund?", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Payment pending for 48 hours and amount locked.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Wrong amount billed on my receipt #11029.", "ground_truth_intent": "payment_issue", "should_escalate": True},
    {"customer_text": "Issue refund to my original payment method please.", "ground_truth_intent": "payment_issue", "should_escalate": True},

    # --- 3. PRODUCT DEFECT (30 Samples) ---
    {"customer_text": "My iPhone screen keeps freezing after the latest iOS update.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "The charger I bought caught fire and burned my desk!", "ground_truth_intent": "product_defect", "should_escalate": True}, # Safety hazard
    {"customer_text": "The app keeps crashing every time I open settings.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "The blender I received won't turn on.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Screen has green lines running across display after 2 days of use.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Headphones speaker distorted on left ear.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Laptop battery swelling and overheating dangerously.", "ground_truth_intent": "product_defect", "should_escalate": True}, # Safety hazard
    {"customer_text": "Camera app gives black screen error on startup.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Item arrived broken with cracked glass.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Bluetooth keeps disconnecting every 5 minutes.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Power button stuck and un-pressable.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Software update bricked my device, won't boot up.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Device emitting burnt plastic smell while charging.", "ground_truth_intent": "product_defect", "should_escalate": True}, # Safety hazard
    {"customer_text": "Touchscreen unresponsive on bottom half.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Microphone not picking up any sound during calls.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Smart watch sensor stopped tracking heart rate.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Received defective unit, power port loose.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Keyboard keys sticking and typing double letters.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "WiFi chip malfunction, cannot connect to any router.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Monitor screen flickering constantly.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Earbuds charging case not holding charge.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "App crash loop after logging in.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Speaker crackling noise at high volume.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Hardware defect on brand new unit.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Tablet battery drains from 100% to 0% in 20 minutes.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Device gets extremely hot to touch while playing video.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Defective hinge broke on laptop lid.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Product arrived missing essential power cable.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Firmware error code 403 on startup.", "ground_truth_intent": "product_defect", "should_escalate": False},
    {"customer_text": "Buttons non-functional right out of the box.", "ground_truth_intent": "product_defect", "should_escalate": False},

    # --- 4. GENERAL INQUIRY (25 Samples) ---
    {"customer_text": "What are your customer support store hours on weekends?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I update my profile shipping address?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Can you confirm my order status for the first time?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "What is the return policy for electronics?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I redeem my promo code at checkout?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Is international shipping available to Canada?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I change my account password?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Where can I find warranty details for my purchase?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "What payment methods do you accept?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How to cancel a subscription before next billing cycle?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Do you offer student discounts?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How can I contact customer service phone support?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "What is the maximum weight limit for standard shipping?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I track multiple items in one order?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Are gift wrapping options available?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How to delete my account data permanently?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "What time does Cyber Monday sale start?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I download my order tax invoice PDF?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Can I add items to an existing order before it ships?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do trade-in credit programs work?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Is signature required upon package delivery?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How do I leave seller feedback?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "Where is the nearest physical drop-off location?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "What is the policy for price matching?", "ground_truth_intent": "general_inquiry", "should_escalate": False},
    {"customer_text": "How to update email notification preferences?", "ground_truth_intent": "general_inquiry", "should_escalate": False},

    # --- 5. OTHER & SAFETY TRIGGERS (25 Samples -> Escalate Safety) ---
    {"customer_text": "Someone made an unauthorized order on my account, I think I was hacked.", "ground_truth_intent": "other", "should_escalate": True}, # Safety ATO
    {"customer_text": "I am filing a lawsuit with my attorney if this isn't resolved today.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Legal
    {"customer_text": "Hello, good morning!", "ground_truth_intent": "other", "should_escalate": False},
    {"customer_text": "Great service, thanks!", "ground_truth_intent": "other", "should_escalate": False},
    {"customer_text": "I will contact consumer court if I don't get a response.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Legal
    {"customer_text": "My account was hacked and card used without my knowledge.", "ground_truth_intent": "other", "should_escalate": True}, # Safety ATO
    {"customer_text": "Delivery driver stole package from porch, caught on camera.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Incident
    {"customer_text": "Filing a police report for fraudulent transactions.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Legal
    {"customer_text": "Disputing this chargeback with my bank immediately.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Financial
    {"customer_text": "Product exploded in my hand causing injury.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Hazard
    {"customer_text": "Hi there team!", "ground_truth_intent": "other", "should_escalate": False},
    {"customer_text": "Reporting fake counterfeit medicine delivered to me.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Hazard
    {"customer_text": "Filing complaint with FTC and BBB tomorrow.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Legal
    {"customer_text": "Driver damaged my driveway gate during delivery.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Incident
    {"customer_text": "Identity theft issue on my linked payment card.", "ground_truth_intent": "other", "should_escalate": True}, # Safety ATO
    {"customer_text": "Stolen card used to buy digital gift cards on your site.", "ground_truth_intent": "other", "should_escalate": True}, # Safety ATO
    {"customer_text": "Just saying thanks for quick resolution!", "ground_truth_intent": "other", "should_escalate": False},
    {"customer_text": "I suspect bank fraud on my recent orders.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Financial
    {"customer_text": "Received expired food product, made my child sick.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Hazard
    {"customer_text": "Legal action will be taken if refund isn't issued.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Legal
    {"customer_text": "Have a nice day!", "ground_truth_intent": "other", "should_escalate": False},
    {"customer_text": "Unauthorized log in attempt detected on my profile.", "ground_truth_intent": "other", "should_escalate": True}, # Safety ATO
    {"customer_text": "Reporting driver harassment during parcel handoff.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Incident
    {"customer_text": "Electric shock from faulty appliance charger.", "ground_truth_intent": "other", "should_escalate": True}, # Safety Hazard
    {"customer_text": "Testing 1 2 3 hello", "ground_truth_intent": "other", "should_escalate": False}
]

def benchmark_build_set():
    """Generates benchmark_set.csv with 150 ground-truth samples."""
    BENCHMARK_SET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(BENCHMARK_SAMPLES)
    df.to_csv(BENCHMARK_SET_PATH, index=False)
    print(f"✅ Generated Golden Benchmark set with {len(df)} samples at:\n   {BENCHMARK_SET_PATH}")

if __name__ == "__main__":
    benchmark_build_set()