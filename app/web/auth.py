from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user

from . import web

from ..forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from ..helpers.libs.email import send_email
from ..models.base import db
from ..models.user import User


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # 把注册所有的信息，写进model的属性
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            # 提交到数据库
            db.session.add(user)
            # db.session.commit()
        # login_user(user, False)
        # 重定向到登录界面
        return redirect(url_for('web.index'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):

            # 如果用户名密码正确，则使用flask-login插件进行管理cookie，传入User Model的该用户的实例user，默认cookie的有效期为关闭浏览器就没了，使用remember=True进行持久化（默认365天）
            login_user(user, remember=True)

            # 用户访问某些需要登录才能访问的URL时，比如 /my/gifts
            # flask-login 插件会跳转到该登录界面，并会带上参数next存储登录成功后继续访问的URL，如：http://0.0.0.0:8181/login?next=%2Fmy%2Fgifts
            next = request.args.get('next')
            # 如果是直接访问的登录界面，默认直接重定向到首页，next.startswith('/') 则是 「防止重定向攻击」
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('auth/login.html', form=form)


@web.route('/logout')
# flask-login 使用 login_required 装饰器 实现 视图函数的「访问权限控制」
# 需要为flask-login插件 注册根据用户id获取用户信息的函数（在 modek/user 下）
# 权限分级，可以改写flask-login实现，比如会员/管理员的权限等
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            # first_or_404() 相比 first() ：当没有查询到数据时，会向外抛出 flask定义的 HTTPException 的子类 NotFound （code为404）
            # 且可以 通过蓝图内app_errorhandler装饰器，将所有视图下的404异常统一捕获，进行统一处理
            user = User.query.filter_by(email=account_email).first_or_404()
            send_email(form.email.data, '重置你的密码',
                       'email/reset_password', user=user,
                       token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + '，请及时查收')
            return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        result = User.reset_password(token, form.password1.data)
        if result:
            flash('你的密码已更新,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            return redirect(url_for('web.index'))
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
# @login_required
def change_password():
    pass
    # form = ChangePasswordForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     current_user.password = form.new_password1.data
    #     db.session.commit()
    #     # 查看 flash 和 get_flashed_messages 你就会发现，
    #     # 其实 flask message flashing 功能是基于一个名字叫做 session 的 cookie 实现的
    #     # 无状态 HTTP 请求如何解决 上次请求和本次请求的关联：
    #     # 就是把上次请求产生的结果回传到用户 cookie 中，
    #     # 然后下次用户请求是带上这个 cookie，从而实现两个请求的关联
    #     flash('密码已更新成功')
    #     return redirect(url_for('web.personal_center'))
    # return render_template('auth/change_password.html', form=form)


@web.route('/personal')
# @login_required
def personal_center():
    pass
    # return "personal page"
    # return render_template('personal.html', user=current_user.summary)
