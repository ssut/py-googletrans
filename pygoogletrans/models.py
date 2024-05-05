from typing import Any, Dict, Union

from httpx import Response


class Base:
    """Base result object"""

    def __init__(self, response: Union[Response, None] = None):
        self._response = response


class Translated(Base):
    """Translate result object

    :param src: source language (default: auto)
    :param dest: destination language (default: en)
    :param origin: original text
    :param text: translated text
    :param pronunciation: pronunciation
    """

    def __init__(
        self,
        src: str,
        dest: str,
        origin: str,
        text: str,
        pronunciation: str,
        extra_data: Union[Dict[Any, Any], None] = None,
        response: Union[Response, None] = None,
    ):
        super().__init__(response)
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation
        self.extra_data = extra_data

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return (
            f"Translated(src={self.src}, dest={self.dest}, text={self.text}, pronunciation={self.pronunciation},"
            f'extra_data={repr(self.extra_data)[:10] + "..."})'
        )


class Detected(Base):
    """Language detection result object

    :param lang: detected language
    :param confidence: the confidence of detection result (0.00 to 1.00)
    """

    def __init__(
        self,
        lang: str,
        confidence: float,
        response: Union[Response, None] = None,
    ):
        super().__init__(response)
        self.lang = lang
        self.confidence = confidence

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return f"Detected(lang={self.lang}, confidence={self.confidence})"
