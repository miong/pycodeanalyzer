from typing import Any

import jsonpickle

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClassClassifier,
    AbstractObjectLanguage,
)


class Pickler:
    def __init__(self) -> None:
        jsonpickle.set_preferred_backend("simplejson")
        jsonpickle.set_encoder_options("simplejson", sort_keys=True, indent=4)
        jsonpickle.util.PRIMITIVES.add(AbstractObjectLanguage)
        jsonpickle.util.PRIMITIVES.add(AbstractClassClassifier)

    def encode(self, obj: Any) -> str:
        return jsonpickle.encode(obj)

    def decode(self, json: str) -> Any:
        return jsonpickle.decode(json)
