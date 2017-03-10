# -*- coding: utf-8 -*-
"""
Predefined URLs used to make google translate requests.
"""
BASE = 'https://translate.google.com'
TRANSLATE = 'https://translate.google.com/translate_a/single?client=t&sl={src}&tl={dest}&hl={dest}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&tk={token}&q={query}'
DETECT = 'https://translate.google.com/translate_a/single?client=t&sl=auto&tl=en&hl=en&dt=bd&ie=UTF-8&oe=UTF-8&tk={token}&q={query}'