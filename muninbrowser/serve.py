import logging

logging.basicConfig(level=logging.DEBUG)

from controller import app

def main():
    app.debug = True
    app.run(host=app.config['BIND'],
            port=app.config['PORT'])
