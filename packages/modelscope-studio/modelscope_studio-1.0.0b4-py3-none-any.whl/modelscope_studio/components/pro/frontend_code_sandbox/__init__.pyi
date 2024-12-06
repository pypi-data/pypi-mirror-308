from __future__ import annotations

import json
from typing import Any

from gradio.events import Dependency

from ....utils.dev import ModelScopeComponent, resolve_frontend_dir

class ProFrontendCodeSandbox(ModelScopeComponent):
    """
    Frontend code sandbox is a component that use to preview code to web page.
    """

    def __init__(
            self,
            value: dict[str, dict[str, str | int]] | None = None,
            *,
            import_map: dict[str, str] | None = None,
            _internal: None = None,
            # gradio properties
            visible: bool = True,
            elem_id: str | None = None,
            elem_classes: list[str] | str | None = None,
            elem_style: dict | None = None,
            render: bool = True,
            **kwargs):
        """
        Parameters:
            value: Code to preview.
            import_map: JS import map.
        """
        super().__init__(value=value,
                         visible=visible,
                         elem_id=elem_id,
                         elem_classes=elem_classes,
                         render=render,
                         elem_style=elem_style,
                         **kwargs)
        self.import_map = import_map

    FRONTEND_DIR = resolve_frontend_dir("frontend-code-sandbox", type='pro')

    @property
    def skip_api(self):
        return True

    def preprocess(self,
                   payload: str) -> dict[str, dict[str, str | int]] | None:
        try:
            return json.loads(payload)
        except Exception:
            return None

    def postprocess(self,
                    value: dict[str, dict[str, str | int]] | None) -> str:
        if value is None:
            return ''
        return json.dumps(value)

    def example_payload(self) -> Any:
        return None

    def example_value(self) -> Any:
        return None
    from typing import TYPE_CHECKING, Any, Callable, Literal, Sequence

    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer