#!/usr/bin/env python3
"""
Flask app with Babel for internationalization
"""

from flask import Flask, render_template
from flask_babel import Babel, get_locale
import pytz
from datetime import datetime


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


@app.route('/')
def index() -> str:
    """
    Route to the home page that renders the 1-index.html template.
    """
    current_time = datetime.now(
        pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])
    )
    return render_template(
        '1-index.html', locale=get_locale(), current_time=current_time
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
