===============================================================
Googletrans: Free and Unlimited Google translate API for Python
===============================================================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: http://opensource.org/licenses/MIT
.. image:: https://travis-ci.org/ssut/py-googletrans.svg?branch=master
   :target: https://travis-ci.org/ssut/py-googletrans
.. image:: https://readthedocs.org/projects/py-googletrans/badge/?version=latest
   :target: https://readthedocs.org/projects/py-googletrans/?badge=latest
.. image:: https://badge.fury.io/py/googletrans.svg
   :target: http://badge.fury.io/py/googletrans
.. image:: https://coveralls.io/repos/github/ssut/py-googletrans/badge.svg
   :target: https://coveralls.io/github/ssut/py-googletrans
.. image:: https://codeclimate.com/github/ssut/py-googletrans/badges/gpa.svg
   :target: https://codeclimate.com/github/ssut/py-googletrans

Googletrans is a **free** and **unlimited** python library that
implemented Google Translate API. This uses the `Google Translate Ajax
API <https://translate.google.com>`__ to make calls to such methods as
detect and translate.

--------
Features
--------

-  Fast and reliable - it uses the same servers that
   translate.google.com uses
-  Auto language detection
-  Bulk translations
-  Customizable service URL
-  Connection pooling (the advantage of using requests.Session)
-  HTTP/2 support

~~~~~~~~~~~~~~~~~~~~~
Note on library usage
~~~~~~~~~~~~~~~~~~~~~

-  The maximum character limit on a single text is 15k.

-  Due to limitations of the web version of google translate, this API
   does not guarantee that the library would work properly at all times.
   (so please use this library if you don't care about stability.)

-  If you want to use a stable API, I highly recommend you to use
   `Google's official translate
   API <https://cloud.google.com/translate/docs>`__.

-  If you get HTTP 5xx error or errors like #6, it's probably because
   Google has banned your client IP address.

----------
Quickstart
----------

You can install it from PyPI_:

.. sourcecode:: bash

   $ pip install googletrans

.. _PyPI: https://pypi.python.org/pypi/googletrans

~~~~~~~~~~~~~~
HTTP/2 support
~~~~~~~~~~~~~~

This is a great deal for everyone! (up to 2x times faster in my test) If
you want to get googletrans faster you should install
`hyper <https://github.com/Lukasa/hyper>`__ package. Googletrans will
automatically detect if hyper is installed and if so, it will be used
for http networking.

~~~~~~~~~~~
Basic Usage
~~~~~~~~~~~

If source language is not given, google translate attempts to detect the
source language.

.. code-block:: python

   >>> from googletrans import Translator
   >>> translator = Translator()
   >>> translator.translate('안녕하세요.')
   # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>

   >>> translator.translate('안녕하세요.', dest='ja')
   # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>

   >>> translator.translate('veritas lux mea', src='la')
   # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

~~~~~~~~~~~~~~~~~~~~~
Customize service URL
~~~~~~~~~~~~~~~~~~~~~

You can use another google translate domain for translation. If multiple
URLs are provided it then randomly chooses a domain.

.. code:: python

    >>> from googletrans import Translator
    >>> translator = Translator(service_urls=[
          'translate.google.com',
          'translate.google.co.kr',
        ])

~~~~~~~~~~~~~~~~~~~~~
Advanced Usage (Bulk)
~~~~~~~~~~~~~~~~~~~~~

Array can be used to translate a batch of strings in a single method
call and a single HTTP session. The exact same method shown above work
for arrays as well.

.. code:: python

    >>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
    >>> for translation in translations:
    ...    print(translation.origin, ' -> ', translation.text)
    # The quick brown fox  ->  빠른 갈색 여우
    # jumps over  ->  이상 점프
    # the lazy dog  ->  게으른 개

~~~~~~~~~~~~~~~~~~
Language detection
~~~~~~~~~~~~~~~~~~

The detect method, as its name implies, identifies the language used in
a given sentence.

.. code:: python

    >>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
    # <Detected lang=ko confidence=0.27041003>
    >>> translator.detect('この文章は日本語で書かれました。')
    # <Detected lang=ja confidence=0.64889508>
    >>> translator.detect('This sentence is written in English.')
    # <Detected lang=en confidence=0.22348526>
    >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
    # <Detected lang=eo confidence=0.10538048>

---------
API Guide
---------


======================
googletrans.Translator
======================

.. autoclass:: googletrans.Translator
    :members:

==================
googletrans.models
==================

.. automodule:: googletrans.models
    :members:

==================
googletrans.gtoken
==================

.. hint::

   This is for internal use only to generate a valid token to access
   translate.google.com ajax API.

.. automodule:: googletrans.gtoken
    :members:

=====================
googletrans.LANGUAGES
=====================

.. hint::

   iso639-1 language codes for
   `supported languages <https://developers.google.com/translate/v2/using_rest#language-params>`_
   for translation. Some language codes also include a country code, like zh-CN or zh-TW.

.. literalinclude:: ../googletrans/constants.py
   :language: python
   :lines: 70-182
   :linenos:

================================
googletrans.DEFAULT_SERVICE_URLS
================================

.. hint::

   `DEFAULT_SERVICE_URLS <https://github.com/ssut/py-googletrans/blob/master/googletrans/constants.py#L3:1>`_ is the list of current available Google Translation service urls.
   
   For using these service urls, please check `Customize service URL`_.