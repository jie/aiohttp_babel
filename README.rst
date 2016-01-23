aiohttp_babel
=============


aiohttp_babel adds i18n and l10n support to aiohttp.

Usage:

.. code-block:: python

    import aiohttp_jinja2
    from aiohttp.web import Application
    from aiohttp_babel.middlewares import babel_middleware
    from aiohttp_babel.middlewares import _

    jinja_loader = jinja2.FileSystemLoader('./templates')
    app = Application(middlewares=babel_middleware)

    aiohttp_jinja2.setup(app, loader=jinja_loader)
    jinja_env = aiohttp_jinja2.get_env(app)
    jinja_env.globals['_'] = _



Code from:
---------

tornado-babel: https://github.com/openlabs/tornado-babel

django-babel: https://github.com/python-babel/django-babel

