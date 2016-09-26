from interceptors import execute



def flatten_and_remove_nones(interceptors):
    ints = []
    for i in interceptors:
        if isinstance(i, list):
            ints = ints + flatten_and_remove_nones(i)
        elif i:
            ints.append(i)
    return ints


def register_event_fn(frame):
    def register_event(event_id, interceptors):
        frame.events.update({event_id: flatten_and_remove_nones(interceptors)})

    return register_event


def event_handler_fn(frame):
    def handle(event_v):
        try:
            interceptors = frame.events[event_v[0]]
            execute(event_v, interceptors)
        except KeyError:
            print('no event: ' + event_v[0] + ' in registry')

    return handle
