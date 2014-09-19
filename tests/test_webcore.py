#!/usr/bin/env python

from __future__ import print_function

import index as web_core
import file_encryptor
from webcore import WebCore

import settings

import codecs
from io import BytesIO
import os
import time
import errno
import pprint

import unittest
import tempfile
import hashlib
import stat
import multiprocessing

import sqlite3
import flask
try:
    import flask.ext.api
    status = flask.ext.api.status
except ImportError as e:
    print('webcore tests require "Flask-API"')
import json
import os

import psycopg2
from psycopg2.extensions import STATUS_READY
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import ProgrammingError

import shutil

class MetaDiskWebCoreTestCase(unittest.TestCase):
    '''Tests the web API for the web-core package
    '''
    class FailedResponseException(Exception):
        def __init__(self, text = '', response = None):
            super(MetaDiskWebCoreTestCase.FailedResponseException, self).__init__(text)
            self.response = response

        def __str__(self):
            return super(MetaDiskWebCoreTestCase.FailedResponseException, self).__str__() + '-' + str(self.response)

    def setUp(self):
        self.SAMPLE_UPLOAD_SIZE_BYTES = 256
        self.storage_path = tempfile.mkdtemp()
        settings.CLOUDSYNC_WAIT = 1.
        settings.DATABASE_PATH = os.environ.get('DB_URL', 'postgres://postgres:postgres@localhost/')
        settings.STORAGE_PATH  = self.storage_path
        try:
            os.makedirs('./tmp/') # TODO override app.config['TEMP_STORAGE'] with self.storage_path?
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        settings.ACCOUNTS_API_ENABLED = False
        os.chmod(settings.STORAGE_PATH, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        def mockdc():
            class MockDc(object):
                def address(self, ident):
                    return '0'

                def balance(self):
                    return 0.

            return MockDc()
        settings.DATACOIN_OVERRIDE = mockdc

#       db_name = self.__class__.__name__ + str(int(time.time()))
        db_name = self.__class__.__name__
        self.db = self._init_db(settings.DATABASE_PATH, db_name)

        self.app = web_core.app.test_client()

    def _init_db(self, database_path, db_name):
        '''Initialize the database to a known state.
        '''
        conn = psycopg2.connect(database_path)
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute('DROP DATABASE {}'.format(db_name))
            except ProgrammingError as e:
                pass

            cursor.execute('CREATE DATABASE {}'.format(db_name))
            with open('tests/test_db_teardown.sql') as f:
                cursor.execute(f.read())

            with open('tests/test_db.sql') as f:
                cursor.execute(f.read())

        return conn

    def _find(self, filehash):
        response = self.app.get('/api/find/{}'.format(filehash))

        return response

    def _download(self, filehash, key):
        response = self.app.get('/api/download/{}'.format(filehash))

        if response.status_code != 200:
            raise self.FailedResponseException('Failed download', response)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(response.data)
            f.close()

            file_encryptor.convergence.decrypt_file_inline(f.name, codecs.decode(key, 'hex_codec'))

        with open(f.name) as f_:
            contents = f_.read()

        os.unlink(f.name)

        return contents


    def _upload(self, contents):
        response = self.app.post('/api/upload', data={
            'file': (BytesIO(contents), self.__class__.__name__),
        }, follow_redirects=True)

        if  response.status_code != status.HTTP_201_CREATED:
            raise self.FailedResponseException('Failed upload', response)
        fields = flask.json.loads(response.data)

        return fields['filehash'], fields['key']

    def test_find(self):
        '''Test GET /api/find/[hash]
        '''
        contents = os.urandom(self.SAMPLE_UPLOAD_SIZE_BYTES)
        filehash, key = self._upload(contents)

        WebCore().cloud.cloud_sync()

        response = self._find(filehash)
        assert status.is_success(response.status_code)

        lookup = flask.json.loads(response.data)

        assert 'error' not in lookup
        assert lookup['filesize'] == self.SAMPLE_UPLOAD_SIZE_BYTES
        assert lookup['filehash'] == filehash


        # Hash not found case:
        response = self._find('bogushash')
        assert status.is_client_error(response.status_code)
        lookup = flask.json.loads(response.data)

        assert 'error' in lookup
        assert 'filesize' not in lookup

    def test_upload(self):
        '''Test POST /api/upload
        '''
        contents = b'i' * self.SAMPLE_UPLOAD_SIZE_BYTES
        filehash, key = self._upload(contents)

        filename = '{}_{}'.format(filehash[:7], self.__class__.__name__)
        file_path = os.path.join(self.storage_path, filename)
        file_stat = os.stat(file_path)

        assert len(contents) == file_stat.st_size
        # file must not be executable
        assert (stat.S_IXUSR & file_stat.st_mode) == 0
        assert (stat.S_IXGRP & file_stat.st_mode) == 0
        assert (stat.S_IXOTH & file_stat.st_mode) == 0

        new_contents = self._download(filehash, key)

        assert contents == new_contents


    def test_upload_nostorage(self):
        '''Test file upload when the backend storage is unavailable.
        '''
        os.chmod(settings.STORAGE_PATH, ~stat.S_IRWXU)
        try:
            contents = os.urandom(self.SAMPLE_UPLOAD_SIZE_BYTES)

            with self.assertRaises(self.FailedResponseException) as upl_exc:
                filehash = self._upload(contents)

            assert status.is_server_error(upl_exc.exception.response.status_code)
        finally:
            os.chmod(settings.STORAGE_PATH, stat.S_IRWXU)

    def test_download_invalid_hash(self):
        '''Test GET /api/download with an invalid hash
        '''
        with self.assertRaises(self.FailedResponseException) as down_exc:
            self._download('bogushash', 'boguskey')

        assert status.is_client_error(down_exc.exception.response.status_code)

    def test_status(self):
        '''Test GET /api/status
        '''
        response = self.app.get('/api/status')

        assert status.is_success(response.status_code)

        status_ = flask.json.loads(response.data)
        assert 'bandwidth' in status_
        assert 'storage' in status_ 
        assert 'sync' in status_ 

    @unittest.skip('this causes flask/werkzeug to fill memory, is this a real DoS?')
    def test_malicious_upload(self):
        '''Test POST /api/upload with malicious content
        '''
        # Ultimately, a node must have a ceiling at which
        #  it stops accepting uploaded content.
        class MaliciousUpload(object):
            def read(self, length):
                return bytes([1] * length)

            def close(self):
                pass

        response = self.app.post('/api/upload', data={
            'file': (MaliciousUpload(), 'malicious_'),
        }, follow_redirects=True)
        assert status.is_client_error(response.status_code)

    def tearDown(self):
        with self.db.cursor() as cursor:
            with open('tests/test_db_teardown.sql') as f:
                cursor.execute(f.read())

        self.db.close()
        shutil.rmtree(self.storage_path)

if __name__ == '__main__':
    unittest.main()
