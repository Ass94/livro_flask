# _*_ coding: utf-8 _*_
from sqlalchemy import func
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.base import Executable
from config import app_config, app_active
from model.Role import Role
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin

config = app_config[app_active]
db = SQLAlchemy(config.APP)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable=False)
    last_update = db.Column(db.DateTime(6), onupdate=db.func.current_timestamp(), nullable=True)
    recovery_code = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean(), default=1, nullable=True)
    role = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=False)

    funcao = relationship(Role)

    def __repr__(self):
        return '%s - %s' % (self.id, self.username)


    def get_user_by_email(self):
        try:
            res = db.session.query(User).filter(User.email==self.email).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
            return res



    def get_user_by_id(self):
        try:
            res = db.session.query(User).filter(User.id==self.id).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
            return res
            
    
    def update(self, obj):
        try:
            res = db.session.query(User).filter(User.id == self.id).update(obj)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
    
    def hash_password(self, password):
        try:
            return pbkdf2_sha256.hash(password)
        except Exception as e:
            print("Erro ao criptografar senha %s" % e)

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, password_no_hash, password_database):
        try:
            return pbkdf2_sha256.verify(password_no_hash, password_database)
        except ValueError:
            return False
    
    def get_total_users(self):
        try:
            res = db.session.query(func.count(User.id)).first()
        except Exception as e:
            res = []
            print(e)
        finally:
            db.session.close()
            return res
    

    def get_user_by_recovery(self):
        try:
            res = db.session.query(User).filter(User.recovery_code==self.recovery_code).first()
        except Exception as e:
            res = None
            print(e)
        finally:
            db.session.close()
            return res
    
    

