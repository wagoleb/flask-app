from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from app.mod_auth import LoginForm
from app.mod_user.models import UserModel

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route('/login', methods=['GET', 'POST'])
def login_show():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.show'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login_page.login_show'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main_page.show'))
    return render_template('auth/login.html', title='Login page', form=form)


logout_page = Blueprint('logout_page', __name__)

@logout_page.route('/logout')
def logout_do():
    logout_user()
    return redirect(url_for('main_page.show'))