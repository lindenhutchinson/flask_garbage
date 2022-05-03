from controllers import home_controller, prediction_controller

def routes(app):
    '''All Routes / Url
    This app uses an MVC pattern, hence all the url are routed here
    Just import your logics from the controllers package and route
    using the add_url_rule function

    :param app: Flask app instance
    :return: None
    '''
    app.register_error_handler(404, home_controller.not_found_error)
    app.register_error_handler(500, home_controller.internal_error)
    app.register_error_handler(413, home_controller.image_too_large_error)
    app.register_error_handler(400, home_controller.bad_request_error)

    #----------------------------------------------------------------------------#
    # Home Routes
    #----------------------------------------------------------------------------#

    app.add_url_rule('/', view_func=home_controller.home)
    app.add_url_rule('/about', view_func=home_controller.about)

    #----------------------------------------------------------------------------#
    # Prediction Routes
    #----------------------------------------------------------------------------#

    app.add_url_rule('/predict-image', view_func=prediction_controller.make_prediction, methods=['POST'])