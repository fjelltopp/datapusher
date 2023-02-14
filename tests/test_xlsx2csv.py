# -*- coding: utf-8 -*-
'''
Test the whole datapusher but mock the CKAN datastore.
'''

import json
import logging
import os
import httpretty
import datapusher.main as main
import datapusher.jobs as jobs
from datapusher.xlsx2csv import convert
import pandas

os.environ['JOB_CONFIG'] = os.path.join(os.path.dirname(__file__),
                                        'settings_test.py')

app = main.serve_test()


def join_static_path(filename):
    return os.path.join(os.path.dirname(__file__), 'static', filename)


def get_static_file(filename):
    return open(join_static_path(filename), mode='rb').read()


class TestXLSX():
    @classmethod
    def setup_class(cls):
        cls.host = 'www.ckan.org'
        cls.api_key = 'my-key'
        cls.resource_id = 'foo-bar-42'

    def register_urls(self):
        source_url = 'http://www.source.org/static/4_anc_estimates.xlsx'
        httpretty.register_uri(httpretty.GET, source_url,
                               body=get_static_file('4_anc_estimates.xlsx'),
                               content_type="application/vnd.ms-excel")

        res_url = 'http://www.ckan.org/api/3/action/resource_show'
        httpretty.register_uri(httpretty.POST, res_url,
                               body=json.dumps({
                                   'success': True,
                                   'result': {
                                       'id': '32h4345k34h5l345',
                                       'name': 'short name',
                                       'url': source_url,
                                       'format': 'XLSX'
                                   }
                               }),
                               content_type="application/json")

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

    def test_convert_xlsx_to_csv(self):
        log = logging.getLogger(__name__)
        xlsx = open(file=join_static_path('4_anc_estimates.xlsx'), mode='rb')
        csv_from_xlsx = convert(xlsx, log)
        excel_from_csv = pandas.read_csv(csv_from_xlsx)
        csv = open(join_static_path('4_anc_estimates.csv'))
        csv_from_file = pandas.read_csv(csv)
        assert excel_from_csv.equals(csv_from_file)

    @httpretty.activate
    def test_xlsx(self):
        self.register_urls()
        data = {
            'api_key': self.api_key,
            'job_type': 'push_to_datastore',
            'metadata': {
                'ckan_url': 'http://%s/' % self.host,
                'resource_id': self.resource_id
            }
        }

        jobs.push_to_datastore('fake_id', data)
