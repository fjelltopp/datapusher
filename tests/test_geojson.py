# -*- coding: utf-8 -*-
'''
Test the whole datapusher but mock the CKAN datastore.
'''

import os
import json
import unittest
import logging
import httpretty
import pandas
import json
import datapusher.main as main
import datapusher.jobs as jobs
import ckanserviceprovider.util as util
from datapusher.geojson2csv import convert
from io import StringIO

os.environ['JOB_CONFIG'] = os.path.join(os.path.dirname(__file__),
                                        'settings_test.py')

app = main.serve_test()


def join_static_path(filename):
    return os.path.join(os.path.dirname(__file__), 'static', filename)


def get_static_file(filename):
    return open(join_static_path(filename)).read()


class TestGeoJSON(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.host = 'www.ckan.org'
        cls.api_key = 'my-key'
        cls.resource_id = 'foo-bar-42'

    def register_urls(self):
        source_url = 'http://www.source.org/static/simple.geojson'
        httpretty.register_uri(
            httpretty.GET,
            source_url,
            body=get_static_file('simple_input.geojson'),
            content_type="application/json"
        )
        res_url = 'http://www.ckan.org/api/3/action/resource_show'
        httpretty.register_uri(
            httpretty.POST,
            res_url,
            body=json.dumps({
                'success': True,
                'result': {
                    'id': '32h4345k34h5l345',
                    'name': 'Malawi GeoJSON',
                    'url': source_url,
                    'format': 'GeoJSON'
                }
            }),
            content_type="application/json"
        )
        resource_update_url = 'http://www.ckan.org/api/3/action/resource_update'
        httpretty.register_uri(httpretty.POST, resource_update_url,
                               body='{"success": true}',
                               content_type="application/json")

        datastore_del_url = 'http://www.ckan.org/api/3/action/datastore_delete'
        httpretty.register_uri(httpretty.POST, datastore_del_url,
                               body='{"success": true}',
                               content_type="application/json")

        datastore_url = 'http://www.ckan.org/api/3/action/datastore_create'
        httpretty.register_uri(httpretty.POST, datastore_url,
                               body='{"success": true}',
                               content_type="application/json")

        datastore_check_url = 'http://www.ckan.org/api/3/action/datastore_search'
        httpretty.register_uri(httpretty.POST, datastore_check_url,
                               body=json.dumps({'success': True}),
                               content_type='application/json')

    @httpretty.activate
    def test_integration_simple_geojson(self):
        self.register_urls()
        data = {
            'api_key': self.api_key,
            'job_type': 'push_to_datastore',
            'metadata': {
                'ckan_url': 'http://{}/'.format(self.host),
                'resource_id': self.resource_id
            }
        }
        jobs.push_to_datastore('fake_id', data)

    def test_convert_simple_geojson(self):
        log = logging.getLogger(__name__)
        geojson = open(join_static_path('simple_input.geojson'))
        output_csv = convert(geojson, log)
        output_csv = pandas.read_csv(output_csv)
        expected_csv = pandas.read_csv(join_static_path('simple_output.csv'))
        self.assertEqual(set(output_csv.columns), set(expected_csv.columns))
        output_csv = output_csv[expected_csv.columns]
        output_geometry = output_csv.pop('geometry')
        expected_geometry = expected_csv.pop('geometry')
        pandas.util.testing.assert_frame_equal(output_csv, expected_csv)
        for i, el in enumerate(output_geometry):
            self.assertDictEqual(json.loads(expected_geometry[i]), json.loads(el))

    def test_convert_malawi(self):
        log = logging.getLogger(__name__)
        geojson = open(join_static_path('malawi_input.geojson'))
        output_csv = convert(geojson, log)
        output_csv = pandas.read_csv(output_csv)
        expected_csv = pandas.read_csv(join_static_path('malawi_output.csv'))
        self.assertEqual(set(output_csv.columns), set(expected_csv.columns))
        output_csv = output_csv[expected_csv.columns]
        output_geometry = output_csv.pop('geometry')
        expected_geometry = expected_csv.pop('geometry')
        pandas.util.testing.assert_frame_equal(output_csv, expected_csv)
        for i, el in enumerate(output_geometry):
            self.assertDictEqual(json.loads(expected_geometry[i]), json.loads(el))

    def test_convert_no_features(self):
        log = logging.getLogger(__name__)
        geojson = get_static_file('simple_input.geojson')
        geojson = json.loads(geojson)
        geojson.pop('features')
        geojson = StringIO(json.dumps(geojson))
        self.assertRaises(util.JobError, convert, geojson, log)

    def test_convert_no_properties(self):
        log = logging.getLogger(__name__)
        geojson = get_static_file('simple_input.geojson')
        geojson = json.loads(geojson)
        geojson['features'][0].pop('properties')
        geojson = StringIO(json.dumps(geojson))
        self.assertRaises(util.JobError, convert, geojson, log)

    def test_convert_no_geometry(self):
        log = logging.getLogger(__name__)
        geojson = get_static_file('simple_input.geojson')
        geojson = json.loads(geojson)
        geojson['features'][0].pop('geometry')
        geojson = StringIO(json.dumps(geojson))
        self.assertRaises(util.JobError, convert, geojson, log)

    def test_convert_different_properties(self):
        log = logging.getLogger(__name__)
        geojson = get_static_file('simple_input.geojson')
        geojson = json.loads(geojson)
        geojson['features'][0]['properties'].pop('area_id')
        geojson = StringIO(json.dumps(geojson))
        self.assertRaises(util.JobError, convert, geojson, log)
