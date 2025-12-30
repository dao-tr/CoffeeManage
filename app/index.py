import math

from unicodedata import category

from app import app, login
from flask import render_template, request, redirect, url_for, session, jsonify
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from app.models import UserRole


@app.route("/")
def home():
    category_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)

    products = utils.read_products(category_id=category_id, kw=kw, page=int(page))
    counter = utils.count_products()
    return render_template('index.html',
                           products=products,
                           category_id=category_id,
                           pages=math.ceil(counter/app.config['PAGE_SIZE']),
                           page=int(page))

@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('signin'))
            else:
                err_msg = "Mật khẩu không khớp."
        except Exception as ex:
            err_msg = "Nhập lại." + str(ex)

    return render_template('register.html', err_msg=err_msg)

@app.route("/login", methods=['get', 'post'])
def signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_login(username=username, password=password)
            if user:
                login_user(user=user)

                next = request.args.get('next', 'home')
                return redirect(url_for(next))
            else:
                err_msg = "Sai tài khoản hoặc mật khẩu"
        except Exception as ex:
            err_msg = str(ex)

    return render_template('login.html', err_msg=err_msg)

@app.route("/admin-login", methods=['post'])
def signin_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

        return redirect('/admin')

    return redirect('/admin')

@app.route("/logout")
def signout():
    logout_user()
    return redirect(url_for('home'))


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')


@app.route("/history")
@login_required
def history():
    if current_user.is_authenticated:
        my_receipts = sorted(current_user.receipts, key=lambda x: x.created_date, reverse=True)
    else:
        my_receipts = []

    return render_template('history.html', receipts=my_receipts)

@app.route("/products")
def product_list():
    category_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.read_products(category_id=category_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('products.html', products=products)

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    products = utils.get_product_by_id(product_id)

    return render_template('product_detail.html', product=products)


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart', {})

    # 1. Tính tổng số lượng hiện tại của TẤT CẢ sản phẩm trong giỏ
    current_total_quantity = sum(item['quantity'] for item in cart.values())

    if current_total_quantity + 1 > 10:
        # Trả về lỗi nhưng VẪN KÈM thống kê giỏ hàng (để tránh lỗi NaN/undefined ở frontend)
        response_data = utils.count_cart(cart)
        response_data['code'] = 400
        response_data['msg'] = 'Tổng số lượng sản phẩm trong giỏ không được vượt quá 10!'
        return jsonify(response_data)

    # 3. Nếu chưa vượt quá 10 thì thêm vào giỏ
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    response_data = utils.count_cart(cart)
    response_data['code'] = 200
    return jsonify(response_data)


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    try:
        new_quantity = int(data.get('quantity'))
    except ValueError:
        new_quantity = 0

    cart = session.get('cart', {})

    if id in cart:
        current_total_quantity = sum(item['quantity'] for item in cart.values())
        old_quantity = cart[id]['quantity']

        # tính tổng số lượng mới nếu cập nhật
        expected_total = current_total_quantity - old_quantity + new_quantity

        #Kiểm tra giới hạn tổng 10 món
        if expected_total > 10:
            response_data = utils.count_cart(cart)
            response_data['code'] = 400
            response_data['msg'] = 'Tổng số lượng sản phẩm không được vượt quá 10!'
            # Trả về số lượng cũ để JS có thể khôi phục ô input
            response_data['data'] = {'old_quantity': old_quantity}
            return jsonify(response_data)

        #Cập nhật nếu hợp lệ
        if new_quantity > 0:
            cart[id]['quantity'] = new_quantity

        session['cart'] = cart

    response_data = utils.count_cart(cart)
    response_data['code'] = 200
    return jsonify(response_data)


@app.route("/cart")
def cart():
    return render_template('cart.html',
                   stats=utils.count_cart(session.get('cart')))

@app.route("/api/pay", methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})


    return jsonify({'code': 200})


if __name__ == '__main__':
    from app.admin import *

    app.run(debug=True)