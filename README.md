Papertalk: Discuss scholarly articles online.
=========

Academic research is discussed all over the place - at conferences, in lab meetings, at departmental teas, on blogs, 
on Twitter - but there is no home for these conversations on the web. 

Papertalk is the place to go to discuss, criticize, and learn about academic research.

### Pull Requests Welcome

## setup
```
$ python setup.py develop
$ bower install
$ npm install
```

## config

Edit the config.py to match your mongo database 
(yeah, you'll need one for yourself. try using a free [mongolab sandbox](http://www.mongolab.com))

You'll also need to get some mendeley API keys, but those are [free too](http://apidocs.mendeley.com).
```
$ cp config_sample.py config.py
```

## compile coffeescript to js
```
$ grunt watch
```

## run
```
$ python server.py 
```

much love,  
[@karissamck](https://twitter.com/karissamck)  
[@beaucronin](https://twitter.com/beaucronin)
