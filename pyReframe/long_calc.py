from pyrsistent import pmap, discard
from interceptors import update_effects, update_coeffects
import asyncio


@asyncio.coroutine

def do_long_calc(calc_fn, uid):

    def slow_operation(future):
        result = calc_fn()
        future.set_result(result)

        def callback_fn():
            pass

        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        future.add_done_callback(callback_fn(uid, future.result))

        asyncio.ensure_future(slow_operation(future))
        loop.run_until_complete(future)
        loop.close()




# helper function for scheduling calculations.

# suppose we have a long calculation we want to do.
# Need two functions. a prep function, and a consume function.
# Need some kind of async scheduler., which will issue a dispatch letting it know it's done
# Should try to use interceptors here or something


def async_helper(frame, calc_id, pre_fx_handler, post_fx_handler, scheduler, calc_fn):
    """ : pre_fn: returns a
        : post_fn:
        : calc_id: a unique string for the type of calc
        : scheduler: a schedualer that can be passed a calc, and issue a callback """
    done_str = calc_id + '_done'
    start_str = calc_id + '_started'

    # Should register two events. Run calc, and calc done.
    # and at least one fx, which starts the calc running.

    def pre_after(context):
        # from calc_id in the effects, get out 'state', which holds any info about the calc you might want to keep
        # add the state to the database, in {db, long_calcs, calc_id, uid} (create if necessary)
        # add the function call to the effects
        try:
            state = context['effects'][calc_id]
        except KeyError:
            state = None

        try:
            db = context['db'].update(pmap({calc_id: pmap({'running': True, 'state': state})}))
            context = update_effects(context,'db', db)
            context = update_effects(context, start_str, state['params'])
            return update_effects(context,'db', db)
        except KeyError:
            return context


    pre_interceptor = {'id': start_str,
                       'after': pre_after}

    def post_before(context):
        # get state from db, if it's there and add to the cofx
        cofx = context['coffects']
        uid = cofx['event'][1]

        try:
            state = cofx['db']['long_calc'][calc_id][uid]
            context = update_coeffects(context, 'state', state)
            context = update_coeffects(context, 'db', cofx['db'].transform(['long_calc', calc_id, uid], discard))
        except KeyError:
            pass

        return context

    post_interceptor = {'id': done_str,
                       'before': post_before}

    def callback_fn_fn(uid):
        def callback_fn(result):
            frame.dispatch([done_str, uid, result])
        return callback_fn

    frame.reg_fx_event(calc_id, [pre_interceptor], pre_fx_handler)
    frame.reg_fx_event(done_str, [post_interceptor], post_fx_handler)

    def run_calc_fx(params):
        scheduler.run(calc_fn(params))

    frame.reg_fx(start_str, run_calc_fx)



