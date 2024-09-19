Googletrans
===========

|GitHub license| |travis status| |Documentation Status| |PyPI version|
|Coverage Status| |Code Climate|

ANNOUNCEMENT: `v4.0 is planned <https://github.com/ssut/py-googletrans/issues/411>`_.

Googletrans is a **free** and **unlimited** python library that
implemented Google Translate API. This uses the `Google Translate Ajax
API <https://translate.google.com>`__ to make calls to such methods as
detect and translate.

Compatible with Python 3.6+.

For details refer to the `API
Documentation <https://py-googletrans.readthedocs.io/en/latest>`__.

Features
--------

-  Fast and reliable - it uses the same servers that
   translate.google.com uses
-  Auto language detection
-  Bulk translations
-  Customizable service URL
-  HTTP/2 support

TODO
~~~~

more features are coming soon.

-  Proxy support
-  Internal session management (for better bulk translations)

HTTP/2 support
~~~~~~~~~~~~~~

This library uses httpx for HTTP requests so HTTP/2 is supported by default.

You can check if http2 is enabled and working by the `._response.http_version` of `Translated` or `Detected` object:

.. code:: python

   >>> translator.translate('테스트')._response.http_version
   # 'HTTP/2'


How does this library work
~~~~~~~~~~~~~~~~~~~~~~~~~~

You may wonder why this library works properly, whereas other
approaches such like goslate won't work since Google has updated its
translation service recently with a ticket mechanism to prevent a lot of
crawler programs.

I eventually figure out a way to generate a ticket by reverse
engineering on the `obfuscated and minified code used by Google to
generate such
token <https://translate.google.com/translate/releases/twsfe_w_20170306_RC00/r/js/desktop_module_main.js>`__,
and implemented on the top of Python. However, this could be blocked at
any time.

--------------

Installation
------------

To install, either use things like pip with the package "googletrans"
or download the package and put the "googletrans" directory into your
python path.

.. code:: bash

    $ pip install googletrans

Basic Usage
-----------

If source language is not given, google translate attempts to detect the
source language.

.. code:: python

    >>> from googletrans import Translator
    >>> translator = Translator()
    >>> translator.translate('안녕하세요.')
    # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
    >>> translator.translate('안녕하세요.', dest='ja')
    # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
    >>> translator.translate('veritas lux mea', src='la')
    # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

Customize service URL
~~~~~~~~~~~~~~~~~~~~~

You can use another google translate domain for translation. If multiple
URLs are provided, it then randomly chooses a domain.

.. code:: python

    >>> from googletrans import Translator
    >>> translator = Translator(service_urls=[
          'translate.google.com',
          'translate.google.co.kr',
        ])

Customize service URL to point to standard api
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Considering translate.google.<domain> url services use the webapp requiring a token, 
you can prefer to use the direct api than does not need any token to process.
It can solve your problems of unstable token providing processes (refer to issue #234)

.. code:: python

    >>> from googletrans import Translator
    >>> translator = Translator(service_urls=[
          'translate.googleapis.com'
        ])


Advanced Usage (Bulk)
~~~~~~~~~~~~~~~~~~~~~

Array can be used to translate a batch of strings in a single method
call and a single HTTP session. The exact same method shown above works
for arrays as well.

.. code:: python

    >>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
    >>> for translation in translations:
    ...    print(translation.origin, ' -> ', translation.text)
    # The quick brown fox  ->  빠른 갈색 여우
    # jumps over  ->  이상 점프
    # the lazy dog  ->  게으른 개

Language detection
~~~~~~~~~~~~~~~~~~

The detect method, as its name implies, identifies the language used in
a given sentence.

.. code:: python

    >>> from googletrans import Translator
    >>> translator = Translator()
    >>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
    # <Detected lang=ko confidence=0.27041003>
    >>> translator.detect('この文章は日本語で書かれました。')
    # <Detected lang=ja confidence=0.64889508>
    >>> translator.detect('This sentence is written in English.')
    # <Detected lang=en confidence=0.22348526>
    >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
    # <Detected lang=eo confidence=0.10538048>

GoogleTrans as a command line application
-----------------------------------------

.. code:: bash

    $ translate -h
    usage: translate [-h] [-d DEST] [-s SRC] [-c] text

    Python Google Translator as a command-line tool

    positional arguments:
      text                  The text you want to translate.

    optional arguments:
      -h, --help            show this help message and exit
      -d DEST, --dest DEST  The destination language you want to translate.
                            (Default: en)
      -s SRC, --src SRC     The source language you want to translate. (Default:
                            auto)
      -c, --detect

    $ translate "veritas lux mea" -s la -d en
    [veritas] veritas lux mea
        ->
    [en] The truth is my light
    [pron.] The truth is my light

    $ translate -c "안녕하세요."
    [ko, 1] 안녕하세요.

--------------

Note on library usage
---------------------

DISCLAIMER: this is an unofficial library using the web API of translate.google.com
and also is not associated with Google.

-  **The maximum character limit on a single text is 15k.**

-  Due to limitations of the web version of google translate, this API
   does not guarantee that the library would work properly at all times
   (so please use this library if you don't care about stability).

-  **Important:** If you want to use a stable API, I highly recommend you to use
   `Google's official translate
   API <https://cloud.google.com/translate/docs>`__.

-  If you get HTTP 5xx error or errors like #6, it's probably because
   Google has banned your client IP address.

--------------

Versioning
----------

This library follows `Semantic Versioning <http://semver.org/>`__ from
v2.0.0. Any release versioned 0.x.y is subject to backwards incompatible
changes at any time.

Contributing
-------------------------

Contributions are more than welcomed. See
`CONTRIBUTING.md <CONTRIBUTING.md>`__

-----------------------------------------

License
-------

Googletrans is licensed under the MIT License. The terms are as
follows:

::

    The MIT License (MIT)

    Copyright (c) 2015 SuHun Han

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

.. |GitHub license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: http://opensource.org/licenses/MIT
.. |travis status| image:: https://travis-ci.org/ssut/py-googletrans.svg?branch=master
   :target: https://travis-ci.org/ssut/py-googletrans
.. |Documentation Status| image:: https://readthedocs.org/projects/py-googletrans/badge/?version=latest
   :target: https://readthedocs.org/projects/py-googletrans/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/googletrans.svg
   :target: http://badge.fury.io/py/googletrans
.. |Coverage Status| image:: https://coveralls.io/repos/github/ssut/py-googletrans/badge.svg
   :target: https://coveralls.io/github/ssut/py-googletrans
.. |Code Climate| image:: https://codeclimate.com/github/ssut/py-googletrans/badges/gpa.svg
   :target: https://codeclimate.com/github/ssut/py-googletrans
