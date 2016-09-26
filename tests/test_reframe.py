from pyReframe import Reframe
from unittest import TestCase, TestLoader
from pyrsistent import pmap, inc

default_db = pmap({'foo': 'bar'})


class TestReframe(TestCase):
    def setUp(self):
        self.r = Reframe(default_db)

    def tearDown(self):
        # self.R.dispose()
        self.r = None

    def test_handle_event(self):
        r = self.r

        def handler(db, event):
            print(event)
            return db.update({'test': True})

        r.reg_handler('test', [], handler)
        r.fx['dispatch'](['test'])
        # r.handle_%event(r.event_queue[0])
        self.assertEqual(r.db.value, pmap({'foo': 'bar', 'test': True}))

    def test_queue(self):
        r = Reframe(pmap({'count': 0}))

        def inc_handler(db, event):
            return db.transform(['count'], inc)

        r.reg_handler('count', [], inc_handler)
        r.fx['dispatch'](['count'])
        r.fx['dispatch'](['count'])
        r.fx['dispatch'](['count'])
        r.fx['dispatch'](['count'])
        # r.handle_%event(r.event_queue[0])
        self.assertEqual(r.db.value, pmap({'count': 4}))

    def test_dispatch(self):
        r = self.r
        event = ['test', 'value']
        v = []
        f = lambda x: v.append(x)

        vx = r.event_stream.subscribe(f)
        r.fx['dispatch'](event)
        self.assertEquals(v[0], event)

    def test_add_default_interceptors(self):
        pass

    def test_reg_handler(self):
        pass

    def test_subscribe(self):
        pass


suite = TestLoader().loadTestsFromTestCase(TestReframe)
