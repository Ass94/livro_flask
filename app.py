# _*_ coding: utf-8 _*_

from flask_bootstrap import Bootstrap
from flask import Flask, request, redirect, render_template, Response, json

# config import
from config import app_config, app_active

#Admin
from admin.Admin import start_views

#Controller
from controller.User import UserController
from controller.Product import ProductController

config = app_config[app_active]

from flask_sqlalchemy import SQLAlchemy

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db = SQLAlchemy(config.APP)

    start_views(app, db)

    Bootstrap(app)

    db.init_app(app)

    """" Autorzação para API REST no final do código """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Hello, página inicial'
    
    @app.route('/login/')
    def login():
        return render_template('login.html', message="Esta é uma mensagem que veio da rota")
    
    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()

        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 
                'msg': 'Dados de usuário incorretos', 'type': None})


    @app.route('/recovery-password/')
    def recovery_password():
        return 'Aqui ficará a tela de recuperar senha'


    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()

        result = user.recovery(request.form['email'])

        if result:
            return render_template('recovery.html', data={'status': 200, 
            'msg': 'E-mail de recuperação enviado com sucesso'})
        else:
            return render_template('recovery.html', data={'status': 401, 
            'msg': 'Erro ao enviar e-mail de recuperação'})

    @app.route('/product', methods=['POST'])
    def save_products():
        product = ProductController()

        result = product.salve_product(request.form)

        if result:
            message = "Inserido"
        else:
            message = "Não inserido"
        
        return message

    @app.route('/product', methods=['PUT'])
    def update_products():
        product = ProductController()

        result = product.update_product(request.form)

        if result:
            message = "Editado"
        else:
            message = "Não Editado"

        return message

    @app.route('/product/<int:id>', methods=['DELETE'])
    def delete_products(id):
        product = ProductController()
        result = product.delete_product(id)

        if result:
            message = "Deletado"
        else:
            message = "Não Deletado"
        
        return message

    
    """API REST"""

    @app.route('/products/', methods=['GET'])
    @app.route('/products/<limit>', methods=['GET'])
    def get_products(limit=None):
        header = {}

        product = ProductController()
        response = product.get_products(limit=limit)
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/product/<product_id>', methods=['GET'])
    def get_product(product_id):
        header = {}

        product = ProductController()
        response = product.get_product_by_id(product_id = product_id)

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status'], header
    

    @app.route('/user/<user_id>', methods=['GET'])
    def get_user_profile(user_id):
        header = {}

        user = UserController()
        response = user.get_user_by_id(user_id=user_id)

        return Response(json.dumps(response, ensure_ascii=False), mimetype='applicaton/json'), response['status'], header


    return app
