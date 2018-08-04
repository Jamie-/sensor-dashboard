import logging
import flask
import datetime
from iot import app
from iot import db

logger = logging.getLogger(__name__)


@app.route('/')
def route_index():
    stats = {
        'collections': db.num_collections(),
        'total_documents': db.total_docs()
    }
    return flask.render_template('dashboard.html', title='Dashboard', stats=stats)


@app.route('/temperature')
def route_temp():
    data = {}
    raw_settings = db.get_settings()
    settings = {}
    filters = {}  # Data filters
    age = flask.request.args.get('age')  # Age is time in hours to get
    if age is not None:
        try:
            age = int(age)
        except ValueError:
            flask.abort(400)
    else:
        age = 7 * 24
    filters.update({'age': age})
    for c in db.collection_names():
        info = db.get().settings.find_one({'{}.type'.format(c): 'temperature'})
        if info:
            data[info[c]['name']] = db.get()[c].find({'timestamp': {'$gte': datetime.datetime.now() - datetime.timedelta(hours=age)}})
            settings[info[c]['name']] = raw_settings[c]
    return flask.render_template('temperature.html', title='Temperature', data=data, settings=settings, filters=filters, hide_nav=True)


@app.route('/power')
def route_power():
    return flask.render_template('notimplemented.html', title='Power')


@app.route('/wind')
def route_wind():
    return flask.render_template('notimplemented.html', title='Wind Speed')


@app.route('/rain')
def route_rain():
    return flask.render_template('notimplemented.html', title='Rainfall')


@app.route('/settings', methods=['GET', 'POST'])
def route_settings():
    if flask.request.method == 'POST':
        for item in flask.request.form:
            collection, key = item.split('-')
            value = flask.request.form[item]
            db.get().settings.update({collection: {'$exists': True}}, {'$set': {'{}.{}'.format(collection, key): value}}, upsert=True)
    collections = db.collection_names()
    settings = db.get_settings()
    return flask.render_template('settings.html', title='Collection Categories', collections=collections, settings=settings)


@app.route('/settings/manage', methods=['GET', 'POST'])
def route_manage():
    collections = db.collection_names()
    # Get metadata (from settings) for each collection
    settings = {}
    for e in [{k: v for k, v in d.items() if k != '_id'} for d in db.get().settings.find()]:
        settings.update(e)
    # Get number of data points for each collection
    qtys = {}
    for c in collections:
        qtys[c] = db.get()[c].count()
    return flask.render_template('manage.html', title='Manage Collections', collections=collections, settings=settings, qtys=qtys)


@app.route('/settings/manage/delete', methods=['POST'])
def route_delete():
    if 'collection' not in flask.request.form:
        flask.abort(400)
    try:
        db.delete_collection(flask.request.form['collection'])
        return 'OK'
    except ValueError:
        flask.abort(400)


# API
@app.route('/api/log')
def api_collections():
    return flask.jsonify({'collections': db.collection_names()})


@app.route('/api/log/<string:collection>', methods=['GET', 'POST'])
def api_log(collection):
    if collection.lower() == 'settings':  # Reserve settings collection
        return flask.jsonify({'error': 'collection is reserved'}), 400
    if flask.request.method == 'POST':
        if not flask.request.json:
            logger.warning('Request is not valid JSON.')
            return flask.jsonify({'error': 'request is not valid json'}), 400
        try:
            db.add_record(collection, flask.request.json)
            return flask.jsonify({'status': 'ok'})
        except ValueError:
            logger.warning('Database add threw ValueError.')
            return flask.jsonify({'error': 'error inserting record'}), 400
    else:
        data = db.get()[collection].find()
        return flask.jsonify([{k: v for k, v in d.items() if k != '_id'} for d in data])  # Remove _id from data


@app.route('/api/log/<string:collection>/latest')
def api_log_max(collection):
    if collection.lower() == 'settings':  # Reserve settings collection
        return flask.jsonify({'error': 'collection is reserved'}), 400
    data = db.get()[collection].find_one(sort=[('timestamp', db.DESCENDING)])
    if data is not None:
        return flask.jsonify({k: v for k, v in data.items() if k != '_id'})  # Remove _id from data
    return flask.jsonify({'error': 'collection has no data'}), 404



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
