from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


class Label:
    """
    Génère un fichier JSON représentant un label.

    La structure produite contient :
        - un Stage (avec width / height)
        - un Layer
          - une Image de fond (base64, width, height)
          - N éléments Text (text, fontSize, fontFamily, fill, …)
          - un Rect optionnel (composant QrCode, etc.)

    Utilisation :
        label = Label(width=1153, height=1600)

        # Image de fond
        label.add_background("data:image/png;base64,iVBOR…")

        # Ajouter des textes
        label.add_text("{{country}}", y=60, font_size=40)
        label.add_text("{{region}}",  y=77, font_size=40)

        # Modifier globalement la police / couleur de tous les textes
        label.set_font("Arial", size=36, fill="red")

        # Ajouter un QrCode
        label.add_qrcode(x=190, y=285, width=90, height=90)

        # Exporter
        label.save("output.json")

        # Charger un fichier existant
        label = Label.from_file("template.json")
    """

    # ------------------------------------------------------------------ #
    #  Construction                                                       #
    # ------------------------------------------------------------------ #

    def __init__(
        self,
        width: int,
        height: int,
        base64: str,
        font_family: str = "Trebuchet MS",
        font_size: int = 40,
        fill: str = "black",
    ):
        self._width = width
        self._height = height
        self._base64 = base64
        self._font_family = font_family
        self._font_size = font_size
        self._fill = fill
        self._texts: list[dict[str, Any]] = []
        self._components: list[dict[str, Any]] = []

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
        self._base64 = base64

    def add_text(
        self,
        text: str,
        width: int,
        y: int = 0,
        x: int | None = None,
        font_size: int | None = None,
        font_family: str | None = None,
        fill: str | None = None,
        **extra_attrs: Any,
    ) -> None:
        attrs: dict[str, Any] = {
            "y": y,
            "width": width,
            "text": text,
            "fontSize": font_size or self._font_size,
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

    # ------------------------------------------------------------------ #
    #  Export                                                              #
    # ------------------------------------------------------------------ #

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

        # Composants (QrCode, …)
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

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, path: str | Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    
