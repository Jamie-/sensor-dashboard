import logging
import flask
from iot import app
from iot import db

logger = logging.getLogger(__name__)


@app.route('/')
def route_index():
    stats = {
        'collections': db.num_collections()
    }
    return flask.render_template('dashboard.html', stats=stats)


# API
@app.route('/api/log/<string:collection>', methods=['POST'])
def api_log_add(collection):
    if not flask.request.json:
        logger.warning('Request is not valid JSON.')
        flask.abort(400)
    try:
        db.add_record(collection, flask.request.json)
        return flask.jsonify({'status': 'ok'})
    except ValueError:
        logger.warning('Database add threw ValueError.')
        flask.abort(400)


@app.route('/api/view/<string:collection>')
def api_view(collection):
    data = db.get()[collection].find()
    return flask.jsonify([{k: v for k, v in d.items() if k != '_id'} for d in data])  # Remove _id from data


# Error Handlers
@app.errorhandler(400)
def error_400(error):
    return flask.render_template('error.html', title='Bad Request', heading='Bad Request', text='Error 400'), 400


@app.errorhandler(401)
def error_401(error):
    return flask.render_template('error.html', title='Unauthorized', heading='Unauthorized', text='Error 401'), 401


@app.errorhandler(403)
def error_403(error):
    return flask.render_template('error.html', title='Forbidden', heading='Forbidden', text='Error 403'), 403


@app.errorhandler(404)
def error_404(error):
    return flask.render_template('error.html', title='Not Found', heading='Page Not Found', text='Error 404'), 404


@app.errorhandler(405)
def error_405(error):
    return flask.render_template('error.html', title='Method Not Allowed', heading='Method Not Allowed', text='Error 405'), 405


@app.errorhandler(500)
def error_500(error):
    return flask.render_template('error.html', title='Internal Server Error', heading='Internal Server Error', text='Error 500'), 500
