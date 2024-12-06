import inspect
from pydantic import create_model
import openai
from typing import Callable


def craft_tool_from_function(func):
    """convert python function to openai tool"""
    signature = inspect.signature(func)

    fields = {}
    for name, param in signature.parameters.items():
        _annotation = str if param.annotation is param.empty else param.annotation
        _default = ... if param.default is param.empty else param.default
        fields[name] = (_annotation,_default)


    docstring = func.__doc__

    model = create_model(func.__name__, __doc__=docstring, **fields)
    tool = openai.pydantic_function_tool(model)

    # 由于openai转换有bug，因此重新赋值required
    tool['function']['parameters']['required'] = model.model_json_schema()['required']
    return tool


def batch_make_tools(funcs) -> list[dict]:
    tools = []
    for func in funcs:
        if isinstance(func, dict):
            tools.append(func)
        elif isinstance(func, Callable):
            tools.append(craft_tool_from_function(func))
        else:
            raise ValueError(f"Wrong type of parameters: {func.__name__}:{type(func)}")
    return tools


def call_tool(tool_call_id, func_name, func_list: list, **kwargs):
    for func in func_list:
        if func.__name__ == func_name:
            return {
                "tool_call_id": tool_call_id,
                "role": "tool",
                "content": str(func(**kwargs)),
            }
