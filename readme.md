# pyReframe

A python port of reframe from clojure.

## Why?

[reframe](http://www.github.com/day8/reframe) is a great pattern for working with changing state. reframe originally is intended to be used in building SPAs, but I found myself using the library in other contexts.

## How:
Instead of a single library, we acutally have a reframe object, which instanticates the database, and methods.

### reframe class 
```
from pyReframe import Reframe, pmap
from pyrsistent import pmap

# instantiate a reframe object
R = Reframe(db=pmap({'foo': 'bar'}))
```



the beauty and speed of fpr comes from the use of persistent, immutable datastructures. for that reason, the reframe database is a [pyrsistent](https://github.com/tobgu/pyrsistent) pmap,
 which implements persistent data strucutures in python.

The other dependnecy is [pyRx](https://github.com/ReactiveX/RxPY), which implements reactive programming in python.

### subscriptions



### events

### dispatch

### interceptors

Default interceptors for a reframe object can be retrived in the `.interceptors` attribute. 


