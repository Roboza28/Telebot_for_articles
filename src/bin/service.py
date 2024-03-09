# -*- coding: utf-8 -*-
import re


def get_article_address(text_message: str) -> str:
    parce_message = re.search(r'(http|https)://([a-z0-9.-]+)', text_message)

    if parce_message:
        return parce_message.group()
    else:
        return ''
