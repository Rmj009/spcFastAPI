from flask import render_template
from alchemy_db import *
from app import app
db = SQLAlchemy()

#-------ERROR Handling----------
"""
500 bad request for exception
Returns:
500 and msg which caused problems
"""
# class PassGateway:
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),error, 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),error, 500

@app.teardown_appcontext
def shotdown_session(error):
    print ("@app.teardown_appcontext: shotdown_session()")
    db.session.remove()
    db.session.rollback()
    return error, 500
