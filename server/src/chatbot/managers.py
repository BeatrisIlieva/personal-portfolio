import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


class ComponentManager:
    """Singleton-like manager for initializing and accessing shared components."""
    _instance = None
    _vectorstore = None
    _llm = None

    _workflow = None
    _memory = None
    _app = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()

        return cls._instance

    def _initialize(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "docs", "product_catalog.pdf")

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=540,
            chunk_overlap=0,
            separators=["\n\n", ". ", "!", '\n']
        )

        chunks = text_splitter.split_documents(pages)

        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

        self._vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=None
        )

        self._llm = ChatOpenAI(
            model="gpt-4o-mini",
            max_tokens=120,
            temperature=0,
            top_p=0,
            frequency_penalty=1.0,
            presence_penalty=1.0,
            streaming=True,
        )

        self._memory = MemorySaver()

        self._workflow = StateGraph(state_schema=MessagesState)
        self._workflow.add_edge(START, "model")
        self._workflow.add_node("model", self._call_model)
        self._app = self.workflow.compile(checkpointer=self.memory)

    def _call_model(self, state: MessagesState):
        response = self._llm.invoke(state["messages"])
        return {"messages": response}

    @property
    def vectorstore(self):
        return self._vectorstore

    @property
    def llm(self):
        return self._llm

    @property
    def memory(self):
        return self._memory

    @property
    def workflow(self):
        return self._workflow

    @property
    def memory(self):
        return self._memory

    @property
    def app(self):
        return self._app
