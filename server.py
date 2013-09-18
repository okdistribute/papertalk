#!/usr/bin/env python
from papertalk import papertalk

def app():
    papertalk.run(port=4324, debug = True)

if __name__ == "__main__":
    app()
