# -*- coding: utf-8 -*-
"""
Predefined URLs used to make google translate requests.
"""
TRANSLATOR = 'https://translate.google.com/'
TRANSLATE = 'https://translate.google.com/translate_a/single?client=t&sl={src}&tl={dest}&hl={dest}&dt=bd&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&q={query}'
DETECT = 'https://translate.google.com/translate_a/single?client=t&sl=auto&tl=en&hl=en&dt=bd&ie=UTF-8&oe=UTF-8&q={query}'