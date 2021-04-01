from bank import app
from flask import render_template, redirect, url_for, flash, request
from bank.models import Tuition, User
# from bank.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from bank.forms import RegisterForm, LoginForm, PayForm, QueryTuitionForm
from bank import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


# @app.route('/bank', methods=['GET', 'POST'])
# @login_required
# def market_page():
#     purchase_form = PurchaseItemForm()
#     selling_form = SellItemForm()
#     if request.method == "POST":
#         #Purchase Item Logic
#         purchased_item = request.form.get('purchased_item')
#         p_item_object = Item.query.filter_by(name=purchased_item).first()
#         if p_item_object:
#             if current_user.can_purchase(p_item_object):
#                 p_item_object.buy(current_user)
#                 flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
#             else:
#                 flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
#         #Sell Item Logic
#         sold_item = request.form.get('sold_item')
#         s_item_object = Item.query.filter_by(name=sold_item).first()
#         if s_item_object:
#             if current_user.can_sell(s_item_object):
#                 s_item_object.sell(current_user)
#                 flash(f"Congratulations! You sold {s_item_object.name} back to bank!", category='success')
#             else:
#                 flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
#
#
#         return redirect(url_for('market_page'))
#
#     if request.method == "GET":
#         items = Item.query.filter_by(owner=None)
#         owned_items = Item.query.filter_by(owner=current_user.id)
#         return render_template('bank.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/bank', methods=['GET', 'POST'])
@login_required
def bank_page():
    pay_form = PayForm()
    if request.method == "POST":
        # Pay Logic
        paid_fee = request.form.get('paid_fee')
        p_fee_object = Tuition.query.filter_by(name=paid_fee).first()
        if p_fee_object:
            if current_user.can_pay(p_fee_object):
                p_fee_object.pay(current_user)
                flash(f"Congratulations! Paid success {p_fee_object.name} for {p_fee_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to pay {p_fee_object.name}!", category='danger')

        return redirect(url_for('bank_page'))

    if request.method == "GET":
        tuitions = Tuition.query.filter_by(id=Tuition.id)
        fees = Tuition.query.filter_by(owner=current_user.id)
        return render_template('bank.html', tuitions=tuitions, pay_form=pay_form, fees=fees)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(id=form.id.data, username=form.username.data, phone=form.phone.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('bank_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(id=form.id.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Email and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

#
# @app.route('/query', methods=['GET', 'POST'])
# @login_required
# def query_tuition_page():
#     form = QueryTuition()
#     if form.validate_on_submit():
#         query_id = User.query.filter_by(id=form.id.data).first()
#         if query_id is not None:
#             return render_template('tuition.html')
#         else:
#             flash('Student ID not found, please try again', category='danger')
#     redirect(url_for('home_page'))
