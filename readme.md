# pyReframe

A python port of reframe from clojure.

## Why?

[reframe](http://www.github.com/day8/reframe "Title) is a great pattern for working with changing state. reframe originally is intended to be used in building SPAs, but I found myself using the library in other contexts.

## How:
Instead of a single library, we acutally have a reframe object, which instanticates the database, and methods.
```
from pyReframe import Reframe
R = Reframe()

```

the beauty and speed of fpr comes from the use of persistent, immutable datastructures. for that reason, the reframe database is a [pyrsistent](https://github.com/tobgu/pyrsistent "Title") pmap, which impliments persistent sdata strucutures in python.

The other dependnecy is pyRx, which impliments reactive programming in python.

