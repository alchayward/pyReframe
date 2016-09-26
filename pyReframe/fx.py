def update_db_fn(frame):
    def update_db(db):
        frame.db.reset(db)
    return update_db


def do_fx_fn(frame):
    def do_fx(effects):
        for e, v in effects.items():
            try:
                frame.fx[e](v)
            except KeyError:
                print('fx not registered: ' + e)

    return do_fx


def dispatch_fn(frame):
    try:
        stream = frame.event_stream
    except AttributeError:
        print('no stream to dispatch to')
        raise

    def dispatch(event):
        stream.on_next(event)
    return dispatch


def import_fx(frame):
    return {'dispatch': dispatch_fn(frame),
            'do_fx': do_fx_fn(frame),
            'db': update_db_fn(frame),
            }
