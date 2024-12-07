from typing import Type
import difflib
import inspect
import warnings
import sys
import re

__all__ = ['Operator', 'BaseModel', 'RegexModel']
__models__ = [
    'is_pinned', 'is_mute', 'count_unseen', 'message_id',
    'is_group', 'is_private', 'is_channel', 'is_in_contact',
    'raw_text', 'original_update', 'object_guid', 'author_guid', 'time', 'reply_message_id']

def create(name, __base, authorise: list = [], exception: bool = True, *args, **kwargs):
        result = None
        if name in authorise:
            result = name

        else:
            proposal = difflib.get_close_matches(name, authorise, n=1)
            if proposal:
                result = proposal[0]
                caller = inspect.getframeinfo(inspect.stack()[2][0])
                warnings.warn(
                    f'{caller.filename}:{caller.lineno}: do you mean'
                    f' "{name}", "{result}"? correct it')

        if result is not None or not exception:
            if result is None:
                result = name
            return type(result, __base, {'__name__': result, **kwargs})

        raise AttributeError(f'module has no attribute ({name})')


class Operator:
    Or = 'OR'
    And = 'AND'
    Less = 'Less'
    Lesse = 'Lesse'
    Equal = 'Equal'
    Greater = 'Greater'
    Greatere = 'Greatere'
    Inequality = 'Inequality'

    def __init__(self, value, operator, *args, **kwargs):
        self.value = value
        self.operator = operator

    def __eq__(self, value) -> bool:
        return self.operator == value


class BaseModel:
    def __init__(self, func=None, filters=[], *args, **kwargs) -> None:
        self.func = func
        if not isinstance(filters, list):
            filters = [filters]
        self.filters = filters

    def insert(self, filter):
        self.filters.append(filter)
        return self

    def __or__(self, value):
        return self.insert(Operator(value, Operator.Or))

    def __and__(self, value):
        return self.insert(Operator(value, Operator.And))

    def __eq__(self, value):
        return self.insert(Operator(value, Operator.Equal))

    def __ne__(self, value):
        return self.insert(Operator(value, Operator.Inequality))

    def __lt__(self, value):
        return self.insert(Operator(value, Operator.Less))

    def __le__(self, value):
        return self.insert(Operator(value, Operator.Lesse))

    def __gt__(self, value):
        return self.insert(Operator(value, Operator.Greater))

    def __ge__(self, value):
        return self.insert(Operator(value, Operator.Greatere))

    async def build(self, update):
        # get key
        result = getattr(update, self.__class__.__name__, None)
        if callable(self.func):
            if update.is_async(self.func):
                result = await self.func(result)
            else:
                result = self.func(result)

        for filter in self.filters:
            value = filter.value

            # if the comparison was with a function
            if callable(value):
                if update.is_async(value):
                    value = await value(update, result)
                else:
                    value = value(update, result)

            if self.func:
                if update.is_async(self.func):
                    value = await self.func(value)
                else:
                    value = self.func(value)

            if filter == Operator.Or:
                result = result or value

            elif filter == Operator.And:
                result = result and value

            elif filter == Operator.Less:
                result = result < value

            elif filter == Operator.Lesse:
                result = result <= value

            elif filter == Operator.Equal:
                result = result == value

            elif filter == Operator.Greater:
                result = result > value

            elif filter == Operator.Greatere:
                result = result >= value

            elif filter == Operator.Inequality:
                result = result != value

        return bool(result)

    async def __call__(self, update, *args, **kwargs):
        return await self.build(update)


class RegexModel(BaseModel):
    def __init__(self, pattern: str, *args, **kwargs) -> None:
        self.pattern = re.compile(pattern)
        super().__init__(*args, **kwargs)

    async def __call__(self, update, *args, **kwargs) -> bool:
        if update.raw_text is None:
            return False

        update.pattern_match = self.pattern.match(update.raw_text)
        return bool(update.pattern_match)


class Models:
    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        return BaseModel in value.__bases__

    def __dir__(self):
        return sorted(__models__)

    def __call__(self, name, *args, **kwargs):
        return self.__getattr__(name)

    def __getattr__(self, name):
        if name in __all__:
            return globals()[name]
        return create(name, (BaseModel,), authorize=__models__, exception=False)

    # async def text(self):
    #     print('call text')
    #     return create('text', (BaseModel,), exception=False)

    # async def text(self, *args, **kwargs):
    #     print('called.')
    #     return Operator('text', Operator.Equal)

sys.modules[__name__] = Models(__name__)

is_pinned: Type[BaseModel]
is_mute: Type[BaseModel]
count_unseen: Type[BaseModel]
message_id: Type[BaseModel]
is_group: Type[BaseModel]
is_private: Type[BaseModel]
is_channel: Type[BaseModel]
is_in_contact: Type[BaseModel]
raw_text: Type[BaseModel]
original_update: Type[BaseModel]
object_guid: Type[BaseModel]
author_guid: Type[BaseModel]
time: Type[BaseModel]
reply_message_id: Type[BaseModel]