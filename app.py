from flask import Flask, render_template, request, url_for, redirect, session
from models import db, Product, init_db, get_all_products, get_products_by_ids

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'contraseña_inicial'
db.init_app(app)
init_db(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('Mainpage.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    selected_products = request.form.getlist('product')
    cart = session.get('cart', {})
    if not cart:
        cart = {}
    for product_id in selected_products:
        cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    print(session.get('cart', []))
    cart_products = session.get('cart', [])
    products = get_products_by_ids(cart_products)
    print(products)
    return render_template('cart.html', products=products)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    del session['cart'][product_id]
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    total_price = request.args.get('total_price', type=float)
    return render_template('checkout.html', total_price=total_price)


@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    # retrieve cart from session
    cart = session.get('cart', {})

    # update inventory for each item in the cart
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        product.quantity -= quantity

    # clear the cart
    session['cart'] = {}

    # save changes to the database
    db.session.commit()

    # simulate a successful payment
    payment_result = True
    order_id = '12345'

    if payment_result:
        # Clear the cart after successful payment
        session.pop('cart', None)
        return render_template('success.html', order_id=order_id)
    else:
        return render_template('error.html', message="Payment failed. Please try again.")


if __name__ == "__main__":
    app.run(debug=True)
