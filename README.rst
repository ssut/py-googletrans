aioaiogoogletrans
=================

aiogoogletrans is a [googletrans](https://github.com/ssut/py-googletrans) fork with asyncio support.

Compatible with Python 3.6+

Features
--------

-  asyncio
-  Fast and reliable - it uses the same servers that
   translate.google.com uses
-  Auto language detection
-  Bulk translations
-  Customizable service URL

Installation
------------

To install, either use things like pip with the package "aiogoogletrans"
or download the package and put the "aiogoogletrans" directory into your
python path. Anyway, it is noteworthy that, this just requires two
modules: requests and future.

.. code:: bash

    $ pip install aiogoogletrans

Basic Usage
-----------

If source language is not given, google translate attempts to detect the
source language.

.. code:: python

    >>> from aiogoogletrans import Translator
    >>> translator = Translator()
    >>> import asyncio
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(translator.translate('안녕하세요.'))
    # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
    >>> loop.run_until_complete(translator.translate('안녕하세요.', dest='ja'))
    # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
    >>> loop.run_until_complete(translator.translate('veritas lux mea', src='la'))
    # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

Customize service URL
~~~~~~~~~~~~~~~~~~~~~

You can use another google translate domain for translation. If multiple
URLs are provided it then randomly chooses a domain.

.. code:: python

    >>> from aiogoogletrans import Translator
    >>> translator = Translator(service_urls=[
          'translate.google.com',
          'translate.google.co.kr',
        ])

Advanced Usage (Bulk)
~~~~~~~~~~~~~~~~~~~~~

Array can be used to translate a batch of strings in a single method
call and a single HTTP session. The exact same method shown above work
for arrays as well.

.. code:: python

    >>> translations = await translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
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

    >>> from aiogoogletrans import Translator
    >>> import asyncio
    >>> loop = asyncio.get_event_loop()
    >>> translator = Translator()
    >>> loop.run_until_forever(translator.detect('이 문장은 한글로 쓰여졌습니다.'))
    # <Detected lang=ko confidence=0.27041003>
    >>> loop.run_until_forever(translator.detect('この文章は日本語で書かれました。'))
    # <Detected lang=ja confidence=0.64889508>
    >>> loop.run_until_forever(translator.detect('This sentence is written in English.'))
    # <Detected lang=en confidence=0.22348526>
    >>> loop.run_until_forever(translator.detect('Tiu frazo estas skribita en Esperanto.'))
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

-  The maximum character limit on a single text is 15k.

-  Due to limitations of the web version of google translate, this API
   does not guarantee that the library would work properly at all times.
   (so please use this library if you don't care about stability.)

-  If you want to use a stable API, I highly recommend you to use
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

Submitting a Pull Request
-------------------------

Contributions to this library are always welcome and highly encouraged
:)

1. Fork this project.
2. Create a topic branch.
3. Implement your feature or bug fix.
4. Run ``pytest``.
5. Add a test for yout feature or bug fix.
6. Run step 4 again. If your changes are not 100% covered, go back to
   step 5.
7. Commit and push your changes.
8. Submit a pull request.

--------------

License
-------

Googletrans is licensed under the MIT License. The terms are as
follows:

::

    The MIT License (MIT)

    Copyright (c) 2015 Simone Esposito

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
.. |travis status| image:: https://travis-ci.org/chauffer/aiogoogletrans.svg?branch=master
   :target: https://travis-ci.org/chauffer/aiogoogletrans
.. |Documentation Status| image:: https://readthedocs.org/projects/py-aiogoogletrans/badge/?version=latest
   :target: https://readthedocs.org/projects/py-aiogoogletrans/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/aiogoogletrans.svg
   :target: http://badge.fury.io/py/aiogoogletrans
.. |Coverage Status| image:: https://coveralls.io/repos/github/chauffer/aiogoogletrans/badge.svg
   :target: https://coveralls.io/github/chaufferaiogoogletrans
.. |Code Climate| image:: https://codeclimate.com/github/chauffer/aiogoogletrans/badges/gpa.svg
   :target: https://codeclimate.com/github/chauffer/aiogoogletrans
