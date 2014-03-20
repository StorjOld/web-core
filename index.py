#!/usr/bin/env python
#
# Indentation is 4 spaces.
#
# Available routes:
#
#   GET  /download/filehash
#   POST /upload
#   GET  /server-usage
#   GET  /disk-usage

import os

from flask import Flask, render_template, request, g, jsonify, send_file
from werkzeug import secure_filename

import settings
import cloudmanager
import metachains_dtc

app = Flask(__name__)
app.config['TEMP_FOLDER'] = 'tmp'
app.config['MAX_CONTENT_LENGTH'] = settings.STORAGE_SIZE

def make_cloudmanager():
    return cloudmanager.CloudManager(
        settings.DATABASE,
        settings.STORAGE_PATH,
        settings.STORAGE_SIZE)

def make_coin():
    return metachains_dtc.Datacoin(
        settings.DATACOIN_URL,
        settings.DATACOIN_USERNAME,
        settings.DATACOIN_PASSWORD)


def get_cloud_manager():
    """Instantiate a cloudmanager instance, if needed."""

    cloud_manager = getattr(g, '_cloud_manager', None)
    if cloud_manager is None:
        cloud_manager = g._cloud_manager = make_cloudmanager()

    return cloud_manager

def get_coin():
    coin = getattr(g, '_coin', None)
    if coin is None:
        coin = g._coin = make_coin()

    return coin


@app.teardown_appcontext
def close_connection(exception):
    get_cloud_manager().close()


#Upload post method to save files into directory
@app.route("/api/upload",methods=['POST'])
def upload():
    """Upload a file using cloud manager.

    This may take a while, as it uploads the given
    file to three different host providers (in parallel).

    """
    # Save the uploaded file into a temporary location.
    file        = request.files['file']
    filename    = secure_filename(file.filename)
    temp_name   = os.path.join(app.config['TEMP_FOLDER'], filename)
    file.save(temp_name)

    try:
        result = get_cloud_manager().upload(temp_name)

        if not result:
            return jsonify(error='Upload Failed'), 500
        else:
            return jsonify(filehash=result), 201
    finally:
        os.remove(temp_name)


@app.route("/api/download/<filehash>",methods=['GET'])
def download(filehash):
    """Download a file from cloud manager.

    This may take a while, since the file may not
    be currently in local cache. If there is no
    file matching the given hash, returns a string
    with an error message.

    """
    cm = get_cloud_manager()

    full_path = cm.warm_up(filehash)
    if full_path is None:
        return jsonify(error='File not found'), 404

    return send_file(full_path,
            attachment_filename=os.path.basename(full_path),
            as_attachment=True)


@app.route("/api/find/<filehash>", methods=['GET'])
def find(filehash):
    cm = get_cloud_manager()

    info = cm.info(filehash)

    if info is None:
        return jsonify(error='File not found'), 404

    return jsonify(info)


@app.route("/api/bandwidth/usage", methods=['GET'])
def bandwidth_usage():
    """Return bandwidth usage statistics."""

    cm = get_cloud_manager()

    return jsonify({
        "total": {
            "incoming": cm.total_incoming(),
            "outgoing": cm.total_outgoing()
            },
        "current": {
            "incoming": cm.current_incoming(),
            "outgoing": cm.current_outgoing()
            }
        })


@app.route("/api/bandwidth/limits", methods=['GET'])
def bandwidth_limits():
    """Return the bandwidth limits for this server."""

    cm = get_cloud_manager()

    return jsonify(incoming=cm.incoming_limit(), outgoing=cm.outgoing_limit())


@app.route("/api/storage/usage", methods=['GET'])
def disk_usage():
    """Return cloud manager disk usage.

    Returns the number of bytes used up by the local
    cache storage.

    """
    cm = get_cloud_manager()

    return jsonify(usage=cm.used_space())

@app.route("/api/storage/capacity", methods=['GET'])
def storage_capacity():
    """Return cloud manager disk capacity.

    """
    cm = get_cloud_manager()

    return jsonify(capacity=cm.capacity())

@app.route("/api/sync/status", methods=['GET'])
def status_sync():
    """Return cloud manager synchronization status.

    """
    cm = get_cloud_manager()

    return jsonify(cm.sync_status())


@app.route("/api/dtc/balance", methods=['GET'])
def coin_balance():
    coin = get_coin()

    return jsonify(balance=coin.balance())


@app.route("/api/dtc/address", methods=['GET'])
def coin_address():
    coin = get_coin()

    return jsonify(address=coin.address("incoming"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
