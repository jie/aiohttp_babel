from speaklater import is_lazy_string, make_lazy_string
from aiohttp_babel import locale
from threading import local

_thread_locals = local()


def make_lazy_gettext(lookup_func):
    def lazy_gettext(string, *args, **kwargs):
        if is_lazy_string(string):
            return string
        return make_lazy_string(lookup_func(), string, *args, **kwargs)
    return lazy_gettext


def translate(source):
    return _thread_locals.locale.translate(source)


lazy_translate = make_lazy_gettext(lambda: translate)

# next line is keep just for backward compatibility
_ = make_lazy_gettext(lambda: _thread_locals.locale.translate)


async def babel_middleware(app, handler):
    async def middleware(request):
        # get locale from cookie
        _code = locale.detect_locale(request)
        _thread_locals.locale = request.locale = locale.get(_code)
        response = await handler(request)
        return response
    return middleware


def get_current_locale():
    return getattr(_thread_locals, 'locale', None)
