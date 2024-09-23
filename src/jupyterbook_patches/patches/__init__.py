from abc import ABC, abstractmethod

from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)


class BasePatch(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def initialize(self, app: Sphinx) -> None:
        ...
