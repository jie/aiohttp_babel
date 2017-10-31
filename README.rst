aiohttp_babel
=============


aiohttp_babel adds i18n and l10n support to aiohttp.

Usage:

.. code-block:: python

    import aiohttp_jinja2
    from aiohttp.web import Application
    from aiohttp_babel.locale import (load_gettext_translations,
                                      set_default_locale,
                                      set_locale_detector)
    from aiohttp_babel.middlewares import babel_middleware, _


    set_default_locale('en_GB')  # set default locale, if necessary
    # load compiled locales
    load_gettext_translations('/path/to/locales', 'domain')

    # you can use your own locale detection method, if necessary.
    # aiohttp_babel checks cookie parameter `locale` or `Accept-Language`
    # header by default.
    def detector(request):
        if request.url.host == 'es.example.com':
            return 'es'
        elif request.url.host == 'zh.example.com':
            return 'zh'
        else:
            return 'en'
    set_locale_detector(detector)

    jinja_loader = jinja2.FileSystemLoader('./templates')
    app = Application(middlewares=[babel_middleware])

    aiohttp_jinja2.setup(app, loader=jinja_loader)
    jinja_env = aiohttp_jinja2.get_env(app)
    jinja_env.globals['_'] = _


How to extract & compile locales:
-----

http://babel.pocoo.org/en/latest/messages.html

http://babel.pocoo.org/en/latest/cmdline.html


Code from:
---------

tornado-babel: https://github.com/openlabs/tornado-babel

django-babel: https://github.com/python-babel/django-babel


