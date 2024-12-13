# -*- coding: utf-8 -*-
import ast
import math
import re
import time
from typing import Any, Callable, Dict, List

import httpx

from googletrans.utils import rshift


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
        self,
        client: httpx.AsyncClient,
        tkk: str = "0",
        host: str = "translate.google.com",
    ) -> None:
        self.client = client
        self.tkk = tkk
        self.host = host if "http" in host else "https://" + host

    async def _update(self) -> None:
        """update tkk"""
        # we don't need to update the base TKK value when it is still valid
        now = math.floor(int(time.time() * 1000) / 3600000.0)
        if self.tkk and int(self.tkk.split(".")[0]) == now:
            return

        r = await self.client.get(self.host)

        raw_tkk = self.RE_TKK.search(r.text)
        if raw_tkk:
            self.tkk = raw_tkk.group(1)
            return

        code = self.RE_TKK.search(r.text)

        if code is not None:
            # this will be the same as python code after stripping out a reserved word 'var'
            code = code.group(1).replace("var ", "")
            # unescape special ascii characters such like a \x3d(=)
            code = code.encode().decode("unicode-escape")

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = "+"
            n: int = 0
            keys: Dict[str, int] = dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = None
                    if isinstance(node.targets[0], ast.Name):
                        name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Constant):
                            keys[name] = int(node.value.value)
                        # the value can sometimes be negative
                        elif isinstance(node.value, ast.UnaryOp) and isinstance(
                            node.value.op, ast.USub
                        ):  # pragma: nocover
                            if isinstance(node.value.operand, ast.Constant):
                                keys[name] = -int(node.value.operand.value)
                elif isinstance(node, ast.Return):
                    # parameters should be set after this point
                    visit_return = True
                elif visit_return and isinstance(node, ast.Constant):
                    n = int(node.value)
                elif visit_return and isinstance(n, int) and n > 0:
                    # the default operator is '+' but implement some more for
                    # all possible scenarios
                    if isinstance(node, ast.Add):  # pragma: nocover
                        pass
                    elif isinstance(node, ast.Sub):  # pragma: nocover
                        operator = "-"
                    elif isinstance(node, ast.Mult):  # pragma: nocover
                        operator = "*"
                    elif isinstance(node, ast.Pow):  # pragma: nocover
                        operator = "**"
                    elif isinstance(node, ast.BitXor):  # pragma: nocover
                        operator = "^"
            # a safety way to avoid Exceptions
            clause = compile(
                "{1}{0}{2}".format(operator, keys["a"], keys["b"]), "", "eval"
            )
            value = eval(clause, dict(__builtin__={}))
            result = "{}.{}".format(n, value)

            self.tkk = result

    def _lazy(self, value: Any) -> Callable[[], Any]:
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
        b_val = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e: List[int] = []
        g = 0
        size = len(a)
        while g < size:
            l = a[g]  # noqa: E741
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
                        l = (  # noqa: E741
                            65536 + ((l & 1023) << 10) + (a[g] & 1023)
                        )  # This bracket is important
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
            g += 1
        a_val = b_val
        for value in e:
            a_val += value
            a_val = self._xr(a_val, "+-a^+6")
        a_val = self._xr(a_val, "+-3^+b+-f")
        a_val ^= int(d[1]) if len(d) > 1 else 0
        if a_val < 0:  # pragma: nocover
            a_val = (a_val & 2147483647) + 2147483648
        a_val %= 1000000  # int(1E6)

        return "{}.{}".format(a_val, a_val ^ b_val)

    async def do(self, text: str) -> str:
        await self._update()
        tk = self.acquire(text)
        return tk
