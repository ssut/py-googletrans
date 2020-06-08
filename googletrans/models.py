class Translated:
    """Translate result object

    :param src: source langauge (default: auto)
    :param dest: destination language (default: en)
    :param origin: original text
    :param text: translated text
    :param pronunciation: pronunciation
    """
    def __init__(self, src, dest, origin, text, pronunciation, extra_data=None):
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation
        self.extra_data = extra_data

    def __str__(self):  # pragma: nocover
        return self.__unicode__()

    def __unicode__(self):  # pragma: nocover
        return (
            u'Translated(src={src}, dest={dest}, text={text}, pronunciation={pronunciation}, '
            u'extra_data={extra_data})'.format(
                src=self.src, dest=self.dest, text=self.text,
                pronunciation=self.pronunciation,
                extra_data='"' + repr(self.extra_data)[:10] + '..."'
            )
        )


class Detected:
    """Language detection result object

    :param lang: detected language
    :param confidence: the confidence of detection result (0.00 to 1.00)
    """
    def __init__(self, lang, confidence):
        self.lang = lang
        self.confidence = confidence

    def __str__(self):  # pragma: nocover
        return self.__unicode__()

    def __unicode__(self):  # pragma: nocover
        return u'Detected(lang={lang}, confidence={confidence})'.format(
            lang=self.lang, confidence=self.confidence)
