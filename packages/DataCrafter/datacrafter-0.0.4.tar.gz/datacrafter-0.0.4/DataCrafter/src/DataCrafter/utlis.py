import re

class TextCleaner:
    """A class to clean text by removing unwanted characters and symbols."""
    
    def __init__(self):
        # Define the allowed symbols pattern
        self.allowed_symbols = r"[^a-zA-Z0-9\s\.\,\?\!\-\(\)]"
    
    def clean_text(self, text):
        """Cleans the text by removing unwanted characters and symbols."""
        text = re.sub(self.allowed_symbols, '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
