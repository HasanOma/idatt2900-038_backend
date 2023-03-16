import asynctest
from MTP_038_backend.models import Ship  # Replace with your actual import statement
from MTP_038_backend.models import Token  # Replace with your actual import statement

from collections import namedtuple


class TestModelAdmin(asynctest.TestCase):

    async def test_create(self):
        # Replace with your actual table fields
        kwargs = {
            'mmsi': 123456789,
            'name': 'Test Ship'
        }
        created = await Ship.create(kwargs)
        Skip = namedtuple('Skip',
                          ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                           'destination',
                           'eta', 'shipLength', 'shipWidth'])
        created = dict(zip(Skip._fields, created))
        # Add more assertions based on your specific data model
        self.assertIsNotNone(created)
        self.assertEqual(created['mmsi'], kwargs['mmsi'])
        self.assertEqual(created['name'], kwargs['name'])

    async def test_create_multi(self):
        # Replace with your actual table fields and multiple entities
        entities = [
            {
                'mmsi': 123456789,
                'name': 'Test Ship 1'
            },
            {
                'mmsi': 987654321,
                'name': 'Test Ship 2'
            }
        ]
        await Ship.create_multi(entities)
        # Add more assertions based on your specific data model
        for entity in entities:
            stored_entity = await Ship.get(entity['mmsi'])
            Skip = namedtuple('Skip',
                              ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                               'destination',
                               'eta', 'shipLength', 'shipWidth'])
            stored_entity = dict(zip(Skip._fields, stored_entity))
            self.assertIsNotNone(stored_entity)
            self.assertEqual(stored_entity['mmsi'], entity['mmsi'])
            self.assertEqual(stored_entity['name'], entity['name'])

    async def test_merge_token(self):
        # Replace with your actual table fields
        kwargs = {
            'id': 1,
            'bearer': 'some_token'
        }
        merged = await Token.merge_token(**kwargs)
        Skip = namedtuple('Skip',
                          ['id', 'bearer'])
        merged = dict(zip(Skip._fields, merged))
        # Add more assertions based on your specific data model
        self.assertIsNotNone(merged)
        self.assertEqual(merged['id'], kwargs['id'])
        self.assertEqual(merged['bearer'], kwargs['bearer'])

    async def test_update_ship_fields(self):
        # Replace with your actual table fields and desired updates
        mmsi = 123456789
        fields = {
            'name': 'Updated Test Ship'
        }
        updated = await Ship.update_ship_fields(mmsi, fields)
        Skip = namedtuple('Skip',
                          ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                           'destination',
                           'eta', 'shipLength', 'shipWidth'])
        updated = dict(zip(Skip._fields, updated))
        # Add more assertions based on your specific data model
        self.assertIsNotNone(updated)
        self.assertEqual(updated['mmsi'], mmsi)
        self.assertEqual(updated['name'], fields['name'])

    async def test_get(self):
        # Replace with an existing ID in your database
        mmsi = 123456789
        fetched = await Ship.get(mmsi)
        Skip = namedtuple('Skip',
                          ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                           'destination',
                           'eta', 'shipLength', 'shipWidth'])
        fetched = dict(zip(Skip._fields, fetched))
        # Add more assertions based on your specific data model
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched['mmsi'], mmsi)

    async def test_get_basic(self):
        # Replace with an existing ID in your database
        mmsi = 123456789
        fetched = await Ship.get_basic(mmsi)
        Skip = namedtuple('Skip',
                          ['mmsi', 'name', 'msgtime', 'latitude', 'longitude', 'speedOverGround', 'shipType',
                           'destination',
                           'eta', 'shipLength', 'shipWidth'])
        fetched = dict(zip(Skip._fields, fetched))
        # Add more assertions based on your specific data model
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched['mmsi'], mmsi)

    async def test_get_token(self):
        # Replace with an existing ID in your database
        id = 1
        fetched = await Token.get_token(id)
        Skip = namedtuple('Skip',
                          ['id', 'bearer'])
        fetched = dict(zip(Skip._fields, fetched))
        # Add more assertions based on your specific data model
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched['id'], id)


if __name__ == '__main__':
    asynctest.main()
