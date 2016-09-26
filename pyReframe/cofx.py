from helper_tools import update_in


def cofx_injector(frame):
    def inject_cofx(cofx_id, value=None):
        def before(context):
            handler = frame.cofx[cofx_id]
            if value:
                handler = lambda: handler(value)
            return update_in(context, ['coeffects'], {cofx_id: handler()})

        return {'id': 'coeffects', 'before': before}

    return inject_cofx


def add_db_fn(frame):
    def add_db():
        return frame.db.value

    return add_db


def import_cofx(frame):
    return {'db': add_db_fn(frame)}
