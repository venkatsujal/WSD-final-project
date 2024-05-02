import sqlite3
import json
conn = sqlite3.connect("db.sqlite")
curr = conn.cursor()

curr.execute("""
             CREATE TABLE customers(
             id INTEGER PRIMARY KEY,
             name CHAR(64),
             phone CHAR(10)
             );
             """
             )




curr.execute(
    """
    CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name CHAR(64),
    price REAL
    );
"""
)


curr.execute(
    """
CREATE TABLE orders (
id INTEGER PRIMARY KEY,
notes TEXT,
cust_id INTEGER,
timestamp INTEGER,
FOREIGN KEY(cust_id) REFERENCES customers(id)
);
"""
)


curr.execute(
    """
    CREATE TABLE order_list(
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    item_id INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
"""
)

with open('example_orders.json') as file:
    order_list = json.load(file)

orders = []
customers = {}
items = {}
for order in order_list:
    customers[order["phone"]] = order["name"]
    for item in order["items"]:
        items[item["name"]] = item["price"]
for phone, name in customers.items():
    curr.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))

curr.execute("SELECT * FROM customers;")
print("Customers:")
print(curr.fetchall())

for name, price in items.items():
    curr.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))

for order in order_list:
    curr.execute("SELECT id FROM customers WHERE phone=?;", (order["phone"],))
    cust_id = curr.fetchone()[0]
    curr.execute("INSERT INTO orders (notes, timestamp, cust_id) VALUES (?, ?, ?);",
                 (order["notes"], order["timestamp"], cust_id))
    order_id = curr.lastrowid
    for item in order["items"]:
        curr.execute("SELECT id FROM items WHERE name=?;", (item["name"],))
        item_id = curr.fetchone()[0]
        curr.execute("INSERT INTO order_list (order_id, item_id) VALUES (?, ?);", 
                     (order_id, item_id))


conn.commit()
conn.close()
