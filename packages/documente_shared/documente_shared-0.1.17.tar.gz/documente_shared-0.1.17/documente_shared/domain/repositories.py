from abc import ABC, abstractmethod

from documente_shared.domain.entities import DocumentProcess
from python_layer.python.typing_extensions import Optional


class DocumentProcessRepository(ABC):

    @abstractmethod
    def find(self, digest: str) ->Optional[DocumentProcess]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, instance: DocumentProcess) -> DocumentProcess:
        raise NotImplementedError

    @abstractmethod
    def remove(self, instance: DocumentProcess):
        raise NotImplementedError