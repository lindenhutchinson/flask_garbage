from flask import render_template, make_response, jsonify

def home():
    return render_template('pages/home.html')

def about():
    return render_template('pages/placeholder.about.html')

def internal_error(error):
    return render_template('errors/500.html'), 500

def not_found_error(error):
    return render_template('errors/404.html'), 404

def image_too_large_error(error):
    return make_response(jsonify(error_text="Sorry I can't handle files that large, please try again with a smaller file"), 413)

def bad_request_error(error):
    return make_response(jsonify(error_text="Please upload a valid image file"), 400)