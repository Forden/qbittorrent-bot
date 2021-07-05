import re
import typing

from aiogram.dispatcher.filters import Filter
from aiogram.types import CallbackQuery, InlineQuery, Message, Poll


class MultiRegexp(Filter):
    """
    Regexp filter for messages and callback query
    """

    def __init__(self, regexp):
        if not isinstance(regexp, typing.Pattern):
            regexp = re.compile(regexp, flags=re.IGNORECASE | re.MULTILINE)
        self.regexp = regexp

    @classmethod
    def validate(cls, full_config: typing.Dict[str, typing.Any]):
        if 'regexp' in full_config:
            return {'regexp': full_config.pop('regexp')}

    async def check(self, obj: typing.Union[Message, CallbackQuery, InlineQuery, Poll]):
        if isinstance(obj, Message):
            content = obj.text or obj.caption or ''
            if not content and obj.poll:
                content = obj.poll.question
        elif isinstance(obj, CallbackQuery) and obj.data:
            content = obj.data
        elif isinstance(obj, InlineQuery):
            content = obj.query
        elif isinstance(obj, Poll):
            content = obj.question
        else:
            return False

        matches = self.regexp.findall(content)

        if matches:
            return {'regexp': matches}
        return False
