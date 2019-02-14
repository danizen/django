from django.test import TestCase, override_settings
from django.db import connection
from .models import WorkSet

import ipdb


class TestTicket30124(TestCase):

    expected_work_names = [
        'Flying Car',
        'Jetpack',
        'Robot',
    ]

    def setUp(self):
        ws = WorkSet.objects.create(name='Fubar')
        for name in self.expected_work_names:
            ws.works.create(name=name)
        self.ws = WorkSet.objects.filter(name='Fubar').first()

    @override_settings(DEBUG=True)
    def test_iterate(self):
        actual_work_names = []
        for work in self.ws.works.all().only('name').order_by('name'):
            actual_work_names.append(work.name)
        self.assertEqual(actual_work_names, self.expected_work_names)
        self.assertEqual(len(connection.queries), 1)

