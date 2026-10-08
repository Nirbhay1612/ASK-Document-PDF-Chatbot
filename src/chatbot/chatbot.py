
"""
RAG chatbot implementation for Ask Document AI.

This module handles document retrieval, prompt construction,
LLM interaction, and final response generation.
"""

from typing import Any

from pydantic import SecretStr
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    TOP_K,
)

from src.chatbot.prompts import SYSTEM_PROMPT
from src.chatbot.response_handler import build_final_response


class DocumentChatbot:
    """
    RAG-based chatbot for answering questions
    using information retrieved from documents.
    """

    def __init__(
        self,
        vectorstore: Any,
        top_k: int = TOP_K,
    ) -> None:

        # --------------------------------------------------
        # Validate vector store
        # --------------------------------------------------

        if vectorstore is None:
            raise ValueError(
                "Vector store cannot be None."
            )

        # --------------------------------------------------
        # Validate retrieval configuration
        # --------------------------------------------------

        if top_k < 1:
            raise ValueError(
                "top_k must be greater than or equal to 1."
            )

        self.vectorstore = vectorstore
        self.top_k = top_k

        # --------------------------------------------------
        # Validate Groq API key
        # --------------------------------------------------

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. "
                "Please add it to your .env file."
            )

        # --------------------------------------------------
        # Initialize LLM
        # --------------------------------------------------

        try:
            self.llm = ChatGroq(
                api_key=SecretStr(GROQ_API_KEY),
                model=GROQ_MODEL,
                temperature=0,
            )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to initialize Groq LLM: {exc}"
            ) from exc

        # --------------------------------------------------
        # Initialize retriever
        # --------------------------------------------------

        try:
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": self.top_k,
                },
            )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to initialize document retriever: {exc}"
            ) from exc

        # --------------------------------------------------
        # Create RAG prompt
        # --------------------------------------------------

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                (
                    "human",
                    """
Context:
{context}

Question:
{question}

Answer:
""",
                ),
            ]
        )

    # ======================================================
    # Document Retrieval
    # ======================================================

    def retrieve_documents(
        self,
        question: str,
    ) -> list[Document]:
        """
        Retrieve the most relevant document chunks.

        Args:
            question:
                User's question.

        Returns:
            Relevant document chunks.
        """

        question = question.strip()

        if not question:
            return []

        try:
            documents = self.retriever.invoke(
                question
            )

            return documents

        except Exception as exc:
            raise RuntimeError(
                f"Failed to retrieve relevant documents: {exc}"
            ) from exc

    # ======================================================
    # Context Building
    # ======================================================

    @staticmethod
    def build_context(
        documents: list[Document],
    ) -> str:
        """
        Combine retrieved document chunks into context
        for the language model.

        Args:
            documents:
                Retrieved document chunks.

        Returns:
            Formatted context string.
        """

        if not documents:
            return ""

        context_parts: list[str] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            content = document.page_content.strip()

            if not content:
                continue

            context_parts.append(
                f"[Document Chunk {index}]\n"
                f"{content}"
            )

        return "\n\n".join(context_parts)

    # ======================================================
    # Generate Answer
    # ======================================================

    def ask(
        self,
        question: str,
    ) -> str:
        """
        Generate an answer using retrieved document context.

        Args:
            question:
                User's question.

        Returns:
            Final chatbot response.

        Raises:
            RuntimeError:
                If retrieval or LLM generation fails.
        """

        question = question.strip()

        if not question:
            return "Please enter a question."

        try:

            # ------------------------------------------------
            # Retrieve relevant chunks
            # ------------------------------------------------

            documents = self.retrieve_documents(
                question
            )

            if not documents:
                return (
                    "I couldn't find relevant information "
                    "in the uploaded document."
                )

            # ------------------------------------------------
            # Build context
            # ------------------------------------------------

            context = self.build_context(
                documents
            )

            if not context:
                return (
                    "I couldn't find readable information "
                    "in the relevant document sections."
                )

            # ------------------------------------------------
            # Build prompt
            # ------------------------------------------------

            messages = self.prompt.format_messages(
                context=context,
                question=question,
            )

            # ------------------------------------------------
            # Generate response
            # ------------------------------------------------

            response = self.llm.invoke(
                messages
            )

            # ------------------------------------------------
            # Format final response
            # ------------------------------------------------

            return build_final_response(
                response=response,
                documents=documents,
            )

        except Exception as exc:
            raise RuntimeError(
                f"Failed to generate chatbot response: {exc}"
            ) from exc


# ============================================================
# Factory Function
# ============================================================

def create_chatbot(
    vectorstore: Any,
    top_k: int = TOP_K,
) -> DocumentChatbot:
    """
    Create and return a configured DocumentChatbot.

    Args:
        vectorstore:
            FAISS vector store containing document embeddings.

        top_k:
            Number of relevant chunks to retrieve.

    Returns:
        Configured DocumentChatbot instance.
    """

    return DocumentChatbot(
        vectorstore=vectorstore,
        top_k=top_k,
    )
