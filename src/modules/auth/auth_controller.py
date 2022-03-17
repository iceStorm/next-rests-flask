from uuid import uuid1
from flask import Blueprint, jsonify, request, render_template, flash, current_app, url_for, make_response, session
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import redirect

from src import limiter, logger, db_session
from src.base.constants.base_constanst import FlashCategory
from src.modules.auth.auth_service import AuthService
from src.modules.user.user_model import User, gen_alternative_id
from .auth_constants import *

# defining controller
auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static', static_url_path='auth/static')


@auth.route('/')
def index():
    return jsonify({"hello": "world"})


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # grabbing the form
    from src.modules.auth.forms.login_form import LoginForm
    form = LoginForm()

    # checking if is GET request
    if request.method == 'GET':
        # redirecting logged-in user to the index page
        if current_user.is_authenticated:
            flash('You\'re already logged in!', category=FlashCategory.warning(5000))
            return redirect('/')

        # auto fill the email field
        if request.args.get('email'):
            form.email.data = request.args.get('email')

        return render_template('login.html', form=form)

    # POST REQUEST
    # checking if the form is not valid yet
    if not form.validate_on_submit():
        return render_template('login.html', form=form)

    # FORM IS VALID, LET'S GET THE USER OBJECT FROM DB
    user = AuthService.get_user_from_email(form.email.data)

    if user is not None:
        # let's log the user in
        login_user(user, remember=form.remember)

        #  Tell Flask-Principal the identity changed
        # from flask_principal import identity_changed, Identity
        # identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        # finally, redirect the user to desired page or index page
        next_url = request.args.get('next')
        return redirect(next_url if next_url else '/')
    
    flash(message='The user no longer exists', category=FlashCategory.Error)
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['POST'])
@limiter.limit('5/minute')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    # for key in ('identity.name', 'identity.auth_type'):
    #     session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    # from flask_principal import identity_changed, Identity, AnonymousIdentity
    # identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(location="/")


@auth.route('/register', methods=['GET', 'POST'])
@limiter.limit('1/second; 15/minute; 20/day')
def register():
    # grabbing the form
    from src.modules.auth.forms.signup_form import SignUpForm
    form = SignUpForm()

    # checking if is GET request
    if request.method == 'GET':
        # redirecting logged-in user to the index page
        if current_user.is_authenticated:
            flash('Please logout first, then signup!', category=FlashCategory.warning())
            return redirect('/')
        return render_template('signup.html', form=form)

    # post requests
    # checking if the form is not valid yet
    if not form.validate_on_submit():
        flash('Please ensure all fields have no errors!', category=FlashCategory.warning(7500))
        return render_template('signup.html', form=form)

    try:
        # all validation passed, let's continue handle the signup process
        confirmation_code = AuthService.gen_registration_code()
        # assigning the confirmation code to user's session cookie
        session[SESSION_REGISTRATION_CONFIRMATION_CODE] = confirmation_code

        # send confirmation email
        AuthService.send_register_confirm_email(
            receiver_email=form.email.data,
            receiver_name=form.organization_name.data,
            code=confirmation_code,
        )

        # push the form data to session, so we dont have to store these info in the DB --> prevent registrastion spamming ultil the email in confirmed
        session[SESSION_REGISTRATION_ORGANIZATION_NAME] = form.organization_name.data
        session[SESSION_REGISTRATION_ORGANIZATION_REPRESENTER_PERSON_NAME] = form.organization_representer_person_name.data
        session[SESSION_REGISTRATION_ORGANIZATION_TAX_ID] = form.organization_tax_id.data
        session[SESSION_REGISTRATION_CITIZEN_ID] = form.citizen_id.data
        session[SESSION_REGISTRATION_EMAIL] = form.email.data
        session[SESSION_REGISTRATION_PHONE] = form.phone.data
        session[SESSION_REGISTRATION_ADDRESS] = form.address.data

        # showing a flash message -> redirecting to the home page
        flash(message=f'Vui lòng kiểm tra tin nhắn được gửi tới email {form.email.data} để hoàn tất quá trình đăng ký!', category=FlashCategory.success(20000))
        return redirect('/verify')
    except Exception as e:
        logger.error(e)
        flash(message=f'Có lỗi xảy ra trong quá trình xử lý, vui lòng thử lại sau', category=FlashCategory.error(20000))
        return render_template('signup.html', form=form)


@auth.route('verify', methods=['GET', 'POST'])
@limiter.limit('1/second; 15/minute; 20/day')
def verify_registration():
    # grabbing the form
    from src.modules.auth.forms.verification_form import RegisterVerificationForm
    form = RegisterVerificationForm()

    if not session.get(SESSION_REGISTRATION_EMAIL) or not session.get(SESSION_REGISTRATION_CONFIRMATION_CODE):
        flash(message='It seems like you have already registered or your data has been corrupted, please try later', category=FlashCategory.warning(10000))
        return redirect('/')

    if request.method == 'GET':
        return render_template('verify-registration.html', form=form, email=session[SESSION_REGISTRATION_EMAIL])

    if not form.validate_on_submit():
        flash(message='Please fill out the code', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session[SESSION_REGISTRATION_EMAIL])

    # form validated --> check if the provided code is correct
    if form.verification_code.data != session[SESSION_REGISTRATION_CONFIRMATION_CODE]:
        flash(message='The code you provided was incorrect', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session[SESSION_REGISTRATION_EMAIL])

    # form validated -> add the envoy info to DB
    try:
        new_user = User(email=session[SESSION_REGISTRATION_EMAIL], phone_number=session[SESSION_REGISTRATION_PHONE])
        new_user.role_id = 3 # envoy
        new_user.activated = False # disallow to login
        new_user.alternative_id = gen_alternative_id()

        # ??? check trùng thông tin trước khi thêm vào DB

        if AuthService.register(new_user=new_user):
            flash(message='Đăng ký tài khoản Đại sứ BVU thành công', category=FlashCategory.success(10000))
            response = make_response(render_template('registration-success.html', email=new_user.email))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            session.clear()
            return response

        # DB insert error
        flash(message='Something went wrong with your info, please try to register again', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session['registration_email'])

    except Exception as e:
        logger.error(e)
        flash(message='Something went wrong (maybe your data has been corrupted), please try later', category=FlashCategory.warning())
        return render_template('verify-registration.html', form=form, email=session['registration_email'])



@auth.route('/reset-password', methods=['GET', 'POST'])
async def reset_password():
    from .forms.reset_password_form import ResetPasswordForm
    form = ResetPasswordForm()

    if request.method == 'GET':
        return render_template('password-reset.html', form=form)

    if not form.validate_on_submit():
        flash(message='Please ensure all fields are valid', category=FlashCategory.warning())
        return render_template('password-reset.html', form=form)

    try:
        new_password = uuid1().hex
        AuthService.send_reset_password_email(email=form.email.data, password=new_password)
        the_user = AuthService.get_user_from_email(form.email.data)
        if the_user != None:
            the_user.alternative_id = gen_alternative_id()
            the_user.password_hash = User.gen_password_hash(new_password)
            db_session.commit()
            flash(message='Your password has been reset, please check your email to get the new password', category=FlashCategory.success())
            return render_template("password-reset.html", form=form)
        else:
            raise Exception()
    except Exception as e:
        flash(message='Error occurred while sending reset password email', category=FlashCategory.error())
        return render_template('password-reset.html', form=form)
