import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List
import numpy as np
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import asyncio
import os
from langchain_google_community import GoogleSearchAPIWrapper
from langsmith import traceable
from dotenv import load_dotenv