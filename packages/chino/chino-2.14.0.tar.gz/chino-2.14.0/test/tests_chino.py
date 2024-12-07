import hashlib
import logging
import logging.config
import os
import random
import time
import unittest

import pytz

from chino.api import ChinoAPIClient
from chino.exceptions import CallError
from chino.objects import _DictContent, _Field
from datetime import datetime, timedelta

from . import cfg


__author__ = 'Stefano Tranquillini <stefano@chino.io>'


# logging.config.fileConfig(path.join(path.dirname(__file__), 'logging.conf'))


class BaseChinoTest(unittest.TestCase):
    def setUp(self):
        self.chino = ChinoAPIClient(customer_id=cfg.customer_id,
                                    customer_key=cfg.customer_key,
                                    url=cfg.url, client_id=cfg.client_id,
                                    client_secret=cfg.client_secret,
                                    timeout=3600, force_https=False)
        self.logger = logging.getLogger('test.api')
        self.logger.debug("log")

    def _equals(self, i_d1, i_d2):
        """
        checks if d1 is equal of d2
        """
        if type(i_d1) is not dict:
            d1 = i_d1.to_dict()
        else:
            d1 = i_d1
        if type(i_d2) is not dict:
            d2 = i_d2.to_dict()
        else:
            d2 = i_d2
        for key, value in d1.items():
            if not key in d2:
                self.logger.error("ERROR: Key missing  %s" % key)
                return False
            v2 = d2[key]
            if type(v2) is _DictContent and value:
                if not self._equals(value.to_dict(), v2.to_dict()):
                    return False
            else:
                if not v2 == value:
                    # last update is 99% of the time different, especially after an update
                    if key != 'last_update':
                        self.logger.error(
                            "Value error %s: %s %s " % (key, value, v2))
                        return False
        for key in d2.keys():
            if not key in d1:
                self.logger.error("ERROR: Key missing  %s" % key)
                return False
        return True

    def _has_keys(self, keys, d):
        """
        checks if the dictionary has the keys
        """
        for key in keys:
            if not key in d:
                # self.logger.debug("Key missing  %s: %s" % (key, d))
                self.logger.error("ERROR: Key is missing %s" % key)
                return False
        for key in d.keys():
            if not key in keys:
                self.logger.error(
                    "ERROR: Dictionary has an extra key %s" % key)
                return False

        return True


class UserChinoTest(BaseChinoTest):
    user = None

    def setUp(self):
        super(UserChinoTest, self).setUp()
        fields = [dict(name='first_name', type='string'),
                  dict(name='last_name', type='string'),
                  dict(name='email', type='string'),
                  dict(name='age', type='integer', default=None, indexed=True),
                  dict(name='city', type='string', default=None, indexed=True),
                  ]
        self.us = self.chino.user_schemas.create('test', fields)
        self.us_1 = self.chino.user_schemas.create('test1', fields)
        self.app_list = []

    def tearDown(self):
        # if user has been created we remove it.
        self.logger.debug("tearing down %s", self.user)
        self.chino.auth.set_auth_admin()
        list = self.chino.users.list(self.us._id)
        for user in list.users:
            self.chino.users.delete(user._id, force=True)
        self.chino.user_schemas.delete(self.us._id, force=True)
        if hasattr(self, 'app'):
            self.chino.applications.delete(self.app._id)

        # delete also every Application which was created forthis test
        for app in self.chino.applications.list().to_dict()['applications']:
            self.chino.applications.delete(app['app_id'], force=True)

    def test_list(self):
        list = self.chino.users.list(self.us._id)
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.users)

    def test_bulk_get(self):
        # Add 3 users
        user_values = dict(
            username='', password='12345678',
            attributes=dict(first_name='john', last_name='doe',
                            email='test@chino.io')
        )

        users = []
        for i in range(3):
            # We mix up the schemas of each doc a bit
            schema = self.us._id if i % 2 == 0 else self.us_1._id
            user_values['username'] = f'testing.bulk_get.id.{i}'
            users.append(
                self.chino.users.create(schema, **user_values)
            )

        # Wait for indexing
        time.sleep(3)

        user_ids = [user._id for user in users]
        # We should get 3 docs
        bulk_get_result = self.chino.users.bulk_get(user_ids=user_ids)
        self.assertEqual(3, len(bulk_get_result))

        # This checks the __iter__ method
        for user in bulk_get_result:
            # Check that the ID is one of the ids in the list
            self.assertIn(user._id, user_ids)

        # This checks the __getitem__ method
        for user_id in user_ids:
            # Check that document_id can be used for accessing the document
            # and that the document is not None
            user = bulk_get_result[user_id]
            self.assertIsNotNone(user)
            self.assertEquals(user_id, user._id)

        # Check the to_dict method
        actual_dict = bulk_get_result.to_dict()
        self.assertEqual(3, actual_dict['count'])
        self.assertEqual(3, actual_dict['total_count'])
        self.assertDictEqual({}, actual_dict['errors'])

    def test_CRUD(self):
        NAME = 'test.user.new'
        EDIT = NAME + '.edited'
        user = self.chino.users.create(self.us._id, username=NAME,
                                       password='12345678',
                                       attributes=dict(first_name='john',
                                                       last_name='doe',
                                                       email='test@chino.io'))
        self.user = user
        self.assertIsNotNone(user)
        self.assertEqual(user.username, NAME)
        list = self.chino.users.list(self.us._id)
        # NOTE: this may fail if key are used by someone else.
        ste_2 = self.chino.users.detail(list.users[0]._id)
        self.assertEqual(ste_2.username, NAME)

        user.username = EDIT
        # remove extra params
        data = user.to_dict()
        del data['insert_date']
        del data['last_update']
        del data['groups']
        del data['schema_id']
        ste_2 = self.chino.users.update(**data)
        self.logger.debug(ste_2)
        self.assertEqual(user._id, ste_2._id)
        self.assertEqual(ste_2.username, EDIT)

        ste_2 = self.chino.users.detail(user._id)
        self.assertEqual(ste_2.username, EDIT)

        # partial update
        ste_3 = self.chino.users.partial_update(user._id, **dict(
            attributes=dict(first_name=EDIT)))
        self.assertEqual(user._id, ste_3._id)
        self.assertEqual(ste_3.attributes.first_name, EDIT)
        ste_4 = self.chino.users.detail(user._id)
        self.assertEqual(ste_4.attributes.first_name, EDIT)
        # current not working for main user
        self.assertRaises(CallError, self.chino.users.current)

        # this invalidates the user
        self.chino.users.delete(user._id)

    def test_search(self):
        # add two users
        data = {"first_name": "John", "last_name": "Doe",
                "email": "test+1@chino.io", "age": 42, "city": "Berlin"}
        user_1 = self.chino.users.create(self.us._id, username="user_1",
                                         password="12345678", attributes=data)
        data = {"first_name": "John", "last_name": "Smith",
                "email": "test+2@chino.io", "age": 21, "city": "Rome"}
        user_2 = self.chino.users.create(self.us._id, username="user_2",
                                         password="12345678", attributes=data)

        # wait for users to be indexed
        time.sleep(1)

        # search
        # - all the users with city == 'Berlin'
        query = {"field": "city", "type": "eq", "value": "Berlin"}
        r = self.chino.users.search(self.us._id, query=query)
        self.assertEquals(1, len(r.users))
        self.assertEquals(user_1._id, r.users[0]._id)

        # - all the users with age <= 30
        query = {"field": "age", "type": "lte", "value": 30}
        r = self.chino.users.search(self.us._id, query=query)
        self.assertEquals(1, len(r.users))
        self.assertEquals(user_2._id, r.users[0]._id)

        # - all the users with age < 30 and city == 'Berlin'
        query = {"and": [
            {"field": "age", "type": "lte", "value": 30},
            {"field": "city", "type": "eq", "value": "Berlin"}
        ]}
        r = self.chino.users.search(self.us._id, query=query)
        self.assertEquals(0, len(r.users))

        # - all the users with age < 30 or city == 'Berlin' order by age desc
        query = {"or": [
            {"field": "age", "type": "lte", "value": 30},
            {"field": "city", "type": "eq", "value": "Berlin"}
        ]}
        sort = [{"field": "age", "order": "desc"}]
        r = self.chino.users.search(self.us._id, query=query, sort=sort)
        self.assertEquals(2, len(r.users))
        self.assertEquals(user_1._id, r.users[0]._id)
        self.assertEquals(user_2._id, r.users[1]._id)

        # - same search with inverted order
        sort = [{"field": "age", "order": "asc"}]
        r = self.chino.users.search(self.us._id, query=query, sort=sort)
        self.assertEquals(2, len(r.users))
        self.assertEquals(user_2._id, r.users[0]._id)
        self.assertEquals(user_1._id, r.users[1]._id)

    # @unittest.skip("method disabled locally")
    def test_auth(self):
        # login
        NAME = 'test.user.new'
        EDIT = NAME + '.edited'
        self.app = self.chino.applications.create("test",
                                                  grant_type='password')
        self.chino_user = ChinoAPIClient(customer_id=cfg.customer_id,
                                         customer_key=cfg.customer_key,
                                         url=cfg.url,
                                         client_id=self.app.app_id,
                                         client_secret=self.app.app_secret,
                                         force_https=False)
        user = self.chino.users.create(self.us._id, username=EDIT,
                                       password='12345678',
                                       attributes=dict(first_name='john',
                                                       last_name='doe',
                                                       email='test@chino.io'))
        self.chino_user.users.login(EDIT, '12345678')
        ste_2 = self.chino_user.users.current()
        self.assertEqual(ste_2.username, EDIT)

        self.chino_user.users.refresh()
        # it should be impossible to create the user after login with self.chino_user (no admin access)
        self.assertRaises(CallError, self.chino_user.users.create, self.us._id,
                          username='error', password='12345678',
                          attributes=dict(first_name='john', last_name='doe',
                                          email='test@chino.io'))

        self.chino_user.users.logout()
        self.assertRaises(Exception, self.chino_user.users.login, EDIT, '')

        self.assertRaises(CallError, self.chino.users.current)

    def test_token_introspection(self):
        username = 'test.user.new'
        self.app = self.chino.applications.create(
            "test",
            grant_type='password'
        )
        self.chino_user = ChinoAPIClient(
            customer_id=cfg.customer_id,
            customer_key=cfg.customer_key,
            url=cfg.url,
            client_id=self.app.app_id,
            client_secret=self.app.app_secret,
            force_https=False
        )
        attrs = {'first_name': 'john', 'last_name': 'doe',
                 'email': 'test@chino.io'}
        user = self.chino_user.users.create(self.us._id, username=username,
                                            password='12345678',
                                            attributes=attrs)
        self.chino_user.users.login(username, '12345678')

        # ok, get the token and read data about it
        token = self.chino_user.auth.bearer_token
        expected_data = {'active': True, 'scope': "read write",
                         'client_id': self.app.app_id, 'username': username}
        res = self.chino_user.users.introspect(token)
        for key, value in expected_data.items():
            self.assertIn(key, res)
            self.assertEqual(value, res[key])

        # we also expect the 'exp' key - we cannot know the value
        self.assertIn('exp', res)

        # check that with url param ?uid_type=uuid we have the user_id (uuid)
        # inside the username field
        expected_data['username'] = user.user_id
        res = self.chino_user.users.introspect(token, uid_type='uuid')
        for key, value in expected_data.items():
            self.assertIn(key, res)
            self.assertEqual(value, res[key])

        # we also expect the 'exp' key - we cannot know the value
        self.assertIn('exp', res)

    def test_auth_public(self):
        # login
        NAME = 'test.user.new'
        EDIT = NAME + '.edited'
        self.app = self.chino.applications.create("test",
                                                  grant_type='password',
                                                  client_type='public')
        # Init 'public' client
        self.chino_user = ChinoAPIClient(customer_id=cfg.customer_id,
                                         url=cfg.url,
                                         client_id=self.app.app_id,
                                         client_secret=None,
                                         force_https=False
                                         )
        self.assertIsNone(self.chino_user.auth.client_secret)

        user = self.chino.users.create(self.us._id, username=EDIT,
                                       password='12345678',
                                       attributes=dict(first_name='john',
                                                       last_name='doe',
                                                       email='test@chino.io'))

        self.chino_user.users.login(EDIT, '12345678')
        ste_2 = self.chino_user.users.current()
        self.assertEqual(ste_2.username, EDIT)

        self.chino_user.users.refresh()
        # it should be impossible to create the user after login with self.chino_user (no admin access)
        self.assertRaises(CallError, self.chino_user.users.create, self.us._id,
                          username='error', password='12345678',
                          attributes=dict(first_name='john', last_name='doe',
                                          email='test@chino.io'))

        self.chino_user.users.logout()
        self.assertRaises(Exception, self.chino_user.users.login, EDIT, '')

        self.assertRaises(CallError, self.chino.users.current)

    def test_update_check_reuse(self):
        data = {
            'username': 'antani',
            'password': '12345678',
            'attributes': {
                'first_name': "John",
                'last_name': "Doe",
                'email': 'test@chino.io'
            }
        }
        user = self.chino.users.create(self.us._id, **data)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])

        # UPDATE (PUT)
        # change the password without the `check_reuse` flag: we should succeed
        user_1 = self.chino.users.update(user.user_id, **data)
        self.assertEquals(user.user_id, user_1.user_id)

        # now set the flag, we should get error 400
        with self.assertRaises(CallError) as ctx:
            self.chino.users.update(user.user_id, check_reuse=True, **data)
        exc = ctx.exception
        self.assertEquals(exc.message, "You already used this password")

        # PARTIAL UPDATE (PATCH)
        # change the password without the `check_reuse` flag: we should succeed
        partial = {"password": data['password']}
        user_2 = self.chino.users.partial_update(user.user_id, **partial)
        self.assertEquals(user.user_id, user_2.user_id)

        # now set the flag, we should get error 400
        with self.assertRaises(CallError) as ctx:
            self.chino.users.partial_update(user.user_id, check_reuse=True,
                                            **partial)
        exc = ctx.exception
        self.assertEquals(exc.message, "You already used this password")

    def test_block_user_api(self):
        # call the API (list) with wrong data
        with self.assertRaises(CallError) as ctx:
            self.chino.users.list_blocked_users(user_id="antani")

        with self.assertRaises(CallError) as ctx:
            self.chino.users.list_blocked_users(ip="bad ip")

        # create an app and a user
        self.app = self.chino.applications.create("test",
                                                  grant_type='password')
        user_client = ChinoAPIClient(customer_id=cfg.customer_id,
                                     customer_key=cfg.customer_key,
                                     url=cfg.url,
                                     client_id=self.app.app_id,
                                     client_secret=self.app.app_secret,
                                     force_https=False)

        rnd_n = ''.join([random.choice('1234567890') for _ in range(10)])
        data = {
            'username': "antani" + rnd_n,
            'password': '12345678',
            'attributes': {
                'first_name': "John",
                'last_name': "Doe",
                'email': 'test@chino.io'
            }
        }
        user = self.chino.users.create(self.us._id, **data)
        user.password = data['password']  # store here for later use
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])

        # list blocked users, should be empty
        res = self.chino.users.list_blocked_users()
        self.assertEquals(len(res), 0)

        # now block the user performing n wrong logins
        max_attempts = 20
        while max_attempts:
            max_attempts -= 1
            with self.assertRaises(CallError) as ctx:
                user_client.users.login(user.username, "wrong password")

            if ctx.exception.code == 400:
                continue
            elif ctx.exception.code == 403:
                # user have been blocked
                break

        # call the API (list) now we should have the user blocked
        res = self.chino.users.list_blocked_users()
        self.assertGreater(len(res), 0)

        # filter by user, it should be one
        res = self.chino.users.list_blocked_users(user_id=user.user_id)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['user_id'], user.user_id)
        self.assertEquals(res[0]['username'], user.username)
        self.assertGreater(res[0]['block_ttl'], 0)

        # extract the IP
        ip = res[0]["ip"]

        # we try to login the user with good credentials, we should still get
        # 403 since it's blocked
        with self.assertRaises(CallError) as ctx:
            user_client.users.login(user.username, user.password)
            self.assertEquals(ctx.exception.code, 403)

        # wrong attempts to unblock user
        with self.assertRaises(CallError) as ctx:
            self.chino.users.unblock_user("antani", "127.9.9.1")
            self.assertEquals(ctx.exception.code, 401)

        with self.assertRaises(CallError) as ctx:
            self.chino.users.unblock_user(user.user_id, "bad ip")
            self.assertEquals(ctx.exception.code, 401)

        # this should return 200 cos it's formally correct, but the tuple
        # user-ip does not exist, so nothing changes
        self.chino.users.unblock_user(user.user_id, "8.8.8.8")

        # we filter by exact user_id and ip, we should get our user
        res = self.chino.users.list_blocked_users(user_id=user.user_id, ip=ip)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['user_id'], user.user_id)
        self.assertEquals(res[0]['ip'], ip)

        # we perform a good unblock and check that user is unblocked
        self.chino.users.unblock_user(user.user_id, ip)
        res = self.chino.users.list_blocked_users(user_id=user.user_id, ip=ip)
        self.assertEquals(len(res), 0)

        # we try to login the user, we should succeed
        user_client.users.login(user.username, user.password)

        # try to call the unblock API with the user auth: not allowed
        with self.assertRaises(CallError) as ctx:
            user_client.users.list_blocked_users()

        with self.assertRaises(CallError) as ctx:
            user_client.users.unblock_user(user_id=user.user_id, ip=ip)


class ApplicationsChinoTest(BaseChinoTest):
    user = None

    def setUp(self):
        super(ApplicationsChinoTest, self).setUp()

    def tearDown(self):
        # if user has been created we remove it.
        self.logger.debug("tearing down %s", self.user)

    def test_CRUD(self):
        app = self.chino.applications.create(name='tesssst_confidential',
                                             grant_type='password')
        app_public = self.chino.applications.create(name='test_public',
                                                    grant_type='password',
                                                    client_type='public')

        app_public1 = self.chino.applications.detail(app_public._id)
        self.assertEqual(app_public._id, app_public1._id)
        self.assertEqual(app_public.app_name, app_public1.app_name)

        newname = 'test_confidential'
        self.chino.applications.update(app._id, name=newname)
        app1 = self.chino.applications.detail(app._id)
        self.assertEqual(app1.app_name, newname)

        apps = self.chino.applications.list()
        self.chino.applications.delete(app_public1._id, force=True)
        self.chino.applications.delete(app1._id, force=True)


# @unittest.skip("Class disabled locally")
class GroupChinoTest(BaseChinoTest):
    def tearDown(self):
        list = self.chino.groups.list()
        for group in list.groups:
            self.chino.groups.delete(group._id, force=True)

        list = self.chino.user_schemas.list()
        for schema in list.user_schemas:
            self.chino.user_schemas.delete(schema._id, force=True)

    def test_list(self):
        list = self.chino.groups.list()
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.groups)

    def test_list_filter(self):
        # create three groups with different names
        now = int(time.time())
        names = ['%s abc1' % now, '%s abc2' % now, 'other %s' % now]
        for name in names:
            self.chino.groups.create(name)

        # search repos with '<now>' in the description: should be 3
        list_all = self.chino.groups.list(name=now)
        self.assertEquals(len(list_all.groups), 3)

        # search repos with '<now> abc' in the description
        list_abc = self.chino.groups.list(name='%s abc' % now)
        self.assertEquals(len(list_abc.groups), 2)

        # search repos with '<now> other' in the description
        list_other = self.chino.groups.list(name='other %s' % now)
        self.assertEquals(len(list_other.groups), 1)

    def test_CRUD(self):
        group_created = self.chino.groups.create('testing', attributes=dict(
            hospital='test'))
        self.assertTrue(self._equals(group_created.attributes.to_dict(),
                                     dict(hospital='test')))
        self.assertEqual(group_created.group_name, 'testing')
        # NOTE: this may fail
        list = self.chino.groups.list()
        group = list.groups[0]
        details = self.chino.groups.detail(group._id)
        # print group.to_dict()
        # print details.to_dict()
        self.assertTrue(self._equals(details, group), "\n %s \n %s \n" % (
        details.to_json(), group.to_json()))
        group.group_name = 'updatedtesting'
        # remove extra params
        data = group.to_dict()
        del data['insert_date']
        del data['last_update']
        self.chino.groups.update(**data)
        details = self.chino.groups.detail(group._id)
        self.assertTrue(self._equals(details, group), "\n %s \n %s \n" % (
        details.to_json(), group.to_json()))
        self.chino.groups.delete(details._id)

    def test_group_user(self):
        group_created = self.chino.groups.create('testing', attributes=dict(
            hospital='test'))
        fields = [dict(name='first_name', type='string'),
                  dict(name='last_name', type='string'),
                  dict(name='email', type='string')]
        us = self.chino.user_schemas.create('test', fields)

        user = self.chino.users.create(us._id, username="ste",
                                       password='12345678',
                                       attributes=dict(first_name='john',
                                                       last_name='doe',
                                                       email='test@chino.io'))
        self.user = user
        # if nothing is raised, then fine
        add = self.chino.groups.add_user(group_created._id, user._id)
        users = self.chino.groups.list_users(group_created._id)
        self.assertEqual(users.paging.count, 1)
        users = self.chino.groups.list_users(group_created._id, offset=2)
        self.assertEqual(users.paging.count, 0)
        rem = self.chino.groups.del_user(group_created._id, user._id)
        # delete the user at the end
        self.chino.groups.delete(group_created._id, force=True)
        self.chino.users.delete(user._id, force=True)

    def test_add_all_users_to_group(self):
        # create a group
        group = self.chino.groups.create('testing', attributes={})

        # create a user schema
        us = self.chino.user_schemas.create('test', [])

        # create 5 users
        user_ids = []
        for i in range(5):
            username = "user_%s" % i
            pwd = "pwd_%s_123456"
            user = self.chino.users.create(us._id, username=username,
                                           password=pwd, attributes={})
            user_ids.append(user.user_id)

        # add all the users to group - if ok no exception is raised
        self.chino.groups.add_users_to_group(group.group_id, us._id)

        # check that all the users are actually in the group
        group_users = self.chino.groups.list_users(group.group_id)
        group_user_ids = [u.user_id for u in group_users]
        self.assertEquals(set(user_ids), set(group_user_ids))


class RepositoryChinoTest(BaseChinoTest):
    def setUp(self):
        super(RepositoryChinoTest, self).setUp()
        list = self.chino.repositories.list()
        for repo in list.repositories:
            self.chino.repositories.delete(repo._id, force=True,
                                           all_content=True)

    def tearDown(self):
        list = self.chino.repositories.list()
        for repo in list.repositories:
            self.chino.repositories.delete(repo._id, force=True,
                                           all_content=True)

    def test_list(self):
        list = self.chino.repositories.list()
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.repositories)

    def test_list_filter(self):
        # create three repositories with different descriptions
        now = int(time.time())
        descriptions = ['%s abc1' % now, '%s abc2' % now, 'other %s' % now]
        repos = [self.chino.repositories.create(d) for d in descriptions]

        # search repos with '<now>' in the description: should be 3
        list_all = self.chino.repositories.list(descr=now)
        self.assertEquals(len(list_all.repositories), 3)

        # search repos with '<now> abc' in the description
        list_abc = self.chino.repositories.list(descr='%s abc' % now)
        self.assertEquals(len(list_abc.repositories), 2)

        # search repos with '<now> other' in the description
        list_other = self.chino.repositories.list(descr='other %s' % now)
        self.assertEquals(len(list_other.repositories), 1)

    def test_crud(self):
        created = self.chino.repositories.create('test')
        self.assertEqual(created.description, 'test')
        first = self.chino.repositories.list().repositories[0]
        self.assertTrue(
            self._equals(created.to_dict(), first.to_dict()),
            "\n %s \n %s \n" % (created.to_json(), first.to_json()))
        first.description = 'edited'

        resp = self.chino.repositories.update(first._id,
                                              description=first.description)
        detail = self.chino.repositories.detail(first._id)
        self.assertTrue(
            self._equals(resp.to_dict(), detail.to_dict()),
            "\n %s \n %s \n" % (resp.to_json(), detail.to_json()))

        self.chino.repositories.delete(first._id)


class SchemaChinoTest(BaseChinoTest):
    def setUp(self):
        super(SchemaChinoTest, self).setUp()
        self.repo = self.chino.repositories.create('test')._id

    def tearDown(self):
        list = self.chino.schemas.list(self.repo)
        for schema in list.schemas:
            self.chino.schemas.delete(schema._id, force=True, all_content=True)
        self.chino.repositories.delete(self.repo, True)

    def test_list(self):
        list = self.chino.schemas.list(self.repo)
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.schemas)

    def test_list_filter(self):
        # create three schemas with different descriptions
        now = int(time.time())
        descriptions = ['%s abc 1' % now, '%s abc 2' % now, 'other %s' % now]
        struct = [{"name": "test", "type": "string"}]
        for description in descriptions:
            self.chino.schemas.create(self.repo, description, fields=struct)

        # now search for them using filter
        list_all = self.chino.schemas.list(self.repo, descr=now)
        self.assertEquals(len(list_all.schemas), 3)
        list_abc = self.chino.schemas.list(self.repo, descr='%s abc' % now)
        self.assertEquals(len(list_abc.schemas), 2)
        list_other = self.chino.schemas.list(self.repo, descr='other %s' % now)
        self.assertEquals(len(list_other.schemas), 1)

    def test_crud(self):
        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        created = self.chino.schemas.create(self.repo, 'test', fields)
        list = self.chino.schemas.list(self.repo)
        detail = self.chino.schemas.detail(list.schemas[0]._id)
        detail2 = self.chino.schemas.detail(created._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))

        detail.structure.fields.append(_Field('string', 'new one'))
        data = detail.to_dict()
        del data['repository_id']
        del data['insert_date']
        del data['last_update']
        self.chino.schemas.update(**data)
        detail2 = self.chino.schemas.detail(detail._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))
        self.chino.schemas.delete(detail._id)

    def test_convert_datatype(self):
        # create a schema
        fields = [{'name': 'numeric', 'type': 'float'}]
        created = self.chino.schemas.create(self.repo, 'test_ct', fields)

        # convert the field to int
        new_fields = {'numeric': 'integer'}
        defaults = {'numeric': 42}
        res = self.chino.schemas.convert_datatypes_submit(created.schema_id,
                                                          fields=new_fields,
                                                          defaults=defaults)
        self.assertIn('message', res)

        # now check the status
        status = self.chino.schemas.convert_datatypes_status(created.schema_id)
        keys = ['start', 'end', 'status']
        for key in keys:
            self.assertIn(key, status)

    def test_dump__json(self):
        # create a schema
        fields = [{'name': 'numeric', 'type': 'integer', 'indexed': True}]
        created = self.chino.schemas.create(self.repo, 'test_dump', fields)

        # add 10 documents
        for i in range(10):
            record = {'numeric': i}
            self.chino.documents.create(created.schema_id, record,
                                        consistent=True)

        # submit the dump job for JSON format
        query = {"field": "numeric", "type": "lt", "value": 5}
        sort = [{"field": "numeric", "order": "asc"}]
        res = self.chino.schemas.dump_submit(
            created.schema_id, query=query, sort=sort
            # format='json' is the default
        )
        self.assertIn('dump_id', res)
        dump_id = res['dump_id']

        timeout = 10
        while timeout:
            res = self.chino.schemas.dump_status(dump_id)
            if res['status'] == 'COMPLETED':
                break
            time.sleep(1)
            timeout -= 1

        self.assertEqual(res['status'], 'COMPLETED')

        # now download the file
        dump = self.chino.schemas.dump_download(dump_id)

        # check that the file is not corrupted
        self.assertTrue(dump.hash_matches())

        # should keep 5 records
        self.assertEqual(5, dump.records_count)
        self.assertEqual(5, len(dump.json))

        # check the records' content
        for i, record in enumerate(dump.json):
            self.assertEqual(i, record['numeric'])
                
    def test_dump__csv(self):
        # create a schema
        fields = [{'name': 'numeric', 'type': 'integer', 'indexed': True}]
        created = self.chino.schemas.create(self.repo, 'test_dump', fields)

        # add 10 documents
        for i in range(10):
            record = {'numeric': i}
            self.chino.documents.create(created.schema_id, record,
                                        consistent=True)

        # submit the dump job for CSV format
        query = {"field": "numeric", "type": "lt", "value": 5}
        sort = [{"field": "numeric", "order": "asc"}]
        res = self.chino.schemas.dump_submit(
            created.schema_id, query=query, sort=sort,
            format='csv'
        )
        self.assertIn('dump_id', res)
        dump_id = res['dump_id']

        timeout = 10
        while timeout:
            res = self.chino.schemas.dump_status(dump_id)
            if res['status'] == 'COMPLETED':
                break
            time.sleep(1)
            timeout -= 1

        self.assertEqual(res['status'], 'COMPLETED')

        # now download the file
        dump = self.chino.schemas.dump_download(dump_id)

        # check that the file is not corrupted
        self.assertTrue(dump.hash_matches())

        # should keep 5 records + 1 line of headers
        self.assertEqual(5, dump.records_count)
        self.assertEqual(6, len(dump.csv))

        # check the records' content, ordered
        for i, record in enumerate(dump.csv):
            if i == 0:
                self.assertEqual('_id', record[0])
                self.assertEqual('numeric', record[1])
            else:
                self.assertEqual(str(i - 1), record[1])


class UserSchemaChinoTest(BaseChinoTest):
    def setUp(self):
        super(UserSchemaChinoTest, self).setUp()

    def tearDown(self):
        list = self.chino.user_schemas.list()
        for repo in list.user_schemas:
            self.chino.user_schemas.delete(repo._id, force=True)

    def test_list(self):
        list = self.chino.user_schemas.list()
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.user_schemas)

    def test_list_filter(self):
        # create three user schemas with different descriptions
        now = int(time.time())
        descriptions = ['%s abc 1' % now, '%s abc 2' % now, 'other %s' % now]
        for description in descriptions:
            self.chino.user_schemas.create(description, [])

        # now search for them using filter
        list_all = self.chino.user_schemas.list(descr=now)
        self.assertEquals(len(list_all.user_schemas), 3)
        list_abc = self.chino.user_schemas.list(descr='%s abc' % now)
        self.assertEquals(len(list_abc.user_schemas), 2)
        list_other = self.chino.user_schemas.list(descr='other %s' % now)
        self.assertEquals(len(list_other.user_schemas), 1)

    def test_crud(self):
        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        created = self.chino.user_schemas.create('test', fields)
        list = self.chino.user_schemas.list()
        self.assertGreater(list.paging.count, 0)
        id = 0
        for schema in list.user_schemas:
            if schema._id == created._id:
                id = schema._id
        detail = self.chino.user_schemas.detail(id)
        detail2 = self.chino.user_schemas.detail(created._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))

        detail.structure.fields.append(_Field('string', 'new one'))
        data = detail.to_dict()
        del data['insert_date']
        del data['last_update']
        del data['user_schema_id']
        del data['groups']
        self.chino.user_schemas.update(detail.user_schema_id, **data)
        detail2 = self.chino.user_schemas.detail(detail._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))
        self.chino.user_schemas.delete(detail._id, force=True)


    def test_dump(self):
        # create a user schema
        fields = [{'name': 'numeric', 'type': 'integer', 'indexed': True}]
        created = self.chino.user_schemas.create('test_dump', fields)

        # add 10 users
        password = '12345678'
        for i in range(10):
            record = {'numeric': i}
            username = "user_{}".format(i)
            self.chino.users.create(created.user_schema_id, username=username,
                                    password=password, attributes=record)

        # submit the dump job
        query = {"field": "numeric", "type": "lt", "value": 5}
        sort = [{"field": "numeric", "order": "asc"}]
        res = self.chino.user_schemas.dump_submit(created.user_schema_id,
                                                  query=query, sort=sort)
        self.assertIn('dump_id', res)
        dump_id = res['dump_id']

        timeout = 15  # with 10 is not enough to complete
        while timeout:
            res = self.chino.user_schemas.dump_status(dump_id)
            if res['status'] == 'COMPLETED':
                break
            time.sleep(1)
            timeout -= 1

        self.assertEqual(res['status'], 'COMPLETED')

        # now download the file
        dump = self.chino.user_schemas.dump_download(dump_id)

        # check that the file is not corrupted
        self.assertTrue(dump.hash_matches())

        # should keep 5 records
        self.assertEqual(5, dump.records_count)
        self.assertEqual(5, len(dump.json))

        # check the records' content
        for i, record in enumerate(dump.json):
            self.assertEqual(i, record['numeric'])

        # now test the csv format
        res = self.chino.user_schemas.dump_submit(created.user_schema_id,
                                                  query=query, sort=sort,
                                                  format='csv')
        self.assertIn('dump_id', res)
        dump_id = res['dump_id']

        timeout = 15  # with 10 is not enough to complete
        while timeout:
            res = self.chino.user_schemas.dump_status(dump_id)
            if res['status'] == 'COMPLETED':
                break
            time.sleep(1)
            timeout -= 1

        self.assertEqual(res['status'], 'COMPLETED')

        # now download the file
        dump = self.chino.user_schemas.dump_download(dump_id)

        # check that the file is not corrupted
        self.assertTrue(dump.hash_matches())

        # should keep 5 records + 1 line of headers
        self.assertEqual(5, dump.records_count)
        self.assertEqual(6, len(dump.csv))

        # check the records' content, ordered
        for i, record in enumerate(dump.csv):
            if i == 0:
                self.assertEqual('_id', record[0])
                self.assertEqual('numeric', record[1])
            else:
                self.assertEqual(str(i - 1), record[1])


class CollectionChinoTest(BaseChinoTest):
    def setUp(self):
        super(CollectionChinoTest, self).setUp()

        self.repo = self.chino.repositories.create('test')._id
        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        self.schema = self.chino.schemas.create(self.repo, 'test', fields)._id
        fields = [dict(name='fieldString', type='text')]

    def tearDown(self):
        list = self.chino.collections.list()
        for coll in list.collections:
            self.chino.collections.delete(coll._id, force=True)

        list = self.chino.documents.list(self.schema)
        for doc in list.documents:
            self.chino.documents.delete(doc._id, force=True)
        self.chino.schemas.delete(self.schema, True)
        self.chino.repositories.delete(self.repo, force=True, all_content=True)

    def test_list(self):
        list = self.chino.user_schemas.list()
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.user_schemas)

    def test_list_filter(self):
        # create a collection and two documents. Add one doc to the collection
        # then list the collections filtering by document

        # create the collection
        coll = self.chino.collections.create("test_")

        # create the docs
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')

        doc1 = self.chino.documents.create(self.schema, content=content)
        doc2 = self.chino.documents.create(self.schema, content=content)

        # add the doc1 to the collection
        self.chino.collections.add_document(coll._id, doc1._id)

        # list the collections filtering by doc1: should be 1
        list_1 = self.chino.collections.list(document_id=doc1._id)
        self.assertEquals(len(list_1.collections), 1)

        # list the collections filtering by doc2: should be 0
        list_2 = self.chino.collections.list(document_id=doc2._id)
        self.assertEquals(len(list_2.collections), 0)

    def test_crud(self):
        created = self.chino.collections.create("test_")
        list = self.chino.collections.list()
        detail = self.chino.collections.detail(list.collections[0]._id)
        detail2 = self.chino.collections.detail(created._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))
        self.chino.collections.update(detail._id, name='test2')
        detail2 = self.chino.collections.detail(detail._id)
        self.assertTrue(detail2.name == 'test2')
        self.chino.collections.delete(detail._id)

    def test_search(self):
        ids = []
        for i in range(10):
            created = self.chino.collections.create("test" + str(i))
            ids.append(created._id)

        res = self.chino.collections.search('test', contains=True)
        self.assertEqual(res.paging.total_count, 10)
        res = self.chino.collections.search('test2', contains=False)
        for collection in res.collections:
            self.assertTrue(collection.name.startswith('test'))
        self.assertEqual(res.paging.total_count, 1)
        self.assertEqual(res.collections[0].name, 'test2')
        for id in ids:
            self.chino.collections.delete(id, True)

    def test_docs(self):
        repo = self.chino.repositories.create('test')._id
        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        schema = self.chino.schemas.create(repo, 'test', fields)._id
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')
        document = self.chino.documents.create(schema, content=content)
        collection = self.chino.collections.create("test")
        l = self.chino.collections.list_documents(collection._id)
        self.assertEqual(l.paging.count, 0)
        self.chino.collections.add_document(collection._id, document._id)
        l = self.chino.collections.list_documents(collection._id)
        self.assertEqual(l.paging.count, 1)
        self._equals(l.documents[0].to_dict(), document.to_dict())
        self.chino.collections.rm_document(collection._id, document._id)
        l = self.chino.collections.list_documents(collection._id)
        self.assertEqual(l.paging.count, 0)

        # delete
        self.chino.documents.delete(document._id, force=True)
        self.chino.schemas.delete(schema, force=True)
        self.chino.repositories.delete(repo, force=True)
        self.chino.collections.delete(collection._id, force=True)


@unittest.skip("Test to be updated")
class PermissionChinoTest2(BaseChinoTest):
    def setUp(self):
        super(PermissionChinoTest2, self).setUp()
        # list = self.chino.users.list()
        # for u in list.users:
        # self.chino.users.delete(u._id,force=True)

    def test_permissions(self):
        # create user via userschema
        repo = self.chino.repositories.create('test')._id
        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        schema = self.chino.schemas.create(repo, 'test', fields)._id
        # schema = "c0d0d956-8cd1-405b-90a9-62d3b3f70e84"
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')
        document = self.chino.documents.create(schema, content=content)
        fields = [dict(name='first_name', type='string'),
                  dict(name='last_name', type='string'),
                  dict(name='email', type='string')]
        us = self.chino.user_schemas.create('test', fields)
        username = 'test_%s' % round(time.time())
        user = self.chino.users.create(us._id, username=username,
                                       password='12345678',
                                       attributes=dict(first_name='john',
                                                       last_name='doe',
                                                       email='test@chino.io'))
        self.chino.permissions.resources('grant', 'repositories', 'users',
                                         user._id, manage=['R'])
        self.chino.users.login(username, '12345678')
        permissions = self.chino.permissions.read_perms()
        self.assertTrue(permissions[0].permission.manage == ['R'])
        self.chino.users.logout()
        self.chino.auth.set_auth_admin()
        self.chino.permissions.resource('grant', 'documents', document._id,
                                        'users', user._id, manage=['R', 'U'])
        self.chino.users.login(username, '12345678')
        permissions = self.chino.permissions.read_perms_document(document._id)
        self.assertTrue(permissions[0].permission.manage == ['R', 'U'])
        self.chino.users.logout()
        self.chino.auth.set_auth_admin()
        self.chino.permissions.resource_children('grant', 'schemas', schema,
                                                 'documents', 'users',
                                                 user._id,
                                                 manage=['R', 'U', 'L'],
                                                 authorize=['A'])
        self.chino.users.login(username, '12345678')
        permissions = self.chino.permissions.read_perms()
        # 0 is the one above
        self.assertTrue(permissions[1].permission.manage == ['R', 'U', 'L'])
        self.assertTrue(permissions[1].permission.authorize == ['A'])

        permissions = self.chino.permissions.read_perms_user(user._id)
        self.assertTrue(permissions[0].permission.manage == ['R'])
        self.assertTrue(permissions[1].permission.manage == ['R', 'U', 'L'])
        self.assertTrue(permissions[1].permission.authorize == ['A'])
        self.chino.users.logout()
        self.chino.auth.set_auth_admin()
        self.chino.documents.delete(document._id, force=True)
        self.chino.schemas.delete(schema, force=True)
        self.chino.repositories.delete(repo, force=True)
        self.chino.users.delete(user._id, force=True)
        self.chino.user_schemas.delete(us._id, force=True)


class DocumentChinoTest(BaseChinoTest):
    def setUp(self):
        super(DocumentChinoTest, self).setUp()
        self.repo = self.chino.repositories.create('test')._id
        fields = [dict(name='fieldInt', type='integer', indexed=True),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean', indexed=True),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        self.schema = self.chino.schemas.create(self.repo, 'test', fields)._id
        fields = [dict(name='fieldString', type='text')]
        self.schema_1 = self.chino.schemas.create(self.repo, 'test',
                                                  fields)._id

    def tearDown(self):
        list = self.chino.documents.list(self.schema)
        for doc in list.documents:
            self.chino.documents.delete(doc._id, force=True)
        self.chino.schemas.delete(self.schema, force=True, all_content=True)
        self.chino.repositories.delete(self.repo, force=True, all_content=True)

    def test_list(self):
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')
        document = self.chino.documents.create(self.schema, content=content)
        list = self.chino.documents.list(self.schema)
        self.assertIsNotNone(list.paging)
        self.assertIsNotNone(list.documents)
        self.assertIsNone(list.documents[0].content)
        list = self.chino.documents.list(self.schema, True)
        self.assertIsNotNone(list.documents[0].content)
        self.chino.documents.delete(document._id, True)

    def test_list_metadata_filters(self):
        # add a document
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')
        document = self.chino.documents.create(self.schema, content=content)

        # we should get 1 doc
        doc_list = self.chino.documents.list(self.schema)
        self.assertEqual(1, len(doc_list.documents))

        # input('waiting (strike any key to continue)')
        time.sleep(1)
        now = datetime.now(tz=pytz.timezone('Europe/Berlin'))

        # document - transform strings to datetime objects
        doc_insert_date = datetime.strptime(
            document.insert_date,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        doc_last_update = datetime.strptime(
            document.last_update,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        filters = [
            ({"is_active": True}, 1),
            ({"is_active": False}, 0),
            ({"is_active": True,
              "last_update__gt": doc_last_update + timedelta(seconds=1)}, 0),
            ({"is_active": True,
              "insert_date__gt": doc_insert_date - timedelta(seconds=1)}, 1),
            ({"last_update__lt": doc_last_update + timedelta(hours=1)}, 1),
            ({"insert_date__lt": doc_insert_date + timedelta(hours=1)}, 1),
            ({"is_active": True, "insert_date__lt": now,
              "last_update__lt": now}, 1),
            ({"is_active": True, "insert_date__gt": now,
              "last_update__gt": now}, 0),
        ]
        # we build a list of possible combination of filters - expected values
        for params, expected_count in filters:
            result = self.chino.documents.list(self.schema, **params)
            self.assertEqual(expected_count, len(result.documents), params)
            if expected_count > 0:
                self.assertEqual(document._id, result.documents[0]._id)

    def test_list_metadata_ordering(self):
        # add 3 documents
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')

        docs = []
        for i in range(3):
            doc = self.chino.documents.create(self.schema, content=content)
            docs.append(doc)
            time.sleep(1)

        # now we edit the first one, in order to change its last_update_value
        first = docs[0]
        content['fieldString'] = 'changed'
        self.chino.documents.update(first._id, content=content)

        # now we list em by insert_date and we check ordering
        params = {'ordering': 'insert_date'}
        res = self.chino.documents.list(self.schema, **params)

        for i, item in enumerate(res.documents):
            self.assertEqual(docs[i]._id, item._id)

        # invert order
        params = {'ordering': '-insert_date'}
        res = self.chino.documents.list(self.schema, **params)
        for i, item in enumerate(res.documents):
            self.assertEqual(docs[-i-1]._id, item._id)

        # now we check the order by last_update
        params = {'ordering': 'last_update'}
        res = self.chino.documents.list(self.schema, **params)
        docs_last_update = [docs[1], docs[2], docs[0]]
        for i, item in enumerate(res.documents):
            self.assertEqual(docs_last_update[i]._id, item._id)

        # invert order
        params = {'ordering': '-last_update'}
        res = self.chino.documents.list(self.schema, **params)
        for i, item in enumerate(res.documents):
            self.assertEqual(docs_last_update[-i-1]._id, item._id)

        # combine ordering
        params = {'ordering': 'insert_date,-last_update'}
        res = self.chino.documents.list(self.schema, **params)
        docs_combo = [docs[0], docs[1], docs[2]]
        for i, item in enumerate(res.documents):
            self.assertEqual(docs_combo[i]._id, item._id)

    def test_bulk_get(self):
        # Add 3 documents
        content_schema = dict(fieldInt=1, fieldString='test',
                              fieldBool=True, fieldDate='2015-02-19',
                              fieldDateTime='2015-02-19T16:39:47')
        content_schema_1 = dict(fieldString='test')

        documents = []
        for i in range(3):
            # We mix up the schemas of each doc a bit
            content = content_schema if i % 2 == 0 else content_schema_1
            schema = self.schema if i % 2 == 0 else self.schema_1
            documents.append(
                self.chino.documents.create(schema, content=content)
            )

        # Wait for indexing
        time.sleep(3)

        doc_ids = [document._id for document in documents]
        # We should get 3 docs
        bulk_get_result = self.chino.documents.bulk_get(document_ids=doc_ids)
        self.assertEqual(3, len(bulk_get_result))

        # This checks the __iter__ method
        for document in bulk_get_result:
            # Check that the ID is one of the ids in the list
            self.assertIn(document._id, doc_ids)

        # This checks the __getitem__ method
        for document_id in doc_ids:
            # Check that document_id can be used for accessing the document
            # and that the document is not None
            document = bulk_get_result[document_id]
            self.assertIsNotNone(document)
            self.assertEquals(document_id, document._id)

        # Check the to_dict method
        actual_dict = bulk_get_result.to_dict()
        self.assertEqual(3, actual_dict['count'])
        self.assertEqual(3, actual_dict['total_count'])
        self.assertDictEqual({}, actual_dict['errors'])

        for index, document_dict in enumerate(actual_dict['documents']):
            # We pick the content according to the order of the documents above
            content = content_schema if index % 2 == 0 else content_schema_1
            self.assertDictEqual(content, document_dict['content'])

    @unittest.skip("not working, timeout")
    def test_too_big(self):
        k_bit = 'YXNkc2FkamtzZGprYWhqa3NkaGFqa3NoZGpzYWhkamtzYWhkamtoc2Fqa2xoamRrc2ZsaGpka2xzaGZhamtkbHNoamFrZmxoZGp' \
                'za2xhaGZqZGtsc2hqZmtsYWhqZmtkbGhzYWpma2xkaHNqa2xhaGZqZGtsc2hhamZrbGFoamtkc2xoamZrZGxzaGpma2xkc2hham' \
                'tmbGRoc2pha2xmaGpka2xzaGpma2FzZGRqc2FpbyBkanNpYW9qZGlzYWpkaW9zYWpkaW9zYWppZG9qc2Fpb2RqaXNhb2pkaXNvY' \
                'WpkaW9zamFpZG9qc2Fpb2RqaXcxMDkzMDgyMTkwOGRtMXdpMDltZGk5MDFtaTlkMG13MWk5MGRtaXc5MTBtaWQ5dzBtaGRzamFr' \
                'aGRqa3NoYWRqbGFoZnNqa2xkaHNhamZrbGRoc2pha2xoZmpkc2tsYWhmamRrc2xoZmllYXVoZmlvZWgyYXVpb2ZoZXVpb3BxamV' \
                'pb3dlangsYXNhZHNhc2RzYWRqa3NkamthaGprc2RoYWprc2hkanNhaGRqa3NhaGRqa2hzYWprbGhqZGtzZmxoamRrbHNoZmFqa2' \
                'Rsc2hqYWtmbGhkanNrbGFoZmpka2xzaGpma2xhaGpma2RsaHNhamZrbGRoc2prbGFoZmpka2xzaGFqZmtsYWhqa2RzbGhqZmtkb' \
                'HNoamZrbGRzaGFqa2ZsZGhzamFrbGZoamRrbHNoamZrYXNkZGpzYWlvIGRqc2lhb2pkaXNhamRpb3NhamRpb3Nhamlkb2pzYWlv' \
                'ZGppc2FvamRpc29hamRpb3NqYWlkb2pzYWlvZGppdzEwOTMwODIxOTA4ZG0xd2kwOW1kaTkwMW1pOWQwbXcxaTkwZG1pdzkxMG1' \
                'pZDl3MG1oZHNqYWtoZGprc2hhZGpsYWhmc2prbGRoc2FqZmtsZGhzamFrbGhmamRza2xhaGZqZGtzbGhmaWVhdWhmaW9laDJhdW' \
                'lvZmhldWlvcHFqZWlvd2VqeCxhc2Fkc2FzZHNhZGprc2Rqa2FoamtzZGhhamtzaGRqc2FoZGprc2FoZGpraHNhamtsaGpka3Nmb' \
                'GhqZGtsc2hmYWprZGxzaGpha2ZsaGRqc2tsYWhmamRrbHNoamZrbGFoamZrZGxoc2FqZmtsZGhzamtsYWhmamRrbHNoYWpma2xh' \
                'aGprZHNsaGpma2Rsc2hqZmtsZHNoYWprZmxkaHNqYWtsZmhqZGtsc2hqZmthc2RkanNhaW8gZGpzaWFvamRpc2FqZGlvc2FqZGl' \
                'vc2FqaWRvanNhaW9kamlzYW9qZGlzb2FqZGlvc2phaWRvanNhaW9kaml3MTA5MzA4MjE5MDhkbTF3aTA5bWRpOTAxbWk5ZDBtdz' \
                'FpOTBkbWl3OTEwbWlkOXcwbWhkc2pha2hkamtzaGFkamxhaGZzamtsZGhzYWpma2xkaHNqYWtsaGZqZHNrbGFoZmpka3NsaGZpZ' \
                'WF1aGZpb2VoMmF1aW9maGV1aW9wcWplaW93ZWp4LGFzYWRzYXNkc2FkamtzZGprYWhqa3NkaGFqa3NoZGpzYWhkamtzYWhkamto' \
                'c2Fqa2xoamRrc2ZsaGpka2xzaGZhamtkbHNoamFrZmxoZGpza2xhaGZqZGtsc2hqZmtsYWhqZmtkbGhzYWpma2xkaHNqa2xhaGZ' \
                'qZGtsc2hhamZrbGFoamtkc2xoamZrZGxzaGpma2xkc2hhamtmbGRoc2pha2xmaGpka2xzaGpma2FzZGRqc2FpbyBkanNpYW9qZG' \
                'lzYWpkaW9zYWpkaW9zYWppZG9qc2Fpb2RqaXNhb2pkaXNvYWpkaW9zamFpZG9qc2Fpb2RqaXcxMDkzMDgyMTkwOGRtMXdpMDltZ' \
                'Gk5MDFtaTlkMG13MWk5MGRtaXc5MTBtaWQ5dzBtaGRzamFraGRqa3NoYWRqbGFoZnNqa2xkaHNhamZrbGRoc2pha2xoZmpkc2ts' \
                'YWhmamRrc2xoZmllYXVoZmlvZWgyYXVpb2ZoZXVpb3BxamVpb3dlangsYXNhZHNkc2Fh'
        n = 21  # number of MB
        k = 0
        dat = ""
        self.chino.documents.create(self.schema_1,
                                    content=dict(fieldString=dat))
        while k < n * 512:
            dat += "%s" % k_bit
            k += 1
        #
        with self.assertRaises(CallError):  # must fail because is too big
            self.chino.documents.create(self.schema_1,
                                        content=dict(fieldString=dat))

    def test_crud(self):
        content = dict(fieldInt=123, fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')
        document = self.chino.documents.create(self.schema, content=content)
        # get the last
        document_det = self.chino.documents.detail(document._id)
        self.assertEqual(document.last_update, document_det.last_update)
        content = dict(fieldInt=123,
                       fieldString='test', fieldBool=False,
                       fieldDate='2015-02-19',
                       fieldDateTime='2015-02-19T16:39:47')
        self.chino.documents.update(document._id, content=content)
        document = self.chino.documents.detail(document._id)
        self.assertEqual(123, document.content.fieldInt)
        self.chino.documents.update(document._id,
                                    content=dict(fieldInt=349,
                                                 fieldString='test',
                                                 fieldBool=False,
                                                 fieldDate='2015-02-19',
                                                 fieldDateTime='2015-02-19T16:39:47'))
        document = self.chino.documents.detail(document._id)
        self.assertEqual(349, document.content.fieldInt)

        # partial update
        self.chino.documents.update(document._id, content={'fieldInt': 42},
                                    partial=True)
        document = self.chino.documents.detail(document._id)
        self.assertEqual(42, document.content.fieldInt)
        self.assertEqual('test', document.content.fieldString)

        # now remove the doc
        self.chino.documents.delete(document._id)

        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        created = self.chino.schemas.create(self.repo, 'test', fields)
        list = self.chino.schemas.list(self.repo)
        s_id = 0
        for schema in list.schemas:
            if schema._id == created._id:
                s_id = schema._id
        detail = self.chino.schemas.detail(s_id)
        detail2 = self.chino.schemas.detail(created._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))

        detail.structure.fields.append(_Field('string', 'new one'))
        # delete repository_id
        data = detail.to_dict()
        del data['repository_id']
        del data['insert_date']
        del data['last_update']
        self.chino.schemas.update(**data)
        detail2 = self.chino.schemas.detail(detail._id)
        self.assertTrue(
            self._equals(detail.to_dict(), detail2.to_dict()),
            "\n %s \n %s \n" % (detail.to_json(), detail2.to_json()))
        self.chino.schemas.delete(detail._id, force=True)

    def test_search(self):
        # add two documents
        content = {"fieldInt": 42, "fieldString": "antani", "fieldBool": True,
                   "fieldDate": "2021-03-17",
                   "fieldDateTime": "2021-03-17T17:49:00"}
        doc_1 = self.chino.documents.create(self.schema, content=content)

        content = {"fieldInt": 21, "fieldString": "ant", "fieldBool": False,
                   "fieldDate": "2021-03-17",
                   "fieldDateTime": "2021-03-17T17:49:00"}
        doc_2 = self.chino.documents.create(self.schema, content=content)

        # wait for documents to be indexed
        time.sleep(1)

        # search:
        # - all the docs with bool field True
        query = {"field": "fieldBool", "type": "eq", "value": True}
        r = self.chino.documents.search(self.schema, query=query)
        self.assertEquals(1, len(r.documents))
        self.assertEquals(doc_1._id, r.documents[0]._id)

        # - all the docs with int field < 30
        query = {"field": "fieldInt", "type": "lt", "value": 30}
        r = self.chino.documents.search(self.schema, query=query)
        self.assertEquals(1, len(r.documents))
        self.assertEquals(doc_2._id, r.documents[0]._id)

        # - all the docs with bool field True or int field < 30
        query = {"or": [
            {"field": "fieldBool", "type": "eq", "value": True},
            {"field": "fieldInt", "type": "lt", "value": 30}
        ]}
        r = self.chino.documents.search(self.schema, query=query)
        self.assertEquals(2, len(r.documents))
        found_doc_ids = [doc._id for doc in r.documents]
        self.assertIn(doc_1._id, found_doc_ids)
        self.assertIn(doc_2._id, found_doc_ids)

        # - all the docs with bool field False and int field > 50
        query = {"and": [
            {"field": "fieldBool", "type": "eq", "value": False},
            {"field": "fieldInt", "type": "gt", "value": 50}
        ]}
        r = self.chino.documents.search(self.schema, query=query)
        self.assertEquals(0, len(r.documents))

        # - all the docs with int field > 0 ordered DESC
        query = {"field": "fieldInt", "type": "gt", "value": 0}
        sort = [{"field": "fieldInt", "order": "desc"}]
        r = self.chino.documents.search(self.schema, query=query,
                                        sort=sort)
        self.assertEquals(2, len(r.documents))
        self.assertIn(doc_1._id, r.documents[0]._id)
        self.assertIn(doc_2._id, r.documents[1]._id)

        # - same search with inverted order
        sort = [{"field": "fieldInt", "order": "asc"}]
        r = self.chino.documents.search(self.schema, query=query,
                                        sort=sort)
        self.assertEquals(2, len(r.documents))
        self.assertIn(doc_2._id, r.documents[0]._id)
        self.assertIn(doc_1._id, r.documents[1]._id)


class BlobChinoTest(BaseChinoTest):
    def setUp(self):
        super(BlobChinoTest, self).setUp()
        self.repo = self.chino.repositories.create('test')._id
        fields = [dict(name='blobTest', type='blob'),
                  dict(name='name', type='string')]
        self.schema = self.chino.schemas.create(self.repo, 'test', fields)._id

    def tearDown(self):
        if hasattr(self, 'blob'):
            self.chino.blobs.delete(self.blob.blob_id)
        self.chino.documents.delete(self.document._id, True)
        self.chino.schemas.delete(self.schema, True)
        self.chino.repositories.delete(self.repo, True)

    # @unittest.skip("not working on prod")
    def test_blob(self):
        self.document = self.chino.documents.create(self.schema,
                                                    content=dict(name='test'))
        src = os.path.join(os.path.sep, os.path.dirname(__file__), 'logo.png')
        blob = self.chino.blobs.send(self.document._id, 'blobTest', str(src),
                                     chunk_size=32 * 1024)
        blob_detail = self.chino.blobs.detail(blob.blob_id)
        rw = open("out" + blob_detail.filename, "wb")
        rw.write(blob_detail.content)
        rw.close()
        # rd = open('test/logo.png', "rb")
        md5_detail = hashlib.md5()
        md5_detail.update(blob_detail.content)
        # self.assertEqual(md5_detail.digest(), md5_original.digest())
        self.assertEqual(md5_detail.hexdigest(), blob.md5)
        self.blob = blob
        self.chino.blobs.delete(self.blob.blob_id)
        src = os.path.join(os.path.sep, os.path.dirname(__file__), 'test.sh')
        blob = self.chino.blobs.send(self.document._id, 'blobTest', str(src),
                                     chunk_size=32 * 1024)

        blob_detail = self.chino.blobs.detail(blob.blob_id)
        rw = open("out" + blob_detail.filename, "wb")
        rw.write(blob_detail.content)
        rw.close()
        # rd = open('test/logo.png', "rb")
        md5_detail = hashlib.md5()
        md5_detail.update(blob_detail.content)
        # self.assertEqual(md5_detail.digest(), md5_original.digest())
        self.assertEqual(md5_detail.hexdigest(), blob.md5)
        self.blob = blob

    def test_url(self):
        self.document = self.chino.documents.create(self.schema,
                                                    content=dict(name='test'))
        src = os.path.join(os.path.sep, os.path.dirname(__file__), 'logo.png')
        blob = self.chino.blobs.send(self.document._id, 'blobTest', str(src),
                                     chunk_size=32 * 1024)
        data = self.chino.blobs.generate(blob.blob_id,one_time=True)
        blob_detail = self.chino.blobs.detail_token(blob.blob_id,
                                                    data['token'], 'test.out')
        rw = open("out" + blob_detail.filename, "wb")
        rw.write(blob_detail.content)
        rw.close()
        # rd = open('test/logo.png', "rb")
        md5_detail = hashlib.md5()
        md5_detail.update(blob_detail.content)
        self.assertEqual(md5_detail.hexdigest(), blob.md5)

        with self.assertRaises(CallError):
            blob_detail = self.chino.blobs.detail_token(blob.blob_id,
                                                    data['token'], 'test.out')

        self.chino.blobs.delete(blob.blob_id)


    @unittest.skip("Skipping for size")
    def test_large_blob(self):
        self.document = self.chino.documents.create(self.schema,
                                                    content=dict(name='test'))
        import random
        blob = self.chino.blobs.send(self.document._id, 'blobTest',
                                     'dummy.file',
                                     chunk_size=random.choice(
                                         [1, 10]) * 1024 * 1024)
        blob_detail = self.chino.blobs.detail(blob.blob_id)
        rw = open("out" + blob_detail.filename, "wb")
        rw.write(blob_detail.content)
        rw.close()
        # rd = open('test/logo.png', "rb")
        md5_detail = hashlib.md5()
        md5_detail.update(blob_detail.content)
        sha1_detail = hashlib.sha1()
        sha1_detail.update(blob_detail.content)
        # self.assertEqual(md5_detail.digest(), md5_original.digest())
        self.assertEqual(md5_detail.hexdigest(), blob.md5)
        self.assertEqual(sha1_detail.hexdigest(), blob.sha1)
        # self.blob = blob


# @unittest.skip("not working on prod`")
class SearchDocsChinoTest(BaseChinoTest):
    def setUp(self):
        super(SearchDocsChinoTest, self).setUp()
        fields = [dict(name='fieldInt', type='integer', indexed=True),
                  dict(name='fieldString', type='string', indexed=True),
                  dict(name='fieldBool', type='boolean', indexed=True),
                  dict(name='fieldDate', type='date', indexed=True),
                  dict(name='fieldDateTime', type='datetime', indexed=True)]
        self.repo = self.chino.repositories.create('test')._id
        self.schema = self.chino.schemas.create(self.repo, 'test', fields)._id

    # def tearDown(self):
    #     documents = self.chino.documents.list(self.schema)
    #     for document in documents.documents:
    #         self.chino.documents.delete(document._id, force=True)
    #     self.chino.schemas.delete(self.schema, True)
    #     self.chino.repositories.delete(self.repo, True)

    # DEPRECATED: to be removed in v>=3.0.0
    def test_search_docs(self):
        tot = 9
        # print(self.schema)
        for i in range(tot):
            res = self.chino.documents.create(self.schema,
                                              content=dict(fieldInt=123,
                                                           fieldString='test',
                                                           fieldBool=False,
                                                           fieldDate='2015-02-19',
                                                           fieldDateTime='2015-02-19T16:39:47'),
                                              consistent=True)
        last_doc = self.chino.documents.create(self.schema,
                                               content=dict(fieldInt=123,
                                                            fieldString='test',
                                                            fieldBool=False,
                                                            fieldDate='2015-02-19',
                                                            fieldDateTime='2015-02-19T16:39:47'),
                                               consistent=True)

        # self.chino.searches.search(self.schema) # TODO: improve tests
        time.sleep(float(cfg.sleep))  # wait the index max update time
        res = self.chino.searches.documents(self.schema, filters=[
            {"field": "fieldInt", "type": "eq", "value": 123}])
        self.assertEqual(res.paging.total_count, 10, res)
        self.chino.documents.delete(last_doc.document_id, force=True)
        time.sleep(float(cfg.sleep) * 3.0)
        res = self.chino.searches.documents(self.schema, filters=[
            {"field": "fieldInt", "type": "eq", "value": 123}])
        self.assertEqual(res.paging.total_count, 9, res)
        res = self.chino.searches.documents_complex(self.schema,
                                                    query={"field": "fieldInt",
                                                           "type": "eq",
                                                           "value": 123})
        self.assertEqual(res.paging.total_count, 9, res)
        # print res.documents
        ids = []
        for d in res.documents[:3]:
            ids.append(d._id)
        res = self.chino.searches.documents(self.schema, filters=[
            {"field": "_id", "type": "in", "value": ids}])
        self.assertEqual(res.paging.total_count, 3, res)

    # DEPRECATED: to be removed in v>=3.0.0
    def test_search_docs_consistent(self):
        doc = None
        max = 4
        for i in range(max):
            doc = self.chino.documents.create(self.schema,
                                              content=dict(fieldInt=i,
                                                           fieldString='test',
                                                           fieldBool=False,
                                                           fieldDate='2015-02-19',
                                                           fieldDateTime='2015-02-19T16:39:47'),
                                              consistent=True)
        time.sleep(float(cfg.sleep))
        res = self.chino.searches.documents(self.schema,
                                            filters=[{"field": "fieldInt",
                                                      "type": "eq",
                                                      "value": i}])
        self.assertEqual(res.paging.total_count, 1, res)
        res = self.chino.searches.documents(self.schema,
                                            filters=[{"field": "fieldInt",
                                                      "type": "eq",
                                                      "value": max - 1}])
        self.assertEqual(res.paging.total_count, 1, res)
        self.chino.documents.delete(doc._id, consistent=True, force=True)
        res = self.chino.searches.documents(self.schema,
                                            filters=[{"field": "fieldInt",
                                                      "type": "eq",
                                                      "value": max - 1}])
        self.assertEqual(res.paging.total_count, 0, res)

    # DEPRECATED: to be removed in v>=3.0.0
    def test_search_docs_complex(self):
        doc = None
        max = 4
        for i in range(max):
            doc_content = dict(fieldInt=i, fieldString='test', fieldBool=False,
                               fieldDate='2018-12-19',
                               fieldDateTime='2018-12-19T16:39:47')
            doc = self.chino.documents.create(
                self.schema,
                content=doc_content,
                consistent=True
            )
            res = self.chino.searches.documents_complex(self.schema,
                                                        result_type="ONLY_ID",
                                                        query={
                                                            "and": [{
                                                                        "field": key,
                                                                        "type": "eq",
                                                                        "value":
                                                                            doc_content[
                                                                                key]}
                                                                    for key in
                                                                    doc_content.keys()]
                                                                   + [
                                                                       {
                                                                           "field": "_id",
                                                                           "type": "eq",
                                                                           "value": doc.document_id}
                                                                   ]
                                                        }
                                                        )
            self.assertEquals(
                doc.document_id, str(res.IDs[0])
            )

        self.assertEquals(
            0,
            len(
                self.chino.searches.documents_complex(self.schema,
                                                      result_type="NO_CONTENT",
                                                      query={
                                                          "or": [
                                                              {
                                                                  "field": "fieldInt",
                                                                  "type": "eq",
                                                                  "value": max + 1},
                                                              {"not": [
                                                                  {
                                                                      "field": "fieldInt",
                                                                      "type": "lte",
                                                                      "value": max}
                                                              ]}
                                                          ]
                                                      }
                                                      ).documents
            )
        )

        count_docs = self.chino.searches.documents_complex(self.schema,
                                                           result_type="COUNT",
                                                           query={
                                                               "field": "fieldDate",
                                                               "type": "gte",
                                                               "value": '2018-12-19'}
                                                           )
        self.assertEqual(max, count_docs)

        all_ids = self.chino.searches.documents_complex(self.schema,
                                                        result_type="ONLY_ID",
                                                        query={
                                                            "field": "fieldDate",
                                                            "type": "gte",
                                                            "value": '2018-12-19'}
                                                        )
        self.assertIn(doc.document_id,
                      [str(_id['id']) for _id in all_ids.to_dict()["IDs"]])

        self.assertEquals(
            doc.document_id,  # last created document
            self.chino.searches.documents_complex(self.schema,
                                                  sort=[dict(field="fieldInt",
                                                             order="desc")],
                                                  query={"field": "fieldDate",
                                                         "type": "gte",
                                                         "value": '2018-12-19'},
                                                  limit=1
                                                  ).documents[0].document_id
        )


class SearchUsersChinoTest(BaseChinoTest):
    def setUp(self):
        super(SearchUsersChinoTest, self).setUp()
        fields = [dict(name='fieldInt', type='integer', indexed=True),
                  dict(name='fieldString', type='string', indexed=True),
                  dict(name='fieldBool', type='boolean', indexed=True),
                  dict(name='fieldDate', type='date', indexed=True),
                  dict(name='fieldDateTime', type='datetime', indexed=True)]
        self.schema = self.chino.user_schemas.create('test', fields)._id

    def tearDown(self):
        users = self.chino.users.list(self.schema)
        for user in users.users:
            self.chino.users.delete(user._id, force=True)
        self.chino.user_schemas.delete(self.schema, True)

    # DEPRECATED: to be removed in v>=3.0.0
    def test_search_users(self):
        for i in range(9):
            self.chino.users.create(self.schema, username="user_test_%s" % i,
                                    password='1234567890AAaa',
                                    attributes=dict(fieldInt=123,
                                                    fieldString='test',
                                                    fieldBool=False,
                                                    fieldDate='2015-02-19',
                                                    fieldDateTime='2015-02-19T16:39:47'))
        time.sleep(float(cfg.sleep) / 2.0)
        last_doc = self.chino.users.create(self.schema,
                                           username="user_test_last",
                                           password='1234567890AAaa',
                                           attributes=dict(fieldInt=123,
                                                           fieldString='test',
                                                           fieldBool=False,
                                                           fieldDate='2015-02-19',
                                                           fieldDateTime='2015-02-19T16:39:47'))

        # self.chino.searches.search(self.schema) # TODO: improve tests
        time.sleep(
            float(cfg.sleep) * 3.0)  # wait twice the index max update time

        res = self.chino.searches.users(self.schema, filters=[
            {"field": "fieldInt", "type": "eq", "value": 123}])
        self.assertEqual(res.paging.total_count, 10, res)
        res = self.chino.searches.users(self.schema,
                                        filters=[
                                            {"field": "username", "type": "eq",
                                             "value": 'user_test_last'}])
        self.assertEqual(res.paging.total_count, 1, res)
        res = self.chino.searches.users(self.schema, filters=[
            {"field": "username", "type": "eq", "value": 'user_test_last'}],
                                        result_type="EXISTS")
        self.assertEqual(res, True, res)
        res = self.chino.searches.users(self.schema, filters=[
            {"field": "username", "type": "eq", "value": 'user_test_last'}],
                                        result_type="USERNAME_EXISTS")
        self.assertEqual(res, True, res)
        self.chino.users.delete(last_doc.user_id, force=True)
        time.sleep(float(cfg.sleep))
        res = self.chino.searches.users(self.schema, filters=[
            {"field": "fieldInt", "type": "eq", "value": 123}])
        self.assertEqual(res.paging.total_count, 9, res)

        res = self.chino.searches.users_complex(self.schema,
                                                query={"field": "fieldInt",
                                                       "type": "eq",
                                                       "value": 123})
        self.assertEqual(res.paging.total_count, 9, res)

    # DEPRECATED: to be removed in v>=3.0.0
    def test_search_users_consistent(self):
        doc = None
        for i in range(4):
            doc = self.chino.users.create(self.schema,
                                          username="user_test_%s" % i,
                                          password='1234567890AAaa',
                                          attributes=dict(fieldInt=123,
                                                          fieldString='test',
                                                          fieldBool=False,
                                                          fieldDate='2015-02-19',
                                                          fieldDateTime='2015-02-19T16:39:47'),
                                          consistent=True)
        res = self.chino.searches.users(self.schema, filters=[
            {"field": "fieldInt", "type": "eq", "value": 123}])
        self.assertEqual(res.paging.total_count, i + 1, res)

        # self.chino.users.delete(doc.user_id, force=True,consistent=True)
        # res = self.chino.searches.users(self.schema, filters=[{"field": "fieldInt", "type": "eq", "value": 123}])
        # self.assertEqual(res.paging.total_count, 9, res)

    # DEPRECATED: to be removed in v>=3.0.0
    def test_search_users_complex(self):
        usr = None
        max = 4
        for i in range(max):
            usr_attributes = dict(fieldInt=i, fieldString='test',
                                  fieldBool=False,
                                  fieldDate='2018-12-19',
                                  fieldDateTime='2018-12-19T16:39:47')
            usr = self.chino.users.create(self.schema,
                                          username="user_test_%s" % i,
                                          password='1234567890AAaa',
                                          attributes=usr_attributes,
                                          consistent=True
                                          )
            self.assertTrue(
                self.chino.searches.users_complex(self.schema,
                                                  result_type="EXISTS",
                                                  query={
                                                      "and": [{"field": key,
                                                               "type": "eq",
                                                               "value":
                                                                   usr_attributes[
                                                                       key]}
                                                              for key in
                                                              usr_attributes.keys()]
                                                             + [
                                                                 {
                                                                     "field": "_id",
                                                                     "type": "eq",
                                                                     "value": usr.user_id}
                                                             ]
                                                  }
                                                  )
            )
            self.assertTrue(
                self.chino.searches.users_complex(self.schema,
                                                  result_type="USERNAME_EXISTS",
                                                  query={"field": "username",
                                                         "type": "eq",
                                                         "value": usr.username}
                                                  )
            )

        self.assertFalse(
            self.chino.searches.users_complex(self.schema,
                                              result_type="EXISTS",
                                              query={
                                                  "or": [
                                                      {"field": "fieldInt",
                                                       "type": "eq",
                                                       "value": max + 1},
                                                      {"not": [
                                                          {"field": "fieldInt",
                                                           "type": "lte",
                                                           "value": max}
                                                      ]}
                                                  ]
                                              }
                                              )
        )

        count_docs = self.chino.searches.users_complex(self.schema,
                                                       result_type="COUNT",
                                                       query={
                                                           "field": "fieldDate",
                                                           "type": "gte",
                                                           "value": '2018-12-19'}
                                                       )
        self.assertEqual(max, count_docs)

        self.assertEquals(
            usr.user_id,  # last created user
            self.chino.searches.users_complex(self.schema,
                                              sort=[dict(field="fieldInt",
                                                         order="desc")],
                                              query={"field": "fieldDate",
                                                     "type": "gte",
                                                     "value": '2018-12-19'},
                                              limit=1
                                              ).users[0].user_id
        )


class PermissionChinoTest(BaseChinoTest):
    def setUp(self):
        super(PermissionChinoTest, self).setUp()
        groups = self.chino.groups.list()
        for g in groups.groups:
            self.chino.groups.delete(g._id, True)
        u_schemas = self.chino.user_schemas.list()
        for us in u_schemas.user_schemas:
            li = self.chino.users.list(us._id)
            for user in li.users:
                self.chino.users.delete(user._id, force=True)
        fields = [dict(name='first_name', type='string'),
                  dict(name='last_name', type='string'),
                  dict(name='email', type='string')]
        self.user_schema = self.chino.user_schemas.create('test', fields)._id
        self.password = '12345678'
        self.user0 = self.chino.users.create(user_schema_id=self.user_schema,
                                             username='test',
                                             password=self.password,
                                             attributes=dict(
                                                 first_name='user_0',
                                                 last_name='doe',
                                                 email='test@chino.io'))
        self.user1 = self.chino.users.create(user_schema_id=self.user_schema,
                                             username='test1',
                                             password=self.password,
                                             attributes=dict(
                                                 first_name='user_1',
                                                 last_name='doe',
                                                 email='test@chino.io'))

        self.group = self.chino.groups.create('testing',
                                              attributes=dict(hospital='test'))

        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        self.repo = self.chino.repositories.create('test')._id
        self.schema = self.chino.schemas.create(self.repo, 'test', fields)
        app = self.chino.applications.create("test", grant_type='password')
        self.chino_user0 = ChinoAPIClient(customer_id=cfg.customer_id,
                                          customer_key=cfg.customer_key,
                                          url=cfg.url, client_id=app.app_id,
                                          client_secret=app.app_secret,
                                          force_https=False)
        self.chino_user0.users.login(self.user0.username, self.password)
        self.chino_user1 = ChinoAPIClient(customer_id=cfg.customer_id,
                                          customer_key=cfg.customer_key,
                                          url=cfg.url, client_id=app.app_id,
                                          client_secret=app.app_secret,
                                          force_https=False)
        self.chino_user1.users.login(self.user1.username, self.password)

    def tearDown(self):
        u_schemas = self.chino.user_schemas.list()
        for us in u_schemas.user_schemas:
            li = self.chino.users.list(us._id)
            for user in li.users:
                self.chino.users.delete(user._id, force=True)
            self.chino.user_schemas.delete(us._id, True)
        groups = self.chino.groups.list()
        for g in groups.groups:
            self.chino.groups.delete(g._id, True)
        try:
            self.chino.schemas.delete(self.schema.schema_id, True, all_content=True)
            self.chino.repositories.delete(self.repo, True, all_content=True)
        except CallError:
            pass

    def test_create_a_repository(self):
        with self.assertRaises(CallError):
            # user has no create permission, expected an error.
            self.repository = self.chino_user0.repositories.create('test')
        self.chino.permissions.resources(
            'grant',
            'repositories',
            'users', self.user0._id,
            manage=['C', 'R', 'U', 'L'], authorize=['A']
        )
        # now it has the permissions
        self.repository = self.chino_user0.repositories.create('test')
        # grant to user1 permission (except "C") on all the repository
        self.chino.permissions.resources(
            'grant',
            'repositories',
            'users', self.user1._id,
            manage=['R', 'U', 'L']
        )

        with self.assertRaises(CallError):
            # must fail because user has no create permission
            self.chino_user1.repositories.create('test')

        li = self.chino_user1.repositories.list()
        for repo in li.repositories:
            # must succeed because user has "R" permission
            self.chino_user1.repositories.detail(repo._id)
        with self.assertRaises(CallError):
            # must fail because user has no "D" permission
            self.chino_user1.repositories.delete(self.repository._id)

        self.chino_user0.permissions.resource(
            'grant',
            'repositories', self.repository._id,
            'users', self.user1._id,
            manage=['D']
        )

        with self.assertRaises(CallError):
            # must fail because user is not authorized
            self.chino_user1.permissions.resource(
                'grant',
                'repositories', self.repository._id,
                'users', self.user0._id,
                manage=['D']
            )
        self.chino_user1.repositories.delete(self.repository._id)

    def test_create_documents(self):
        self.chino.permissions.resources('grant', 'repositories', 'users',
                                         self.user0._id, manage=['C'])
        self.repository = self.chino_user0.repositories.create('test')
        fields = [dict(name='fieldInt', type='integer'),
                  dict(name='fieldString', type='string'),
                  dict(name='fieldBool', type='boolean'),
                  dict(name='fieldDate', type='date'),
                  dict(name='fieldDateTime', type='datetime')]
        self.schema = self.chino_user0.schemas.create(self.repository._id,
                                                      'test_schema',
                                                      fields)._id
        content = {
            'fieldInt': 123,
            'fieldString': 'test',
            'fieldBool': False,
            'fieldDate': '2015-02-19',
            'fieldDateTime': '2015-02-19T16:39:47'
        }
        self.document = self.chino_user0.documents.create(
            self.schema, content=content
        )._id

        with self.assertRaises(CallError):
            # must fail because user is not authorized
            self.chino_user1.documents.create(self.schema, content=content)

        with self.assertRaises(CallError):
            # must fail because user is not authorized
            self.chino_user1.documents.list(self.schema)

        self.chino_user0.permissions.resource_children(
            'grant',
            'schemas', self.schema, 'documents',
            'users', self.user1._id,
            manage=['L']
        )
        self.assertEqual(
            self.chino_user1.documents.list(self.schema).paging.total_count, 0)
        self.assertEqual(
            self.chino_user0.documents.list(self.schema).paging.total_count, 1)

    def test_bulk_perms(self):
        """
        tests the method that sets permissions in bulk
        """
        #read perms, make sure there are none
        res = self.chino_user0.permissions.read_perms()
        self.assertEquals(0, len(res))
        res = self.chino.permissions.read_perms_group(self.group.group_id)
        self.assertEquals(0, len(res))

        # grant multiple permissions
        perms = [
            {
                "action": "grant",
                "resource_type" : "repositories",
                "subject_type": "users",
                "subject_id": self.user0.user_id,
                "payload" : {
                    "manage": ["R", "U", "L"],
                    "authorize": ["A"],
                }
            },
            {
                "action": "grant",
                "resource_type": "schemas",
                "subject_type": "groups",
                "subject_id": self.group.group_id,
                "resource_id": self.schema.schema_id,
                "payload": {
                    "manage": ["R"],
                    "authorize": ["A"],
                }
            }
        ]
        self.chino.permissions.bulk_perms(perms)

        # read perms of the user, make sure it has the new ones
        res = self.chino.permissions.read_perms_user(self.user0.user_id)
        self.assertEquals(1, len(res))
        # Check content of the Permission
        self.assertTrue(hasattr(res[0], 'permission'),
                        msg="Missing 'permission'")

        # read perms of the group, make sure it has the new ones
        res = self.chino.permissions.read_perms_group(self.group.group_id)
        self.assertEquals(1, len(res))
        # Check content of the Permission
        self.assertTrue(hasattr(res[0], 'permission'),
                        msg="Missing 'permission'")


    def test_read_perms(self):
        """Tests the method that reads Permissions on all Resources
        """
        # Read perms, make sure there are none
        res = self.chino_user0.permissions.read_perms()
        self.assertEquals(0, len(res))

        # Grant permissions over the schemas
        self.chino.permissions.resource(
            'grant',
            'schemas', self.schema.schema_id,
            'users', self.user0.user_id,
            manage=['R'], authorize=['R']
        )

        # Read perms, make sure there is the new one
        res = self.chino_user0.permissions.read_perms()
        self.assertEquals(1, len(res))
        # Check content of the Permission
        self.assertTrue(hasattr(res[0], 'permission'),
                        msg="Missing 'permission'")
        perm = res[0].permission
        self.assertTrue(hasattr(perm, 'manage'), msg="Missing 'manage'")
        self.assertEquals(['R'], perm.manage, msg="Wrong 'manage'")
        self.assertTrue(hasattr(perm, 'authorize'), msg="Missing 'authorize'")
        self.assertEquals(['R'], perm.authorize, msg="Wrong 'authorize'")
        self.assertFalse(hasattr(perm, 'created_document'),
                         msg="Unexpected 'created_document'")

    def test_read_perms_document(self):
        """Tests the method that reads Permissions on a Document
        """
        # Create Document
        doc = self.chino.documents.create(self.schema.schema_id, content={
            'fieldInt': 42,
            'fieldString': "test",
            'fieldBool': False,
            'fieldDate': "2023-11-22",
            'fieldDateTime': "2023-11-22T17:22:47"
        }, consistent=True)

        # Read perms of the user, make sure it has none
        res = self.chino.permissions.read_perms_document(doc.document_id)
        self.assertEquals(0, len(res))

        # Grant permissions over the schemas
        self.chino.permissions.resource(
            'grant',
            'documents', doc.document_id,
            'users', self.user0.user_id,
            manage=['R'], authorize=['R']
        )

        # Read perms of the user, make sure it has the new one
        res = self.chino.permissions.read_perms_document(doc.document_id)
        self.assertEquals(1, len(res))
        # Check content of the Permission
        self.assertTrue(hasattr(res[0], 'permission'),
                        msg="Missing 'permission'")
        perm = res[0].permission
        self.assertTrue(hasattr(perm, 'manage'), msg="Missing 'manage'")
        self.assertEquals(['R'], perm.manage, msg="Wrong 'manage'")
        self.assertTrue(hasattr(perm, 'authorize'), msg="Missing 'authorize'")
        self.assertEquals(['R'], perm.authorize, msg="Wrong 'authorize'")
        self.assertFalse(hasattr(perm, 'created_document'),
                         msg="Unexpected 'created_document'")

    def test_read_perms_user(self):
        """Tests the method that reads Permissions of a User
        """
        # Read perms of the user, make sure there are none
        res1 = self.chino.permissions.read_perms_user(self.user0.user_id)
        res2 = self.chino_user0.permissions.read_perms_user(self.user0.user_id)
        for res in [res1, res2]:
            self.assertEquals(0, len(res))

        # Grant permissions over the schemas
        self.chino.permissions.resource(
            'grant',
            'schemas', self.schema.schema_id,
            'users', self.user0.user_id,
            manage=['R'], authorize=['R']
        )

        # Read perms of the user, make sure there is the new one
        res1 = self.chino.permissions.read_perms_user(self.user0.user_id)
        res2 = self.chino_user0.permissions.read_perms_user(self.user0.user_id)
        for res in [res1, res2]:
            self.assertEquals(1, len(res))
            # Check content of the Permission
            self.assertTrue(hasattr(res[0], 'permission'),
                            msg="Missing 'permission'")
            perm = res[0].permission
            self.assertTrue(hasattr(perm, 'manage'), msg="Missing 'manage'")
            self.assertEquals(['R'], perm.manage, msg="Wrong 'manage'")
            self.assertTrue(hasattr(perm, 'authorize'),
                            msg="Missing 'authorize'")
            self.assertEquals(['R'], perm.authorize, msg="Wrong 'authorize'")
            self.assertFalse(hasattr(perm, 'created_document'),
                             msg="Unexpected 'created_document'")

    def test_read_perms_group(self):
        """Tests the method that reads Permissions of a Group
        """
        # # Add users to the group
        # self.chino.groups.add_user(self.group.group_id, self.user0.user_id)
        # self.chino.groups.add_user(self.group.group_id, self.user1.user_id)

        # Read perms of the group, make sure there are none
        res = self.chino.permissions.read_perms_group(self.group.group_id)
        self.assertEquals(0, len(res))

        # Grant permissions over the schema
        self.chino.permissions.resource(
            'grant',
            'schemas', self.schema.schema_id,
            'groups', self.group.group_id,
            manage=['R'], authorize=['R']
        )

        # Read perms of the user, make sure it has the new one
        res = self.chino.permissions.read_perms_group(self.group.group_id)
        self.assertEquals(1, len(res))
        # Check content of the Permission
        self.assertTrue(hasattr(res[0], 'permission'),
                        msg="Missing 'permission'")
        perm = res[0].permission
        self.assertTrue(hasattr(perm, 'manage'), msg="Missing 'manage'")
        self.assertEquals(['R'], perm.manage, msg="Wrong 'manage'")
        self.assertTrue(hasattr(perm, 'authorize'), msg="Missing 'authorize'")
        self.assertEquals(['R'], perm.authorize, msg="Wrong 'authorize'")
        self.assertFalse(hasattr(perm, 'created_document'),
                         msg="Unexpected 'created_document'")



# # NOTE: this test case will be removed along with the Consent Management API
#         in the upcoming major version (3.0.0)
# @unittest.skipIf(cfg.url.startswith('https://api.chino.io'),
#                  "not on production")
# @unittest.skipIf(os.environ.get('SKIP_PROD', False),
#                  "Not for production like systems")
# class ConsentChinoTest(BaseChinoTest):
#
#     def setUp(self):
#         super(ConsentChinoTest, self).setUp()
#         self.details = {
#             "description": "This policy was created for test purposes. The policy url is linked to Chino.io policy.",
#             "policy_url": "https://www.chino.io/legal/privacy-policy",
#             "policy_version": "test",
#             "collection_mode": "none"
#         }
#         self.data_controller = {
#             "company": "Chino.io",
#             "contact": "controller",
#             "address": "Via S.G. Bosco 27, 38068 Rovereto",
#             "email": "controller@mail.tld",
#             "VAT": "n/d",
#             "on_behalf": True
#         }
#         self.purposes = [
#             {
#                 "authorized": True,
#                 "purpose": "testing",
#                 "description": "Testing class api.ChinoAPIConsents"
#             },
#             {
#                 "authorized": False,
#                 "purpose": "testing",
#                 "description": "Testing class objects.Consent"
#             }
#         ]
#         self.user_id = "user_id"
#         self.user_id_alt = "another-user_id"
#         # list of Consents for test_list and test_withdraw
#         self.consent_ls = []
#         self.consent_ls.append(
#             self.chino.consents.create(self.user_id, self.details,
#                                        self.data_controller, self.purposes))
#         self.consent_ls.append(
#             self.chino.consents.create(self.user_id_alt, self.details,
#                                        self.data_controller, self.purposes))
#         self.consent_ls.append(
#             self.chino.consents.create(self.user_id, self.details,
#                                        self.data_controller, self.purposes))
#
#     def tearDown(self):
#         ls = self.chino.consents.list(limit=100)
#         for c in ls.consents:
#             if c.to_dict()['policy_version'] == 'test':
#                 self.chino.consents.delete(c._id)
#
#     def test_list(self):
#         ls = self.chino.consents.list()
#         self.assertIsNotNone(ls.paging)
#         self.assertIsNotNone(ls.consents)
#
#         ls = self.chino.consents.list(self.user_id)
#         for consent in ls.consents:
#             self.assertEqual(consent.to_dict()['user_id'], self.user_id)
#
#     def test_CRUD(self):
#         USER_ID1 = "username@mail.tld"
#         USER_ID2 = "another_username@mail.tld"
#         # CREATE
#         new = self.chino.consents.create(USER_ID1, self.details,
#                                          self.data_controller, self.purposes)
#         list = self.chino.consents.list(limit=100)
#         self.assertGreater(list.paging.count, 0)
#         read_id = 0
#         for consent in list.consents:
#             if consent._id == new._id:
#                 read_id = consent._id
#         self.assertFalse(read_id == 0)
#         # READ
#         read = self.chino.consents.detail(read_id)
#         read_compare = self.chino.consents.detail(new._id)
#         self.assertTrue(self._equals(new.to_dict(), read.to_dict()),
#                         msg="created:\n%s\n\nread:\n\n%s\n" % (
#                         new.to_json(), read.to_json())
#                         )
#         # UPDATE
#         updated = self.chino.consents.update(read._id, USER_ID2, self.details,
#                                              self.data_controller,
#                                              self.purposes)
#         self.assertFalse(self._equals(new.to_dict(), updated.to_dict()),
#                          msg=(
#                                      "Update returned an unmodified object.\nid1: %s\nid2: %s" % (
#                              new._id, updated._id)))
#
#         read = self.chino.consents.detail(read_id)
#         self.assertTrue(self._equals(updated.to_dict(), read.to_dict()),
#                         msg="updated:\n%s\n\nread:\n\n%s\n" % (
#                         updated.to_json(), read.to_json())
#                         )
#         history = self.chino.consents.history(read._id)
#         self.assertGreater(len(history.consents), 1)
#         # DELETE
#         self.chino.consents.delete(read._id)
#         for cid in [new._id, read._id, updated._id]:
#             self.assertRaises(CallError,
#                               self.chino.consents.detail,
#                               {'consent_id': cid}
#                               )
#
#     def test_withdraw(self):
#         withdraw = self.chino.consents.list(user_id=self.user_id_alt).consents[
#             0]
#         self.chino.consents.withdraw(withdraw._id)
#
#         read = self.chino.consents.detail(withdraw._id)
#         self.assertIsNotNone(read.to_dict()['withdrawn_date'])


if __name__ == '__main__':
    unittest.main()
