Flaskr
======

Localhost version


The OpenAlpr app built with  Flask `tutorial`_.


Install dev 
-------
    $ python3 -m venv .venv
    $ . .venv/bin/activate
    $ pip install -e .
---

Install Production
-------
    $ python3 -m venv .venv
    $ . .venv/bin/activate
    $ python3 -m build --wheel
    $ pip install -e .
---
.. code-block:: text

    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug

Open http://192.168.56.10:5000 in a browser.

