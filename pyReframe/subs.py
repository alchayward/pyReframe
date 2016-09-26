from rx.subjects import Subject
from pyReframe.helper_tools import to_list


class RAtom(object):
    def __init__(self, initial_value=None):
        self.subject = Subject()
        self.stream = self.subject.distinct_until_changed()
        self.value = initial_value
        self.reset(initial_value)

        def change_value(v):
            self.value = v

        self.stream.subscribe(change_value)

    def reset(self, new_value):
        self.subject.on_next(new_value)

    def dereference(self):
        return self.value


def reaction(source_atoms, fn):
    """takes a list of r atoms, and a combining function, and returns an Ratom holding the result.
    If any of the values of the sources change then so will the returned value of the Ratom"""
    a = RAtom(fn(*tuple(map(lambda at: at.value, source_atoms))))
    if not len(source_atoms) == 0:
        streams = list(map(lambda at: at.stream, source_atoms))
        s = streams[0].combine_latest(*tuple(streams[1:] + [to_list]))
        s.subscribe(lambda x: a.reset(fn(*tuple(x))))
    return a


def register_sub_fn(frame):
    def register_sub(sub, sources, fn):
        frame.subscriptions.update({sub: reaction(sources, fn)})

    return register_sub


def register_db(frame):
    frame.register_sub('db', [frame.db], lambda x: x)
