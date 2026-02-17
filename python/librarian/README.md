# Librarian 📚

Librarian is an intelligent agent developed to automatically organize digital PDF libraries (books). It analyzes the file content and distributes them into "shelves" (folders) based on AI-identified categories.

## 🚀 How It Works

The agent's workflow is divided into three main stages, optimized for low cost and high precision:

1. **Smart Sampling:** The system extracts only the first 15 to 20 pages of the PDF. This ensures enough context (prefaces, tables of contents, and introductions) while saving processing tokens.
2. **Agent Processing (LLM):** In this stage, the Agent analyzes the sample to:
    * **Classification:** Defines the ideal "shelf" (destination folder).
    * **Summary:** Generates a concise summary of the content.
    * **Indexing:** Creates strategic tags to facilitate future retrieval via RAG (Retrieval-Augmented Generation).
    * *Note: For security reasons, the agent does not have direct write permissions (MCP/Tools) to the file system.*
3. **Organization:** The file is physically moved to the folder corresponding to the defined category.

## 🛠️ Tech Stack

* **Language:** Python
* **Agent Framework:** Agno (formerly Phidata)
* **Environment:** Windows

## 🚧 Project Status

This project is currently **Work in Progress (WIP)**.
Upcoming implementations include improvements in metadata extraction and refinement of classification prompts.