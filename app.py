from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

product_images = {
    1: 'wilson_raquet.jpg', 2: 'casio.jpg', 3: 'printer_ink.jpg', 4: 'notepad.jpg', 5: 'flashlight.jpg', 6: 'headphones.jpg', 7: 'plant.jpg',
    8: 'airpods.jpg', 9: 'mousepad.jpg', 10: 'n95.jpg', 11: 'red_sox.jpg', 12: 'coke.jpg', 13: 'dishwasher.jpg', 14: 'powerbank.jpg',
    15: 'hdmi.jpg', 16: 'pen.jpg', 17: 'espresso.jpg', 18: 'doormat.jpg', 19: 'milk.jpg', 20: 'wipers.jpg', 21: 'stand.jpg',
    22: 'cat.jpg', 23: 'lamp.jpg', 24: 'surge.jpg', 25: 'mac.jpg', 26: 'pixel.jpg', 27: 'office.jpg', 28: 'target.jpg',
}

def get_last_customer():
    conn = sqlite3.connect('retail_app_canvas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT customer_first_name, customer_last_name, customer_gender, customer_dob FROM customer ORDER BY customer_id DESC LIMIT 1')
    last_customer = cursor.fetchone()
    conn.close()
    return last_customer

def get_product_by_id(product_id):
    conn = sqlite3.connect('retail_app_canvas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    last_customer = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        dob = request.form['dob']
        
        conn = sqlite3.connect('retail_app_canvas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customer (customer_first_name, customer_last_name, customer_gender, customer_dob)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, gender, dob))
        conn.commit()
        conn.close()
        
        last_customer = get_last_customer()
    return render_template('add_customer.html', last_customer=last_customer)

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/get_product', methods=['GET', 'POST'])
def get_product():
    product = None
    image_filename = None
    if request.method == 'POST':
        product_id = request.form['product_id']
        product = get_product_by_id(product_id)
        if product:
            image_filename = product_images.get(int(product_id), 'default.jpg') 
    return render_template('get_products.html', product=product, image_filename=image_filename)

if __name__ == '__main__':
    app.run(debug=True)
