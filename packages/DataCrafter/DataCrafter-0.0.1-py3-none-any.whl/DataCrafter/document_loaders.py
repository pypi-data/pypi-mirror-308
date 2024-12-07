from langchain_community.document_loaders import (
    PyPDFLoader,
    PyPDFDirectoryLoader,
    CSVLoader,
    YoutubeLoader,
    RecursiveUrlLoader,
    SeleniumURLLoader
)
from langchain_core.documents import Document
from pydantic import BaseModel, Field, field_validator
from typing import Iterator, Optional


class PyPDFLoader_(BaseModel):
    file_path: str
    docs: Optional[Iterator[Document]] = None

    def load(self) -> Iterator[Document]:
        """Load documents from a PDF file."""
        self.docs = PyPDFLoader(self.file_path).load()
        return self.docs


class PyPDFDirectory_(BaseModel):
    file_path: str
    docs: Optional[Iterator[Document]] = None

    def load(self) -> Iterator[Document]:
        """Load documents from a directory containing PDF files."""
        self.docs = PyPDFDirectoryLoader(self.file_path).load()
        return self.docs


class CSVLoader_(BaseModel):
    file_path: str
    docs: Optional[Iterator[Document]] = None

    def load(self) -> Iterator[Document]:
        """Load documents from a CSV file."""
        self.docs = CSVLoader(self.file_path).load()
        return self.docs


class YoutubeLoader_(BaseModel):
    video_link: str
    docs: Optional[Iterator[Document]] = None

    def load(self) -> Iterator[Document]:
        """Load documents from a YouTube video."""
        self.docs = YoutubeLoader.from_youtube_url(self.video_link, add_video_info=False).load()
        return self.docs


class RecursiveUrlLoader_(BaseModel):
    web_link: str
    max_depth: int = Field(default=1, ge=1)  # Ensure max_depth is at least 1
    docs: Optional[Iterator[Document]] = None

    @field_validator('max_depth')
    def validate_max_depth(cls, v):
        """ """
        if v <= 0:
            raise ValueError('max_depth must be greater than 0')
        return v

    def load(self) -> Iterator[Document]:
        """Load documents from a URL recursively."""
        self.docs = RecursiveUrlLoader(
            self.web_link,
            max_depth=self.max_depth,
        ).load()
        return self.docs


class SeleniumURLLoader_(BaseModel):
    web_link: str
    docs: Optional[Iterator[Document]] = None

    def load(self) -> Iterator[Document]:
        """Load documents from a URL using Selenium."""
        self.docs = SeleniumURLLoader(urls=[self.web_link]).load()
        return self.docs


# Example usage
# if __name__ == "__main__":
#     pdf_loader = PyPDFLoader_(file_path='example.pdf')
#     pdf_docs = pdf_loader.load()
#     print(f"Loaded {len(list(pdf_docs))} documents from PDF.")

#     csv_loader = CSVLoader_(file_path='example.csv')
#     csv_docs = csv_loader.load()
#     print(f"Loaded {len(list(csv_docs))} documents from CSV.")

#     youtube_loader = YoutubeLoader_(video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
#     youtube_docs = youtube_loader.load()
#     print(f"Loaded {len(list(youtube_docs))} documents from YouTube.")

#     recursive_url_loader = RecursiveUrlLoader_(web_link='https://example.com', max_depth=2)
#     recursive_url_docs = recursive_url_loader.load()
#     print(f"Loaded {len(list(recursive_url_docs))} documents from URL recursively.")

#     selenium_url_loader = SeleniumURLLoader_(web_link='https://example.com')
#     selenium_url_docs = selenium_url_loader.load()
#     print(f"Loaded {len(list(selenium_url_docs))} documents from URL using Selenium.")