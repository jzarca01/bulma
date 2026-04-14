from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


class Label:
    def __init__(
        self,
        width: int,
        height: int,
        fill: str = "black",
    ):
        self._width = width
        self._height = height
        self._fill = fill
        self._font_size = 40
        self._font_family = "Trebuchet MS"
        self._texts: list[dict[str, Any]] = []
        self._images: list[dict[str, Any]] = []
        self._components: list[dict[str, Any]] = []
        self.valid_components = ['background', 'country', 'region', 'beanName', 'process', 'variety', 'flavors', 'date']


    def __repr__(self) -> str:
        return (
            f"Label(width={self._width}, height={self._height}, "
            f"texts={len(self._texts)}, components={len(self._components)})"
        )

    @classmethod
    def from_file(cls, path: str | Path) -> Label:
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def width(self, value: int) -> None:
        self._width = value

    def height(self, value: int) -> None:
        self._height = value

    def add_background(self, base64: str) -> None:
        self._base64 = f"data:image/png;base64,{base64}"

    def add_image(
        self,
        width: int,
        height: int,
        base64: str,
        y: int = 0,
        x: int | None = None,
        **extra_attrs: Any,
    ) -> None:
        attrs: dict[str, Any] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "base64": f"data:image/png;base64,{base64}",
            "scaleX": 1,
            "scaleY": 1,
        }
        if x is not None:
            attrs["x"] = x
        attrs.update(extra_attrs)
        self._images.append(attrs)

    def add_text(
        self,
        text: str,
        width: int,
        y: int = 0,
        x: int | None = None,
        font_size: float | None = None,
        font_family: str | None = None,
        fill: str | None = None,
        **extra_attrs: Any,
    ) -> None:
        attrs: dict[str, Any] = {
            "y": y,
            "width": width,
            "text": text,
            "fontSize": str(font_size or self._font_size),
            "fontFamily": font_family or self._font_family,
            "fill": fill or self._fill,
        }
        if x is not None:
            attrs["x"] = x
        attrs.update(extra_attrs)
        self._texts.append(attrs)

    def add_qrcode(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 90,
        height: int = 90,
        stroke: str = "black",
        dash: list[int] | None = None,
    ) -> None:
        self._components.append({
            "attrs": {
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "stroke": stroke,
                "dash": dash or [4, 2],
                "component": "QrCode",
            },
            "className": "Rect",
        })

    def to_dict(self) -> dict[str, Any]:
        children: list[dict[str, Any]] = []

        # Image de fond
        children.append({
            "attrs": {
                "x": 0,
                "y": 0,
                "width": self._width,
                "height": self._height,
                "base64": self._base64,
                "scaleX": 1,
                "scaleY": 1,
            },
            "className": "Image",
        })

        # Textes
        for t in self._texts:
            children.append({"attrs": dict(t), "className": "Text"})

        for t in self._images:
            children.append({"attrs": dict(t), "className": "Image"})

        children.extend(deepcopy(self._components))

        return {
            "attrs": {"width": self._width, "height": self._height},
            "className": "Stage",
            "children": [
                {
                    "attrs": {"x": 0, "y": 0},
                    "className": "Layer",
                    "children": children,
                }
            ],
        }

    def save(self, path: str | Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    
