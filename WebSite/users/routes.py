from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from WebSite import db, bcrypt
from WebSite.models import User, Post, Chat
from WebSite.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from flask_socketio import send

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:

        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        # Encripta la contraseña
        h_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=h_password)

        # Registra los datos del usuario
        db.session.add(user)
        db.session.commit()

        flash(f'Se ha creado una cuenta para {form.username.data}', 'success')

        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        # Compara la encriptación de las contraseña con la almacenada en la base de datos
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:

            flash('Inicio de sesión fallido. Verifique el email y la contraseña.', 'danger')

    return render_template('login.html', title='Inicia Sesión', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:

            picture_file = save_picture(form.picture.data)

            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        
        current_user.email = form.email.data

        db.session.commit()

        flash('Tu perfil ha sido actualizado!', 'success')

        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':

        form.username.data = current_user.username

        form.email.data = current_user.email

        db.session.commit()

    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account - ' + current_user.username, image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):

    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    return render_template('user_posts.html', posts=posts, user=user)



@users.route("/logout")
def logout():
    
    logout_user()

    return redirect(url_for('users.login'))


@users.route('/message/<string:username>')
@login_required
def message(username):

    chat = Chat.query.all()
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('message_group.html', chat=chat, username=username)

