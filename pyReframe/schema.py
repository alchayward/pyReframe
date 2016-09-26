# Need to get a schema library to do a bit of validation

from pyrsistent import pmap, pvector

context = pmap({'queue': pvector, 'stack': pvector, 'effects': pmap, 'coeffects':pmap})

interceptor_fn = {'context': 'context'}

interceptor = {'id': str, 'before': interceptor_fn, 'after': interceptor_fn}