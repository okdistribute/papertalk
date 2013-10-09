papertalk
=========

Discuss scholarly articles online.

## setup
```
$ python setup.py develop
$ bower install
$ npm install
```

## config

Edit the config.py to match your mongo database (yeah, you'll need one for yourself. try using a free [mongolab sandbox](http://www.mongolab.com))
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
