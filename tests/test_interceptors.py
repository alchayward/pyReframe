from interceptors import new_context
from pyrsistent import pmap, pvector
# from py_reframe import Reframe
from unittest import TestCase, TestLoader


class TestInterceptors(TestCase):
    def test_new_context(self):
        self.assertEquals(new_context(['test', 1], []),
                          pmap({'coeffects': pmap({'event': ['test', 1]}),
                                'effects': pmap(),
                                'queue': pvector([]),
                                'stack': pvector()}))


suite = TestLoader().loadTestsFromTestCase(TestInterceptors)
