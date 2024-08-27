#!/usr/bin/env python3
"""
Flask app with Babel for internationalization, mock user login system,
and time zone handling.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _
import pytz
from pytz.exceptions import UnknownTimeZoneError


class Config:
    """
    Configuration class for Flask app.
    Sets available languages, default locale, and time zone.
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
    Determine the best match for supported languages based on:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request headers
    4. Default locale
    """
    locale_param = request.args.get('locale')
    if locale_param and locale_param in app.config['LANGUAGES']:
        return locale_param

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the best time zone based on:
    1. Time zone from URL parameters
    2. Time zone from user settings
    3. Default to UTC
    Validates that the time zone is supported.
    """
    timezone_param = request.args.get('timezone')
    if timezone_param:
        try:
            pytz.timezone(timezone_param)  # Validate the time zone
            return timezone_param
        except UnknownTimeZoneError:
            pass  # Ignore invalid time zones

    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])  # Validate the time zone
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass  # Ignore invalid time zones

    return app.config['BABEL_DEFAULT_TIMEZONE']


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
    Route to the home page that renders the 6-index.html template.
    """
    return render_template(
        '7-index.html', locale=get_locale(), timezone=get_timezone()
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
