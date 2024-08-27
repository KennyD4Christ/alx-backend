#!/usr/bin/env python3
"""
Flask app with Babel for internationalization and mock user login system.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _


class Config:
    """
    Configuration class for Flask app.
    Sets available languages and default locale/timezone.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages using
    request.accept_languages, or use the 'locale' query parameter
    if present and valid.
    """
    locale_param = request.args.get('locale')
    if locale_param and locale_param in app.config['LANGUAGES']:
        return locale_param
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> dict:
    """
    Retrieve the user based on the 'login_as' query parameter.
    """
    user_id = request.args.get('login_as', type=int)
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """
    Executed before each request. Sets the global user object.
    """
    g.user = get_user()


@app.route('/')
def index() -> str:
    """
    Route to the home page that renders the 5-index.html template.
    """
    return render_template('5-index.html', locale=get_locale())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
