class Translated(object):
    """Translate result object

    :param src: source language detected by google
    :param confidence: confidence of the detection
    :param dest: destination language (default: en)
    :param origin: original text
    :param text: translated text
    :param pronunciation: pronunciation
    """
    def __init__(self, src, confidence, dest, origin, text, pronunciation):
        self.src = src
        self.confidence = confidence
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation

    def __str__(self):  # pragma: nocover
        return self.__unicode__()

    def __unicode__(self):  # pragma: nocover
        return u'Translated(src={src}, confidence={confidence}, dest={dest}, text={text}, pronunciation={pronunciation})'.format(
            src=self.src, confidence=self.confidence, dest=self.dest,
            text=self.text, pronunciation=self.pronunciation,
        )

class Detected(object):
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
