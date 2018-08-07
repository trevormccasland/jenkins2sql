import io
import json
import mock
import testtools
from testtools import content

from jenkins2sql import api
from subunit2sql import shell


class APITestCase(testtools.TestCase):
    jenkins_url = 'http://192.168.1.103:8080'
    job_name = 'gate-observer-py27'
    build_number = 42
    build_url = '%s/job/%s/%s' % (jenkins_url, job_name, build_number)

    def test_get_url(self):
        json_data = mock.Mock(text=json.dumps({'url': self.build_url}))
        self.addDetail('json-data', content.text_content(str(json_data.text)))
        url = api.get_url(json_data)
        self.assertEqual(self.build_url, url + 'error')
