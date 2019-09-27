import os

from app import create_app


# config_name = os.getenv('FLASK_CONFIG')
# app = create_app('config')

if __name__ == '__main__':
    app = create_app('config')

    app.run(host='localhost', port=5050, debug=True)
