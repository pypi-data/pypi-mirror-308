"""Stub file for reflex/experimental/layout.py"""

# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------
from typing import Any, Dict, List, Literal, Optional, Union, overload

from reflex import color
from reflex.components.base.fragment import Fragment
from reflex.components.component import Component, ComponentNamespace, MemoizationLeaf
from reflex.components.radix.primitives.drawer import DrawerRoot
from reflex.components.radix.themes.layout.box import Box
from reflex.event import BASE_STATE, EventType
from reflex.state import ComponentState
from reflex.style import Style
from reflex.vars.base import Var

class Sidebar(Box, MemoizationLeaf):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
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
    ) -> "Sidebar":
        """Create the sidebar component.

        Args:
            children: The children components.
            props: The properties of the sidebar.

        Returns:
            The sidebar component.
        """
        ...

    def add_style(self) -> dict[str, Any] | None: ...
    def add_hooks(self) -> List[Var]: ...

class StatefulSidebar(ComponentState):
    open: bool

    def toggle(self): ...
    @classmethod
    def get_component(cls, *children, **props): ...

class DrawerSidebar(DrawerRoot):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        default_open: Optional[Union[Var[bool], bool]] = None,
        open: Optional[Union[Var[bool], bool]] = None,
        modal: Optional[Union[Var[bool], bool]] = None,
        direction: Optional[
            Union[
                Literal["bottom", "left", "right", "top"],
                Var[Literal["bottom", "left", "right", "top"]],
            ]
        ] = None,
        dismissible: Optional[Union[Var[bool], bool]] = None,
        handle_only: Optional[Union[Var[bool], bool]] = None,
        snap_points: Optional[List[Union[float, str]]] = None,
        fade_from_index: Optional[Union[Var[int], int]] = None,
        scroll_lock_timeout: Optional[Union[Var[int], int]] = None,
        preventScrollRestoration: Optional[Union[Var[bool], bool]] = None,
        should_scale_background: Optional[Union[Var[bool], bool]] = None,
        close_threshold: Optional[Union[Var[float], float]] = None,
        as_child: Optional[Union[Var[bool], bool]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, Any]]] = None,
        on_animation_end: Optional[
            Union[EventType[[], BASE_STATE], EventType[[bool], BASE_STATE]]
        ] = None,
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
        on_open_change: Optional[
            Union[EventType[[], BASE_STATE], EventType[[bool], BASE_STATE]]
        ] = None,
        on_scroll: Optional[EventType[[], BASE_STATE]] = None,
        on_unmount: Optional[EventType[[], BASE_STATE]] = None,
        **props,
    ) -> "DrawerSidebar":
        """Create the sidebar component.

        Args:
            children: The children components.
            props: The properties of the sidebar.

        Returns:
            The drawer sidebar component.
        """
        ...

sidebar_trigger_style = {
    "position": "fixed",
    "z_index": "15",
    "color": color("accent", 12),
    "background_color": "transparent",
    "padding": "0",
}

class SidebarTrigger(Fragment):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
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
    ) -> "SidebarTrigger":
        """Create the sidebar trigger component.

        Args:
            sidebar: The sidebar component.
            props: The properties of the sidebar trigger.

        Returns:
            The sidebar trigger component.
        """
        ...

class Layout(Box):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        sidebar: Optional[Component] = None,
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
    ) -> "Layout":
        """Create the layout component.

        Args:
            content: The content component.
            sidebar: The sidebar component.
            props: The properties of the layout.

        Returns:
            The layout component.
        """
        ...

class LayoutNamespace(ComponentNamespace):
    drawer_sidebar = staticmethod(DrawerSidebar.create)
    stateful_sidebar = staticmethod(StatefulSidebar.create)
    sidebar = staticmethod(Sidebar.create)

    @staticmethod
    def __call__(
        *children,
        sidebar: Optional[Component] = None,
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
    ) -> "Layout":
        """Create the layout component.

        Args:
            content: The content component.
            sidebar: The sidebar component.
            props: The properties of the layout.

        Returns:
            The layout component.
        """
        ...

layout = LayoutNamespace()
