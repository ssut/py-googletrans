# pyGoogletrans

> This is a fork to continue the [amazing work of Suhun Han](https://github.com/ssut/py-googletrans)

Googletrans is a **free** and **unlimited** Python library that implements Google Translate API. This uses the [Google Translate Ajax API](https://translate.google.com) to make calls to such methods as detect and translate.

Compatible with Python 3.9 and above

## Features

- [x] Fast and reliable - it uses the same servers that translate.google.com uses
- [x] Auto language detection
- [x] Bulk translations
- [x] Customizable service URL
- [x] HTTP/2 support
- [x] Poetry support
- [x] Fast JSON parsing
- [ ] Proxy support
- [ ] Internal session management (for better bulk translations)

### HTTP/2 support

This library uses `httpx` for HTTP requests so HTTP/2 is supported by default.

## Installation

To install, either use things like pip with the package \"googletrans\"
or download the package and put the \"googletrans\" directory into your
python path.

``` bash
poetry install https://github.com/Siddhesh-Agarwal/py-googletrans/
```

## Basic Usage

If the source language is not given, Google Translate attempts to detect the source language.

``` python
>>> from googletrans import Translator
>>> translator = Translator()
>>> translator.translate('안녕하세요.')
# <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
>>> translator.translate('안녕하세요.', dest='ja')
# <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
>>> translator.translate('veritas lux mea', src='la')
# <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>
```

### Customize service URL

You can use another Google Translate domain for translation. If multiple URLs are provided, it then randomly chooses a domain.

``` python
>>> from googletrans import Translator
>>> translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
```

### Advanced Usage (Bulk)

Use an array to translate a batch of strings in a single method call and HTTP session. The same method shown above works for arrays as well.

``` python
>>> translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
>>> for translation in translations:
...    print(translation.origin, ' -> ', translation.text)
# The quick brown fox  ->  빠른 갈색 여우
# jumps over  ->  이상 점프
# the lazy dog  ->  게으른 개
```

### Language detection

As its name implies, the `detect` method identifies the language used in a given sentence.

``` python
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
```

### GoogleTrans as a command line application

``` bash
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

## Note on library usage

DISCLAIMER: This is an unofficial library using the web API of translate.google.com and also is not associated with Google.

- **The maximum character limit on a single text is 15k.**
- Due to limitations of the web version of Google Translate, this API does not guarantee that the library will work properly at all times (so please use this library if you don't care about stability).
- **Important:** If you want to use a stable API, I highly recommend you to use [Google\'s official translate API](https://cloud.google.com/translate/docs).
- If you get an HTTP 5xx error or errors like #6, it\'s probably because Google has banned your client IP address.

## Versioning

This library follows [Semantic Versioning](http://semver.org/). Any release versioned `0.x.y` is subject to backwards incompatible
changes at any time.

## Contributing

I want you to know that contributions are more than welcome. See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

This project is licensed under the MIT License.
