from interceptors import update_effects, update_coeffects
from cofx import cofx_injector
from pyrsistent import discard, pmap, inc
from helper_tools import update_in, get_in


def do_fx_interceptor(frame):
    do_fn = frame.fx['do_fx']

    def after(context):
        do_fn(context['effects'])
        return context

    return {'id': 'do_fx', 'after': after}


def db_interceptor(frame):
    def before(context):
        return update_coeffects(context, 'db', frame.db)

    return {'id': 'add_db', 'before': before}


def fx_handler_to_interceptor(handler_fn):
    def before(context):
        return update_in(context, ['effects'], pmap(handler_fn(context['coeffects'], context['coeffects']['event'])))

    return {'id': 'fx_handler', 'before': before}


def db_handler_to_interceptor(handler_fn):
    def before(context):
        return update_in(context, ['effects'], pmap({'db': handler_fn(context['coeffects']['db'],
                                                                      context['coeffects']['event'])}))

    return {'id': 'db_handler', 'before': before}


def ctx_handler_to_interceptor(handler_fn):
    return {'id': 'ctx_handler', 'before': handler_fn}


def path_interceptor(path):
    # not done correctly yet
    # need to make this nestable. but that would require a unique identifier for the db
    def before(context):
        db = context['coeffects']['db']
        context = update_effects(context, 'original_db', db)
        context = update_coeffects(context, 'db', get_in(db, path))
        return context

    def after(context):
        db = context['effects']['original_db'].transform(path, context['effects']['db'])
        context = context.transform(['effects', 'db'], db)
        context = context.transform(['effects', 'original_db'], discard)
        return context

    return {'id': 'path', 'before': before, 'after': after}


def trim_v_interceptor():
    def before(context):
        return context.transform(['coeffects', 'event', 0], discard)

    return {'id': 'trim_v', 'before': before}


def event_counter():
    """interceptor that adds a counter for a type of event"""

    def before(context):
        event_id = context['coeffects']['event'][0]  # better call before trim. could put a check in for that...
        # Maybe this should happen after the handler is called?
        # check for existence and create first. This is bad python
        if not context['coeffects']['db'].__contains__('counters'):
            context = update_in(context, ['coeffects', 'db'], pmap({'counters': pmap()}))
        if not context['coeffects']['db']['counters'].__contains__(event_id):
            context = update_in(context, ['coeffects', 'db', 'counters'], {event_id: 0})
        return context.transform(['coeffects', 'db', 'counters', event_id], inc)

    return {'id': 'event_counter', 'before': before}


def import_std_interceptors(frame):
    # some of these return interceptor factories...
    return {'do_fx': do_fx_interceptor(frame),
            'coeffects': cofx_injector(frame),
            'db': cofx_injector(frame)('db'),
            'trim_v': trim_v_interceptor(),
            'path': path_interceptor,
            'db_handler': db_handler_to_interceptor,
            'fx_handler': fx_handler_to_interceptor,
            'ctx_handler': ctx_handler_to_interceptor,
            'counter': event_counter(),
            }
