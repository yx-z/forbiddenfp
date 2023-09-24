"""
forbiddenfp - Some builtin/itertools functions that can be chained after objects, in favor of more functional programming.

https://github.com/yx-z/forbiddenfp
"""
import collections
import functools
import itertools
import operator
from numbers import Number
from typing import Callable, List, NoReturn, Optional, Dict, TypeVar, Iterable, Sequence, Tuple, Union, Set, Type, \
    ContextManager, Any

from forbiddenfruit import curse
from typing_extensions import ParamSpec

_P = ParamSpec("_P")
_R = TypeVar("_R")
_F = Callable[[_P], _R]
_Pred = Callable[[_P], bool]
_P2 = ParamSpec("_P2")
_R2 = TypeVar("_R2")
_F2 = Callable[[_P2], _R2]
_ExceptionType = Type[Exception]
_ExceptionOrExceptionFunc = Union[_ExceptionType, Callable[[_P], _ExceptionType]]


def chain_as(name: str, cls: Type = object) -> Callable[[_F], _F]:
    def decorator(func: _F) -> _F:
        curse(cls, name, func)
        return func

    return decorator


def chain_for(cls: Type) -> Callable[[_F], _F]:
    def decorator(func: _F) -> _F:
        return chain_as(func.__name__, cls)(func)

    return decorator


def chainable(func: _F) -> _F:
    return chain_as(func.__name__)(func)


def make_func(func: _F) -> Callable[[_P2, _P], _R]:
    return functools.wraps(func)(lambda *args, **kwargs: lambda self: func(self, *args, **kwargs))


def chain_and_make_func(func: _F) -> Callable[[_P2, _P], _R]:
    return make_func(chainable(func))


def use(val: _P) -> Callable[..., _P]:
    return lambda *args, **kwargs: val


@chain_and_make_func
def greater_than(self: _P, val: _P2) -> bool:
    return self > val


@chain_and_make_func
def less_than(self: _P, val: _P2) -> bool:
    return self < val


@chain_and_make_func
def greater_than_or_equals(self: _P, val: _P2) -> bool:
    return self >= val


@chain_and_make_func
def less_than_or_equals(self: _P, val: _P) -> bool:
    return self <= val


def identity(val: _P) -> _P:
    return val


@chainable
def negate_val(val: _P) -> _R:
    return not val


@chainable
def negate(func: _Pred) -> _Pred:
    return lambda *args, **kwargs: not func(*args, **kwargs)


@chain_and_make_func
def equals(self: _P, val: _P2) -> bool:
    return self == val


@chain_and_make_func
def not_equals(self: _P, val: _P2) -> bool:
    return self != val


@chain_and_make_func
def contains(self: _P, val: _P2) -> bool:
    return val in self


@chain_and_make_func
def not_contains(self: _P, val: _P2) -> bool:
    return val not in self


truthful = chain_as("truthful")(bool)
falseful = chain_as("falseful")(negate(bool))
default = use(True)


@chain_and_make_func
def in_iter(self: _P, it: Iterable[_P]) -> bool:
    return self in it


@chain_and_make_func
def not_in(self: _P, it: Iterable[_P]) -> bool:
    return self not in it


@chain_and_make_func
def asserting(self: _P, pred: _Pred) -> _P:
    assert pred(self)
    return self


@chainable
def is_none(val: _P) -> bool:
    return val is None


@chainable
def is_not_none(val: _P) -> bool:
    return val is not None


@chain_and_make_func
def add(self: _P, val: _P2) -> _R:
    return self + val


@chain_and_make_func
def subtract(self: _P, val: _P2) -> _R:
    return self - val


@chain_and_make_func
def multiply(self: _P, val: _P2) -> _R:
    return self * val


@chain_and_make_func
def divide(self: _P, val: _P2) -> _R:
    return self / val


@chain_and_make_func
def true_div(self: _P, val: _P2) -> _R:
    return self // val


@chain_and_make_func
def and_val(self: _P, other: _P2) -> _R:
    return self and other


@chain_and_make_func
def and_func(self: _Pred, other: _Pred) -> _Pred:
    return lambda *args, **kwargs: self(*args, **kwargs) and other(*args, **kwargs)


@chain_and_make_func
def or_val(self: _P, other: _P2) -> _R:
    return self or other


@chain_and_make_func
def or_func(self: _Pred, other: _Pred) -> _Pred:
    return lambda *args, **kwargs: self(*args, **kwargs) or other(*args, **kwargs)


@chain_and_make_func
def map_val(self: _P, vals: Optional[Dict[_P, _R]] = None, default: Optional[_R] = None, **kwargs: _R) -> Optional[_R]:
    return {**(vals or {}), **kwargs}.get(self, default)


@chain_and_make_func
def map_pred(self: _P, pred_to_val: Dict[_Pred, _R], default: Optional[_R] = None) -> Optional[_R]:
    for pred, val in pred_to_val.items():
        if pred(self):
            return val
    return default


@chain_and_make_func
def match_val(self: _P,
              val_to_action: Optional[Dict[_P, _F]] = None,
              default: Callable[[_P], Optional[_R]] = use(None), **kwargs: _F) -> Optional[_R]:
    return {**(val_to_action or {}), **kwargs}.get(self, default)(self)


@chain_and_make_func
def match_pred(self: _P, pred_to_action: Dict[_Pred, _R], default: _F = use(None)) -> Optional[_R]:
    for pred, action in pred_to_action.items():
        if pred(self):
            return action(self)
    return default(self)


@make_func
@chain_as("isinstance")
def isinstance_val(self: _P, t: Type) -> bool:
    return isinstance(self, t)


@chainable
def call(self: _F, *args: _P.args, **kwargs: _P.kwargs) -> _R:
    return self(*args, **kwargs)


def _compose2(f: Callable[[_R], _R2], g: _F) -> Callable[[_P], _R2]:
    return lambda *args, **kwargs: f(g(*args, **kwargs))


@chainable
def compose(*funcs: Sequence[Callable[[_P], _R]]) -> _F2:
    return functools.reduce(_compose2, funcs)


@chainable
def compose_r(*funcs: Sequence[Callable[[_P], _R]]) -> _F2:
    return compose(*reversed(funcs))


@chainable
def flatten(self: Iterable, recurse: bool = False) -> Iterable:
    for x in self:
        if isinstance(x, Iterable):
            yield from flatten(x, recurse) if recurse else x
        else:
            yield x


@chainable
def partial(self: _F, *args: _P.args, **kwargs: _P.kwargs) -> _F:
    return functools.partial(self, *args, **kwargs)


@chain_and_make_func
def apply(self: _P, func: _F) -> _P:
    func(self)
    return self


@make_func
@chain_as("print")
def apply_print(self: _P, print_func: _F = print) -> _P:
    print_func(self)
    return self


@chainable
def print_list(self: Iterable[_P], print_func: _F = print) -> List[_P]:
    ls = list(self)
    print_func(ls)
    return ls


@chain_and_make_func
def pair(self: _P, val: _P2) -> Tuple[_P, _P2]:
    return self, val


@chain_and_make_func
def pair_func(self: _P, func: _F) -> Tuple[_P, _R]:
    return self, func(self)


@chain_and_make_func
def pairwise(self: Iterable[_P]) -> Iterable[Tuple[_P, _P]]:
    return itertools.pairwise(self)


@chain_and_make_func
def groupwise(self: Iterable[_P], n: int) -> Iterable[Tuple[_P, ...]]:
    acc = collections.deque((), n)
    for element in self:
        acc.append(element)
        if len(acc) == n:
            yield tuple(acc)


@chain_and_make_func
def split_at(self: Iterable[_P], pred: _Pred) -> Iterable[Tuple[_P, ...]]:
    it = iter(self)
    curr_slice = []
    for item in it:
        curr_slice.append(item)
        if pred(item):
            yield tuple(curr_slice)
            curr_slice = []
    if len(curr_slice) > 0:
        yield tuple(curr_slice)


@chain_and_make_func
def batch(self: Iterable[_P], n: int) -> Iterable[Tuple[_P, ...]]:
    it = iter(self)
    while batch := tuple(islice(it, n)):
        yield batch


@chain_and_make_func
def i_th(self: Iterable[_P], i: int) -> _P:
    try:
        return self[i]
    except:
        return next(itertools.islice(self, i))


@chainable
def also(self: _P, _: _R) -> _P:
    # side effect is evaluated before passing in to this function
    return self


@chain_as("dir")
def dir_obj(self: _P) -> List[str]:
    return dir(self)


@chain_as("vars")
def vars_obj(self: _P) -> Dict[str, Any]:
    return vars(self)


@chain_and_make_func
def then(self: _P, func: _F) -> _R:
    return func(self)


@chainable
def then_use(self: _P, val: _R) -> _R:
    return val


@make_func
@chain_as("getattr")
def get_attr(self: _P, name: str, default: Optional[_P] = None) -> Optional[_P]:
    return getattr(self, name, default)


@make_func
@chain_as("getitem")
def get_item(self: _P, key: _P2) -> _R:
    return self[key]


@make_func
@chain_as("setattr")
def set_attr(self: _P, **kwargs: _P.kwargs) -> _P:
    for k, v in kwargs.items():
        setattr(self, k, v)
    return self


@make_func
@chain_as("setitem")
def set_item(self: _P, key: _P2, val: _R) -> _P:
    self[key] = val
    return self


@chain_and_make_func
def apply_unpack(self: _P, func: _F) -> _R:
    func(*self)
    return self


@chain_and_make_func
def then_unpack(self: _P, func: _F) -> _R:
    return func(*self)


@chainable
def empty(self: Iterable[_P]) -> bool:
    try:
        return len(self) == 0
    except:
        return all(False for _ in self)


@chain_and_make_func
def tee(self: Iterable[_P], n: int = 2) -> Tuple[_P, ...]:
    return itertools.tee(self, n)


@make_func
@chain_as("min")
def min_iter(self: Iterable[_P], default: Optional[_P] = None, key: _F = identity) -> Optional[_P]:
    return min(self, default=default, key=key)


@make_func
@chain_as("max")
def max_iter(self: Iterable[_P], default: Optional[_P] = None, key: _F = identity) -> Optional[_P]:
    return max(self, default=default, key=key)


@chain_as("range")
def range_up_to(self: int, start: Optional[int] = None, step: Optional[int] = None) -> Iterable[int]:
    if start is None and step is None:
        return range(self)
    if step is None:
        return range(start, self)
    return range(start, self, step)


@make_func
@chain_as("all")
def all_iter(self: Iterable[_P], predicate: _Pred = truthful) -> bool:
    return all(predicate(x) for x in self)


@make_func
@chain_as("any")
def any_iter(self: Iterable[_P], predicate: _Pred = truthful) -> bool:
    return any(predicate(x) for x in self)


@make_func
@chain_as("map")
def map_iter(self: Iterable[_P], func: _F, *other: Iterable[_P2]) -> Iterable[_R]:
    return map(func, self, *other)


@chain_and_make_func
def map_dict(self: Dict[_P, _P2],
             key_func: _F = identity,
             val_func: _F2 = identity) -> Iterable[Tuple[_R, _R2]]:
    return map(lambda t: (key_func(t[0]), val_func(t[1])), self.items())


@make_func
@chain_as("filter")
def filter_iter(self: Iterable[_P], predicate: _Pred = truthful) -> Iterable[_P]:
    return filter(predicate, self)


@chain_and_make_func
def filter_unpacked(self: Iterable[Iterable[_P]],
                    predicate: Callable[[_P.args], bool] = truthful) -> Iterable[Iterable[_P]]:
    return filter(lambda t: predicate(*t), self)


@chain_and_make_func
def filter_key(self: Dict[_P, _P2], predicate: Callable[[_P], bool]) -> Iterable[Tuple[_P, _P2]]:
    return filter(lambda t: predicate(t[0]), self.items())


@chain_and_make_func
def filter_val(self: Dict[_P, _P2], predicate: Callable[[_P2], bool]) -> Iterable[Tuple[_P, _P2]]:
    return filter(lambda t: predicate(t[1]), self.items())


@chainable
def last(self: Sequence[_P], predicate: _Pred = use(True)) -> Optional[_P]:
    return next(filter(predicate, reversed(self)), None)


@chain_as("next")
def next_iter(self: Iterable[_P], predicate: _Pred = use(True)) -> Optional[_P]:
    return next(filter(predicate, self), None)


@make_func
@chain_as("sum")
def sum_iter(self: Iterable[_P], of: Callable[[_P], Number] = identity, predicate: _Pred = use(True)) -> int:
    return sum(map(of, filter(predicate, self)))


@make_func
@chain_as("len")
def len_iter(self: Iterable[_P], predicate: _Pred = use(True)) -> int:
    return sum(map(lambda _: 1, filter(predicate, self)))


@chain_as("reversed")
def reversed_iter(self: Sequence[_P]) -> Sequence[_P]:
    return reversed(self)


@make_func
@chain_as("sorted")
def sorted_iter(self: Iterable[_P], key: _F = identity, reverse: bool = False) -> List[_P]:
    return sorted(self, key=key, reverse=reverse)


_initial = object()


@chain_and_make_func
def reduce(self: Iterable[_P], func: Callable[[_P, _P], _R], initial: _P2 = _initial) -> _R:
    return functools.reduce(func, self) if initial is _initial else functools.reduce(func, self, initial)


@chain_and_make_func
def reduce_r(self: Sequence[_P], func: Callable[[_P, _P], _R], initial: _P2 = _initial) -> _R:
    rev = reversed(self)
    return functools.reduce(func, rev) if initial is _initial else functools.reduce(func, rev, initial)


@chain_and_make_func
def partition(self: Iterable[_P], predicate: _Pred = truthful) -> Tuple[Iterable[_P], Iterable[_P]]:
    return (x for x in self if predicate(x)), (x for x in self if not predicate(x))


@chainable
def counter(self: Iterable[_P]) -> Dict[_P, int]:
    return collections.Counter(self)


@chain_and_make_func
def groupby(self: Iterable[_P], key: _F) -> Iterable[Tuple[_R, Iterable[_P]]]:
    return itertools.groupby(self, key=key)


@chainable
def chain(*self: Iterable[Iterable[_P]]) -> Iterable[_P]:
    return itertools.chain(*self)


@make_func
@chain_as("zip")
def zip_iter(*self: Iterable[_P]) -> Iterable[Tuple[_P, ...]]:
    return zip(*self)


@chain_as("enumerate")
def enumerate_iter(self: Iterable[_P]) -> Iterable[Tuple[int, _P]]:
    return enumerate(self)


@chain_as("tuple")
def tuple_iter(self: Iterable[_P]) -> Tuple[_P, ...]:
    return tuple(self)


@chain_as("list")
def list_iter(self: Iterable[_P]) -> List[_P]:
    return list(self)


@chain_as("set")
def set_iter(self: Iterable[_P]) -> Set[_P]:
    return set(self)


@chain_as("dict")
def dict_iter(self: Iterable[Tuple[_P, _P2]]) -> Dict[_P, _P2]:
    return dict(self)


@chain_and_make_func
def join(self: Iterable[_P], sep: str = "", to_str: Callable[[_P], str] = str) -> str:
    return sep.join(map(to_str, self))


@chain_and_make_func
def starmap(self: Iterable[Iterable[_P]], func: Callable[[_P.args], _R]) -> Iterable[_R]:
    return itertools.starmap(func, self)


@chain_and_make_func
def each_also(self: Sequence[Sequence[_P]], func: Callable[[Iterable[_P]], _R]) -> Sequence[Sequence[_P]]:
    for x in self:
        func(x)
    return self


@chain_and_make_func
def each_also_unpacked(self: Sequence[Sequence[_P]], func: Callable[[_P.args], _R]) -> Sequence[Sequence[_P]]:
    for x in self:
        func(*x)
    return self


@chain_and_make_func
def each(self: Iterable[Iterable[_P]], func: Callable[[Iterable[_P]], _R]) -> None:
    for x in self:
        func(x)


@chain_and_make_func
def each_unpacked(self: Iterable[Iterable[_P]], func: Callable[[_P.args], _R]) -> None:
    for x in self:
        func(*x)


@chain_and_make_func
def accumulate(self: Iterable[Iterable[_P]],
               func: Callable[[_R, _P], _R] = operator.add,
               initial: _P2 = _initial) -> Iterable[_R]:
    return itertools.accumulate(self, func) if initial is _initial else itertools.accumulate(self, func, initial)


@chainable
def pairwise(self: Iterable[_P]) -> Iterable[Tuple[_P, _P]]:
    return itertools.pairwise(self)


@chain_and_make_func
def product(self: Iterable[_P], repeat: int = 1) -> Iterable[Tuple[_P, ...]]:
    return itertools.product(*self, repeat=repeat)


@chain_and_make_func
def repeat(self: _P, times: int) -> Iterable[_P]:
    return itertools.repeat(self, times)


@chainable
def infinite(self: _P) -> Iterable[_P]:
    return itertools.repeat(self)


@chainable
def cycle(self: _P) -> Iterable[_P]:
    return itertools.cycle(self)


@chain_and_make_func
def takewhile(self: Iterable[_P], predicate: _Pred = truthful) -> Iterable[_P]:
    return itertools.takewhile(predicate, self)


@chain_and_make_func
def islice_up_to(self: Iterable[_P], stop: int, predicate: _Pred = use(True)) -> Iterable[_P]:
    return itertools.islice(filter(predicate, self), stop)


@chain_and_make_func
def islice(
        self: Iterable[_P], start: int, stop: Optional[int], step: int = 1, predicate: _Pred = use(True)
) -> Iterable[_P]:
    return itertools.islice(filter(predicate, self), start, stop, step)


@chain_and_make_func
def dropwhile(self: Iterable[_P], predicate: _Pred = truthful) -> Iterable[_P]:
    return itertools.dropwhile(predicate, self)


@chain_as("float")
def float_obj(self: _P) -> float:
    return float(self)


@chain_as("int")
def int_obj(self: _P) -> int:
    return int(self)


@chain_and_make_func
def startswith(self: str, prefix: str) -> bool:
    return self.startswith(prefix)


@chain_and_make_func
def endswith(self: str, suffix: str) -> bool:
    return self.endswith(suffix)


@chain_and_make_func
def replace(self: str, from_str: str, to_str: str) -> str:
    return self.replace(from_str, to_str)


@chain_and_make_func
def split(self: str, sep: str) -> List[str]:
    return self.split(sep)


@chain_as("str")
def str_obj(self: _P) -> str:
    return str(self)


@chain_as("repr")
def repr_obj(self: _P) -> str:
    return repr(self)


@make_func
@chain_as("format")
def format_obj(self: _P, format_str: str) -> str:
    return format(self, format_str)


@chain_and_make_func
def if_branches(self: _P, true_func: _F, false_func: _F, predicate: _Pred = truthful) -> _R:
    return true_func(self) if predicate(self) else false_func(self)


@chain_and_make_func
def if_true(self: _P, func: _F, predicate: _Pred = truthful) -> Optional[_R]:
    return func(self) if predicate(self) else None


@chain_and_make_func
def apply_if_branches(self: _P, true_func: _F, false_func: _F, predicate: _Pred = truthful) -> _P:
    if predicate(self):
        true_func(self)
    else:
        false_func(self)
    return self


@chain_and_make_func
def apply_if_true(self: _P, func: _F, predicate: _Pred = truthful) -> _P:
    if predicate(self):
        func(self)
    return self


@chain_and_make_func
def or_else(self: _P, val: _R, predicate: _Pred = truthful) -> _R:
    return self if predicate(self) else val


@chain_and_make_func
def or_eval(self: _P, func: _F, predicate: _Pred = truthful) -> _R:
    return self if predicate(self) else func(self)


@chain_and_make_func
def or_raise(self: _P, val_or_func: _ExceptionOrExceptionFunc, predicate: _Pred = truthful) -> _P:
    if predicate(self):
        return self
    if callable(val_or_func):
        raise val_or_func(self)
    raise val_or_func


@chain_and_make_func
def raise_as(self: _P, val_or_func: _ExceptionOrExceptionFunc) -> NoReturn:
    if callable(val_or_func):
        raise val_or_func(self)
    raise val_or_func


@chain_and_make_func
def then_suppressed(
        self: _P, func: _F, exception_type: _ExceptionType = Exception, on_except: Optional[_R] = None
) -> Optional[_R]:
    try:
        return func(self)
    except exception_type:
        return on_except


@chain_and_make_func
def apply_suppressed(self: _P, func: _F, exception_type: _ExceptionType = Exception) -> _P:
    try:
        func(self)
    except exception_type:
        pass
    finally:
        return self


@chain_and_make_func
def then_catch(self: _P, func: _F, exception_type: _ExceptionType = Exception,
               exception_handler: Callable[[_P, _ExceptionType], _R2] = use(None)) -> Union[_R, _R2]:
    try:
        return func(self)
    except exception_type as e:
        return exception_handler(self, e)


@chain_and_make_func
def apply_catch(self: _P, func: _F, exception_type: _ExceptionType = Exception,
                exception_handler: Optional[Callable[[_P, _ExceptionType], _R2]] = None) -> _P:
    try:
        func(self)
    except exception_type as e:
        if exception_handler is not None:
            exception_handler(self, e)
    finally:
        return self


@chain_and_make_func
def apply_while(self: _P, func: Callable[[_P], _P], predicate: _Pred = truthful) -> _P:
    while predicate(self):
        self = func(self)
    return self


@chain_and_make_func
def yield_while(self: _P, func: Callable[[_P], _P], predicate: _Pred = truthful) -> Iterable[_P]:
    while predicate(self):
        yield self
        self = func(self)


@chain_and_make_func
def with_context(self: _P, context_func: Callable[[_P], ContextManager],
                 then: Union[Callable[[_P, _R], _R2], Callable[[_P], _R2]]) -> _R2:
    with context_func(self) as r:
        if r is None:
            return then(self)
        return then(self, r)


@chain_and_make_func
def with_open(self: _P,
              then: Callable[[_P, _R], _R2],
              open_func: Callable[[_P], _R] = open,
              mode: str = "r",
              *args: _P.args,
              **kwargs: _P.kwargs) -> _R2:
    with open_func(self, mode, *args, **kwargs) as f:
        return then(self, f)


def take_unpacked(
        func_on_iterable_of_iterable: Callable[[Callable[[Iterable[_P]], _R], Iterable[Iterable[_P]]], _R2]
) -> Callable[[Callable[[_P.args], _R], Iterable[Iterable[_P]]], _R2]:
    """
    e.g.
    filter(lambda tup: tup[0] > tup[1], [(1, 2), (3, 2)]
    can be transformed so that it takes a predicate with two arguments (for clarity):
    take_unpacked(filter)(lambda x, y: x > y, [(1, 2), (3, 2)])
    """

    @functools.wraps(func_on_iterable_of_iterable)
    def decorated(func: Callable[[_P.args], _R], iterable_of_iterable: Iterable[Iterable[_P]]) -> _R2:
        return func_on_iterable_of_iterable(lambda args: func(*args), iterable_of_iterable)

    return decorated


chain_as("take_unpacked")(lambda self, func: lambda f: take_unpacked(func)(f, self))
