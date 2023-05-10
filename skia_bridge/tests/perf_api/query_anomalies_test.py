# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import absolute_import

import json
import sys
from pathlib import Path
import unittest

app_path = Path(__file__).parent.parent.parent
if str(app_path) not in sys.path:
  sys.path.insert(0, str(app_path))

from application import app
from google.cloud import datastore

import mock


class QueryAnomaliesTest(unittest.TestCase):

  def setUp(self):
    self.client = app.Create().test_client()


  @mock.patch('application.perf_api.datastore_client'
              '.DataStoreClient.QueryAnomalies')
  def testNoAnomaliesExist(self, query_mock):

    query_mock.return_value = []
    test_name = 'master/bot/test1/metric'
    with mock.patch('application.perf_api.auth_helper.AuthorizeBearerToken') \
        as auth_mock:
      auth_mock.return_value = True
      response = self.client.post(
          '/anomalies/find',
          data='{"tests":["%s"], "max_revision":"1234", "min_revision":"1233"}'
               % test_name)
      data = response.get_data(as_text=True)
      self.assertEqual('{}\n', data, 'Empty json expected in the response')

  @mock.patch('application.perf_api.datastore_client'
              '.DataStoreClient.QueryAnomalies')
  def testNoAnomaliesFound(self, query_mock):
    test_name = 'master/bot/test1/metric'
    client = datastore.Client()
    def mock_query(tests, min_revision, max_revision):
      start_rev = 1233
      end_rev = 1234
      if test_name in tests and \
         start_rev >= int(min_revision) and end_rev <= int(max_revision):
        test_key1 = client.key('TestMetadata', test_name)
        anomaly_key = client.key('Anomaly', '1111')
        test_anomaly = datastore.entity.Entity(anomaly_key)
        test_anomaly['start_revision'] = start_rev
        test_anomaly['end_revision'] = end_rev
        test_anomaly['test'] = test_key1
        return [test_anomaly]

      return []

    query_mock.side_effect = mock_query

    test_name_2 = 'some/other/test'

    with mock.patch('application.perf_api.auth_helper.AuthorizeBearerToken') \
        as auth_mock:
      auth_mock.return_value = True
      # Search for a test for which anomaly does not exist
      response = self.client.post(
          '/anomalies/find',
          data='{"tests":["%s"], "max_revision":"1234", "min_revision":"1233"}'
               % test_name_2)
      data = response.get_data(as_text=True)
      self.assertEqual('{}\n', data, 'Empty json expected in the response')

      # Search for an existing test anomaly, but a different revision
      response = self.client.post(
          '/anomalies/find',
          data='{"tests":["%s"], "max_revision":"1232", "min_revision":"1230"}'
               % test_name)
      data = response.get_data(as_text=True)
      self.assertEqual('{}\n', data, 'Empty json expected in the response')

  @mock.patch('application.perf_api.datastore_client'
              '.DataStoreClient.QueryAnomalies')
  def testAnomaliesFound(self, query_mock):
    test_name = 'master/bot/test1/metric'
    client = datastore.Client()
    start_rev = 1233
    end_rev = 1234
    test_key1 = client.key('TestMetadata', test_name)
    anomaly_key = client.key('Anomaly', 1111)

    test_anomaly = datastore.entity.Entity(anomaly_key)
    test_anomaly['start_revision'] = start_rev
    test_anomaly['end_revision'] = end_rev
    test_anomaly['test'] = test_key1

    def mock_query(tests, min_revision, max_revision):
      if test_name in tests and \
         start_rev >= int(min_revision) and end_rev <= int(max_revision):
        return [test_anomaly]

      return []

    query_mock.side_effect = mock_query
    with mock.patch('application.perf_api.auth_helper.AuthorizeBearerToken') \
        as auth_mock:
      auth_mock.return_value = True
      response = self.client.post(
          '/anomalies/find',
          data='{"tests":["%s"], "max_revision":"1234", "min_revision":"1233"}'
               % test_name)
      data = response.get_data(as_text=True)
      response_data = json.loads(data)
      self.assertIsNotNone(response_data)
      anomaly_list = response_data[test_name]
      self.assertIsNotNone(anomaly_list, 'Anomaly list for test expected.')
      self.assertEqual(1, len(anomaly_list), 'One anomaly expected in list')
      anomaly_data = json.loads(anomaly_list[0])
      self.assertEqual(test_name, anomaly_data['test_path'])
      self.assertEqual(test_anomaly['start_revision'],
                       anomaly_data['start_revision'])
      self.assertEqual(test_anomaly['end_revision'],
                       anomaly_data['end_revision'])


if __name__ == '__main__':
  unittest.main()
