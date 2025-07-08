import requests
from bs4 import BeautifulSoup
import smtplib

# Product URL (change this to your product)
URL = "https://www.amazon.com/dp/B0C6V36H8L"  # Example product URL

# Your desired price (in your currency)
TARGET_PRICE = 400.00

# Headers to simulate a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

# Function to check the price
def check_price():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the product title and price
    title = soup.find(id="productTitle").get_text().strip()

    # Handle price formats
    try:
        price = soup.find("span", class_="a-offscreen").get_text()
        price = float(price.replace("₹", "").replace("$", "").replace(",", "").strip())
    except:
        print("❌ Could not find the price.")
        return

    print(f"🛒 {title}\nCurrent Price: {price}")

    # Compare with target price
    if price < TARGET_PRICE:
        send_email(title, price)

# Function to send email
def send_email(product_title, price):
    sender_email = "youremail@gmail.com"
    sender_password = "yourpassword"
    receiver_email = "receiver@gmail.com"

    subject = "📉 Amazon Price Alert!"
    body = f"The price for '{product_title}' dropped to {price}.\nCheck it here: {URL}"

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)
            print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)

# Run the checker
check_price()
