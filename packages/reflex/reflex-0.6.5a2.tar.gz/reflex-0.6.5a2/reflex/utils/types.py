"""Contains custom types and methods to check types."""

from __future__ import annotations

import contextlib
import dataclasses
import inspect
import sys
import types
from functools import cached_property, lru_cache, wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    _GenericAlias,  # type: ignore
    get_args,
    get_type_hints,
)
from typing import get_origin as get_origin_og

import sqlalchemy

import reflex
from reflex.components.core.breakpoints import Breakpoints

try:
    from pydantic.v1.fields import ModelField
except ModuleNotFoundError:
    from pydantic.fields import ModelField  # type: ignore

from sqlalchemy.ext.associationproxy import AssociationProxyInstance
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, QueryableAttribute, Relationship

from reflex import constants
from reflex.base import Base
from reflex.utils import console

if sys.version_info >= (3, 12):
    from typing import override as override
else:

    def override(func: Callable) -> Callable:
        """Fallback for @override decorator.

        Args:
            func: The function to decorate.

        Returns:
            The unmodified function.
        """
        return func


# Potential GenericAlias types for isinstance checks.
GenericAliasTypes = [_GenericAlias]

with contextlib.suppress(ImportError):
    # For newer versions of Python.
    from types import GenericAlias  # type: ignore

    GenericAliasTypes.append(GenericAlias)

with contextlib.suppress(ImportError):
    # For older versions of Python.
    from typing import _SpecialGenericAlias  # type: ignore

    GenericAliasTypes.append(_SpecialGenericAlias)

GenericAliasTypes = tuple(GenericAliasTypes)

# Potential Union types for isinstance checks (UnionType added in py3.10).
UnionTypes = (Union, types.UnionType) if hasattr(types, "UnionType") else (Union,)

# Union of generic types.
GenericType = Union[Type, _GenericAlias]

# Valid state var types.
JSONType = {str, int, float, bool}
PrimitiveType = Union[int, float, bool, str, list, dict, set, tuple]
StateVar = Union[PrimitiveType, Base, None]
StateIterVar = Union[list, set, tuple]

if TYPE_CHECKING:
    from reflex.vars.base import Var

    # ArgsSpec = Callable[[Var], list[Var]]
    ArgsSpec = (
        Callable[[], Sequence[Var]]
        | Callable[[Var], Sequence[Var]]
        | Callable[[Var, Var], Sequence[Var]]
        | Callable[[Var, Var, Var], Sequence[Var]]
        | Callable[[Var, Var, Var, Var], Sequence[Var]]
        | Callable[[Var, Var, Var, Var, Var], Sequence[Var]]
        | Callable[[Var, Var, Var, Var, Var, Var], Sequence[Var]]
        | Callable[[Var, Var, Var, Var, Var, Var, Var], Sequence[Var]]
    )
else:
    ArgsSpec = Callable[..., List[Any]]


PrimitiveToAnnotation = {
    list: List,
    tuple: Tuple,
    dict: Dict,
}

RESERVED_BACKEND_VAR_NAMES = {
    "_abc_impl",
    "_backend_vars",
    "_was_touched",
}

if sys.version_info >= (3, 11):
    from typing import Self as Self
else:
    from typing_extensions import Self as Self


class Unset:
    """A class to represent an unset value.

    This is used to differentiate between a value that is not set and a value that is set to None.
    """

    def __repr__(self) -> str:
        """Return the string representation of the class.

        Returns:
            The string representation of the class.
        """
        return "Unset"

    def __bool__(self) -> bool:
        """Return False when the class is used in a boolean context.

        Returns:
            False
        """
        return False


@lru_cache()
def get_origin(tp):
    """Get the origin of a class.

    Args:
        tp: The class to get the origin of.

    Returns:
        The origin of the class.
    """
    return get_origin_og(tp)


@lru_cache()
def is_generic_alias(cls: GenericType) -> bool:
    """Check whether the class is a generic alias.

    Args:
        cls: The class to check.

    Returns:
        Whether the class is a generic alias.
    """
    return isinstance(cls, GenericAliasTypes)


def unionize(*args: GenericType) -> Type:
    """Unionize the types.

    Args:
        args: The types to unionize.

    Returns:
        The unionized types.
    """
    if not args:
        return Any
    if len(args) == 1:
        return args[0]
    # We are bisecting the args list here to avoid hitting the recursion limit
    # In Python versions >= 3.11, we can simply do `return Union[*args]`
    midpoint = len(args) // 2
    first_half, second_half = args[:midpoint], args[midpoint:]
    return Union[unionize(*first_half), unionize(*second_half)]


def is_none(cls: GenericType) -> bool:
    """Check if a class is None.

    Args:
        cls: The class to check.

    Returns:
        Whether the class is None.
    """
    return cls is type(None) or cls is None


@lru_cache()
def is_union(cls: GenericType) -> bool:
    """Check if a class is a Union.

    Args:
        cls: The class to check.

    Returns:
        Whether the class is a Union.
    """
    return get_origin(cls) in UnionTypes


@lru_cache()
def is_literal(cls: GenericType) -> bool:
    """Check if a class is a Literal.

    Args:
        cls: The class to check.

    Returns:
        Whether the class is a literal.
    """
    return get_origin(cls) is Literal


def has_args(cls) -> bool:
    """Check if the class has generic parameters.

    Args:
        cls: The class to check.

    Returns:
        Whether the class has generic
    """
    if get_args(cls):
        return True

    # Check if the class inherits from a generic class (using __orig_bases__)
    if hasattr(cls, "__orig_bases__"):
        for base in cls.__orig_bases__:
            if get_args(base):
                return True

    return False


def is_optional(cls: GenericType) -> bool:
    """Check if a class is an Optional.

    Args:
        cls: The class to check.

    Returns:
        Whether the class is an Optional.
    """
    return is_union(cls) and type(None) in get_args(cls)


def value_inside_optional(cls: GenericType) -> GenericType:
    """Get the value inside an Optional type or the original type.

    Args:
        cls: The class to check.

    Returns:
        The value inside the Optional type or the original type.
    """
    if is_union(cls) and len(args := get_args(cls)) >= 2 and type(None) in args:
        return unionize(*[arg for arg in args if arg is not type(None)])
    return cls


def get_property_hint(attr: Any | None) -> GenericType | None:
    """Check if an attribute is a property and return its type hint.

    Args:
        attr: The descriptor to check.

    Returns:
        The type hint of the property, if it is a property, else None.
    """
    if not isinstance(attr, (property, hybrid_property)):
        return None
    hints = get_type_hints(attr.fget)
    return hints.get("return", None)


def get_attribute_access_type(cls: GenericType, name: str) -> GenericType | None:
    """Check if an attribute can be accessed on the cls and return its type.

    Supports pydantic models, unions, and annotated attributes on rx.Model.

    Args:
        cls: The class to check.
        name: The name of the attribute to check.

    Returns:
        The type of the attribute, if accessible, or None
    """
    from reflex.model import Model

    try:
        attr = getattr(cls, name, None)
    except NotImplementedError:
        attr = None

    if hint := get_property_hint(attr):
        return hint

    if (
        hasattr(cls, "__fields__")
        and name in cls.__fields__
        and hasattr(cls.__fields__[name], "outer_type_")
    ):
        # pydantic models
        field = cls.__fields__[name]
        type_ = field.outer_type_
        if isinstance(type_, ModelField):
            type_ = type_.type_
        if not field.required and field.default is None:
            # Ensure frontend uses null coalescing when accessing.
            type_ = Optional[type_]
        return type_
    elif isinstance(cls, type) and issubclass(cls, DeclarativeBase):
        insp = sqlalchemy.inspect(cls)
        if name in insp.columns:
            # check for list types
            column = insp.columns[name]
            column_type = column.type
            try:
                type_ = insp.columns[name].type.python_type
            except NotImplementedError:
                type_ = None
            if type_ is not None:
                if hasattr(column_type, "item_type"):
                    try:
                        item_type = column_type.item_type.python_type  # type: ignore
                    except NotImplementedError:
                        item_type = None
                    if item_type is not None:
                        if type_ in PrimitiveToAnnotation:
                            type_ = PrimitiveToAnnotation[type_]  # type: ignore
                        type_ = type_[item_type]  # type: ignore
                if column.nullable:
                    type_ = Optional[type_]
                return type_
        if name in insp.all_orm_descriptors:
            descriptor = insp.all_orm_descriptors[name]
            if hint := get_property_hint(descriptor):
                return hint
            if isinstance(descriptor, QueryableAttribute):
                prop = descriptor.property
                if isinstance(prop, Relationship):
                    type_ = prop.mapper.class_
                    # TODO: check for nullable?
                    type_ = List[type_] if prop.uselist else Optional[type_]
                    return type_
            if isinstance(attr, AssociationProxyInstance):
                return List[
                    get_attribute_access_type(
                        attr.target_class,
                        attr.remote_attr.key,  # type: ignore[attr-defined]
                    )
                ]
    elif isinstance(cls, type) and not is_generic_alias(cls) and issubclass(cls, Model):
        # Check in the annotations directly (for sqlmodel.Relationship)
        hints = get_type_hints(cls)
        if name in hints:
            type_ = hints[name]
            type_origin = get_origin(type_)
            if isinstance(type_origin, type) and issubclass(type_origin, Mapped):
                return get_args(type_)[0]  # SQLAlchemy v2
            if isinstance(type_, ModelField):
                return type_.type_  # SQLAlchemy v1.4
            return type_
    elif is_union(cls):
        # Check in each arg of the annotation.
        return unionize(
            *(get_attribute_access_type(arg, name) for arg in get_args(cls))
        )
    elif isinstance(cls, type):
        # Bare class
        if sys.version_info >= (3, 10):
            exceptions = NameError
        else:
            exceptions = (NameError, TypeError)
        try:
            hints = get_type_hints(cls)
            if name in hints:
                return hints[name]
        except exceptions as e:
            console.warn(f"Failed to resolve ForwardRefs for {cls}.{name} due to {e}")
            pass
    return None  # Attribute is not accessible.


@lru_cache()
def get_base_class(cls: GenericType) -> Type:
    """Get the base class of a class.

    Args:
        cls: The class.

    Returns:
        The base class of the class.

    Raises:
        TypeError: If a literal has multiple types.
    """
    if is_literal(cls):
        # only literals of the same type are supported.
        arg_type = type(get_args(cls)[0])
        if not all(type(arg) is arg_type for arg in get_args(cls)):
            raise TypeError("only literals of the same type are supported")
        return type(get_args(cls)[0])

    if is_union(cls):
        return tuple(get_base_class(arg) for arg in get_args(cls))

    return get_base_class(cls.__origin__) if is_generic_alias(cls) else cls


def _breakpoints_satisfies_typing(cls_check: GenericType, instance: Any) -> bool:
    """Check if the breakpoints instance satisfies the typing.

    Args:
        cls_check: The class to check against.
        instance: The instance to check.

    Returns:
        Whether the breakpoints instance satisfies the typing.
    """
    cls_check_base = get_base_class(cls_check)

    if cls_check_base == Breakpoints:
        _, expected_type = get_args(cls_check)
        if is_literal(expected_type):
            for value in instance.values():
                if not isinstance(value, str) or value not in get_args(expected_type):
                    return False
        return True
    elif isinstance(cls_check_base, tuple):
        # union type, so check all types
        return any(
            _breakpoints_satisfies_typing(type_to_check, instance)
            for type_to_check in get_args(cls_check)
        )
    elif cls_check_base == reflex.vars.Var and "__args__" in cls_check.__dict__:
        return _breakpoints_satisfies_typing(get_args(cls_check)[0], instance)

    return False


def _issubclass(cls: GenericType, cls_check: GenericType, instance: Any = None) -> bool:
    """Check if a class is a subclass of another class.

    Args:
        cls: The class to check.
        cls_check: The class to check against.
        instance: An instance of cls to aid in checking generics.

    Returns:
        Whether the class is a subclass of the other class.

    Raises:
        TypeError: If the base class is not valid for issubclass.
    """
    # Special check for Any.
    if cls_check == Any:
        return True
    if cls in [Any, Callable, None]:
        return False

    # Get the base classes.
    cls_base = get_base_class(cls)
    cls_check_base = get_base_class(cls_check)

    # The class we're checking should not be a union.
    if isinstance(cls_base, tuple):
        return False

    # Check that fields of breakpoints match the expected values.
    if isinstance(instance, Breakpoints):
        return _breakpoints_satisfies_typing(cls_check, instance)

    # Check if the types match.
    try:
        return cls_check_base == Any or issubclass(cls_base, cls_check_base)
    except TypeError as te:
        # These errors typically arise from bad annotations and are hard to
        # debug without knowing the type that we tried to compare.
        raise TypeError(f"Invalid type for issubclass: {cls_base}") from te


def _isinstance(obj: Any, cls: GenericType, nested: bool = False) -> bool:
    """Check if an object is an instance of a class.

    Args:
        obj: The object to check.
        cls: The class to check against.
        nested: Whether the check is nested.

    Returns:
        Whether the object is an instance of the class.
    """
    if cls is Any:
        return True

    if cls is None or cls is type(None):
        return obj is None

    if is_literal(cls):
        return obj in get_args(cls)

    if is_union(cls):
        return any(_isinstance(obj, arg) for arg in get_args(cls))

    origin = get_origin(cls)

    if origin is None:
        # cls is a simple class
        return isinstance(obj, cls)

    args = get_args(cls)

    if not args:
        # cls is a simple generic class
        return isinstance(obj, origin)

    if nested and args:
        if origin is list:
            return isinstance(obj, list) and all(
                _isinstance(item, args[0]) for item in obj
            )
        if origin is tuple:
            if args[-1] is Ellipsis:
                return isinstance(obj, tuple) and all(
                    _isinstance(item, args[0]) for item in obj
                )
            return (
                isinstance(obj, tuple)
                and len(obj) == len(args)
                and all(_isinstance(item, arg) for item, arg in zip(obj, args))
            )
        if origin is dict:
            return isinstance(obj, dict) and all(
                _isinstance(key, args[0]) and _isinstance(value, args[1])
                for key, value in obj.items()
            )
        if origin is set:
            return isinstance(obj, set) and all(
                _isinstance(item, args[0]) for item in obj
            )

    if args:
        from reflex.vars import Field

        if origin is Field:
            return _isinstance(obj, args[0])

    return isinstance(obj, get_base_class(cls))


def is_dataframe(value: Type) -> bool:
    """Check if the given value is a dataframe.

    Args:
        value: The value to check.

    Returns:
        Whether the value is a dataframe.
    """
    if is_generic_alias(value) or value == Any:
        return False
    return value.__name__ == "DataFrame"


def is_valid_var_type(type_: Type) -> bool:
    """Check if the given type is a valid prop type.

    Args:
        type_: The type to check.

    Returns:
        Whether the type is a valid prop type.
    """
    from reflex.utils import serializers

    if is_union(type_):
        return all((is_valid_var_type(arg) for arg in get_args(type_)))
    return (
        _issubclass(type_, StateVar)
        or serializers.has_serializer(type_)
        or dataclasses.is_dataclass(type_)
    )


def is_backend_base_variable(name: str, cls: Type) -> bool:
    """Check if this variable name correspond to a backend variable.

    Args:
        name: The name of the variable to check
        cls: The class of the variable to check

    Returns:
        bool: The result of the check
    """
    if name in RESERVED_BACKEND_VAR_NAMES:
        return False

    if not name.startswith("_"):
        return False

    if name.startswith("__"):
        return False

    if name.startswith(f"_{cls.__name__}__"):
        return False

    # Extract the namespace of the original module if defined (dynamic substates).
    if callable(getattr(cls, "_get_type_hints", None)):
        hints = cls._get_type_hints()
    else:
        hints = get_type_hints(cls)
    if name in hints:
        hint = get_origin(hints[name])
        if hint == ClassVar:
            return False

    if name in cls.inherited_backend_vars:
        return False

    from reflex.vars.base import is_computed_var

    if name in cls.__dict__:
        value = cls.__dict__[name]
        if type(value) is classmethod:
            return False
        if callable(value):
            return False

        if isinstance(
            value,
            (
                types.FunctionType,
                property,
                cached_property,
            ),
        ) or is_computed_var(value):
            return False

    return True


def check_type_in_allowed_types(value_type: Type, allowed_types: Iterable) -> bool:
    """Check that a value type is found in a list of allowed types.

    Args:
        value_type: Type of value.
        allowed_types: Iterable of allowed types.

    Returns:
        If the type is found in the allowed types.
    """
    return get_base_class(value_type) in allowed_types


def check_prop_in_allowed_types(prop: Any, allowed_types: Iterable) -> bool:
    """Check that a prop value is in a list of allowed types.
    Does the check in a way that works regardless if it's a raw value or a state Var.

    Args:
        prop: The prop to check.
        allowed_types: The list of allowed types.

    Returns:
        If the prop type match one of the allowed_types.
    """
    from reflex.vars import Var

    type_ = prop._var_type if _isinstance(prop, Var) else type(prop)
    return type_ in allowed_types


def is_encoded_fstring(value) -> bool:
    """Check if a value is an encoded Var f-string.

    Args:
        value: The value string to check.

    Returns:
        Whether the value is an f-string
    """
    return isinstance(value, str) and constants.REFLEX_VAR_OPENING_TAG in value


def validate_literal(key: str, value: Any, expected_type: Type, comp_name: str):
    """Check that a value is a valid literal.

    Args:
        key: The prop name.
        value: The prop value to validate.
        expected_type: The expected type(literal type).
        comp_name: Name of the component.

    Raises:
        ValueError: When the value is not a valid literal.
    """
    from reflex.vars import Var

    if (
        is_literal(expected_type)
        and not isinstance(value, Var)  # validating vars is not supported yet.
        and not is_encoded_fstring(value)  # f-strings are not supported.
        and value not in expected_type.__args__
    ):
        allowed_values = expected_type.__args__
        if value not in allowed_values:
            allowed_value_str = ",".join(
                [str(v) if not isinstance(v, str) else f"'{v}'" for v in allowed_values]
            )
            value_str = f"'{value}'" if isinstance(value, str) else value
            raise ValueError(
                f"prop value for {str(key)} of the `{comp_name}` component should be one of the following: {allowed_value_str}. Got {value_str} instead"
            )


def validate_parameter_literals(func):
    """Decorator to check that the arguments passed to a function
    correspond to the correct function parameter if it (the parameter)
    is a literal type.

    Args:
        func: The function to validate.

    Returns:
        The wrapper function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_params = list(inspect.signature(func).parameters.items())
        annotations = {param[0]: param[1].annotation for param in func_params}

        # validate args
        for param, arg in zip(annotations, args):
            if annotations[param] is inspect.Parameter.empty:
                continue
            validate_literal(param, arg, annotations[param], func.__name__)

        # validate kwargs.
        for key, value in kwargs.items():
            annotation = annotations.get(key)
            if not annotation or annotation is inspect.Parameter.empty:
                continue
            validate_literal(key, value, annotation, func.__name__)
        return func(*args, **kwargs)

    return wrapper


# Store this here for performance.
StateBases = get_base_class(StateVar)
StateIterBases = get_base_class(StateIterVar)


def typehint_issubclass(possible_subclass: Any, possible_superclass: Any) -> bool:
    """Check if a type hint is a subclass of another type hint.

    Args:
        possible_subclass: The type hint to check.
        possible_superclass: The type hint to check against.

    Returns:
        Whether the type hint is a subclass of the other type hint.
    """
    if possible_superclass is Any:
        return True
    if possible_subclass is Any:
        return False

    provided_type_origin = get_origin(possible_subclass)
    accepted_type_origin = get_origin(possible_superclass)

    if provided_type_origin is None and accepted_type_origin is None:
        # In this case, we are dealing with a non-generic type, so we can use issubclass
        return issubclass(possible_subclass, possible_superclass)

    # Remove this check when Python 3.10 is the minimum supported version
    if hasattr(types, "UnionType"):
        provided_type_origin = (
            Union if provided_type_origin is types.UnionType else provided_type_origin
        )
        accepted_type_origin = (
            Union if accepted_type_origin is types.UnionType else accepted_type_origin
        )

    # Get type arguments (e.g., [float, int] for Dict[float, int])
    provided_args = get_args(possible_subclass)
    accepted_args = get_args(possible_superclass)

    if accepted_type_origin is Union:
        if provided_type_origin is not Union:
            return any(
                typehint_issubclass(possible_subclass, accepted_arg)
                for accepted_arg in accepted_args
            )
        return all(
            any(
                typehint_issubclass(provided_arg, accepted_arg)
                for accepted_arg in accepted_args
            )
            for provided_arg in provided_args
        )

    # Check if the origin of both types is the same (e.g., list for List[int])
    # This probably should be issubclass instead of ==
    if (provided_type_origin or possible_subclass) != (
        accepted_type_origin or possible_superclass
    ):
        return False

    # Ensure all specific types are compatible with accepted types
    # Note this is not necessarily correct, as it doesn't check against contravariance and covariance
    # It also ignores when the length of the arguments is different
    return all(
        typehint_issubclass(provided_arg, accepted_arg)
        for provided_arg, accepted_arg in zip(provided_args, accepted_args)
        if accepted_arg is not Any
    )
