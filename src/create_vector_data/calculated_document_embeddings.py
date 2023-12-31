import chromadb
import sentence_transformers
import os

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import Docx2txtLoader
# from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

core_working_directory = r"C:\Users\Alex\Google Drive\projects\llama2_retrieval_augmented_generation"
document_data_dir_path = os.path.join(core_working_directory, "data", "documents")

# Note that the name is in the convention for huggingface.co and this model is apache 2.0 licensed.
reference_models_directory = r"F:\reference_models"
embedding_model_name_used = "hkunlp/instructor-xl"
embedding_model_path = os.path.join(reference_models_directory, "embedding_models", "instructor-xl")

# Somewhat arbitrary but shouldn't be too large to avoid hitting issues with context window size on various LLMs
# without using context window extension methods, llama2 should have a 2048ish token context window
# Therefore want to keep chunks small enough that a few chunks of context can be added to a prompt.
n_size_in_doc_chunk = 512
n_size_in_chunk_overlap = 32

# Setup document loaders and text splitters

# Note, below is pieced together from langchain docs here:
# https://python.langchain.com/docs/modules/data_connection/document_transformers/
# from langchain.document_loaders import DocxLoader
file_endings_considered = {"markdown": "md",
                           "html": "html",
                           "text": "txt",
                           "pdf": "pdf",
                           "word_doc": "docx"}

file_globbers = {file_type: os.path.join("**", f"*.{file_ending}")
                 for file_type, file_ending in file_endings_considered.items()}

# Build a markdown file loader
markdown_file_loader = DirectoryLoader(document_data_dir_path,
                                       glob = file_globbers['markdown'],
                                       show_progress = True,
                                       loader_cls = UnstructuredMarkdownLoader)

# Build a text file loader handling different text encodings
text_loader_kwargs= {'autodetect_encoding': True}
text_file_loader = DirectoryLoader(document_data_dir_path,
                                   glob = file_globbers['text'],
                                   show_progress = True,
                                   loader_cls = TextLoader,
                                   loader_kwargs=text_loader_kwargs)

# Build a html file loader handling different text encodings
html_file_loader = DirectoryLoader(document_data_dir_path,
                                   glob = file_globbers['html'],
                                   show_progress = True,
                                   loader_cls = UnstructuredHTMLLoader)

# Build a pdf file loader
pdf_file_loader = DirectoryLoader(document_data_dir_path,
                                  glob = file_globbers['pdf'],
                                  show_progress = True,
                                  loader_cls = PyMuPDFLoader)

# Build docx file loader
docx_file_loader = DirectoryLoader(document_data_dir_path,
                                  glob = file_globbers['word_doc'],
                                  show_progress = True,
                                  loader_cls = Docx2txtLoader)

# We also defined our text splitters here for each use-case
default_text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = n_size_in_doc_chunk,
    chunk_overlap = n_size_in_chunk_overlap,
    length_function = len,
    is_separator_regex = False,
)

# Load in the necessary files
loaded_markdown_files = markdown_file_loader.load()
loaded_text_files = text_file_loader.load()
loaded_html_files = html_file_loader.load()
loaded_pdf_files = pdf_file_loader.load()
loaded_docx_files = docx_file_loader.load()

# Text chunking is built together from langchain documentation here:
# https://python.langchain.com/docs/modules/data_connection/document_transformers/
markdown_file_chunks = default_text_splitter.split_documents(loaded_markdown_files)
text_file_chunks = default_text_splitter.split_documents(loaded_text_files)
html_file_chunks = default_text_splitter.split_documents(loaded_html_files)
pdf_file_chunks = default_text_splitter.split_documents(loaded_pdf_files)
docx_file_chunks = default_text_splitter.split_documents(loaded_docx_files)