from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask.templating import render_template
from src.base.constants.base_constanst import FlashCategory

from src import db, admin_permission, manager_permission
from src.modules.user.user_model import User
from .user_service import UserService

# defining controller
user = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='user/static')


@user.route('', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def list():
    users = db.session.query(User).filter(User.activated == True).order_by(User.role_id.asc(), User.verified_time.desc())
    return render_template("users.html", users=users.paginate(), title='Tài khoản đang hoạt động')


@user.route('/disabled', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def disabled():
    users = db.session.query(User).filter(User.activated == False, User.verified_time != None).order_by(User.created_time.desc())
    return render_template("users.html", users=users.paginate(), title='Tài khoản đã khóa')


@user.route('/waiting', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def accounts_waiting():
    users = db.session.query(User).filter(User.activated == False, User.verified_time == None, User.role_id == 3).order_by(User.created_time.desc())
    return render_template("users.html", users=users.paginate(), title='Đang chờ xác nhận tài khoản')


@user.route('/<int:id>', methods=['GET'])
@manager_permission.require(http_exception=403)
def detail(id: int):
    the_user = db.session.query(User).filter(User.id == id).first()

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))

    # đại sứ chỉ cho xem profile chính mình
    if current_user.role.id == 3 and the_user.id != current_user.id:
        flash('Can only view your profile', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))

    return render_template("profile.html", user=the_user)


@user.route('/profile', methods=['GET'])
def profile():
    return render_template("profile.html", user=current_user)



@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def edit(id: int):
    the_user = db.session.query(User).filter(User.id == id).first()

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))
    
    return redirect(request.referrer or url_for('user.list'))


@user.route('/activate/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def activate(id: int):
    the_user = db.session.query(User).filter(User.id == id).first()

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))
    
    # verify new envoy account
    if (the_user.role_id == 3 and the_user.verified_time == None) and not UserService.verify(the_user):
        flash('Error occured when verify the envoy', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))
    
    # re-activate old account
    elif not UserService.activate(the_user):
        flash('Error occured when activate the user', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))

    flash('Activated', category=FlashCategory.success())
    return redirect(request.referrer or url_for('user.list'))


@user.route('/deactivate/<int:id>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def deactivate(id: int):
    the_user = db.session.query(User).filter(User.id == id).first()

    if not the_user:
        flash('The user no longer exists', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))

    if the_user.role_id == 1: # cannot deactivate the admin user
        flash('Cannot deactivate the admin user', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))

    if not UserService.deactivate(the_user):
        flash('Error occured when deactivate the user', category=FlashCategory.error())
        return redirect(request.referrer or url_for('user.list'))
    
    flash('Deactivated', category=FlashCategory.success())
    return redirect(request.referrer or url_for('user.list'))
