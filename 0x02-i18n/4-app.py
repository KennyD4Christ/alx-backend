#!/usr/bin/env python3
"""
Flask app with Babel for internationalization, including message
translations and locale switching via URL parameter.
"""

from flask import Flask, render_template, request
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


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages using
    request.accept_languages,
    or use the 'locale' query parameter if present and valid.
    """
    locale_param = request.args.get('locale')
    if locale_param and locale_param in app.config['LANGUAGES']:
        return locale_param
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Route to the home page that renders the 3-index.html template.
    """
    return render_template('4-index.html', locale=get_locale())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
