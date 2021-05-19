import functools
import inspect

import argparse
from typing import Callable

import docstring_parser


def create_argument_parser_for_function(func):
    signature = inspect.signature(func)
    docstring = docstring_parser.parse(getattr(func, "__doc__", ""))
    param_docs = {p.arg_name: p for p in getattr(docstring, "params", [])}

    parser = argparse.ArgumentParser(
        description=getattr(docstring, "short_description"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for key, parameter in signature.parameters.items():
        parameter_kwargs = {}
        if parameter.kind == inspect.Parameter.KEYWORD_ONLY:
            name = "--{}".format(key.replace("_", "-"))
        else:
            if type(None) in getattr(parameter.annotation, "__args__", []):
                # e.g. `Optional[str]`
                parameter_kwargs["nargs"] = "?"
            name = key

        if parameter.default is not inspect._empty:
            parameter_kwargs["default"] = parameter.default

        parameter_kwargs["help"] = ""
        if key in param_docs and param_docs.get(key).description:
            param_doc: docstring_parser.DocstringParam = param_docs.get(key)
            parameter_kwargs["help"] = param_doc.description

        parser.add_argument(name, **parameter_kwargs)
    return parser


def application(*args, **kwargs):
    def wrapper(function):
        @functools.wraps(function)
        def decorator(*args, **kwargs):
            if len(args) or len(kwargs):
                return function(*args, **kwargs)
            else:
                parser = create_argument_parser_for_function(function)
                args = parser.parse_args()
                kwargs = {key: getattr(args, key) for key in vars(args)}
                return function(**kwargs)
        return decorator

    if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], Callable):
        return wrapper(args[0])
    else:
        return wrapper
