from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from myapp.app import app, login_manager, db, admins
from myapp.models import User, Wishlist, Lottery
from myapp.forms import LoginForm, WishlistForm, RunLotteryForm, ClearLotteryTableForm
from random import choice

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def get_current_user():
    user = current_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.username in admins:
        users = User.query.filter(User.is_admin!='Y').all()
        admins_list = User.query.filter(User.is_admin=='Y').all()
        wishlists = Wishlist().query.all()
        lottery = Lottery().query.all()
        form_run_lottery = RunLotteryForm(request.form)
        form_clear_lottery = ClearLotteryTableForm(request.form)
        
        user_ids = [user.id for user in users]
        if request.method == 'POST' and form_run_lottery.validate():
            for user in users:
                random_id = choice(user_ids)
                while user.id == random_id:
                    random_id = choice(user_ids)
                user_ids.remove(random_id)
                assigned_wishlist = Lottery(user_id=user.id, assigned_wishlist=Wishlist.query.filter(Wishlist.user_id==random_id).first().id)
                db.session.add(assigned_wishlist)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            return redirect(url_for('admin'))

        if request.method == 'POST' and form_clear_lottery.validate():
            for item in lottery:
                db.session.delete(item)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            return redirect(url_for('admin'))        
        
        return render_template('admin.html', users=users, admins=admins_list, wishlists=wishlists, lottery=lottery, form_run_lottery=form_run_lottery, form_clear_lottery=form_clear_lottery)
    
    return redirect(url_for('index'))

@app.route('/cabinet', methods = ['GET', 'POST'])
@login_required
def cabinet():
    form = WishlistForm(request.form)
    
    if current_user.username in admins:
        return redirect(url_for('admin'))

    query_user_wishlist = Wishlist.query.filter(Wishlist.user_id==current_user.id).first()
    if query_user_wishlist:
        current_wishlist = query_user_wishlist.wishlist

        if request.method == 'POST' and form.validate():
            wishlist_added = request.form['wishlist_text']
            query_user_wishlist.wishlist = wishlist_added
            try:
                db.session.commit()
            except:
                db.session.rollback()
            current_wishlist = Wishlist.query.filter(Wishlist.user_id==current_user.id).first().wishlist
    else:
        current_wishlist = 'YOU HAVE NO WISHLIST YET!'

        if request.method == 'POST' and form.validate():
            wishlist_added = request.form['wishlist_text']
            wishlist = Wishlist(wishlist=wishlist_added, user_id=current_user.id)
            db.session.add(wishlist)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            current_wishlist = Wishlist.query.filter(Wishlist.user_id==current_user.id).first().wishlist
    
    try:
        query_assigned_wishlist = Lottery.query.filter(Lottery.user_id==current_user.id).first().assigned_wishlist
    except:
        query_assigned_wishlist = []
    if query_assigned_wishlist:
        assigned_wishlist = Wishlist.query.get(query_assigned_wishlist).wishlist
        return render_template('cabinet.html', form=form, wishlist=current_wishlist, admins=admins, assigned_wishlist=assigned_wishlist)

    return render_template('cabinet.html', form=form, wishlist=current_wishlist, admins=admins)


@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('cabinet'))
    
    form_login = LoginForm(request.form)
    
    if request.method == 'POST' and form_login.validate():
        username = request.form['username'].lower()
        password = request.form['password']
        try:
            User.try_login(username, password)
        except Exception as e:
            flash(f'ERROR: {e}', 'danger')
            return render_template('login.html', form=form_login)
        user = User.query.filter_by(username=username).first()
        if not user:
            #user = User(username=username.lower(), password=password)
            if username.lower() not in admins:
                user = User(username=username, is_admin='N')
            else:
                user = User(username=username, is_admin='Y')
            db.session.add(user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
        
        login_user(user)
        flash('You have successfully logged in.', 'success')
        if username in admins:
            return redirect(url_for('admin'))    
        else:
            return redirect(url_for('cabinet'))
    
    if form_login.errors:
        flash(form_login.errors, 'danger')
 
    return render_template('login.html', form=form_login)
        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))