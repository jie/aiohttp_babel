import asyncio
from speaklater import is_lazy_string, make_lazy_string
from aiohttp_babel import locale

REQUEST_CONTEXT_KEY = 'aiohttp_jinja2_context'

# from tornadobabel import locale


def make_lazy_gettext(lookup_func):
    def lazy_gettext(string, *args, **kwargs):
        if is_lazy_string(string):
            return string
        return make_lazy_string(lookup_func(), string, *args, **kwargs)
    return lazy_gettext


@asyncio.coroutine
def context_processors_middleware(app, handler):
    @asyncio.coroutine
    def middleware(request):
        _locale = locale.get(request.cookies.get('locale', 'zh_CN'))
        if REQUEST_CONTEXT_KEY in request:
            request['_'] = make_lazy_gettext(lambda: _locale.translate)
        return (yield from handler(request))
    return middleware
