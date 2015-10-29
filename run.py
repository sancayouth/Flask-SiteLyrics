# -*- coding: utf-8 -*-
from app import app


if __name__ == '__main__':
    app = app.create_app()
    app.run(debug=True)
