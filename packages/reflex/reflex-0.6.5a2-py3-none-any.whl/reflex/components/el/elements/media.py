"""Element classes. This is an auto-generated file. Do not edit. See ../generate.py."""

from typing import Any, Union

from reflex import Component, ComponentNamespace
from reflex.constants.colors import Color
from reflex.vars.base import Var

from .base import BaseHTML


class Area(BaseHTML):
    """Display the area element."""

    tag = "area"

    # Alternate text for the area, used for accessibility
    alt: Var[Union[str, int, bool]]

    # Coordinates to define the shape of the area
    coords: Var[Union[str, int, bool]]

    # Specifies that the target will be downloaded when clicked
    download: Var[Union[str, int, bool]]

    # Hyperlink reference for the area
    href: Var[Union[str, int, bool]]

    # Language of the linked resource
    href_lang: Var[Union[str, int, bool]]

    # Specifies what media/device the linked resource is optimized for
    media: Var[Union[str, int, bool]]

    # A list of URLs to be notified if the user follows the hyperlink
    ping: Var[Union[str, int, bool]]

    # Specifies which referrer information to send with the link
    referrer_policy: Var[Union[str, int, bool]]

    # Specifies the relationship of the target object to the link object
    rel: Var[Union[str, int, bool]]

    # Defines the shape of the area (rectangle, circle, polygon)
    shape: Var[Union[str, int, bool]]

    # Specifies where to open the linked document
    target: Var[Union[str, int, bool]]


class Audio(BaseHTML):
    """Display the audio element."""

    tag = "audio"

    # Specifies that the audio will start playing as soon as it is ready
    auto_play: Var[Union[str, int, bool]]

    # Represents the time range of the buffered media
    buffered: Var[Union[str, int, bool]]

    # Displays the standard audio controls
    controls: Var[Union[str, int, bool]]

    # Configures the CORS requests for the element
    cross_origin: Var[Union[str, int, bool]]

    # Specifies that the audio will loop
    loop: Var[Union[str, int, bool]]

    # Indicates whether the audio is muted by default
    muted: Var[Union[str, int, bool]]

    # Specifies how the audio file should be preloaded
    preload: Var[Union[str, int, bool]]

    # URL of the audio to play
    src: Var[Union[str, int, bool]]


class Img(BaseHTML):
    """Display the img element."""

    tag = "img"

    # Image alignment with respect to its surrounding elements
    align: Var[Union[str, int, bool]]

    # Alternative text for the image
    alt: Var[Union[str, int, bool]]

    # Configures the CORS requests for the image
    cross_origin: Var[Union[str, int, bool]]

    # How the image should be decoded
    decoding: Var[Union[str, int, bool]]

    # Specifies an intrinsic size for the image
    intrinsicsize: Var[Union[str, int, bool]]

    # Whether the image is a server-side image map
    ismap: Var[Union[str, int, bool]]

    # Specifies the loading behavior of the image
    loading: Var[Union[str, int, bool]]

    # Referrer policy for the image
    referrer_policy: Var[Union[str, int, bool]]

    # Sizes of the image for different layouts
    sizes: Var[Union[str, int, bool]]

    # URL of the image to display
    src: Var[Any]

    # A set of source sizes and URLs for responsive images
    src_set: Var[Union[str, int, bool]]

    # The name of the map to use with the image
    use_map: Var[Union[str, int, bool]]

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Override create method to apply source attribute to value if user fails to pass in attribute.

        Args:
            *children: The children of the component.
            **props: The props of the component.

        Returns:
            The component.

        """
        return (
            super().create(src=children[0], **props)
            if children
            else super().create(*children, **props)
        )


class Map(BaseHTML):
    """Display the map element."""

    tag = "map"

    # Name of the map, referenced by the 'usemap' attribute in 'img' and 'object' elements
    name: Var[Union[str, int, bool]]


class Track(BaseHTML):
    """Display the track element."""

    tag = "track"

    # Indicates that the track should be enabled unless the user's preferences indicate otherwise
    default: Var[Union[str, int, bool]]

    # Specifies the kind of text track
    kind: Var[Union[str, int, bool]]

    # Title of the text track, used by the browser when listing available text tracks
    label: Var[Union[str, int, bool]]

    # URL of the track file
    src: Var[Union[str, int, bool]]

    # Language of the track text data
    src_lang: Var[Union[str, int, bool]]


class Video(BaseHTML):
    """Display the video element."""

    tag = "video"

    # Specifies that the video will start playing as soon as it is ready
    auto_play: Var[Union[str, int, bool]]

    # Represents the time range of the buffered media
    buffered: Var[Union[str, int, bool]]

    # Displays the standard video controls
    controls: Var[Union[str, int, bool]]

    # Configures the CORS requests for the video
    cross_origin: Var[Union[str, int, bool]]

    # Specifies that the video will loop
    loop: Var[Union[str, int, bool]]

    # Indicates whether the video is muted by default
    muted: Var[Union[str, int, bool]]

    # Indicates that the video should play 'inline', inside its element's playback area
    plays_inline: Var[Union[str, int, bool]]

    # URL of an image to show while the video is downloading, or until the user hits the play button
    poster: Var[Union[str, int, bool]]

    # Specifies how the video file should be preloaded
    preload: Var[Union[str, int, bool]]

    # URL of the video to play
    src: Var[Union[str, int, bool]]


class Embed(BaseHTML):
    """Display the embed element."""

    tag = "embed"

    # URL of the embedded content
    src: Var[Union[str, int, bool]]

    # Media type of the embedded content
    type: Var[Union[str, int, bool]]


class Iframe(BaseHTML):
    """Display the iframe element."""

    tag = "iframe"

    # Alignment of the iframe within the page or surrounding elements
    align: Var[Union[str, int, bool]]

    # Permissions policy for the iframe
    allow: Var[Union[str, int, bool]]

    # Content Security Policy to apply to the iframe's content
    csp: Var[Union[str, int, bool]]

    # Specifies the loading behavior of the iframe
    loading: Var[Union[str, int, bool]]

    # Name of the iframe, used as a target for hyperlinks and forms
    name: Var[Union[str, int, bool]]

    # Referrer policy for the iframe
    referrer_policy: Var[Union[str, int, bool]]

    # Security restrictions for the content in the iframe
    sandbox: Var[Union[str, int, bool]]

    # URL of the document to display in the iframe
    src: Var[Union[str, int, bool]]

    # HTML content to embed directly within the iframe
    src_doc: Var[Union[str, int, bool]]


class Object(BaseHTML):
    """Display the object element."""

    tag = "object"

    # URL of the data to be used by the object
    data: Var[Union[str, int, bool]]

    # Associates the object with a form element
    form: Var[Union[str, int, bool]]

    # Name of the object, used for scripting or as a target for forms and links
    name: Var[Union[str, int, bool]]

    # Media type of the data specified in the data attribute
    type: Var[Union[str, int, bool]]

    # Name of an image map to use with the object
    use_map: Var[Union[str, int, bool]]


class Picture(BaseHTML):
    """Display the picture element."""

    tag = "picture"
    # No unique attributes, only common ones are inherited


class Portal(BaseHTML):
    """Display the portal element."""

    tag = "portal"
    # No unique attributes, only common ones are inherited


class Source(BaseHTML):
    """Display the source element."""

    tag = "source"

    # Media query indicating what device the linked resource is optimized for
    media: Var[Union[str, int, bool]]

    # Sizes of the source for different layouts
    sizes: Var[Union[str, int, bool]]

    # URL of the media file or an image for the element to use
    src: Var[Union[str, int, bool]]

    # A set of source sizes and URLs for responsive images
    src_set: Var[Union[str, int, bool]]

    # Media type of the source
    type: Var[Union[str, int, bool]]


class Svg(BaseHTML):
    """Display the svg element."""

    tag = "svg"
    # The width of the svg.
    width: Var[Union[str, int]]
    # The height of the svg.
    height: Var[Union[str, int]]
    # The XML namespace declaration.
    xmlns: Var[str]


class Text(BaseHTML):
    """The SVG text component."""

    tag = "text"
    # The x coordinate of the starting point of the text baseline.
    x: Var[Union[str, int]]
    # The y coordinate of the starting point of the text baseline.
    y: Var[Union[str, int]]
    # Shifts the text position horizontally from a previous text element.
    dx: Var[Union[str, int]]
    # Shifts the text position vertically from a previous text element.
    dy: Var[Union[str, int]]
    # Rotates orientation of each individual glyph.
    rotate: Var[Union[str, int]]
    # How the text is stretched or compressed to fit the width defined by the text_length attribute.
    length_adjust: Var[str]
    # A width that the text should be scaled to fit.
    text_length: Var[Union[str, int]]


class Line(BaseHTML):
    """The SVG line component."""

    tag = "line"
    # The x-axis coordinate of the line starting point.
    x1: Var[Union[str, int]]
    # The x-axis coordinate of the the line ending point.
    x2: Var[Union[str, int]]
    # The y-axis coordinate of the line starting point.
    y1: Var[Union[str, int]]
    # The y-axis coordinate of the the line ending point.
    y2: Var[Union[str, int]]
    # The total path length, in user units.
    path_length: Var[int]


class Circle(BaseHTML):
    """The SVG circle component."""

    tag = "circle"
    # The x-axis coordinate of the center of the circle.
    cx: Var[Union[str, int]]
    # The y-axis coordinate of the center of the circle.
    cy: Var[Union[str, int]]
    # The radius of the circle.
    r: Var[Union[str, int]]
    # The total length for the circle's circumference, in user units.
    path_length: Var[int]


class Ellipse(BaseHTML):
    """The SVG ellipse component."""

    tag = "ellipse"
    # The x position of the center of the ellipse.
    cx: Var[Union[str, int]]
    # The y position of the center of the ellipse.
    cy: Var[Union[str, int]]
    # The radius of the ellipse on the x axis.
    rx: Var[Union[str, int]]
    # The radius of the ellipse on the y axis.
    ry: Var[Union[str, int]]
    # The total length for the ellipse's circumference, in user units.
    path_length: Var[int]


class Rect(BaseHTML):
    """The SVG rect component."""

    tag = "rect"
    # The x coordinate of the rect.
    x: Var[Union[str, int]]
    # The y coordinate of the rect.
    y: Var[Union[str, int]]
    # The width of the rect
    width: Var[Union[str, int]]
    # The height of the rect.
    height: Var[Union[str, int]]
    # The horizontal corner radius of the rect. Defaults to ry if it is specified.
    rx: Var[Union[str, int]]
    # The vertical corner radius of the rect. Defaults to rx if it is specified.
    ry: Var[Union[str, int]]
    # The total length of the rectangle's perimeter, in user units.
    path_length: Var[int]


class Polygon(BaseHTML):
    """The SVG polygon component."""

    tag = "polygon"
    # defines the list of points (pairs of x,y absolute coordinates) required to draw the polygon.
    points: Var[str]
    # This prop lets specify the total length for the path, in user units.
    path_length: Var[int]


class Defs(BaseHTML):
    """Display the defs element."""

    tag = "defs"


class LinearGradient(BaseHTML):
    """Display the linearGradient element."""

    tag = "linearGradient"

    # Units for the gradient.
    gradient_units: Var[Union[str, bool]]

    # Transform applied to the gradient.
    gradient_transform: Var[Union[str, bool]]

    # Method used to spread the gradient.
    spread_method: Var[Union[str, bool]]

    # X coordinate of the starting point of the gradient.
    x1: Var[Union[str, int, bool]]

    # X coordinate of the ending point of the gradient.
    x2: Var[Union[str, int, bool]]

    # Y coordinate of the starting point of the gradient.
    y1: Var[Union[str, int, bool]]

    # Y coordinate of the ending point of the gradient.
    y2: Var[Union[str, int, bool]]


class RadialGradient(BaseHTML):
    """Display the radialGradient element."""

    tag = "radialGradient"

    # The x coordinate of the end circle of the radial gradient.
    cx: Var[Union[str, int, bool]]

    # The y coordinate of the end circle of the radial gradient.
    cy: Var[Union[str, int, bool]]

    # The radius of the start circle of the radial gradient.
    fr: Var[Union[str, int, bool]]

    # The x coordinate of the start circle of the radial gradient.
    fx: Var[Union[str, int, bool]]

    # The y coordinate of the start circle of the radial gradient.
    fy: Var[Union[str, int, bool]]

    # Units for the gradient.
    gradient_units: Var[Union[str, bool]]

    # Transform applied to the gradient.
    gradient_transform: Var[Union[str, bool]]

    # The radius of the end circle of the radial gradient.
    r: Var[Union[str, int, bool]]

    # Method used to spread the gradient.
    spread_method: Var[Union[str, bool]]


class Stop(BaseHTML):
    """Display the stop element."""

    tag = "stop"

    # Offset of the gradient stop.
    offset: Var[Union[str, float, int]]

    # Color of the gradient stop.
    stop_color: Var[Union[str, Color, bool]]

    # Opacity of the gradient stop.
    stop_opacity: Var[Union[str, float, int, bool]]


class Path(BaseHTML):
    """Display the path element."""

    tag = "path"

    # Defines the shape of the path.
    d: Var[Union[str, int, bool]]


class SVG(ComponentNamespace):
    """SVG component namespace."""

    text = staticmethod(Text.create)
    line = staticmethod(Line.create)
    circle = staticmethod(Circle.create)
    ellipse = staticmethod(Ellipse.create)
    rect = staticmethod(Rect.create)
    polygon = staticmethod(Polygon.create)
    path = staticmethod(Path.create)
    stop = staticmethod(Stop.create)
    linear_gradient = staticmethod(LinearGradient.create)
    radial_gradient = staticmethod(RadialGradient.create)
    defs = staticmethod(Defs.create)
    __call__ = staticmethod(Svg.create)


area = Area.create
audio = Audio.create
image = img = Img.create
map = Map.create
track = Track.create
video = Video.create
embed = Embed.create
iframe = Iframe.create
object = Object.create
picture = Picture.create
portal = Portal.create
source = Source.create
svg = SVG()
