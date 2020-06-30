# pyReframe

A python port of re-frame from clojure(script).

## Why?

[re-frame](http://www.github.com/day8/reframe) is a great pattern for working with changing state.
 re-frame originally is intended to be used in building SPAs,
 but I found myself using the pattern in other contexts, and found it useful for python.

## How:

### reframe class 


the beauty and speed of fpr comes from the use of persistent, immutable data structures. 
For that reason, the re-frame database is a [pyrsistent](https://github.com/tobgu/pyrsistent) pmap,
 which implements persistent data structures in python.

The other dependnecy is [pyRx](https://github.com/ReactiveX/RxPY), which implements reactive programming in python.

### subscriptions



### events

### dispatch

### interceptors

Default interceptors for a reframe object can be retrived in the `.interceptors` attribute. 


