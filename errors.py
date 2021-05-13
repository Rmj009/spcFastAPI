# from flask import render_template
from app import app
#-------ERROR Handling----------
"""
500 bad request for exception
Returns:
500 and msg which caused problems
"""
# class PassGateway:
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
  
