class Translated(object):
    """
    The Translated object, which contains Google Translator's result.

    :param src: source langauge (default: auto)
    :param dest: destination language (default: en)
    :param origin: original text
    :param text: translated text
    :param pronunciation: the pronunciation provided by Google Translator
    """
    def __init__(self, src, dest, origin, text, pronunciation):
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'<Translated src={src} dest={dest} text={text} pronunciation={pronunciation}>'.format(
            src=self.src, dest=self.dest, text=self.text, pronunciation=self.pronunciation)

class Detected(object):
    """
    The detected object, which contains Google Translator's langauge detection result.

    :param lang: detected language
    :param confidence: the confidence of detection (0.00 to 1.00)
    """
    def __init__(self, lang, confidence):
        self.lang = lang
        self.confidence = confidence

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'<Detected lang={lang} confidence={confidence}>'.format(
            lang=self.lang, confidence=self.confidence)

