import asyncio
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

_ = make_lazy_gettext(lambda: _thread_locals.locale.translate)


@asyncio.coroutine
def babel_middleware(app, handler):
    @asyncio.coroutine
    def middleware(request):
        _code = request.cookies.get('locale', 'en_US')
        _locale = locale.get(_code)
        _thread_locals.locale = request.locale = _locale
        response = yield from handler(request)
        return response
    return middleware


def get_current_locale():
    return getattr(_thread_locals, 'locale', None)
