# -*- coding: utf-8 -*-
"""
    Internationalisation using Babel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The locale support of tornado as such is pretty basic and does not offer
    support for merging translation catalogs and several other features most
    multi language applications require.

    This module tries to retain the same API as that of tornado.locale while
    implement the required features with the support of babel.

    .. note::
        CSV Translations are not supported

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :copyright: (c) 2009 by Facebook (Tornado Project)
    :license: BSD, see LICENSE for more details.

    :changes:
        12/11/23 - E. PASCUAL (Centre Scientifique et Technique du Batiment):
            fixed implementation of translations merge process in
            load_gettext_translations
"""
import logging
import os

from babel.support import Translations, NullTranslations
from babel.core import Locale as BabelCoreLocale
from babel import dates

_default_locale = "en_US"
_translations = {}
_supported_locales = frozenset([_default_locale])
_use_gettext = False


def get(*locale_codes):
    """Returns the closest match for the given locale codes.

    We iterate over all given locale codes in order. If we have a tight
    or a loose match for the code (e.g., "en" for "en_US"), we return
    the locale. Otherwise we move to the next code in the list.

    By default we return en_US if no translations are found for any of
    the specified locales. You can change the default locale with
    set_default_locale() below.
    """
    return Locale.get_closest(*locale_codes)


def set_default_locale(code):
    """Sets the default locale, used in get_closest_locale().

    The default locale is assumed to be the language used for all strings
    in the system. The translations loaded from disk are mappings from
    the default locale to the destination locale. Consequently, you don't
    need to create a translation file for the default locale.
    """
    global _default_locale
    global _supported_locales
    _default_locale = code
    _supported_locales = frozenset(
        list(_translations.keys()) + [_default_locale])


def load_gettext_translations(directory, domain):
    """Loads translations from gettext's locale tree"""
    global _translations
    global _supported_locales
    global _use_gettext
    for lang in os.listdir(directory):
        if lang.startswith('.'):
            continue  # skip .svn, etc
        if os.path.isfile(os.path.join(directory, lang)):
            continue
        try:
            translation = Translations.load(directory, [lang], domain)
            if lang in _translations:
                _translations[lang].merge(translation)
            else:
                _translations[lang] = translation

        except Exception as e:
            logging.error("Cannot load translation for '%s': %s", lang, str(e))
            continue
    _supported_locales = frozenset(
        list(_translations.keys()) + [_default_locale])
    _use_gettext = True
    logging.info("Supported locales: %s", sorted(_supported_locales))


def _default_locale_detector(request):
    _code = request.cookies.get('locale', False)
    if not _code:
        # get locale from browser
        locale_code = request.headers.get('ACCEPT-LANGUAGE', 'en')[:2]
        try:
            _code = str(locale.Locale.parse(locale_code, sep='-'))
        except (ValueError, UnknownLocaleError):
            pass

    return _code

_locale_detector = _default_locale_detector


def set_locale_detector(detector):
    """Sets language detector function.

    Detector function takes a request and return a locale code.
    >>> def detector(request):
    ...     if request.url.host == 'es.example.com':
    ...         return 'es'
    ...     elif request.url.host == 'zh.example.com':
    ...         return 'zh'
    ...     else:
    ...         return 'en'
    """
    global _locale_detector
    _locale_detector = detector


def detect_locale(request):
    global _locale_detector
    return _locale_detector(request)


class Locale(BabelCoreLocale):

    """Object representing a locale.

    After calling one of `load_translations` or `load_gettext_translations`,
    call `get` or `get_closest` to get a Locale object.
    """
    @classmethod
    def get_closest(cls, *locale_codes):
        """Returns the closest match for the given locale code."""
        for code in locale_codes:
            if not code:
                continue
            code = code.replace("-", "_")
            parts = code.split("_")
            if len(parts) > 2:
                continue
            elif len(parts) == 2:
                code = parts[0].lower() + "_" + parts[1].upper()
            if code in _supported_locales:
                return cls.get(code)
            if parts[0].lower() in _supported_locales:
                return cls.get(parts[0].lower())
        return cls.get(_default_locale)

    @classmethod
    def get(cls, code):
        """Returns the Locale for the given locale code.

        If it is not supported, we raise an exception.
        """
        if not hasattr(cls, "_cache"):
            cls._cache = {}
        if code not in cls._cache:
            assert code in _supported_locales
            translations = _translations.get(code, NullTranslations())
            locale = cls.parse(code)
            locale.translations = translations
            cls._cache[code] = locale
        return cls._cache[code]

    def translate(self, message, plural_message=None, count=None, **kwargs):
        """
        Translates message and returns new message as str

        :param str message: original message
        :param str plural_message: plural format of the message
        :param int count: number proper plural message for generation
        :param kwargs: named placeholders for message templating
        :return str: translated message
        """
        if plural_message is not None:
            assert count is not None
            message = self.translations.ungettext(
                message, plural_message, count)
        else:
            message = self.translations.ugettext(message)

        return message.format(**kwargs) if len(kwargs) else message

    def format_datetime(self, datetime=None, format='medium', tzinfo=None):
        """
        Return a date formatted according to the given pattern.

        :param datetime: the datetime object; if None, the current date and
                         time is used
        :param format: one of "full", "long", "medium", or "short", or a
                       custom date/time pattern
        :param tzinfo: the timezone to apply to the time for display

        >>> from datetime import datetime
        >>> locale = Locale.parse('pt_BR')
        >>> locale
        <Locale "pt_BR">
        >>> dt = datetime(2007, 04, 01, 15, 30)
        >>> locale.format_datetime(dt)
        u'01/04/2007 15:30:00'
        """
        return dates.format_datetime(datetime, format, tzinfo, self)

    def format_date(self, date=None, format='medium'):
        """
        Return a date formatted according to the locale.

        :param date: the date or datetime object; if None, the current date
                     is used
        :param format: one of "full", "long", "medium", or "short", or a
                       custom date/time pattern
        """
        return dates.format_date(date, format, self)

    def format_time(self, time=None, format='medium', tzinfo=None):
        """
        Return a time formatted according to the locale.

        :param time: the time or datetime object; if None, the current time
                     in UTC is used
        :param format: one of "full", "long", "medium", or "short", or a
                       custom date/time pattern
        :param tzinfo: the time-zone to apply to the time for display
        """
        return dates.format_time(time, format, tzinfo, self)

    def format_timedelta(self, delta, granularity='second',
                         threshold=0.84999999999999998):
        """
        Return a time delta according to the rules of the given locale.

        :param delta: a timedelta object representing the time difference to
                      format, or the delta in seconds as an int value
        :param granularity: determines the smallest unit that should be
                            displayed, the value can be one of "year",
                            "month", "week", "day", "hour", "minute" or
                            "second"
        :param threshold: factor that determines at which point the
                          presentation switches to the next higher unit
        """
        return dates.format_timedelta(delta, granularity, threshold, self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
