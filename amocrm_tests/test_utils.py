# -*- coding: utf-8 -*-
# swagger
import unittest
import json
import requests

from amocrm.test_utils import amomock


class TestUtils(unittest.TestCase):
    login_data = {'USER_LOGIN': 'test', 'USER_HASH': 'test'}

    def setUp(self):
        amomock.set_login_params('test', 'test')

    @amomock.activate
    def test_auth_request(self):
        resp = requests.post('http://test.amocrm/private/api/auth.php',
                             data=self.login_data)
        self.assertEquals(resp.json()['auth'], True)

    @amomock.activate
    def test_invalid_login(self):
        resp = requests.post('http://test.amocrm/private/api/auth.php',
                             data={'USER_LOGIN': 'test', 'USER_HASH': 'test2'})
        self.assertEquals(resp.json()['auth'], False)

    @amomock.activate
    def test_current_getting(self):
        resp = requests.get('http://test.amocrm/private/api/accounts/current',
                            data=self.login_data).json()
        self.assertNotIn('auth', resp)
        self.assertIn('response', resp)
        info = resp['response']['account']
        self.assertIn('id', info)
        self.assertIn('users', info)
        self.assertIn('id', info['users'].pop())
        self.assertIn('custom_fields', info)
        self.assertIn('leads_statuses', info)
        self.assertEqual(len(info['leads_statuses']), 2)

    @amomock.activate
    def test_contacts_getting(self):
        contact = {'name': 'Frog', 'company_name': 'TestsCo'}
        _data = {'add': json.dumps(contact)}
        _data.update(self.login_data)
        requests.post('http://test.amocrm/private/api/contacts/set',
                      data=_data).json()

        contact = {'name': 'SOme', 'company_name': 'SomeCo'}
        _data = {'add': json.dumps(contact)}
        _data.update(self.login_data)
        requests.post('http://test.amocrm/private/api/contacts/set',
                      data=_data).json()

        data = {'limit_rows': 2}
        data.update(self.login_data)
        resp = requests.get('http://test.amocrm/private/api/contacts/list',
                            data=data).json()
        self.assertNotIn('auth', resp)
        self.assertIn('response', resp)
        contacts = resp['response']['contacts']
        self.assertEquals(len(contacts), 2)
        self.assertIn('id', contacts.pop())

    @amomock.activate
    def test_contacts_search(self):
        contact = {'name': 'Frog', 'company_name': 'TestsCo'}
        _data = {'add': json.dumps(contact)}
        _data.update(self.login_data)
        requests.post('http://test.amocrm/private/api/contacts/set',
                             data=_data).json()

        data = {'limit_rows': 1, 'query': 'Frog'}
        data.update(self.login_data)
        resp = requests.get('http://test.amocrm/private/api/contacts/list',
                            data=data).json()
        self.assertNotIn('auth', resp)
        self.assertIn('response', resp)
        contacts = resp['response']['contacts']
        self.assertEquals(len(contacts), 1)
        self.assertEquals('Frog', contacts.pop()['name'])

    @amomock.activate
    def test_contact_add(self):
        contact = {'name': 'Frog', 'company_name': 'TestsCo'}
        data = {'add': json.dumps(contact)}
        data.update(self.login_data)
        resp = requests.post('http://test.amocrm/private/api/contacts/set',
                             data=data).json()
        self.assertNotIn('auth', resp)

        # Check adding
        data = {'limit_rows': 1, 'query': 'Frog'}
        data.update(self.login_data)
        resp = requests.get('http://test.amocrm/private/api/contacts/list',
                            data=data).json()
        self.assertNotIn('auth', resp)
        self.assertIn('response', resp)
        contacts = resp['response']['contacts']
        self.assertEquals(len(contacts), 1)
        contact = contacts.pop()
        self.assertEquals('Frog', contact['name'])
        self.assertIn('id', contact)


if __name__ == '__main__':
    unittest.main()
