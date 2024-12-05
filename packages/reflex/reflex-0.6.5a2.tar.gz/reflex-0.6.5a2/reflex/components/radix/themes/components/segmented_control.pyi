"""Stub file for reflex/components/radix/themes/components/segmented_control.py"""

# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------
from types import SimpleNamespace
from typing import Any, Dict, List, Literal, Optional, Tuple, Union, overload

from reflex.components.core.breakpoints import Breakpoints
from reflex.event import BASE_STATE, EventType
from reflex.style import Style
from reflex.vars.base import Var

from ..base import RadixThemesComponent

def on_value_change(value: Var[str | List[str]]) -> Tuple[Var[str | List[str]]]: ...

class SegmentedControlRoot(RadixThemesComponent):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        size: Optional[
            Union[
                Breakpoints[str, Literal["1", "2", "3"]],
                Literal["1", "2", "3"],
                Var[
                    Union[
                        Breakpoints[str, Literal["1", "2", "3"]], Literal["1", "2", "3"]
                    ]
                ],
            ]
        ] = None,
        variant: Optional[
            Union[Literal["classic", "surface"], Var[Literal["classic", "surface"]]]
        ] = None,
        type: Optional[
            Union[Literal["multiple", "single"], Var[Literal["multiple", "single"]]]
        ] = None,
        color_scheme: Optional[
            Union[
                Literal[
                    "amber",
                    "blue",
                    "bronze",
                    "brown",
                    "crimson",
                    "cyan",
                    "gold",
                    "grass",
                    "gray",
                    "green",
                    "indigo",
                    "iris",
                    "jade",
                    "lime",
                    "mint",
                    "orange",
                    "pink",
                    "plum",
                    "purple",
                    "red",
                    "ruby",
                    "sky",
                    "teal",
                    "tomato",
                    "violet",
                    "yellow",
                ],
                Var[
                    Literal[
                        "amber",
                        "blue",
                        "bronze",
                        "brown",
                        "crimson",
                        "cyan",
                        "gold",
                        "grass",
                        "gray",
                        "green",
                        "indigo",
                        "iris",
                        "jade",
                        "lime",
                        "mint",
                        "orange",
                        "pink",
                        "plum",
                        "purple",
                        "red",
                        "ruby",
                        "sky",
                        "teal",
                        "tomato",
                        "violet",
                        "yellow",
                    ]
                ],
            ]
        ] = None,
        radius: Optional[
            Union[
                Literal["full", "large", "medium", "none", "small"],
                Var[Literal["full", "large", "medium", "none", "small"]],
            ]
        ] = None,
        default_value: Optional[
            Union[List[str], Var[Union[List[str], str]], str]
        ] = None,
        value: Optional[Union[List[str], Var[Union[List[str], str]], str]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[Var, Any]]] = None,
        on_blur: Optional[EventType[[], BASE_STATE]] = None,
        on_change: Optional[
            Union[EventType[[], BASE_STATE], EventType[[str | List[str]], BASE_STATE]]
        ] = None,
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
    ) -> "SegmentedControlRoot":
        """Create a new component instance.

        Will prepend "RadixThemes" to the component tag to avoid conflicts with
        other UI libraries for common names, like Text and Button.

        Args:
            *children: Child components.
            size: The size of the segmented control: "1" | "2" | "3"
            variant: Variant of button: "classic" | "surface"
            type: The type of the segmented control, either "single" for selecting one option or "multiple" for selecting multiple options.
            color_scheme: Override theme color for button
            radius: The radius of the segmented control: "none" | "small" | "medium" | "large" | "full"
            default_value: The default value of the segmented control.
            value: The current value of the segmented control.
            on_change: Handles the `onChange` event for the SegmentedControl component.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: Component properties.

        Returns:
            A new component instance.
        """
        ...

class SegmentedControlItem(RadixThemesComponent):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        value: Optional[Union[Var[str], str]] = None,
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
    ) -> "SegmentedControlItem":
        """Create a new component instance.

        Will prepend "RadixThemes" to the component tag to avoid conflicts with
        other UI libraries for common names, like Text and Button.

        Args:
            *children: Child components.
            value: The value of the item.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: Component properties.

        Returns:
            A new component instance.
        """
        ...

class SegmentedControl(SimpleNamespace):
    root = staticmethod(SegmentedControlRoot.create)
    item = staticmethod(SegmentedControlItem.create)

segmented_control = SegmentedControl()
