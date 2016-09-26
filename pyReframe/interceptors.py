import pyrsistent as pr


def update_effects(context, key, value):
    return context['effects'].update({key: value})


def update_coeffects(context, key, value):
    return context['coeffects'].update({key: value})


def ppop(v):
    return v[0], v.delete(0)


def invoke_interceptors_fn(context, interceptor, direction):
    try:
        return interceptor[direction](context)
    except KeyError:
        return context


def invoke_interceptors(context, direction):
    c = context
    while c['queue']:
        (interceptor, queue) = ppop(c['queue'])
        stack = c['stack'].append(interceptor)
        c = invoke_interceptors_fn(c, interceptor, direction)
        c = c.update({'queue': queue, 'stack': stack})
    return c


def new_context(event, interceptors):
    return pr.pmap({'coeffects': pr.pmap({'event': event}),
                    'effects': pr.pmap(),
                    'queue': pr.pvector(interceptors),
                    'stack': pr.pvector()})


def change_direction(context):
    return context.update({'queue': context['stack'], 'stack': context['queue']})


def execute(event, interceptors):
    return invoke_interceptors(
        change_direction(
            invoke_interceptors(
                new_context(event, interceptors), 'before')),
        'after')
