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

from flask import Flask, render_template, request, g, jsonify, send_file, make_response, Response, stream_with_context
from werkzeug import secure_filename

import settings
import cloudmanager
import metachains_dtc
import file_encryptor.convergence

app = Flask(__name__)
app.config['TEMP_FOLDER'] = 'tmp'
app.config['MAX_CONTENT_LENGTH'] = settings.STORAGE_SIZE

if not app.debug:
    import logging
    file_handler = logging.FileHandler('production.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


def make_cloudmanager():
    return cloudmanager.CloudManager(
        settings.DATABASE_PATH,
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
        key = file_encryptor.convergence.encrypt_file_inline(temp_name, None)
        result = get_cloud_manager().upload(temp_name)

        if not result:
            response = make_response(jsonify(error='Upload failed'), 500)
        else:
            response = make_response(jsonify(filehash=result, key=key), 201)

        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

        return response

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

    key = request.args.get('key', None)

    full_path = cm.warm_up(filehash)
    if full_path is None:
        return jsonify(error='File not found'), 404

    if key is None:
        return send_file(full_path,
            attachment_filename=os.path.basename(full_path),
            as_attachment=True)
    else:
        return Response(
            stream_with_context(
                file_encryptor.convergence.decrypt_generator(full_path, key)),
            mimetype="application/octet-stream",
            headers={"Content-Disposition":"attachment;filename=" + os.path.basename(full_path) })


@app.route("/api/find/<filehash>", methods=['GET'])
def find(filehash):
    cm = get_cloud_manager()

    info = cm.info(filehash)

    if info is None:
        return jsonify(error='File not found'), 404

    return jsonify(info)


@app.route("/api/status", methods=['GET'])
def status():
    """Return node status information."""

    cm   = get_cloud_manager()
    coin = get_coin()

    return jsonify({
        "bandwidth": {
            "total": {
                "incoming": cm.total_incoming(),
                "outgoing": cm.total_outgoing()
                },
            "current": {
                "incoming": cm.current_incoming(),
                "outgoing": cm.current_outgoing()
                },
            "limits": {
                "incoming": settings.TRANSFER_MAX_INCOMING,
                "outgoing": settings.TRANSFER_MAX_OUTGOING
                }
            },

        "storage": {
            "capacity": cm.capacity(),
            "used": cm.used_space(),
            "max_file_size": settings.STORAGE_FILE
            },

        "sync": {
            "cloud_queue": cm.upload_queue_info(),
            "blockchain_queue": cm.blockchain_queue_info()
            },

        "datacoin": {
            "balance": coin.balance(),
            "address": coin.address("incoming")
            }
        })


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
