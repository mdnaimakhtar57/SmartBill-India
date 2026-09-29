import sqlite3
from datetime import datetime

# Database Setup (Mobile me bhi data safe rahega)
def init_db():
    conn = sqlite3.connect('dukan_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            bill_no INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_phone TEXT,
            grand_total REAL,
            date_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_next_bill_no():
    conn = sqlite3.connect('dukan_records.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(bill_no) FROM bills")
    row = cursor.fetchone()
    conn.close()
    return (row[0] + 1) if row[0] else 1

def save_to_db(name, phone, total, date_time):
    conn = sqlite3.connect('dukan_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bills (customer_name, customer_phone, grand_total, date_time)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, total, date_time))
    conn.commit()
    conn.close()

def start_billing():
    init_db()
    print("=========================================")
    print(" 🏪 APNI DUKAN MOBILE BILLING SYSTEM ")
    print("=========================================\n")
    
    cust_name = input("Customer Name (Enter dabayein agar khali chorna hai): ") or "Cash Customer"
    cust_phone = input("Customer Phone (Enter dabayein agar khali chorna hai): ") or "N/A"
    
    cart = []
    
    while True:
        print("\n--- ITEM ADD KAREIN ---")
        item_name = input("Item ka Naam (Ya bill khatam karne ke liye 'done' likhein): ")
        if item_name.lower() == 'done':
            break
            
        if not item_name:
            print("❌ Item ka naam khali nahi ho sakta!")
            continue
            
        try:
            price = float(input("Item ki Price (₹): "))
            qty = int(input("Quantity (Kitna pieces): "))
            gst_pct = float(input("GST % (0, 5, 12, 18, 28): ") or 0)
        except ValueError:
            print("❌ Sahi number daalein! Price aur Qty galat hai.")
            continue
            
        # Calculation Formula
        sub_total = price * qty
        gst_amount = (sub_total * gst_pct) / 100
        total_item_cost = sub_total + gst_amount
        
        cart.append({
            "name": item_name, "price": price, "qty": qty,
            "gst_pct": gst_pct, "total": total_item_cost
        })
        print(f"✅ {item_name} Cart me add ho gaya!")

    if not cart:
        print("\n🛒 Cart khali hai. Koi bill nahi bana.")
        return

    # Total Invoice Generation
    bill_no = get_next_bill_no()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    grand_total = sum(item["total"] for item in cart)
    
    # Database me save karein
    save_to_db(cust_name, cust_phone, grand_total, now)
    
    # Mobile Screen par Bill Printout
    print("\n\n=========================================")
    print("              💥 TAX INVOICE 💥           ")
    print("=========================================")
    print(f"Bill No: {bill_no:<10} Date: {now}")
    print(f"Customer: {cust_name}")
    print(f"Phone: {cust_phone}")
    print("-----------------------------------------")
    print(f"{'Item':<15} {'Qty':<4} {'Price':<8} {'Total':<10}")
    print("-----------------------------------------")
    for item in cart:
        print(f"{item['name']:<15} {item['qty']:<4} ₹{item['price']:<7.1f} ₹{item['total']:<10.1f}")
    print("-----------------------------------------")
    print(f"GRAND TOTAL:   ₹{grand_total:.2f}")
    print("=========================================")
    print("        Thank You! Visit Again.          ")
    print("=========================================\n")

if __name__ == "__main__":
    while True:
        start_billing()
        choice = input("Naya Bill banane ke liye Enter dabayein (Bahar nikalne ke liye 'exit' likhein): ")
        if choice.lower() == 'exit':
            print("Dukan Billing System dekhne ke liye Shukriya, Bhai!")
            break
