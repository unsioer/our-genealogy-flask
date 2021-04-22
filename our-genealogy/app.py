from flask import Flask, render_template, request, abort, jsonify
from __init__ import create_app
from extensions import scheduler

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    scheduler.start()
    app.run(host='0.0.0.0')
