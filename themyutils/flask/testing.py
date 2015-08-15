# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from flask.ext.testing import TestCase
import logging

logger = logging.getLogger(__name__)

__all__ = [b"FlaskIntegrationTestCase"]


def FlaskIntegrationTestCase(app, db):
    class _FlaskIntegrationTestCase(TestCase):
        def create_app(self):
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
            return app

        def setUp(self):
            self.assertIn("sqlite://", repr(db))
            db.create_all()

        def tearDown(self):
            db.session.remove()
            db.drop_all()

    return _FlaskIntegrationTestCase
