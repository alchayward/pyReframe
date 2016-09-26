def update_in(data, path, new_value):
    return data.transform(path, lambda x: x.update(new_value))


def get_in(data, path):
    while path:
        data = data[path[0]]
        path = path[1:]
    return data


def to_list(*args):
    return list(args)
