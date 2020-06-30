from pyrsistent import pmap
from pyReframe.std_interceptors import import_std_interceptors
from pyReframe.fx import import_fx, dispatch_fn
from pyReframe.cofx import import_cofx
from pyReframe.events import register_event_fn, event_handler_fn
from rx.subject import Subject
from pyReframe.subs import register_sub_fn, register_db, RAtom


class Reframe(object):
    def __init__(self, db=pmap()):
        self.db = RAtom(db)

        # event queue
        self.event_stream = Subject()  # blinker.Signal()
        self.event_handler = self.event_stream.subscribe(event_handler_fn(self))
        self.dispatch = dispatch_fn(self)

        # registries: I may want to move these into a combined registry structure, with a registration function...
        self.fx = dict()
        self.events = dict()
        self.cofx = dict()

        # functions
        self.reg_event = register_event_fn(self)

        # default registrations
        self.fx.update(import_fx(self))
        self.cofx.update(import_cofx(self))
        self.interceptors = import_std_interceptors(self)

        # pyReframe
        self.subscriptions = dict()
        self.register_sub = register_sub_fn(self)
        register_db(self)

    def add_default_interceptors(self, interceptors):
        return [self.interceptors['do_fx'], self.interceptors['db']] + interceptors

    def reg_fx(self, event_id, fx_fn):
        self.fx.update({'event_id': event_id, 'fx': fx_fn})

    def reg_handler(self, event_id, interceptors, handler_fn):
        ints = self.add_default_interceptors(interceptors) + [
            self.interceptors['db_handler'](handler_fn)]
        self.reg_event(event_id, ints)

    def subscribe(self):
        pass

    def dispose(self):
        self.event_stream.dispose()
