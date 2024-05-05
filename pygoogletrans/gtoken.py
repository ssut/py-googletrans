# -*- coding: utf-8 -*-
import ast
import math
import re
import time
from typing import List

import httpx

from pygoogletrans.utils import rshift


class TokenAcquirer:
    """Google Translate API token generator

    translate.google.com uses a token to authorize the requests. If you are
    not Google, you do have this token and will have to pay for use.
    This class is the result of reverse engineering on the obfuscated and
    minified code used by Google to generate such token.

    The token is based on a seed which is updated once per hour and on the
    text that will be translated.
    Both are combined - by some strange math - in order to generate a final
    token (e.g. 744915.856682) which is used by the API to validate the
    request.

    This operation will cause an additional request to get an initial
    token from translate.google.com.

    Example usage:
        >>> from googletrans.gtoken import TokenAcquirer
        >>> acquirer = TokenAcquirer()
        >>> text = 'test'
        >>> tk = acquirer.do(text)
        >>> tk
        950629.577246
    """

    RE_TKK = re.compile(r"tkk:\'(.+?)\'", re.DOTALL)
    RE_RAWTKK = re.compile(r"tkk:\'(.+?)\'", re.DOTALL)

    def __init__(
        self, client: httpx.Client, tkk: str = "0", host: str = "translate.google.com"
    ):
        self.client = client
        self.tkk = tkk
        self.host = host if "http" in host else "https://" + host

    def _update(self):
        """update tkk"""
        # we don't need to update the base TKK value when it is still valid
        now = math.floor(int(time.time() * 1000) / 3600000.0)
        if self.tkk and int(self.tkk.split(".")[0]) == now:
            return

        r = self.client.get(self.host)

        raw_tkk = self.RE_TKK.search(r.text)
        if raw_tkk:
            self.tkk = raw_tkk.group(1)
            return

        # this will be the same as python code after stripping out a reserved word 'var'
        code_ = self.RE_TKK.search(r.text)
        if code_ is None:
            code_ = self.RE_RAWTKK.search(r.text)
            if code_ is None:
                return
        code = code_.group(1).replace("var ", "").encode().decode("unicode-escape")

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = "+"
            n, keys = 0, dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Constant):
                            keys[name] = node.value.n
                        # the value can sometimes be negative
                        elif isinstance(node.value, ast.UnaryOp) and isinstance(
                            node.value.op, ast.USub
                        ):
                            keys[name] = -node.value.operand.n
                elif isinstance(node, ast.Return):
                    # parameters should be set after this point
                    visit_return = True
                elif visit_return and isinstance(node, ast.Constant):
                    n = node.n
                elif visit_return and not isinstance(n, complex) and n > 0:
                    # the default operator is '+' but implement some more for
                    # all possible scenarios
                    if isinstance(node, ast.Add):
                        pass
                    elif isinstance(node, ast.Sub):
                        operator = "-"
                    elif isinstance(node, ast.Mult):
                        operator = "*"
                    elif isinstance(node, ast.Pow):
                        operator = "**"
                    elif isinstance(node, ast.BitXor):
                        operator = "^"
            # a safety way to avoid Exceptions
            clause = compile(f"{keys['a']}{operator}{keys['b']}")
            value = eval(clause, dict(__builtin__={}))
            result = f"{n}.{value}"

            self.tkk = result

    def _lazy(self, value: int):  # -> Callable[[], int]:
        """like lazy evaluation, this method returns a lambda function that
        returns value given.
        We won't be needing this because this seems to have been built for
        code obfuscation.

        the original code of this method is as follows:

            ... code-block: javascript

                var ek = function(a) {
                    return function() {
                        return a;
                    };
                }
        """
        return lambda: value

    def _xr(self, a: int, b: str) -> int:
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if "a" <= d else int(d)
            d = rshift(a, d) if "+" == b[c + 1] else a << d
            a = a + d & 4294967295 if "+" == b[c] else a ^ d

            c += 3
        return a

    def acquire(self, text: str) -> str:
        a: List[int] = []
        # Convert text to ints
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                # Python doesn't natively use Unicode surrogates, so account for those
                a += [
                    math.floor((val - 0x10000) / 0x400 + 0xD800),
                    math.floor((val - 0x10000) % 0x400 + 0xDC00),
                ]

        b = self.tkk if self.tkk != "0" else ""
        d = b.split(".")
        b = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e: List[int] = []
        g = 0
        size = len(a)
        while g < size:
            l = a[g]
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (
                        (l & 64512) == 55296
                        and g + 1 < size
                        and a[g + 1] & 64512 == 56320
                    ):
                        g += 1
                        l = (
                            65536 + ((l & 1023) << 10) + (a[g] & 1023)
                        )  # This bracket is important
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
            g += 1
        a_ = b
        for i, value in enumerate(e):
            a_ += value
            a_ = self._xr(a_, "+-a^+6")
        a_ = self._xr(a_, "+-3^+b+-f")
        a_ ^= int(d[1]) if len(d) > 1 else 0
        if a_ < 0:
            a_ = (a_ & 2147483647) + 2147483648
        a_ %= 1000000  # int(1E6)

        return f"{a_}.{a_ ^ b}"

    def do(self, text: str):
        self._update()
        tk = self.acquire(text)
        return tk
