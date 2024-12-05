#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re


def _replace_multiple(value, needles_and_replacements):
    def replacer(match):
        return needles_and_replacements[match.group(0)]

    pattern = re.compile(
        r"|".join([re.escape(needle) for needle in needles_and_replacements.keys()])
    )
    if isinstance(value, (bytes, str)):
        result = pattern.sub(replacer, value)
    else:
        result = pattern.sub(replacer, str(value))

    return result
