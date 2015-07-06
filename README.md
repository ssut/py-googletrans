# Py-GoogleTrans

[![GitHub license](https://img.shields.io/github/license/mashape/apistatus.svg)](http://opensource.org/licenses/MIT)
[![wercker status](https://app.wercker.com/status/b888422b2e335c431f9a10bd8b2768cd/s "wercker status")](https://app.wercker.com/project/bykey/b888422b2e335c431f9a10bd8b2768cd)
[![Documentation Status](https://readthedocs.org/projects/py-googletrans/badge/?version=latest)](https://readthedocs.org/projects/py-googletrans/?badge=latest)
[![PyPI version](https://badge.fury.io/py/py-googletrans.svg)](http://badge.fury.io/py/py-googletrans)
[![Coverage Status](https://coveralls.io/repos/ssut/py-googletrans/badge.svg)](https://coveralls.io/r/ssut/py-googletrans)
[![Code Climate](https://codeclimate.com/github/ssut/py-googletrans/badges/gpa.svg)](https://codeclimate.com/github/ssut/py-googletrans)
[![Dependency Status](https://gemnasium.com/ssut/py-googletrans.svg)](https://gemnasium.com/ssut/py-googletrans)

Py-GoogleTrans is a Python library that translates the text you want to translate using Google Translate.

Compatible with Python 2.7 and 3.4 (cPython and PyPy. Py 2.6 and 3.3 are not tested yet.)

For details refer to the [API Documentation](https://py-googletrans.readthedocs.org/en/latest/googletrans.html).

---

## Installation

To install, either use things like pip with the package "py-googletrans" or download the package and put the "googletrans" directory into your python path.

```bash
$ pip install py-googletrans
```

### Requirements

- requests
- future

---

## Basic Usage

```python
>>> from googletrans import translator
>>> translator.translate('안녕하세요.')
# <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
>>> translator.translate('안녕하세요.', dest='ja')
# <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
>>> translator.translate('veritas lux mea', src='la')
# <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>
```

### Advanced Usage (Batch)

```python
>>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
>>> for translation in translations:
...    print(translation.origin, ' -> ', translation.text)
# The quick brown fox  ->  빠른 갈색 여우
# jumps over  ->  이상 점프
# the lazy dog  ->  게으른 개
```

### Language detection

```python
>>> from googletrans import translator
>>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
# <Detected lang=ko confidence=0.27041003>
>>> translator.detect('この文章は日本語で書かれました。')
# <Detected lang=ja confidence=0.64889508>
>>> translator.detect('This sentence is written in English.')
# <Detected lang=en confidence=0.22348526>
>>> translator.detect('Tiu frazo estas skribita en Esperanto.')
# <Detected lang=eo confidence=0.10538048>
```

---

## GoogleTrans as a command line application

```bash
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
```


---

## A note on library usage

Due to limitations of Google Translate, this API does not guarantee that the library would work properly. (please use this library if you don't care about stability.)

If you want to a stable, I recommend you to use [Google's official translate API](https://cloud.google.com/translate/docs).

---

## Submitting a Pull Request

1. Fork this project.
2. Create a topic branch.
3. Implement your feature or bug fix.
4. Run `python tests.py` or `python -m unittest -v`.
5. Add a test for yout feature or bug fix.
6. Run step 4 again. If your changes are not 100% covered, go back to step 5.
7. Commit and push your changes.
8. Submit a pull request.

---

## License

Py-GoogleTrans is licensed under the MIT License. The terms are as follows:

```
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
```