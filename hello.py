from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin, RoleMixin, SQLAlchemySessionUserDatastore, Security, login_required, current_user
from config import Configuration

# application
application = Flask(__name__)
application.config.from_object(Configuration)
application.url_map.strict_slashes = False

# Database
db = SQLAlchemy(application)
migrate = Migrate(application, db)
manager = Manager(application)
manager.add_command('db', MigrateCommand)


#Models
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    keywords = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "Article %r" % self.name


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    img = db.Column(db.String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Equipment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "Equipment %r" % self.name

# Admin
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


admin = Admin(application, 'itprotection.ru', url='/admin', index_view=HomeAdminView())
admin.add_view(AdminView(Service, db.session))
admin.add_view(AdminView(Equipment, db.session))           
# end Admin

roles_users = db.Table('roles_users', 
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)


# Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(application, user_datastore)


@application.route("/")
def index():
    ep = Equipment.query.all()
    services = Service.query.order_by(Service.id).all()
    return render_template("index.html", services=services, ep=ep)


@application.route("/services")
# @login_required
def services():
    services = Service.query.order_by(Service.id).all()
    return render_template("services.html", services=services)


@application.route("/services/<string:link>")
def service(link):
    service = Service.query.filter(Service.link == link).first()
    return render_template("common/template.html", service=service)


@application.route("/price")
def price():
    return render_template("price.html")


@application.route("/contacts")
def contacts():
    return render_template("contacts.html")


@application.route("/privacy")
def privacy():
    return render_template("privacy.html")


@application.route("/send-smtp", methods = ['POST'])
def send():
    import json
    import smtplib
    try:
        data = request.form
        message = 'Пользователь ' + data.name + ' оставил заявку, его телефон ' + data.number + '<br>Сообщение этого пользователя: ' + data.text
        smtp = smtplib.SMTP('smtp.mail.ru', 465, None, timeout=10)
        smtp.starttls()
        smtp.login('itprotection@bk.ru','123Fktrcfylh123')
        smtp.sendmail("itprotection@bk.ru","info@itprotection.ru", message)
        smtp.quit()
        return json.dumps({'success': True}), 200
    except:
        return json.dumps({'success': False, 'text': 'Почтовый сервер не отвечает'}), 408


@application.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0')
