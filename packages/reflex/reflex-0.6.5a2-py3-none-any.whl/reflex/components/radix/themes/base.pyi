"""Stub file for reflex/components/radix/themes/base.py"""

# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------
from typing import Any, Dict, Literal, Optional, Union, overload

from reflex.components import Component
from reflex.components.core.breakpoints import Breakpoints
from reflex.event import BASE_STATE, EventType
from reflex.style import Style
from reflex.utils.imports import ImportDict
from reflex.vars.base import Var

LiteralAlign = Literal["start", "center", "end", "baseline", "stretch"]
LiteralJustify = Literal["start", "center", "end", "between"]
LiteralSpacing = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
LiteralVariant = Literal["classic", "solid", "soft", "surface", "outline", "ghost"]
LiteralAppearance = Literal["inherit", "light", "dark"]
LiteralGrayColor = Literal["gray", "mauve", "slate", "sage", "olive", "sand", "auto"]
LiteralPanelBackground = Literal["solid", "translucent"]
LiteralRadius = Literal["none", "small", "medium", "large", "full"]
LiteralScaling = Literal["90%", "95%", "100%", "105%", "110%"]
LiteralAccentColor = Literal[
    "tomato",
    "red",
    "ruby",
    "crimson",
    "pink",
    "plum",
    "purple",
    "violet",
    "iris",
    "indigo",
    "blue",
    "cyan",
    "teal",
    "jade",
    "green",
    "grass",
    "brown",
    "orange",
    "sky",
    "mint",
    "lime",
    "yellow",
    "amber",
    "gold",
    "bronze",
    "gray",
]

class CommonMarginProps(Component):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        m: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        mx: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        my: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        mt: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        mr: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        mb: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
        ml: Optional[
            Union[
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]],
            ]
        ] = None,
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
    ) -> "CommonMarginProps":
        """Create the component.

        Args:
            *children: The children of the component.
            m: Margin: "0" - "9"
            mx: Margin horizontal: "0" - "9"
            my: Margin vertical: "0" - "9"
            mt: Margin top: "0" - "9"
            mr: Margin right: "0" - "9"
            mb: Margin bottom: "0" - "9"
            ml: Margin left: "0" - "9"
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the component.

        Returns:
            The component.
        """
        ...

class CommonPaddingProps(Component):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        p: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
        px: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
        py: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
        pt: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
        pr: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
        pb: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
        pl: Optional[
            Union[
                Breakpoints[
                    str, Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                ],
                Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                Var[
                    Union[
                        Breakpoints[
                            str,
                            Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        ],
                        Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    ]
                ],
            ]
        ] = None,
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
    ) -> "CommonPaddingProps":
        """Create the component.

        Args:
            *children: The children of the component.
            p: Padding: "0" - "9"
            px: Padding horizontal: "0" - "9"
            py: Padding vertical: "0" - "9"
            pt: Padding top: "0" - "9"
            pr: Padding right: "0" - "9"
            pb: Padding bottom: "0" - "9"
            pl: Padding left: "0" - "9"
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the component.

        Returns:
            The component.
        """
        ...

class RadixLoadingProp(Component):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        loading: Optional[Union[Var[bool], bool]] = None,
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
    ) -> "RadixLoadingProp":
        """Create the component.

        Args:
            *children: The children of the component.
            loading: If set, show an rx.spinner instead of the component children.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the component.

        Returns:
            The component.
        """
        ...

class RadixThemesComponent(Component):
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
    ) -> "RadixThemesComponent":
        """Create a new component instance.

        Will prepend "RadixThemes" to the component tag to avoid conflicts with
        other UI libraries for common names, like Text and Button.

        Args:
            *children: Child components.
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

class RadixThemesTriggerComponent(RadixThemesComponent):
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
    ) -> "RadixThemesTriggerComponent":
        """Create a new RadixThemesTriggerComponent instance.

        Args:
            children: The children of the component.
            props: The properties of the component.

        Returns:
            The new RadixThemesTriggerComponent instance.
        """
        ...

class Theme(RadixThemesComponent):
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        color_mode: Optional[Literal["dark", "inherit", "light"]] = None,
        theme_panel: Optional[bool] = False,
        has_background: Optional[Union[Var[bool], bool]] = None,
        appearance: Optional[
            Union[
                Literal["dark", "inherit", "light"],
                Var[Literal["dark", "inherit", "light"]],
            ]
        ] = None,
        accent_color: Optional[
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
        gray_color: Optional[
            Union[
                Literal["auto", "gray", "mauve", "olive", "sage", "sand", "slate"],
                Var[Literal["auto", "gray", "mauve", "olive", "sage", "sand", "slate"]],
            ]
        ] = None,
        panel_background: Optional[
            Union[Literal["solid", "translucent"], Var[Literal["solid", "translucent"]]]
        ] = None,
        radius: Optional[
            Union[
                Literal["full", "large", "medium", "none", "small"],
                Var[Literal["full", "large", "medium", "none", "small"]],
            ]
        ] = None,
        scaling: Optional[
            Union[
                Literal["100%", "105%", "110%", "90%", "95%"],
                Var[Literal["100%", "105%", "110%", "90%", "95%"]],
            ]
        ] = None,
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
    ) -> "Theme":
        """Create a new Radix Theme specification.

        Args:
            *children: Child components.
            color_mode: Map to appearance prop.
            theme_panel: Whether to include a panel for editing the theme.
            has_background: Whether to apply the themes background color to the theme node. Defaults to True.
            appearance: Override light or dark mode theme: "inherit" | "light" | "dark". Defaults to "inherit".
            accent_color: The color used for default buttons, typography, backgrounds, etc
            gray_color: The shade of gray, defaults to "auto".
            panel_background: Whether panel backgrounds are translucent: "solid" | "translucent" (default)
            radius: Element border radius: "none" | "small" | "medium" | "large" | "full". Defaults to "medium".
            scaling: Scale of all theme items: "90%" | "95%" | "100%" | "105%" | "110%". Defaults to "100%"
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

    def add_imports(self) -> ImportDict | list[ImportDict]: ...

class ThemePanel(RadixThemesComponent):
    def add_imports(self) -> dict[str, str]: ...
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        default_open: Optional[Union[Var[bool], bool]] = None,
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
    ) -> "ThemePanel":
        """Create a new component instance.

        Will prepend "RadixThemes" to the component tag to avoid conflicts with
        other UI libraries for common names, like Text and Button.

        Args:
            *children: Child components.
            default_open: Whether the panel is open. Defaults to False.
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

class RadixThemesColorModeProvider(Component):
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
    ) -> "RadixThemesColorModeProvider":
        """Create the component.

        Args:
            *children: The children of the component.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the component.

        Returns:
            The component.
        """
        ...

theme = Theme.create
theme_panel = ThemePanel.create
