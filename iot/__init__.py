import os
import sys
import json
import logging
import flask


app = flask.Flask(__name__)

# Get flask config
with open('config.json') as f:
    config = json.load(f)
app.config.update(config)
app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME']  # Set global app name in Jinja2 too

# Setup logging
log_formatter = logging.Formatter('%(asctime)s[%(levelname)8s][%(module)s] %(message)s', datefmt='[%m/%d/%Y][%I:%M:%S %p]')
root_logger = logging.getLogger()
root_logger.setLevel(logging.getLevelName(app.config['LOG_LEVEL'].upper()))

# Console log handler
log_console_handler = logging.StreamHandler(sys.stdout)
log_console_handler.setFormatter(log_formatter)
root_logger.addHandler(log_console_handler)

# Log file handler
log_file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'])
log_file_handler.setFormatter(log_formatter)
root_logger.addHandler(log_file_handler)

# Continue to setup views
import iot.views
