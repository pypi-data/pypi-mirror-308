from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_core.documents import Document
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)


class PyPDFLoader_:
    def __init__(
        self,
        file_path: str) -> None:
        self.file_path = file_path
            
    def load(
        self,
    ) -> Iterator[Document]:
        self.docs = PyPDFLoader(self.file_path).load()
        
        return self.docs
    

class PyPDFDirectry:
    def __init__(
        self,
        file_path: str) -> None:
        self.file_path = file_path
            
    def load(
        self,
    ) -> Iterator[Document]:
        self.docs = PyPDFDirectoryLoader(self.file_path).load()

        return self.docs