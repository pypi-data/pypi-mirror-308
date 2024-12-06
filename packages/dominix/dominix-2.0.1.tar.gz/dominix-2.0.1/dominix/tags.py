'''
HTMX tag classes.
'''
__license__ = '''
This file is part of Dominix.

Dominix is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

Dominix is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with Dominix.  If not, see
<http://www.gnu.org/licenses/>.
'''
import json
from .dom_tag  import dom_tag, attr, get_current
from .dom1core import dom1core

try:
  basestring = basestring # type: ignore
except NameError: # py3
  basestring = str
  unicode = str

underscored_classes = set(['del', 'input', 'map', 'object'])


_SPECIAL_ATTRS = set(["class", "style", "hx-on", "hx-vals", "hx-headers", "x-bind", "x-on"])

# This would make declaring properties a breeze, but unfortunately VS Code won't display the docstring... :(
# def _attr_prop(attr, doc=None):
#     def getter(attr):
#         def g(self):
#             return self.attributes.get(attr, None)
#         return g
#     def setter(attr):
#         def s(self, value):
#             self.attributes[attr] = value
#         return s
#     return property(getter(attr), setter(attr), doc=doc)
  

# Constants for use with hx_swap

HX_SWAP_INNER_HTML = "innerHtml"    # Replace the inner html of the target element
HX_SWAP_OUTER_HTML = "outerHTML"    # Replace the entire target element with the response
HX_SWAP_BEFOREBEGIN = "beforebegin" # Insert the response before the target element
HX_SWAP_AFGERBEGIN = "afterbegin"   # Insert the response before the first child of the target element
HX_SWAP_BEFOREEND = "beforeend"     # Insert the response after the last child of the target element
HX_SWAP_AFTEREND = "afterend"       # Insert the response after the target element
HX_SWAP_DELETE = "delete"           # Deletes the target element regardless of the response
HX_SWAP_NONE = "none"               # Does not append content from response (out of band items will still be processed).

class html_tag(dom_tag, dom1core):
    
    def __init__(self,
                  *args, 
                  cls:str|list[str]=None,
                  style:str|dict[str, str]=None,
                  hx_get:str=None,
                  hx_post:str=None,
                  hx_on:dict[str, str]=None,
                  hx_push_url:str|bool=None,
                  hx_select:str=None,
                  hx_select_oob:str=None,
                  hx_swap:str=None,
                  hx_swap_oob:str|bool=None,
                  hx_target:str=None,
                  hx_trigger:str=None,
                  hx_vals:str|dict[str, str]=None,
                  hx_boost:bool=None,
                  hx_confirm:str=None,
                  hx_delete:str=None,
                  hx_disable:bool=None,
                  hx_disable_elt:str=None,
                  hx_disinherit:str=None,
                  hx_encoding:str=None,
                  hx_ext:str=None,
                  hx_headers:str|dict[str, str]=None,
                  hx_history:bool=None,
                  hx_history_elt:str=None,
                  hx_include:str=None,
                  hx_indicator:str=None,
                  hx_params:str=None,
                  hx_patch:str=None,
                  hx_preserve:bool=None,
                  hx_prompt:str=None,
                  hx_put:str=None,
                  hx_replace_url:str|bool=None,
                  hx_request:str=None,
                  hx_sync:str=None,
                  hx_validate:bool=None,
                  x_data:str|dict[str, str]=None,
                  x_init:str=None,
                  x_show:str=None,
                  x_bind:dict[str, str]=None,
                  x_on:dict[str, str]=None,
                  x_text:str=None,
                  x_html:str=None,
                  x_model:str=None,
                  x_modelable:str=None,
                  x_for:str=None,
                  x_transition:str=None,
                  x_effect:str=None,
                  x_ignore:str=None,
                  x_ref:str=None,
                  x_cloak:str=None,
                  x_teleport:str=None,
                  x_if:str=None,
                  x_id:str=None,
                  **kwargs):
        '''
        Creates a new tag. Child tags should be passed as arguments and attributes
        should be passed as keyword arguments.

        There is a non-rendering attribute which controls how the tag renders:

        * `__inline (bool)` - If True renders all children tags on the same line.
        * `cls` (str|list[str]) - The class attribute. Can be given either as a string or as a list.
        * `style` (str|dict[str, str]) - The style attribute. Can be given either as a string or as a dictionary.
        * `hx_get (str)` - Issues a GET to the specified URL [hx-get](https://htmx.org/attributes/hx-get/)
        * `hx_post (str)` - Issues a POST to the specified URL [hx-post](https://htmx.org/attributes/hx-post/)
        * `hx_on (dict[str, str])` - Handle events with inline scripts on elements [hx-on](https://htmx.org/attributes/hx-on/)
        * `hx_push_url (str|bool)` - Push a URL into the browser location bar to create history [hx-push-url](https://htmx.org/attributes/hx-push-url/)
        * `hx_select (str)` - Select content to swap in from a response [hx-select](https://htmx.org/attributes/hx-select/)
        * `hx_select_oob (str)` - Select content to swap in from a response, somewhere other than the target (out of band) [hx-select-oob](https://htmx.org/attributes/hx-select-oob/)
        * `hx_swap (str)` - Select content to swap in from a response [hx-swap](https://htmx.org/attributes/hx-swap/)
        * `hx_swap_oob (str|bool)` - Select content to swap in from a response, somewhere other than the target (out of band) [hx-swap-oob](https://htmx.org/attributes/hx-swap-oob/)
        * `hx_target (str)` - Specifies the target element to be swapped [hx-target](https://htmx.org/attributes/hx-target/)
        * `hx_trigger (str)` - Specifies the event that triggers the request [hx-trigger](https://htmx.org/attributes/hx-trigger/)
        * `hx_vals (dict[str, str])` - Add values to submit with the request (JSON format) [hx-vals](https://htmx.org/attributes/hx-vals/)
        * `hx_boost (bool)` - Add progressive enhancement for links and forms [hx-boost](https://htmx.org/attributes/hx-boost/)
        * `hx_confirm (str)` - Shows a confirm() dialog before issuing a request [hx-confirm](https://htmx.org/attributes/hx-confirm/)
        * `hx_delete (str)` - Issues a DELETE to the specified URL [hx-delete](https://htmx.org/attributes/hx-delete/)
        * `hx_disable (bool)` - Disables htmx processing for the given node and any children nodes [hx-disable](https://htmx.org/attributes/hx-disable/)
        * `hx_disable_elt (str)` - Adds the disabled attribute to the specified elements while a request is in fligh [hx-disable-elt](https://htmx.org/attributes/hx-disable-elt/)
        * `hx_disinherit (dict[str, str])` - Control and disable automatic attribute inheritance for child nodes [hx-disinherit](https://htmx.org/attributes/hx-disinherit/)
        * `hx_encoding (str)` - changes the request encoding type [hx-encoding](https://htmx.org/attributes/hx-encoding/)
        * `hx_ext (str)` - Extensions to use for this element [hx-ext](https://htmx.org/attributes/hx-ext/)
        * `hx_headers (dict[str, str])` - Adds to the headers that will be submitted with the request [hx-headers](https://htmx.org/attributes/hx-headers/)
        * `hx_history (bool)` - Prevent sensitive data being saved to the history cache [hx-history](https://htmx.org/attributes/hx-history/)
        * `hx_history_elt (str)` - The element to snapshot and restore during history navigation [hx-history-elt](https://htmx.org/attributes/hx-history-elt/)
        * `hx_include (str)` - Include additional data in requests [hx-include](https://htmx.org/attributes/hx-include/)
        * `hx_indicator (str)` - The element to put the htmx-request class on during the request [hx-indicator](https://htmx.org/attributes/hx-indicator/)
        * `hx_params (str)` - Filters the parameters that will be submitted with a request [hx-params](https://htmx.org/attributes/hx-params/)
        * `hx_patch (str)` - Issues a PATCH to the specified URL [hx-patch](https://htmx.org/attributes/hx-patch/)
        * `hx_preserve (bool)` - Specifies elements to keep unchanged between requests [hx-preserve](https://htmx.org/attributes/hx-preserve/)
        * `hx_prompt (str)` - Shows a prompt() before issuing a request [hx-prompt](https://htmx.org/attributes/hx-prompt/)
        * `hx_put (str)` - Issues a PUT to the specified URL [hx-put](https://htmx.org/attributes/hx-put/)
        * `hx_replace_url (str|bool)` - Replace the URL in the browser location bar [hx-replace-url](https://htmx.org/attributes/hx-replace-url/)
        * `hx_request (str)` - Configures various aspects of the request [hx-request](https://htmx.org/attributes/hx-request/)
        * `hx_sync (str)` - Control the sync behavior of the request [hx-sync](https://htmx.org/attributes/hx-sync/)
        * `hx_validate (bool)` - Force elements to validate themselves before a request [hx-validate](https://htmx.org/attributes/hx-validate/)
        * `x_data (str|dict[str, str])` - Everything in Alpine starts with the x-data directive. [x-data](https://alpinejs.dev/directives/data)
        * `x_init (str)` - The x-init directive allows you to hook into the initialization phase of any element in Alpine. [x-init](https://alpinejs.dev/directives/init)
        * `x_show (str)` - x-show is one of the most useful and powerful directives in Alpine. It provides an expressive way to show and hide DOM elements. [x-show](https://alpinejs.dev/directives/show)
        * `x_bind (dict[str, str])` - x-bind allows you to set HTML attributes on elements based on the result of JavaScript expressions. [x-bind](https://alpinejs.dev/directives/bind)
        * `x_on (dict[str, str])` - x-on allows you to easily run code on dispatched DOM events. [x-on](https://alpinejs.dev/directives/on)
        * `x_text (str)` - x-text sets the text content of an element to the result of a given expression. [x-text](https://alpinejs.dev/directives/text)
        * `x_html (str)` - x-html sets the "innerHTML" property of an element to the result of a given expression. [x-html](https://alpinejs.dev/directives/html)
        * `x_model (str)` - x-model allows you to bind the value of an input element to Alpine data. [x-model](https://alpinejs.dev/directives/model)
        * `x_modelable (str)` - x-modelable allows you to expose any Alpine property as the target of the x-model directive. [x-modelable](https://alpinejs.dev/directives/modelable)
        * `x_for (str)` - Alpine's x-for directive allows you to create DOM elements by iterating through a list. [x-for](https://alpinejs.dev/directives/for)
        * `x_transition (str)` - With a few x-transition directives, you can create smooth transitions between when an element is shown or hidden. [x-transition](https://alpinejs.dev/directives/transition)
        * `x_effect (str)` - x-effect is a useful directive for re-evaluating an expression when one of its dependencies change. [x-effect](https://alpinejs.dev/directives/effect)
        * `x_ignore (str)` - If for some reason, you don't want Alpine to touch a specific section of your HTML, you can prevent it from doing so using x-ignore. [x-ignore](https://alpinejs.dev/directives/ignore)
        * `x_ref (str)` - x-ref in combination with $refs is a useful utility for easily accessing DOM elements directly. [x-ref](https://alpinejs.dev/directives/ref)
        * `x_cloak (str)` - [x-cloak](https://alpinejs.dev/directives/cloak)
        * `x_teleport (str)` - The x-teleport directive allows you to transport part of your Alpine template to another part of the DOM on the page entirely. [x-teleport](https://alpinejs.dev/directives/teleport)
        * `x_if (str)` - x-if allows you to conditionally render elements based on the result of a given expression. [x-if](https://alpinejs.dev/directives/if)
        * `x_id (str)` - x-id allows you to declare a new "scope" for any new IDs generated using $id(). [x-id](https://alpinejs.dev/directives/id)
        * `**kwargs` - Additional attributes to set on the tag.        
        '''
        super(html_tag, self).__init__(
            *args, 
            cls=cls,
            style=style,
            hx_get = hx_get,
            hx_post = hx_post,
            hx_on = hx_on,
            hx_push_url = hx_push_url,
            hx_select = hx_select,
            hx_select_oob = hx_select_oob,
            hx_swap = hx_swap,
            hx_swap_oob = hx_swap_oob,
            hx_target = hx_target,
            hx_trigger = hx_trigger,
            hx_vals = hx_vals,
            hx_boost = hx_boost,
            hx_confirm = hx_confirm,
            hx_delete = hx_delete,
            hx_disable = hx_disable,
            hx_disable_elt = hx_disable_elt,
            hx_disinherit = hx_disinherit,
            hx_encoding = hx_encoding,
            hx_ext = hx_ext,
            hx_headers = hx_headers,
            hx_history = hx_history,
            hx_history_elt = hx_history_elt,
            hx_include = hx_include,
            hx_indicator = hx_indicator,
            hx_params = hx_params,
            hx_patch = hx_patch,
            hx_preserve = hx_preserve,
            hx_prompt = hx_prompt,
            hx_put = hx_put,
            hx_replace_url = hx_replace_url,
            hx_request = hx_request,
            hx_sync = hx_sync,
            hx_validate = hx_validate,
            x_data = x_data,
            x_init = x_init,
            x_show = x_show,
            x_bind = x_bind,
            x_on = x_on,
            x_text = x_text,
            x_html = x_html,
            x_model = x_model,
            x_modelable = x_modelable,
            x_for = x_for,
            x_transition = x_transition,
            x_effect = x_effect,
            x_ignore = x_ignore,
            x_ref = x_ref,
            x_cloak = x_cloak,
            x_teleport = x_teleport,
            x_if = x_if,
            x_id = x_id,
            **kwargs)
    
    
    def _all_attribute_items(self):
        all = [(k, v) 
               for k, v in super()._all_attribute_items() 
               if k not in _SPECIAL_ATTRS]
        for attr in _SPECIAL_ATTRS:
            if attr == "class":
                classes = self.attributes.get(attr, [])
                if isinstance(classes, list):
                    classes = " ".join(classes)
                if (classes):
                    all.append((attr, classes))
            else:
                map = self.attributes.get(attr, {})
                if map:
                    if attr == "hx-on":
                        all += [(f"hx-on:{k}", v) for k, v in self.attributes.get("hx-on", {}).items()]
                    elif attr == "x-bind":
                        all += [(f"x-bind:{k}", v) for k, v in self.attributes.get("x-bind", {}).items()]
                    elif attr == "x-on":
                        all += [(f"x-on:{k}", v) for k, v in self.attributes.get("x-on", {}).items()]
                    elif attr == "style":
                        if isinstance(map, dict):
                            all.append((attr, "; ".join([f"{k}:{v}" for k, v in map.items()])))
                        else:
                            all.append((attr, map))
                    else:
                        # hx-vals, hx-headers
                        all.append((attr, json.dumps(map)))
        return all


    @staticmethod
    def __update_dict(d:dict, k_or_tuple_or_dict, value=None):
        # Support method for dictionary properties.
        if value is None:
            if isinstance(k_or_tuple_or_dict, dict):
                d.update(k_or_tuple_or_dict)
            elif isinstance(k_or_tuple_or_dict, tuple):
                d[k_or_tuple_or_dict[0]] = k_or_tuple_or_dict[1]
            else:
                raise ValueError("Invalid argument type. Must be a tuple or a dictionary when value is None, got " + str(k_or_tuple_or_dict))
        else:
            d[k_or_tuple_or_dict] = value
        return d
    
    def __del_dict(self, d:dict, *keys:str):
        # Support method for dictionary properties.
        for key in keys:
            d.pop(key, None)
        return self
    
    def __json_value(self, attr) -> dict[str, str]:
        # Support method for JSON properties.
        value = self.attributes.setdefault(attr, {})
        if isinstance(value, str):
            value = json.loads(value)
            self.attributes[attr] = value
        return value
    
    def __json_upd(self, attr, key_or_tuple_or_dict_or_str, value=None):
        # Support method for JSON properties.
        dict_ = self.__json_value(attr)
        if isinstance(key_or_tuple_or_dict_or_str, str) and value is None:
            value = json.loads(key_or_tuple_or_dict_or_str)
            dict_.update(dict_)
        else:
            html_tag.__update_dict(dict_, key_or_tuple_or_dict_or_str, value)
        return self


    # HTML attributes

    @property
    def cls(self) -> list[str]:
        """
        The class attribute of the tag as a list. This property lets you manipulate the
        class list using Python list operations. The list will be converted to a correct
        string representation when the tag is rendered.
        """
        classes = self.attributes.setdefault("class", [])
        if isinstance(classes, str):
            classes = classes.split()
            self.attributes["class"] = classes
        return classes
    @cls.setter
    def cls(self, value:str|list[str]):
        self.attributes["class"] = value

    def add_class(self, *values:str):
        """Adds one or more classes to the class attribute (modifying existing list)."""
        self.cls.extend(values)
        return self
    
    def rem_class(self, *values:str):
        """Removes one or more classes from the class attribute (modifying existing list)."""
        for value in values:
            # In case of multiple occurrences of the same class
            try:
                while True:
                    self.cls.remove(value)
            except ValueError:
                pass
        return self

    @staticmethod    
    def __split_style(style:str):
        ret = {}
        for pair in style.split(";"):
            k, v = pair.split(":")
            ret[k.strip()] = v.strip()
        return ret

    @property
    def style(self) -> dict:
        """
        The style attribute of the tag as a dictionary. This property lets you manipulate the
        style using Python dictionary operations. The dictionary will be converted to a correct
        string representation when the tag is rendered.
        """
        style = self.attributes.get("style", None)
        if isinstance(style, str):
            ret = self.__split_style(style)
            self.attributes["style"] = ret
            return ret
        else:
            return style
    @style.setter
    def hx_get(self, value:str|dict[str, str]):
        self.attributes["style"] = value

    def upd_style(self, key_or_tuple_or_dict_or_str, value=None):
        """
        Adds one or more styles to the style attribute (modifying existing dictionary).
        If given only one argument, it can be a dictionary, a tuple or a string. If it is a string,
        it will be split into a dictionary. If given two arguments, the first argument is the key
        and the second is the value.
        """
        if isinstance(key_or_tuple_or_dict_or_str, str) and value is None:
            style = self.__split_style(key_or_tuple_or_dict_or_str)
            self.style.update(style)
        else:
            html_tag.__update_dict(self.style, key_or_tuple_or_dict_or_str, value)
        return self

    def del_style(self, *keys:str):
        """Removes one or more styles from the style attribute (modifying existing dictionary)."""
        for key in keys:
            self.style.pop(key, None)
        return self

    # HTMX Core Attributes

    @property
    def hx_get(self) -> str:
        """Issues a GET to the specified URL. [hx-get](https://htmx.org/attributes/hx-get/)"""
        return self.attributes.get("hx-get", None)
    @hx_get.setter
    def hx_get(self, value:str):
        self.attributes["hx-get"] = value

    @property
    def hx_post(self) -> str:
        """Issues a POST to the specified URL. [hx-post](https://htmx.org/attributes/hx-post/)"""
        return self.attributes.get("hx-post", None)
    @hx_post.setter
    def hx_post(self, value:str):
        self.attributes["hx-post"] = value

    @property
    def hx_on(self) -> dict[str, str]:
        """Handle events with inline scripts on elements. [hx-on](https://htmx.org/attributes/hx-on/)"""
        return self.attributes.setdefault("hx-on", {})
    @hx_on.setter
    def hx_on(self, value:dict[str, str]):
        self.attributes["hx-on"] = value

    def upd_hx_on(self, key_or_tuple_or_dict_or_str, value=None):
        """
        Adds one or more events to the hx-on attribute (modifying existing dictionary).
        If given only one argument, it can be a dictionary or a tuple. If it is a string,
        If given two arguments, the first argument is the key and the second is the value.
        """
        html_tag.__update_dict(self.hx_on, key_or_tuple_or_dict_or_str, value)
        return self

    def del_hx_on(self, *keys:str):
        """Removes one or more events from the style attribute (modifying existing dictionary)."""
        for key in keys:
            self.hx_on.pop(key, None)
        return self
        
    @property
    def hx_push_url(self) -> str|bool:
        """Push a URL into the browser location bar to create history. [hx-push-url](https://htmx.org/attributes/hx-push-url/)"""
        return self.attributes.get("hx-push-url", None)
    @hx_push_url.setter
    def hx_push_url(self, value:str|bool):
        self.attributes["hx-push-url"] = value

    @property
    def hx_select(self) -> str:
        """Select content to swap in from a response. [hx-select](https://htmx.org/attributes/hx-select/)"""
        return self.attributes.get("hx-select", None)
    @hx_select.setter
    def hx_select(self, value:str):
        self.attributes["hx-select"] = value

    @property
    def hx_select_oob(self) -> str:
        """Select content to swap in from a response, somewhere other than the target (out of band). [hx-select-oob](https://htmx.org/attributes/hx-select-oob/)"""
        return self.attributes.get("hx-select-oob", None)
    @hx_select_oob.setter
    def hx_select_oob(self, value:str):
        self.attributes["hx-select-oob"] = value

    @property
    def hx_swap(self) -> str:
        """Select content to swap in from a response. [hx-swap](https://htmx.org/attributes/hx-swap/)"""
        return self.attributes.get("hx-swap", None)
    @hx_swap.setter
    def hx_swap(self, value:str):
        self.attributes["hx-swap"] = value

    @property
    def hx_swap_oob(self) -> str|bool:
        """Select content to swap in from a response, somewhere other than the target (out of band). [hx-swap-oob](https://htmx.org/attributes/hx-swap-oob/)"""
        return self.attributes.get("hx-swap-oob", None)
    @hx_swap_oob.setter
    def hx_swap_oob(self, value:str|bool):
        self.attributes["hx-swap-oob"] = value

    @property
    def hx_target(self) -> str:
        """Specifies the target element to be swapped. [hx-target](https://htmx.org/attributes/hx-target/)"""
        return self.attributes.get("hx-target", None)
    @hx_target.setter
    def hx_target(self, value:str):
        self.attributes["hx-target"] = value

    @property
    def hx_trigger(self) -> str:
        """Specifies the event that triggers the request. [hx-trigger](https://htmx.org/attributes/hx-trigger/)"""
        return self.attributes.get("hx-trigger", None)
    @hx_trigger.setter
    def hx_trigger(self, value:str):
        self.attributes["hx-trigger"] = value
    
    @property
    def hx_vals(self) -> dict[str, str]:
        """Add values to submit with the request (JSON format). [hx-vals](https://htmx.org/attributes/hx-vals/)"""
        return self.__json_value("hx-vals")
    @hx_vals.setter
    def hx_vals(self, value:str|dict[str, str]):
        self.attributes["hx-vals"] = value

    def upd_hx_vals(self, key_or_tuple_or_dict_or_str, value=None):
        """
        Adds one or more values to the hx-vals attribute (modifying existing dictionary).
        If given only one argument, it can be a dictionary, a tuple or a string. If it is a string,
        it will be converted from JSON to a dictionary. If given two arguments, the first argument is the key
        and the second is the value.
        """
        return self.__json_upd("hx-vals", key_or_tuple_or_dict_or_str, value)

    def del_hx_vals(self, *keys:str):
        """Removes one or more styles from the hx-vals attribute (modifying existing dictionary)."""
        for key in keys:
            self.hx_vals.pop(key, None)
        return self


    # HTMX Additional Attributes
        
    @property
    def hx_boost(self) -> bool:
        """Add progressive enhancement for links and forms. [hx-boost](https://htmx.org/attributes/hx-boost/)"""
        return self.attributes.get("hx-boost", None)
    @hx_boost.setter
    def hx_boost(self, value:bool):
        self.attributes["hx-boost"] = value

    @property
    def hx_confirm(self) -> str:
        """Shows a confirm() dialog before issuing a request. [hx-confirm](https://htmx.org/attributes/hx-confirm/)"""
        return self.attributes.get("hx-confirm", None)
    @hx_confirm.setter
    def hx_confirm(self, value:str):
        self.attributes["hx-confirm"] = value

    @property
    def hx_delete(self) -> str:
        """Issues a DELETE to the specified URL. [hx-delete](https://htmx.org/attributes/hx-delete/)"""
        return self.attributes.get("hx-delete", None)
    @hx_delete.setter
    def hx_delete(self, value:str):
        self.attributes["hx-delete"] = value

    @property
    def hx_disable(self) -> bool:
        """Disables htmx processing for the given node and any children nodes. [hx-disable](https://htmx.org/attributes/hx-disable/)"""
        return self.attributes.get("hx-disable", None)
    @hx_disable.setter
    def hx_disable(self, value:bool):
        self.attributes["hx-disable"] = value

    @property
    def hx_disable_elt(self) -> str:
        """Adds the disabled attribute to the specified elements while a request is in fligh. [hx-disable-elt](https://htmx.org/attributes/hx-disable-elt/)"""
        return self.attributes.get("hx-disable-elt", None)
    @hx_disable_elt.setter
    def hx_disable_elt(self, value:str):
        self.attributes["hx-disable-elt"] = value

    @property
    def hx_disinherit(self) -> dict[str, str]:
        """Control and disable automatic attribute inheritance for child nodes. [hx-disinherit](https://htmx.org/attributes/hx-disinherit/)"""
        return self.attributes.setdefault("hx-disinherit", {})
    @hx_disinherit.setter
    def hx_disinherit(self, value:dict[str, str]):
        self.attributes["hx-disinherit"] = value

    @property
    def hx_encoding(self) -> str:
        """changes the request encoding type. [hx-encoding](https://htmx.org/attributes/hx-encoding/)"""
        return self.attributes.get("hx-encoding", None)
    @hx_encoding.setter
    def hx_encoding(self, value:str):
        self.attributes["hx-encoding"] = value

    @property
    def hx_ext(self) -> str:
        """Extensions to use for this element. [hx-ext](https://htmx.org/attributes/hx-ext/)"""
        return self.attributes.get("hx-ext", None)
    @hx_ext.setter
    def hx_ext(self, value:str):
        self.attributes["hx-ext"] = value

    @property
    def hx_headers(self) -> dict[str, str]:
        """Adds to the headers that will be submitted with the request. [hx-headers](https://htmx.org/attributes/hx-headers/)"""
        return self.__json_value("hx-headers")
    @hx_headers.setter
    def hx_headers(self, value:dict[str, str]):
        self.attributes["hx-headers"] = value

    def upd_hx_headers(self, key_or_tuple_or_dict_or_str, value=None):
        """
        Adds one or more styles to the hx-headers attribute (modifying existing dictionary).
        If given only one argument, it can be a dictionary, a tuple or a string. If it is a string,
        it will be converted from JSON to a dictionary. If given two arguments, the first argument is the key
        and the second is the value.
        """
        return self.__json_upd("hx-headers", key_or_tuple_or_dict_or_str, value)
    
    def del_hx_headers(self, *keys:str):
        """Removes one or more styles from the hx-headers attribute (modifying existing dictionary)."""
        for key in keys:
            self.hx_headers.pop(key, None)
        return self

    @property
    def hx_history(self) -> bool:
        """Prevent sensitive data being saved to the history cache. [hx-history](https://htmx.org/attributes/hx-history/)"""
        return self.attributes.get("hx-history", None)
    @hx_history.setter
    def hx_history(self, value:bool):
        self.attributes["hx-history"] = value

    @property
    def hx_history_elt(self) -> str:
        """The element to snapshot and restore during history navigation. [hx-history-elt](https://htmx.org/attributes/hx-history-elt/)"""
        return self.attributes.get("hx-history-elt", None)
    @hx_history_elt.setter
    def hx_history_elt(self, value:str):
        self.attributes["hx-history-elt"] = value

    @property
    def hx_include(self) -> str:
        """Include additional data in requests. [hx-include](https://htmx.org/attributes/hx-include/)"""
        return self.attributes.get("hx-include", None)
    @hx_include.setter
    def hx_include(self, value:str):
        self.attributes["hx-include"] = value

    @property
    def hx_indicator(self) -> str:
        """The element to put the htmx-request class on during the request. [hx-indicator](https://htmx.org/attributes/hx-indicator/)"""
        return self.attributes.get("hx-indicator", None)
    @hx_indicator.setter
    def hx_indicator(self, value:str):
        self.attributes["hx-indicator"] = value

    @property
    def hx_params(self) -> str:
        """Filters the parameters that will be submitted with a request. [hx-params](https://htmx.org/attributes/hx-params/)"""
        return self.attributes.get("hx-params", None)
    @hx_params.setter
    def hx_params(self, value:str):
        self.attributes["hx-params"] = value

    @property
    def hx_patch(self) -> str:
        """Issues a PATCH to the specified URL. [hx-patch](https://htmx.org/attributes/hx-patch/)"""
        return self.attributes.get("hx-patch", None)
    @hx_patch.setter
    def hx_patch(self, value:str):
        self.attributes["hx-patch"] = value

    @property
    def hx_preserve(self) -> bool:
        """Specifies elements to keep unchanged between requests. [hx-preserve](https://htmx.org/attributes/hx-preserve/)"""
        return self.attributes.get("hx-preserve", None)
    @hx_preserve.setter
    def hx_preserve(self, value:bool):
        self.attributes["hx-preserve"] = value

    @property
    def hx_prompt(self) -> str:
        """Shows a prompt() before issuing a request. [hx-prompt](https://htmx.org/attributes/hx-prompt/)"""
        return self.attributes.get("hx-prompt", None)
    @hx_prompt.setter
    def hx_prompt(self, value:str):
        self.attributes["hx-prompt"] = value

    @property
    def hx_put(self) -> str:
        """Issues a PUT to the specified URL. [hx-put](https://htmx.org/attributes/hx-put/)"""
        return self.attributes.get("hx-put", None)
    @hx_put.setter
    def hx_put(self, value:str):
        self.attributes["hx-put"] = value

    @property
    def hx_replace_url(self) -> str|bool:
        """Replace the URL in the browser location bar. [hx-replace-url](https://htmx.org/attributes/hx-replace-url/)"""
        return self.attributes.get("hx-replace-url", None)
    @hx_replace_url.setter
    def hx_replace_url(self, value:str|bool):
        self.attributes["hx-replace-url"] = value

    @property
    def hx_request(self) -> str:
        """Configures various aspects of the request. [hx-request](https://htmx.org/attributes/hx-request/)"""
        return self.attributes.get("hx-request", None)
    @hx_request.setter
    def hx_request(self, value:str):
        self.attributes["hx-request"] = value

    @property
    def hx_sync(self) -> str:
        """Control the sync behavior of the request. [hx-sync](https://htmx.org/attributes/hx-sync/)"""
        return self.attributes.get("hx-sync", None)
    @hx_sync.setter
    def hx_sync(self, value:str):
        self.attributes["hx-sync"] = value

    @property
    def hx_validate(self) -> bool:
        """Force elements to validate themselves before a request. [hx-validate](https://htmx.org/attributes/hx-validate/)"""
        return self.attributes.get("hx-validate", None)
    @hx_validate.setter
    def hx_validate(self, value:bool):
        self.attributes["hx-validate"] = value


    # Alpine.js Additional Attributes

    @property
    def x_data(self) -> str|dict[str, str]:
        """
        Everything in Alpine starts with the x-data directive.
        x-data defines a chunk of HTML as an Alpine component and provides the reactive data for that component to reference.
        [x-data](https://alpinejs.dev/directives/data)
        """
        return self.__json_value("x-data")
    @x_data.setter
    def x_data(self, value:str|dict[str, str]):
        self.attributes["x-data"] = value

    @property
    def x_init(self) -> str:
        """The x-init directive allows you to hook into the initialization phase of any element in Alpine. [x-init](https://alpinejs.dev/directives/init)"""
        return self.attributes.get("x-init", None)
    @x_init.setter
    def x_init(self, value:str):
        self.attributes["x-init"] = value

    @property
    def x_show(self) -> str:
        """x-show is one of the most useful and powerful directives in Alpine. It provides an expressive way to show and hide DOM elements. [x-show](https://alpinejs.dev/directives/show)"""
        return self.attributes.get("x-show", None)
    @x_show.setter
    def x_show(self, value:str):
        self.attributes["x-show"] = value

    @property
    def x_bind(self) -> dict[str, str]:
        """x-bind allows you to set HTML attributes on elements based on the result of JavaScript expressions. [x-bind](https://alpinejs.dev/directives/bind)"""
        return self.__json_value("x-bind")
    @x_bind.setter
    def x_bind(self, value:dict[str, str]):
        self.attributes["x-bind"] = value

    def upd_x_bind(self, key_or_tuple_or_dict_or_str, value=None):
        """
        Adds one or more attributes to the x-bind attribute (modifying existing dictionary).
        """
        return self.__json_upd("x-bind", key_or_tuple_or_dict_or_str, value)
    
    def del_x_bind(self, *keys:str):
        """Removes one or more attributes from the x-bind attribute (modifying existing dictionary)."""
        for key in keys:
            self.x_bind.pop(key, None)
        return self

    @property
    def x_on(self) -> dict[str, str]:
        """x-on allows you to easily run code on dispatched DOM events. [x-on](https://alpinejs.dev/directives/on)"""
        return self.__json_value("x-on")
    @x_on.setter
    def x_on(self, value:dict[str, str]):
        self.attributes["x-on"] = value

    def upd_x_on(self, key_or_tuple_or_dict_or_str, value=None):
        """
        Adds one or more events to the x-on attribute (modifying existing dictionary).
        If given only one argument, it can be a dictionary or a tuple. If it is a string,
        If given two arguments, the first argument is the key and the second is the value.
        """
        html_tag.__update_dict(self.x_on, key_or_tuple_or_dict_or_str, value)
        return self

    def del_x_on(self, *keys:str):
        """Removes one or more events from the x-on attribute (modifying existing dictionary). [x-on](https://alpinejs.dev/directives/on)"""
        for key in keys:
            self.x_on.pop(key, None)
        return self
     
    @property
    def x_text(self) -> str:
        """x-text sets the text content of an element to the result of a given expression. [x-text](https://alpinejs.dev/directives/text)"""
        return self.attributes.get("x-text", None)
    @x_text.setter
    def x_text(self, value:str):
        self.attributes["x-text"] = value

    @property
    def x_html(self) -> str:
        """
        x-html sets the "innerHTML" property of an element to the result of a given expression.
        WARNING: Only use on trusted content and never on user-provided content. Dynamically rendering HTML from third parties can easily lead to XSS vulnerabilities.
        [x-html](https://alpinejs.dev/directives/html)
        """
        return self.attributes.get("x-html", None)
    @x_html.setter
    def x_html(self, value:str):
        self.attributes["x-html"] = value

    @property
    def x_model(self) -> str:
        """x-model allows you to bind the value of an input element to Alpine data. [x-model](https://alpinejs.dev/directives/model)"""
        return self.attributes.get("x-model", None)
    @x_model.setter
    def x_model(self, value:str):
        self.attributes["x-model"] = value

    @property
    def x_modelable(self) -> str:
        """x-modelable allows you to expose any Alpine property as the target of the x-model directive. [x-modelable](https://alpinejs.dev/directives/modelable)"""
        return self.attributes.get("x-modelable", None)
    @x_modelable.setter
    def x_modelable(self, value:str):
        self.attributes["x-modelable"] = value

    @property
    def x_for(self) -> str:
        """Alpine's x-for directive allows you to create DOM elements by iterating through a list. [x-for](https://alpinejs.dev/directives/for)"""
        return self.attributes.get("x-for", None)
    @x_for.setter
    def x_for(self, value:str):
        self.attributes["x-for"] = value

    @property
    def x_transition(self) -> str:
        """Alpine provides a robust transitions utility out of the box. With a few x-transition directives, you can create smooth transitions between when an element is shown or hidden. [x-transition](https://alpinejs.dev/directives/transition)"""
        return self.attributes.get("x-transition", None)
    @x_transition.setter
    def x_transition(self, value:str):
        self.attributes["x-transition"] = value

    @property
    def x_effect(self) -> str:
        """
        x-effect is a useful directive for re-evaluating an expression when one of its dependencies change.
        You can think of it as a watcher where you don't have to specify what property to watch, it will watch all properties used within it.
        [x-effect](https://alpinejs.dev/directives/effect)
        """
        return self.attributes.get("x-effect", None)
    @x_effect.setter
    def x_effect(self, value:str):
        self.attributes["x-effect"] = value

    @property
    def x_ignore(self) -> str:
        """
        By default, Alpine will crawl and initialize the entire DOM tree of an element containing x-init or x-data.
        If for some reason, you don't want Alpine to touch a specific section of your HTML, you can prevent it from doing so using x-ignore.
        [x-ignore](https://alpinejs.dev/directives/ignore)
        """
        return self.attributes.get("x-ignore", None)
    @x_ignore.setter
    def x_ignore(self, value:str):
        self.attributes["x-ignore"] = value

    @property
    def x_ref(self) -> str:
        """
        x-ref in combination with $refs is a useful utility for easily accessing DOM elements directly. 
        It's most useful as a replacement for APIs like getElementById and querySelector.
        [x-ref](https://alpinejs.dev/directives/ref)
        """
        return self.attributes.get("x-ref", None)
    @x_ref.setter
    def x_ref(self, value:str):
        self.attributes["x-ref"] = value

    @property
    def x_cloak(self) -> str:
        """
        Sometimes, when you're using AlpineJS for a part of your template, there is a "blip" where you might see your uninitialized template after the page loads, but before Alpine loads.
        x-cloak addresses this scenario by hiding the element it's attached to until Alpine is fully loaded on the page.
        [x-cloak](https://alpinejs.dev/directives/cloak)
        """
        return self.attributes.get("x-cloak", None)
    @x_cloak.setter
    def x_cloak(self, value:str):
        self.attributes["x-cloak"] = value

    @property
    def x_teleport(self) -> str:
        """
        The x-teleport directive allows you to transport part of your Alpine template to another part of the DOM on the page entirely.
        This is useful for things like modals (especially nesting them), where it's helpful to break out of the z-index of the current Alpine component.
        [x-teleport](https://alpinejs.dev/directives/teleport)
        """
        return self.attributes.get("x-teleport", None)
    @x_teleport.setter
    def x_teleport(self, value:str):
        self.attributes["x-teleport"] = value

    @property
    def x_if(self) -> str:
        """
        x-if is used for toggling elements on the page, similarly to x-show, however it completely adds and removes the element it's applied to rather than just changing its CSS display property to "none".
        [x-if](https://alpinejs.dev/directives/if)
        """
        return self.attributes.get("x-if", None)
    @x_if.setter
    def x_if(self, value:str):
        self.attributes["x-if"] = value

    @property
    def x_id(self) -> str:
        """
        x-id allows you to declare a new "scope" for any new IDs generated using $id(). It accepts an array of strings (ID names) and adds a suffix to each $id('...') generated within it that is unique to other IDs on the page.
        x-id is meant to be used in conjunction with the $id(...) magic.
        [x-id](https://alpinejs.dev/directives/id)
        """
        return self.attributes.get("x-id", None)
    @x_id.setter
    def x_id(self, value:str):
        self.attributes["x-id"] = value


# Global functions for use inside `with` statements

def add_class(*values:str):
    """
    Adds one or more classes to the class attribute of the current tag.
    """
    return get_current().add_class(*values)

def rem_class(*values:str):
    """
    Removes one or more classes from the class attribute of the current tag.
    """
    return get_current().rem_class(*values)


def upd_style(key_or_tuple_or_dict_or_str, value=None):
    """
    Adds one or more styles to the style attribute of the current tag.
    If given only one argument, it can be a dictionary, a tuple or a string. If it is a string,
    it will be split into a dictionary. If given two arguments, the first argument is the key
    and the second is the value.
    """
    return get_current().upd_style(key_or_tuple_or_dict_or_str, value)

def del_style(*keys:str):
    """
    Removes one or more styles from the style attribute of the current tag.
    """
    return get_current().del_style(*keys)


def upd_hx_on(key_or_tuple_or_dict_or_str, value=None):
    """
    Adds one or more events to the hx-on attribute (modifying existing dictionary).
    If given only one argument, it can be a dictionary or a tuple. If it is a string,
    If given two arguments, the first argument is the key and the second is the value.
    """
    return get_current().upd_hx_on(key_or_tuple_or_dict_or_str, value)

def del_hx_on(*keys:str):
    """
    Removes one or more events from the hx-on attribute of the current tag.
    """
    return get_current().del_hx_on(*keys)


def upd_hx_vals(key_or_tuple_or_dict_or_str, value=None):
    """
    Adds one or more styles to the hx-vals attribute of the current tag.
    If given only one argument, it can be a dictionary, a tuple or a string. If it is a string,
    it will be converted from JSON to a dictionary. If given two arguments, the first argument is the key
    and the second is the value.
    """
    return get_current().upd_hx_vals(key_or_tuple_or_dict_or_str, value)

def del_hx_vals(*keys:str):
    """
    Removes one or more styles from the hx-vals attribute of the current tag.
    """
    return get_current().del_hx_vals(*keys)


def upd_hx_headers(key_or_tuple_or_dict_or_str, value=None):
    """
    Adds one or more styles to the hx-headers attribute of the current tag.
    If given only one argument, it can be a dictionary, a tuple or a string. If it is a string,
    it will be converted from JSON to a dictionary. If given two arguments, the first argument is the key
    and the second is the value.
    """
    return get_current().upd_hx_headers(key_or_tuple_or_dict_or_str, value)

def del_hx_headers(*keys:str):
    """
    Removes one or more styles from the hx-headers attribute of the current tag.
    """
    return get_current().del_hx_headers(*keys)
    
def upd_x_bind(key_or_tuple_or_dict_or_str, value=None):
    """
    Adds one or more attributes to the x-bind attribute (modifying existing dictionary).
    """
    return get_current().upd_x_bind(key_or_tuple_or_dict_or_str, value)

def del_x_bind(*keys:str):
    """Removes one or more attributes from the x-bind attribute (modifying existing dictionary)."""
    return get_current().del_x_bind(*keys)

def upd_x_on(key_or_tuple_or_dict_or_str, value=None):
    """
    Adds one or more events to the x-on attribute (modifying existing dictionary).
    If given only one argument, it can be a dictionary or a tuple. If it is a string,
    If given two arguments, the first argument is the key and the second is the value.
    """
    return get_current().upd_x_on(key_or_tuple_or_dict_or_str, value)

def del_x_on(*keys:str):
    """Removes one or more events from the x-on attribute (modifying existing dictionary). [x-on](https://alpinejs.dev/directives/on)"""
    return get_current().del_x_on(*keys)
     

################################################################################
############################### Html Tag Classes ###############################
################################################################################

# Root element

class html(html_tag):
  '''
  The html element represents the root of an HTML document.
  '''
  pass


# Document metadata
class head(html_tag):
  '''
  The head element represents a collection of metadata for the document.
  '''
  pass


class title(html_tag):
  '''
  The title element represents the document's title or name. Authors should use
  titles that identify their documents even when they are used out of context,
  for example in a user's history or bookmarks, or in search results. The
  document's title is often different from its first heading, since the first
  heading does not have to stand alone when taken out of context.
  '''
  def _get_text(self):
    return u''.join(self.get(basestring))
  def _set_text(self, text):
    self.clear()
    self.add(text)
  text = property(_get_text, _set_text)


class base(html_tag):
  '''
  The base element allows authors to specify the document base URL for the
  purposes of resolving relative URLs, and the name of the default browsing
  context for the purposes of following hyperlinks. The element does not
  represent any content beyond this information.
  '''
  is_single = True


class link(html_tag):
  '''
  The link element allows authors to link their document to other resources.
  '''
  is_single = True


class meta(html_tag):
  '''
  The meta element represents various kinds of metadata that cannot be
  expressed using the title, base, link, style, and script elements.
  '''
  is_single = True


class style(html_tag):
  '''
  The style element allows authors to embed style information in their
  documents. The style element is one of several inputs to the styling
  processing model. The element does not represent content for the user.
  '''
  is_pretty = False


# Scripting
class script(html_tag):
  '''
  The script element allows authors to include dynamic script and data blocks
  in their documents. The element does not represent content for the user.
  '''
  is_pretty = False


class noscript(html_tag):
  '''
  The noscript element represents nothing if scripting is enabled, and
  represents its children if scripting is disabled. It is used to present
  different markup to user agents that support scripting and those that don't
  support scripting, by affecting how the document is parsed.
  '''
  pass


# Sections
class body(html_tag):
  '''
  The body element represents the main content of the document.
  '''
  pass

class main(html_tag):
  '''
  The main content area of a document includes content that is unique to that
  document and excludes content that is repeated across a set of documents such
  as site navigation links, copyright information, site logos and banners and
  search forms (unless the document or application's main function is that of a
  search form).
  '''

class section(html_tag):
  '''
  The section element represents a generic section of a document or
  application. A section, in this context, is a thematic grouping of content,
  typically with a heading.
  '''
  pass


class nav(html_tag):
  '''
  The nav element represents a section of a page that links to other pages or
  to parts within the page: a section with navigation links.
  '''
  pass


class article(html_tag):
  '''
  The article element represents a self-contained composition in a document,
  page, application, or site and that is, in principle, independently
  distributable or reusable, e.g. in syndication. This could be a forum post, a
  magazine or newspaper article, a blog entry, a user-submitted comment, an
  interactive widget or gadget, or any other independent item of content.
  '''
  pass


class aside(html_tag):
  '''
  The aside element represents a section of a page that consists of content
  that is tangentially related to the content around the aside element, and
  which could be considered separate from that content. Such sections are
  often represented as sidebars in printed typography.
  '''
  pass


class h1(html_tag):
  '''
  Represents the highest ranking heading.
  '''
  pass


class h2(html_tag):
  '''
  Represents the second-highest ranking heading.
  '''
  pass


class h3(html_tag):
  '''
  Represents the third-highest ranking heading.
  '''
  pass


class h4(html_tag):
  '''
  Represents the fourth-highest ranking heading.
  '''
  pass


class h5(html_tag):
  '''
  Represents the fifth-highest ranking heading.
  '''
  pass


class h6(html_tag):
  '''
  Represents the sixth-highest ranking heading.
  '''
  pass


class hgroup(html_tag):
  '''
  The hgroup element represents the heading of a section. The element is used
  to group a set of h1-h6 elements when the heading has multiple levels, such
  as subheadings, alternative titles, or taglines.
  '''
  pass


class header(html_tag):
  '''
  The header element represents a group of introductory or navigational aids.
  '''
  pass


class footer(html_tag):
  '''
  The footer element represents a footer for its nearest ancestor sectioning
  content or sectioning root element. A footer typically contains information
  about its section such as who wrote it, links to related documents,
  copyright data, and the like.
  '''
  pass


class address(html_tag):
  '''
  The address element represents the contact information for its nearest
  article or body element ancestor. If that is the body element, then the
  contact information applies to the document as a whole.
  '''
  pass


# Grouping content
class p(html_tag):
  '''
  The p element represents a paragraph.
  '''
  pass


class hr(html_tag):
  '''
  The hr element represents a paragraph-level thematic break, e.g. a scene
  change in a story, or a transition to another topic within a section of a
  reference book.
  '''
  is_single = True


class pre(html_tag):
  '''
  The pre element represents a block of preformatted text, in which structure
  is represented by typographic conventions rather than by elements.
  '''
  is_pretty = False


class blockquote(html_tag):
  '''
  The blockquote element represents a section that is quoted from another
  source.
  '''
  pass


class ol(html_tag):
  '''
  The ol element represents a list of items, where the items have been
  intentionally ordered, such that changing the order would change the
  meaning of the document.
  '''
  pass


class ul(html_tag):
  '''
  The ul element represents a list of items, where the order of the items is
  not important - that is, where changing the order would not materially change
  the meaning of the document.
  '''
  pass


class li(html_tag):
  '''
  The li element represents a list item. If its parent element is an ol, ul, or
  menu element, then the element is an item of the parent element's list, as
  defined for those elements. Otherwise, the list item has no defined
  list-related relationship to any other li element.
  '''
  pass


class dl(html_tag):
  '''
  The dl element represents an association list consisting of zero or more
  name-value groups (a description list). Each group must consist of one or
  more names (dt elements) followed by one or more values (dd elements).
  Within a single dl element, there should not be more than one dt element for
  each name.
  '''
  pass


class dt(html_tag):
  '''
  The dt element represents the term, or name, part of a term-description group
  in a description list (dl element).
  '''
  pass


class dd(html_tag):
  '''
  The dd element represents the description, definition, or value, part of a
  term-description group in a description list (dl element).
  '''
  pass


class figure(html_tag):
  '''
  The figure element represents some flow content, optionally with a caption,
  that is self-contained and is typically referenced as a single unit from the
  main flow of the document.
  '''
  pass


class figcaption(html_tag):
  '''
  The figcaption element represents a caption or legend for the rest of the
  contents of the figcaption element's parent figure element, if any.
  '''
  pass


class div(html_tag):
  '''
  The div element has no special meaning at all. It represents its children. It
  can be used with the class, lang, and title attributes to mark up semantics
  common to a group of consecutive elements.
  '''
  pass


# Text semantics
class a(html_tag):
  '''
  If the a element has an href attribute, then it represents a hyperlink (a
  hypertext anchor).

  If the a element has no href attribute, then the element represents a
  placeholder for where a link might otherwise have been placed, if it had been
  relevant.
  '''
  pass


class em(html_tag):
  '''
  The em element represents stress emphasis of its contents.
  '''
  pass


class strong(html_tag):
  '''
  The strong element represents strong importance for its contents.
  '''
  pass


class small(html_tag):
  '''
  The small element represents side comments such as small print.
  '''
  pass


class s(html_tag):
  '''
  The s element represents contents that are no longer accurate or no longer
  relevant.
  '''
  pass


class cite(html_tag):
  '''
  The cite element represents the title of a work (e.g. a book, a paper, an
  essay, a poem, a score, a song, a script, a film, a TV show, a game, a
  sculpture, a painting, a theatre production, a play, an opera, a musical, an
  exhibition, a legal case report, etc). This can be a work that is being
  quoted or referenced in detail (i.e. a citation), or it can just be a work
  that is mentioned in passing.
  '''
  pass


class q(html_tag):
  '''
  The q element represents some phrasing content quoted from another source.
  '''
  pass


class dfn(html_tag):
  '''
  The dfn element represents the defining instance of a term. The paragraph,
  description list group, or section that is the nearest ancestor of the dfn
  element must also contain the definition(s) for the term given by the dfn
  element.
  '''
  pass


class abbr(html_tag):
  '''
  The abbr element represents an abbreviation or acronym, optionally with its
  expansion. The title attribute may be used to provide an expansion of the
  abbreviation. The attribute, if specified, must contain an expansion of the
  abbreviation, and nothing else.
  '''
  pass


class time_(html_tag):
  '''
  The time element represents either a time on a 24 hour clock, or a precise
  date in the proleptic Gregorian calendar, optionally with a time and a
  time-zone offset.
  '''
  pass
_time = time_


class code(html_tag):
  '''
  The code element represents a fragment of computer code. This could be an XML
  element name, a filename, a computer program, or any other string that a
  computer would recognize.
  '''
  pass


class var(html_tag):
  '''
  The var element represents a variable. This could be an actual variable in a
  mathematical expression or programming context, an identifier representing a
  constant, a function parameter, or just be a term used as a placeholder in
  prose.
  '''
  pass


class samp(html_tag):
  '''
  The samp element represents (sample) output from a program or computing
  system.
  '''
  pass


class kbd(html_tag):
  '''
  The kbd element represents user input (typically keyboard input, although it
  may also be used to represent other input, such as voice commands).
  '''
  pass


class sub(html_tag):
  '''
  The sub element represents a subscript.
  '''
  pass


class sup(html_tag):
  is_inline = True
  '''
  The sup element represents a superscript.
  '''
  pass


class i(html_tag):
  is_inline = True
  '''
  The i element represents a span of text in an alternate voice or mood, or
  otherwise offset from the normal prose in a manner indicating a different
  quality of text, such as a taxonomic designation, a technical term, an
  idiomatic phrase from another language, a thought, or a ship name in Western
  texts.
  '''
  pass


class b(html_tag):
  '''
  The b element represents a span of text to which attention is being drawn for
  utilitarian purposes without conveying any extra importance and with no
  implication of an alternate voice or mood, such as key words in a document
  abstract, product names in a review, actionable words in interactive
  text-driven software, or an article lede.
  '''
  pass


class u(html_tag):
  '''
  The u element represents a span of text with an unarticulated, though
  explicitly rendered, non-textual annotation, such as labeling the text as
  being a proper name in Chinese text (a Chinese proper name mark), or
  labeling the text as being misspelt.
  '''
  pass


class mark(html_tag):
  '''
  The mark element represents a run of text in one document marked or
  highlighted for reference purposes, due to its relevance in another context.
  When used in a quotation or other block of text referred to from the prose,
  it indicates a highlight that was not originally present but which has been
  added to bring the reader's attention to a part of the text that might not
  have been considered important by the original author when the block was
  originally written, but which is now under previously unexpected scrutiny.
  When used in the main prose of a document, it indicates a part of the
  document that has been highlighted due to its likely relevance to the user's
  current activity.
  '''
  pass


class ruby(html_tag):
  '''
  The ruby element allows one or more spans of phrasing content to be marked
  with ruby annotations. Ruby annotations are short runs of text presented
  alongside base text, primarily used in East Asian typography as a guide for
  pronunciation or to include other annotations. In Japanese, this form of
  typography is also known as furigana.
  '''
  pass


class rt(html_tag):
  '''
  The rt element marks the ruby text component of a ruby annotation.
  '''
  pass


class rp(html_tag):
  '''
  The rp element can be used to provide parentheses around a ruby text
  component of a ruby annotation, to be shown by user agents that don't support
  ruby annotations.
  '''
  pass


class bdi(html_tag):
  '''
  The bdi element represents a span of text that is to be isolated from its
  surroundings for the purposes of bidirectional text formatting.
  '''
  pass


class bdo(html_tag):
  '''
  The bdo element represents explicit text directionality formatting control
  for its children. It allows authors to override the Unicode bidirectional
  algorithm by explicitly specifying a direction override.
  '''
  pass


class span(html_tag):
  '''
  The span element doesn't mean anything on its own, but can be useful when
  used together with the global attributes, e.g. class, lang, or dir. It
  represents its children.
  '''
  pass


class br(html_tag):
  '''
  The br element represents a line break.
  '''
  is_single = True
  is_inline = True


class wbr(html_tag):
  '''
  The wbr element represents a line break opportunity.
  '''
  is_single = True
  is_inline = True


# Edits
class ins(html_tag):
  '''
  The ins element represents an addition to the document.
  '''
  pass


class del_(html_tag):
  '''
  The del element represents a removal from the document.
  '''
  pass
_del = del_

# Embedded content
class img(html_tag):
  '''
  An img element represents an image.
  '''
  is_single = True


class iframe(html_tag):
  '''
  The iframe element represents a nested browsing context.
  '''
  pass


class embed(html_tag):
  '''
  The embed element represents an integration point for an external (typically
  non-HTML) application or interactive content.
  '''
  is_single = True


class object_(html_tag):
  '''
  The object element can represent an external resource, which, depending on
  the type of the resource, will either be treated as an image, as a nested
  browsing context, or as an external resource to be processed by a plugin.
  '''
  pass
_object = object_


class param(html_tag):
  '''
  The param element defines parameters for plugins invoked by object elements.
  It does not represent anything on its own.
  '''
  is_single = True


class video(html_tag):
  '''
  A video element is used for playing videos or movies, and audio files with
  captions.
  '''
  pass


class audio(html_tag):
  '''
  An audio element represents a sound or audio stream.
  '''
  pass


class source(html_tag):
  '''
  The source element allows authors to specify multiple alternative media
  resources for media elements. It does not represent anything on its own.
  '''
  is_single = True


class track(html_tag):
  '''
  The track element allows authors to specify explicit external timed text
  tracks for media elements. It does not represent anything on its own.
  '''
  is_single = True


class canvas(html_tag):
  '''
  The canvas element provides scripts with a resolution-dependent bitmap
  canvas, which can be used for rendering graphs, game graphics, or other
  visual images on the fly.
  '''
  pass


class map_(html_tag):
  '''
  The map element, in conjunction with any area element descendants, defines an
  image map. The element represents its children.
  '''
  pass
_map = map_

class area(html_tag):
  '''
  The area element represents either a hyperlink with some text and a
  corresponding area on an image map, or a dead area on an image map.
  '''
  is_single = True


# Tabular data
class table(html_tag):
  '''
  The table element represents data with more than one dimension, in the form
  of a table.
  '''
  pass


class caption(html_tag):
  '''
  The caption element represents the title of the table that is its parent, if
  it has a parent and that is a table element.
  '''
  pass


class colgroup(html_tag):
  '''
  The colgroup element represents a group of one or more columns in the table
  that is its parent, if it has a parent and that is a table element.
  '''
  pass


class col(html_tag):
  '''
  If a col element has a parent and that is a colgroup element that itself has
  a parent that is a table element, then the col element represents one or more
  columns in the column group represented by that colgroup.
  '''
  is_single = True


class tbody(html_tag):
  '''
  The tbody element represents a block of rows that consist of a body of data
  for the parent table element, if the tbody element has a parent and it is a
  table.
  '''
  pass


class thead(html_tag):
  '''
  The thead element represents the block of rows that consist of the column
  labels (headers) for the parent table element, if the thead element has a
  parent and it is a table.
  '''
  pass


class tfoot(html_tag):
  '''
  The tfoot element represents the block of rows that consist of the column
  summaries (footers) for the parent table element, if the tfoot element has a
  parent and it is a table.
  '''
  pass


class tr(html_tag):
  '''
  The tr element represents a row of cells in a table.
  '''
  pass


class td(html_tag):
  '''
  The td element represents a data cell in a table.
  '''
  pass


class th(html_tag):
  '''
  The th element represents a header cell in a table.
  '''
  pass


# Forms
class form(html_tag):
  '''
  The form element represents a collection of form-associated elements, some of
  which can represent editable values that can be submitted to a server for
  processing.
  '''
  pass


class fieldset(html_tag):
  '''
  The fieldset element represents a set of form controls optionally grouped
  under a common name.
  '''
  pass


class legend(html_tag):
  '''
  The legend element represents a caption for the rest of the contents of the
  legend element's parent fieldset element, if any.
  '''
  pass


class label(html_tag):
  '''
  The label represents a caption in a user interface. The caption can be
  associated with a specific form control, known as the label element's labeled
  control, either using for attribute, or by putting the form control inside
  the label element itself.
  '''
  pass


class input_(html_tag):
  '''
  The input element represents a typed data field, usually with a form control
  to allow the user to edit the data.
  '''
  is_single = True
_input = input_


class button(html_tag):
  '''
  The button element represents a button. If the element is not disabled, then
  the user agent should allow the user to activate the button.
  '''
  pass


class select(html_tag):
  '''
  The select element represents a control for selecting amongst a set of
  options.
  '''
  pass


class datalist(html_tag):
  '''
  The datalist element represents a set of option elements that represent
  predefined options for other controls. The contents of the element represents
  fallback content for legacy user agents, intermixed with option elements that
  represent the predefined options. In the rendering, the datalist element
  represents nothing and it, along with its children, should be hidden.
  '''
  pass


class optgroup(html_tag):
  '''
  The optgroup element represents a group of option elements with a common
  label.
  '''
  pass


class option(html_tag):
  '''
  The option element represents an option in a select element or as part of a
  list of suggestions in a datalist element.
  '''
  pass


class textarea(html_tag):
  '''
  The textarea element represents a multiline plain text edit control for the
  element's raw value. The contents of the control represent the control's
  default value.
  '''
  pass


class keygen(html_tag):
  '''
  The keygen element represents a key pair generator control. When the
  control's form is submitted, the private key is stored in the local keystore,
  and the public key is packaged and sent to the server.
  '''
  is_single = True


class output(html_tag):
  '''
  The output element represents the result of a calculation.
  '''
  pass


class progress(html_tag):
  '''
  The progress element represents the completion progress of a task. The
  progress is either indeterminate, indicating that progress is being made but
  that it is not clear how much more work remains to be done before the task is
  complete (e.g. because the task is waiting for a remote host to respond), or
  the progress is a number in the range zero to a maximum, giving the fraction
  of work that has so far been completed.
  '''
  pass


class meter(html_tag):
  '''
  The meter element represents a scalar measurement within a known range, or a
  fractional value; for example disk usage, the relevance of a query result, or
  the fraction of a voting population to have selected a particular candidate.
  '''
  pass


# Interactive elements
class details(html_tag):
  '''
  The details element represents a disclosure widget from which the user can
  obtain additional information or controls.
  '''
  pass


class summary(html_tag):
  '''
  The summary element represents a summary, caption, or legend for the rest of
  the contents of the summary element's parent details element, if any.
  '''
  pass


class command(html_tag):
  '''
  The command element represents a command that the user can invoke.
  '''
  is_single = True


class menu(html_tag):
  '''
  The menu element represents a list of commands.
  '''
  pass


class font(html_tag):
  '''
  The font element represents the font in a html .
  '''
  pass


class dialog(html_tag):
  '''
  The <dialog> HTML element represents a modal or non-modal dialog box or other 
  interactive component, such as a dismissible alert, inspector, or subwindow.
  '''
  pass


class picture(html_tag):
  '''
  Contains zero or more <source> elements and one <img> element to offer alternative 
  versions of an image for different display/device scenarios.
  '''
  pass


class search(html_tag):
  '''
  Represents a part that contains a set of form controls or other content related to 
  performing a search or filtering operation.
  '''
  pass


class slot(html_tag):
  '''
  Part of the Web Components technology suite, this element is a placeholder inside a 
  web component that you can fill with your own markup, which lets you create separate 
  DOM trees and present them together.
  '''
  pass


class small(html_tag):
  '''
  Represents side-comments and small print, like copyright and legal text, independent 
  of its styled presentation. By default, it renders text within it one font size 
  smaller, such as from small to x-small.
  '''
  pass


class template(html_tag):
  '''
  A mechanism for holding HTML that is not to be rendered immediately when a page is 
  loaded but may be instantiated subsequently during runtime using JavaScript.
  '''
  pass


# Additional markup
class comment(html_tag):
  '''
  Normal, one-line comment:
    >>> print comment("Hello, comments!")
    <!--Hello, comments!-->

  For IE's "if" statement comments:
    >>> print comment(p("Upgrade your browser."), condition='lt IE6')
    <!--[if lt IE6]><p>Upgrade your browser.</p><![endif]-->

  Downlevel conditional comments:
    >>> print comment(p("You are using a ", em("downlevel"), " browser."),
            condition='false', downlevel='revealed')
    <![if false]><p>You are using a <em>downlevel</em> browser.</p><![endif]>

  For more on conditional comments see:
    http://msdn.microsoft.com/en-us/library/ms537512(VS.85).aspx
  '''

  ATTRIBUTE_CONDITION = 'condition'

  # Valid values are 'hidden', 'downlevel' or 'revealed'
  ATTRIBUTE_DOWNLEVEL = 'downlevel'

  def _render(self, sb, indent_level=1, indent_str='  ', pretty=True, xhtml=False):
    has_condition = comment.ATTRIBUTE_CONDITION in self.attributes
    is_revealed   = comment.ATTRIBUTE_DOWNLEVEL in self.attributes and \
        self.attributes[comment.ATTRIBUTE_DOWNLEVEL] == 'revealed'

    sb.append('<!')
    if not is_revealed:
      sb.append('--')
    if has_condition:
      sb.append('[if %s]>' % self.attributes[comment.ATTRIBUTE_CONDITION])

    pretty = self._render_children(sb, indent_level - 1, indent_str, pretty, xhtml)

    # if len(self.children) > 1:
    if any(isinstance(child, dom_tag) for child in self):
      sb.append('\n')
      sb.append(indent_str * (indent_level - 1))

    if has_condition:
      sb.append('<![endif]')
    if not is_revealed:
      sb.append('--')
    sb.append('>')

    return sb
