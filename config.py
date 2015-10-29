# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret key'


class ProductionConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
