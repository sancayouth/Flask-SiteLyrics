# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_():
    return render_template('index.html', title='Flask Lyrics')