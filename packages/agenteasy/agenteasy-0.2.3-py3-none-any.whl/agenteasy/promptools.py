import jinja2
import re
from .agent import AIAgent
from functools import wraps
from copy import deepcopy
from typing import Literal, Callable
import pathlib
import inspect

_root = pathlib.Path(__file__).parent.parent
_sys_ptn = re.compile("^System:([^|]*)(\|\|)?", flags=re.RegexFlag.IGNORECASE)
_user_ptn = re.compile("User:([^|]*)(\|\|)?", flags=re.RegexFlag.IGNORECASE)
_assistant_ptn = re.compile("Assistant:([^|]*)(\|\|)?", flags=re.RegexFlag.IGNORECASE)
_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(f"{_root}/templates"),
    autoescape=jinja2.select_autoescape(enabled_extensions=("jinja2",)),
)


def build_message(role: Literal["system", "user", "assitant"], content):
    return {"role": role, "content": content}


def _get_content_text(content_dict: dict):
    _content_dict = deepcopy(content_dict)
    if isinstance(content_dict["content"], re.Match):
        _content_dict["content"] = content_dict["content"].group(1).strip("\n ")
    return _content_dict

def _assign_function_params(func, *args, **kwargs):
    signature = inspect.signature(func)
    parameter_names = signature.parameters.keys()
    result = kwargs.copy()
    for name,arg in zip(parameter_names,args):
        if name not in result:
           result[name] = arg 
    return result

def ai_template(func: Callable | None = None, post_process: Callable | None = None):
    def outer_wrapper(wrap_func: Callable):
        @wraps(wrap_func)
        def wrapper(
            *args,
            _ae_agent: AIAgent | None = None,
            _ae_params: dict | None = None,
            **kwargs,
        ) -> list[dict] | str:
            params = _assign_function_params(wrap_func,*args,**kwargs)
            doc_str = inspect.getdoc(wrap_func)
            if doc_str is None:
                raw_prompt = _env.get_template(f"{wrap_func.__name__}.jinja2").render(
                    **params
                )
            else:
                raw_prompt = jinja2.Template(doc_str).render(**params)
            match_messages: list[dict] = []
            sys_content = _sys_ptn.search(raw_prompt)
            user_content = _user_ptn.search(raw_prompt)
            assistant_content = _assistant_ptn.search(raw_prompt)

            if sys_content:
                match_messages.append(build_message("system", sys_content))
            if user_content:
                match_messages.append(build_message("user", user_content))
            if assistant_content:
                match_messages.append(build_message("assitant", assistant_content))

            match_messages.sort(key=lambda x: x["content"].span()[0])
            messages = list(map(_get_content_text, match_messages))
            if post_process:
                messages = post_process(messages)
            if _ae_agent:
                _ae_params = _ae_params or {}
                result = _ae_agent.generate(messages=messages, **_ae_params)
                return result
            return messages

        return wrapper

    if func is None:
        return outer_wrapper
    return outer_wrapper(func)
