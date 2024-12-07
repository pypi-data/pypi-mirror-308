from langchain_community.document_loaders import (
    PyPDFLoader,
    PyPDFDirectoryLoader,
    CSVLoader,
    YoutubeLoader,
    RecursiveUrlLoader,
    SeleniumURLLoader
)
from langchain_core.documents import Document
from typing import Iterator, Optional


class PyPDFLoader_:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.docs = None

    def load(self) -> Iterator[Document]:
        """Load documents from a PDF file."""
        self.docs = PyPDFLoader(self.file_path).load()
        return self.docs


class PyPDFDirectory_:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.docs = None

    def load(self) -> Iterator[Document]:
        """Load documents from a directory containing PDF files."""
        self.docs = PyPDFDirectoryLoader(self.file_path).load()
        return self.docs


class CSVLoader_:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.docs = None

    def load(self) -> Iterator[Document]:
        """Load documents from a CSV file."""
        self.docs = CSVLoader(self.file_path).load()
        return self.docs


class YoutubeLoader_:
    def __init__(self, video_link: str):
        self.video_link = video_link
        self.docs = None

    def load(self) -> Iterator[Document]:
        """Load documents from a YouTube video."""
        self.docs = YoutubeLoader.from_youtube_url(self.video_link, add_video_info=False).load()
        return self.docs


class RecursiveUrlLoader_:
    def __init__(self, web_link: str, max_depth: int = 1):
        if max_depth <= 0:
            raise ValueError('max_depth must be greater than 0')
        self.web_link = web_link
        self.max_depth = max_depth
        self.docs = None

    def load(self) -> Iterator[Document]:
        """Load documents from a URL recursively."""
        self.docs = RecursiveUrlLoader(
            self.web_link,
            max_depth=self.max_depth,
        ).load()
        return self.docs


class SeleniumURLLoader_:
    def __init__(self, web_link: str):
        self.web_link = web_link
        self.docs = None

    def load(self) -> Iterator[Document]:
        """Load documents from a URL using Selenium."""
        self.docs = SeleniumURLLoader(urls=[self.web_link]).load()
        return self.docs
