"""Stub file for reflex/components/radix/themes/layout/stack.py"""

# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------
from typing import Any, Dict, Literal, Optional, Union, overload

from reflex.components.core.breakpoints import Breakpoints
from reflex.event import BASE_STATE, EventType
from reflex.style import Style
from reflex.vars.base import Var

from .flex import Flex

class Stack(Flex):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        spacing: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        align: Optional[
            Union[
                Literal["baseline", "center", "end", "start", "stretch"],
                Var[Literal["baseline", "center", "end", "start", "stretch"]],
            ]
        ] = None,
        as_child: Optional[Union[Var[bool], bool]] = None,
        direction: Optional[
            Union[
                Breakpoints[
                    str, Literal["column", "column-reverse", "row", "row-reverse"]
                ],
                Literal["column", "column-reverse", "row", "row-reverse"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["column", "column-reverse", "row", "row-reverse"],
                        ],
                        Literal["column", "column-reverse", "row", "row-reverse"],
                    ]
                ],
            ]
        ] = None,
        justify: Optional[
            Union[
                Breakpoints[str, Literal["between", "center", "end", "start"]],
                Literal["between", "center", "end", "start"],
                Var[
                    Union[
                        Breakpoints[str, Literal["between", "center", "end", "start"]],
                        Literal["between", "center", "end", "start"],
                    ]
                ],
            ]
        ] = None,
        wrap: Optional[
            Union[
                Breakpoints[str, Literal["nowrap", "wrap", "wrap-reverse"]],
                Literal["nowrap", "wrap", "wrap-reverse"],
                Var[
                    Union[
                        Breakpoints[str, Literal["nowrap", "wrap", "wrap-reverse"]],
                        Literal["nowrap", "wrap", "wrap-reverse"],
                    ]
                ],
            ]
        ] = None,
        access_key: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        auto_capitalize: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        content_editable: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        context_menu: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        dir: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        draggable: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        enter_key_hint: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        hidden: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        input_mode: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        item_prop: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        lang: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        role: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        slot: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        spell_check: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        tab_index: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        title: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, Any]]] = None,
        on_blur: Optional[EventType[[], BASE_STATE]] = None,
        on_click: Optional[EventType[[], BASE_STATE]] = None,
        on_context_menu: Optional[EventType[[], BASE_STATE]] = None,
        on_double_click: Optional[EventType[[], BASE_STATE]] = None,
        on_focus: Optional[EventType[[], BASE_STATE]] = None,
        on_mount: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_down: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_enter: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_leave: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_move: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_out: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_over: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_up: Optional[EventType[[], BASE_STATE]] = None,
        on_scroll: Optional[EventType[[], BASE_STATE]] = None,
        on_unmount: Optional[EventType[[], BASE_STATE]] = None,
        **props,
    ) -> "Stack":
        """Create a new instance of the component.

        Args:
            *children: The children of the stack.
            spacing: Gap between children: "0" - "9"
            align: Alignment of children along the main axis: "start" | "center" | "end" | "baseline" | "stretch"
            as_child: Change the default rendered element for the one passed as a child, merging their props and behavior.
            direction: How child items are layed out: "row" | "column" | "row-reverse" | "column-reverse"
            justify: Alignment of children along the cross axis: "start" | "center" | "end" | "between"
            wrap: Whether children should wrap when they reach the end of their container: "nowrap" | "wrap" | "wrap-reverse"
            access_key:  Provides a hint for generating a keyboard shortcut for the current element.
            auto_capitalize: Controls whether and how text input is automatically capitalized as it is entered/edited by the user.
            content_editable: Indicates whether the element's content is editable.
            context_menu: Defines the ID of a <menu> element which will serve as the element's context menu.
            dir: Defines the text direction. Allowed values are ltr (Left-To-Right) or rtl (Right-To-Left)
            draggable: Defines whether the element can be dragged.
            enter_key_hint: Hints what media types the media element is able to play.
            hidden: Defines whether the element is hidden.
            input_mode: Defines the type of the element.
            item_prop: Defines the name of the element for metadata purposes.
            lang: Defines the language used in the element.
            role: Defines the role of the element.
            slot: Assigns a slot in a shadow DOM shadow tree to an element.
            spell_check: Defines whether the element may be checked for spelling errors.
            tab_index: Defines the position of the current element in the tabbing order.
            title: Defines a tooltip for the element.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The properties of the stack.

        Returns:
            The stack component.
        """
        ...

class VStack(Stack):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        direction: Optional[
            Union[
                Literal["column", "column-reverse", "row", "row-reverse"],
                Var[Literal["column", "column-reverse", "row", "row-reverse"]],
            ]
        ] = None,
        spacing: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        align: Optional[
            Union[
                Literal["baseline", "center", "end", "start", "stretch"],
                Var[Literal["baseline", "center", "end", "start", "stretch"]],
            ]
        ] = None,
        as_child: Optional[Union[Var[bool], bool]] = None,
        justify: Optional[
            Union[
                Breakpoints[str, Literal["between", "center", "end", "start"]],
                Literal["between", "center", "end", "start"],
                Var[
                    Union[
                        Breakpoints[str, Literal["between", "center", "end", "start"]],
                        Literal["between", "center", "end", "start"],
                    ]
                ],
            ]
        ] = None,
        wrap: Optional[
            Union[
                Breakpoints[str, Literal["nowrap", "wrap", "wrap-reverse"]],
                Literal["nowrap", "wrap", "wrap-reverse"],
                Var[
                    Union[
                        Breakpoints[str, Literal["nowrap", "wrap", "wrap-reverse"]],
                        Literal["nowrap", "wrap", "wrap-reverse"],
                    ]
                ],
            ]
        ] = None,
        access_key: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        auto_capitalize: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        content_editable: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        context_menu: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        dir: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        draggable: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        enter_key_hint: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        hidden: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        input_mode: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        item_prop: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        lang: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        role: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        slot: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        spell_check: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        tab_index: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        title: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, Any]]] = None,
        on_blur: Optional[EventType[[], BASE_STATE]] = None,
        on_click: Optional[EventType[[], BASE_STATE]] = None,
        on_context_menu: Optional[EventType[[], BASE_STATE]] = None,
        on_double_click: Optional[EventType[[], BASE_STATE]] = None,
        on_focus: Optional[EventType[[], BASE_STATE]] = None,
        on_mount: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_down: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_enter: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_leave: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_move: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_out: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_over: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_up: Optional[EventType[[], BASE_STATE]] = None,
        on_scroll: Optional[EventType[[], BASE_STATE]] = None,
        on_unmount: Optional[EventType[[], BASE_STATE]] = None,
        **props,
    ) -> "VStack":
        """Create a new instance of the component.

        Args:
            *children: The children of the stack.
            direction: How child items are layed out: "row" | "column" | "row-reverse" | "column-reverse"
            spacing: Gap between children: "0" - "9"
            align: Alignment of children along the main axis: "start" | "center" | "end" | "baseline" | "stretch"
            as_child: Change the default rendered element for the one passed as a child, merging their props and behavior.
            justify: Alignment of children along the cross axis: "start" | "center" | "end" | "between"
            wrap: Whether children should wrap when they reach the end of their container: "nowrap" | "wrap" | "wrap-reverse"
            access_key:  Provides a hint for generating a keyboard shortcut for the current element.
            auto_capitalize: Controls whether and how text input is automatically capitalized as it is entered/edited by the user.
            content_editable: Indicates whether the element's content is editable.
            context_menu: Defines the ID of a <menu> element which will serve as the element's context menu.
            dir: Defines the text direction. Allowed values are ltr (Left-To-Right) or rtl (Right-To-Left)
            draggable: Defines whether the element can be dragged.
            enter_key_hint: Hints what media types the media element is able to play.
            hidden: Defines whether the element is hidden.
            input_mode: Defines the type of the element.
            item_prop: Defines the name of the element for metadata purposes.
            lang: Defines the language used in the element.
            role: Defines the role of the element.
            slot: Assigns a slot in a shadow DOM shadow tree to an element.
            spell_check: Defines whether the element may be checked for spelling errors.
            tab_index: Defines the position of the current element in the tabbing order.
            title: Defines a tooltip for the element.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The properties of the stack.

        Returns:
            The stack component.
        """
        ...

class HStack(Stack):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        direction: Optional[
            Union[
                Literal["column", "column-reverse", "row", "row-reverse"],
                Var[Literal["column", "column-reverse", "row", "row-reverse"]],
            ]
        ] = None,
        spacing: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        align: Optional[
            Union[
                Literal["baseline", "center", "end", "start", "stretch"],
                Var[Literal["baseline", "center", "end", "start", "stretch"]],
            ]
        ] = None,
        as_child: Optional[Union[Var[bool], bool]] = None,
        justify: Optional[
            Union[
                Breakpoints[str, Literal["between", "center", "end", "start"]],
                Literal["between", "center", "end", "start"],
                Var[
                    Union[
                        Breakpoints[str, Literal["between", "center", "end", "start"]],
                        Literal["between", "center", "end", "start"],
                    ]
                ],
            ]
        ] = None,
        wrap: Optional[
            Union[
                Breakpoints[str, Literal["nowrap", "wrap", "wrap-reverse"]],
                Literal["nowrap", "wrap", "wrap-reverse"],
                Var[
                    Union[
                        Breakpoints[str, Literal["nowrap", "wrap", "wrap-reverse"]],
                        Literal["nowrap", "wrap", "wrap-reverse"],
                    ]
                ],
            ]
        ] = None,
        access_key: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        auto_capitalize: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        content_editable: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        context_menu: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        dir: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        draggable: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        enter_key_hint: Optional[
            Union[Var[Union[bool, int, str]], bool, int, str]
        ] = None,
        hidden: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        input_mode: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        item_prop: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        lang: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        role: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        slot: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        spell_check: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        tab_index: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        title: Optional[Union[Var[Union[bool, int, str]], bool, int, str]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, Any]]] = None,
        on_blur: Optional[EventType[[], BASE_STATE]] = None,
        on_click: Optional[EventType[[], BASE_STATE]] = None,
        on_context_menu: Optional[EventType[[], BASE_STATE]] = None,
        on_double_click: Optional[EventType[[], BASE_STATE]] = None,
        on_focus: Optional[EventType[[], BASE_STATE]] = None,
        on_mount: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_down: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_enter: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_leave: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_move: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_out: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_over: Optional[EventType[[], BASE_STATE]] = None,
        on_mouse_up: Optional[EventType[[], BASE_STATE]] = None,
        on_scroll: Optional[EventType[[], BASE_STATE]] = None,
        on_unmount: Optional[EventType[[], BASE_STATE]] = None,
        **props,
    ) -> "HStack":
        """Create a new instance of the component.

        Args:
            *children: The children of the stack.
            direction: How child items are layed out: "row" | "column" | "row-reverse" | "column-reverse"
            spacing: Gap between children: "0" - "9"
            align: Alignment of children along the main axis: "start" | "center" | "end" | "baseline" | "stretch"
            as_child: Change the default rendered element for the one passed as a child, merging their props and behavior.
            justify: Alignment of children along the cross axis: "start" | "center" | "end" | "between"
            wrap: Whether children should wrap when they reach the end of their container: "nowrap" | "wrap" | "wrap-reverse"
            access_key:  Provides a hint for generating a keyboard shortcut for the current element.
            auto_capitalize: Controls whether and how text input is automatically capitalized as it is entered/edited by the user.
            content_editable: Indicates whether the element's content is editable.
            context_menu: Defines the ID of a <menu> element which will serve as the element's context menu.
            dir: Defines the text direction. Allowed values are ltr (Left-To-Right) or rtl (Right-To-Left)
            draggable: Defines whether the element can be dragged.
            enter_key_hint: Hints what media types the media element is able to play.
            hidden: Defines whether the element is hidden.
            input_mode: Defines the type of the element.
            item_prop: Defines the name of the element for metadata purposes.
            lang: Defines the language used in the element.
            role: Defines the role of the element.
            slot: Assigns a slot in a shadow DOM shadow tree to an element.
            spell_check: Defines whether the element may be checked for spelling errors.
            tab_index: Defines the position of the current element in the tabbing order.
            title: Defines a tooltip for the element.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The properties of the stack.

        Returns:
            The stack component.
        """
        ...

stack = Stack.create
hstack = HStack.create
vstack = VStack.create
