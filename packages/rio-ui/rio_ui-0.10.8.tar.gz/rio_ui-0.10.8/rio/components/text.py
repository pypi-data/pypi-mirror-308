from __future__ import annotations

import typing as t
from dataclasses import KW_ONLY

from uniserde import JsonDoc

import rio

from .. import deprecations
from .fundamental_component import FundamentalComponent

__all__ = [
    "Text",
]


@t.final
class Text(FundamentalComponent):
    """
    Displays unformatted text.

    `Text` displays text without any formatting, making it one of the most
    commonly used components in Rio.

    While the text itself is unformatted, you can still control the style of
    the text using the `style` attribute. This allows you to change the font
    size, color, and more.


    ## Attributes

    `text`: The text to display.

    `selectable`: Whether the text can be selected by the user.

    `style`: The style of the text. This can either be a `TextStyle` instance,
        or one of the built-in styles: `"heading1"`, `"heading2"`, `"heading3"`,
        `"text"` or `"dim"`.

    `justify`: Controls the alignment of the text within each individual line.

    `overflow`: What to do with long text. If this is `"nowrap"`, the text will
        be as wide as it needs to be to fit without wrapping. If `"wrap"`, the
        text will wrap to the next line when running out of horizontal space.
        Finally, if `"ellipsize"`, the text will be truncated when there isn't
        enough space and an ellipsis (`...`) will be added.


    ## Examples

    Here's a minimal example for displaying text. Just pass it a string:

    ```python
    rio.Text("Hello, world!")
    ```

    To change the style of the text, you can pass a `TextStyle` instance:

    ```python
    rio.Text(
        "Hello, world!",
        style=rio.TextStyle(
            font_size=3,
            # Text Style has a lot of optional parameters. Have a look at its
            # docs for all details!
            #
            # https://rio.dev/docs/api/textstyle
        ),
    )
    ```
    """

    text: str
    _: KW_ONLY
    selectable: bool = True
    style: (
        t.Literal["heading1", "heading2", "heading3", "text", "dim"]
        | rio.TextStyle
    ) = "text"
    justify: t.Literal["left", "right", "center", "justify"] = "left"
    wrap: bool | t.Literal["ellipsize"] = False
    overflow: t.Literal["nowrap", "wrap", "ellipsize"] = "nowrap"

    def _custom_serialize_(self) -> JsonDoc:
        # Serialization doesn't handle unions. Hence the custom serialization
        # here
        if isinstance(self.style, str):
            style = self.style
        else:
            style = self.style._serialize(self.session)

        # The old `wrap` attribute has been replaced with `overflow`. Remap the
        # value.
        if self.wrap is not False:
            deprecations.warn_parameter_renamed(
                since="0.10",
                old_name="wrap",
                new_name="overflow",
                owner="rio.Text",
            )

        if self.wrap is True:
            overflow = "wrap"
        elif self.wrap == "ellipsize":
            overflow = "ellipsize"
        else:
            overflow = self.overflow

        # Build the result
        return {
            "style": style,
            "overflow": overflow,
        }

    def __repr__(self) -> str:
        if len(self.text) > 40:
            text = self.text[:40] + "..."
        else:
            text = self.text

        return f"<{type(self).__name__} id:{self._id} text:{text!r}>"


Text._unique_id_ = "Text-builtin"
