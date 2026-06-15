<div align="center">

# 🛡️ ScamShield AI

### Enterprise-Grade Scam Risk Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama--3.3--70B-orange)](https://groq.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-6C5CE7)](https://qdrant.tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready, multi-tenant **Retrieval-Augmented Generation (RAG)** platform for auditing SMS headers, conversational telemetry, and transactional scripts against active regulatory directives — including **TRAI**, **RBI**, and **CERT-In** compliance standards.

[Features](#-features) · [Architecture](#-architecture) · [Tech Stack](#-tech-stack) · [Getting Started](#-getting-started) · [Demo](#-demo-scenarios) · [Telemetry](#-telemetry-dashboard)

</div>

---

## Overview

ScamShield AI goes beyond a typical LLM wrapper. It is a **specialized compliance intelligence engine** built around four hard engineering constraints:

- **Zero hallucination** — every model citation is programmatically verified against the retrieved source context before output is released
- **Strict multi-tenant isolation** — cryptographic namespace enforcement prevents any cross-tenant data leakage at the vector database layer
- **Deterministic structured output** — JSON grammar constraints via logit-bias force the model to output valid, schema-bound responses with no filler text
- **Real-time infrastructure observability** — a live telemetry dashboard exposes per-component latency across the full pipeline for every inference run

---

## ✨ Features

- 🔍 **Hybrid Retrieval** — parallel dense + sparse vector search fused with Reciprocal Rank Fusion (RRF) for maximum recall
- 🏢 **Multi-Tenant Architecture** — cryptographic `tenant_id` enforcement ensures complete data isolation across organizational workspaces
- 🧠 **Cross-Encoder Reranking** — FlashRank MiniLM L-12 cross-attention reranker compacts 80%+ noise from raw retrieval candidates
- 🔒 **Grounding Audit Engine** — post-generation citation cross-check blocks any response referencing unverified or pre-training knowledge
- 📊 **Live Telemetry Dashboard** — real-time latency breakdown across Qdrant, Cross-Encoder, Groq inference, and hallucination audit stages
- 📄 **Section-Aware Document Ingestion** — state-machine markdown parser preserves structural lineage (headers, tables) across all chunk boundaries

---

## 🏗️ Architecture

```
[Threat Payload] ──► [Multi-Tenant Routing Filter]
                               │
                               ▼
              ┌────────────────────────────────┐
              │    Hybrid Parallel Search      │
              │  ├─ Dense:  BAAI/bge-small-en  │──► [Reciprocal Rank Fusion]
              │  └─ Sparse: Qdrant BM25        │
              └────────────────────────────────┘
                               │
                               ▼
                  [FlashRank Cross-Encoder]
                  Context Compaction · 80% Noise Reduction
                               │
                               ▼
              ┌────────────────────────────────┐
              │    Zero-Trust Context Firewall │──► Block cross-tenant tokens
              └────────────────────────────────┘
                               │
                               ▼
              [Groq · Llama-3.3-70B Inference]
              Logit-Bias JSON Grammar Constraints
                               │
                               ▼
              ┌────────────────────────────────┐
              │   Deterministic Grounding Audit│──► Programmatic Citation Check
              └────────────────────────────────┘
                               │
                               ▼
                 [Live Telemetry Dashboard UI]
```

### Pipeline Components

**1 · Ingestion & Section-Aware Chunking**

Documents are parsed into a continuous Markdown AST using a stateful machine that respects header tokens (`#`, `##`, `###`). Parent section headers are propagated into child chunk metadata, preventing context fragmentation. Tabular structures within regulatory documents are isolated as independent, regex-guarded context blocks — preserving their raw structure for precise clause extraction.

**2 · Multi-Tenant Hybrid Retrieval**

Queries simultaneously traverse two vector subspaces within a single secure Qdrant instance:
- **Dense:** `BAAI/bge-small-en-v1.5` for semantic alignment
- **Sparse:** `Qdrant/bm25` for strict alphanumeric clause matching (e.g., `Regulation 3(1)`)

RRF fuses both ranking planes into a single, mathematically unified candidate pool server-side. Every result is then validated against a cryptographic `tenant_id` — cross-tenant records are hard-dropped before entering the synthesis stage.

**3 · Context Compaction & Reranking**

A locally-executed `ms-marco-MiniLM-L-12-v2` cross-encoder (via FlashRank, CPU-optimized) performs deep token-to-token cross-attention scoring across all retrieval candidates. The reranker selects the top 4 hyper-relevant nodes from the full pool, cutting up to 80% of unnecessary tokens and keeping context well within the LLM's window.

**4 · Deterministic Generation & Grounding Audit**

Groq's Llama-3.3-70B is bound to a strict Pydantic schema via `json-schema` logit-bias constraints, eliminating all conversational filler from the output contract. After generation, every citation in the model's response is cross-checked programmatically against the physical source context pool. Any reference to knowledge outside the retrieved documents is flagged and blocked before reaching the UI.

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq · Llama-3.3-70B |
| Vector Database | Qdrant (Dense + Sparse Named Vectors) |
| Embeddings | BAAI/bge-small-en-v1.5 (ONNX) |
| Sparse Retrieval | Qdrant BM25 |
| Reranking | FlashRank · ms-marco-MiniLM-L-12-v2 |
| Output Validation | Pydantic · JSON Schema Logit-Bias |
| Frontend | Streamlit |
| Compliance Targets | TRAI · RBI · CERT-In |

---

## 📁 Project Structure

```
scamshield-ai-core/
│
├── requirements.txt          # Categorized platform dependencies
├── README.md
│
├── app/
│   └── streamlit_app.py      # Presentation layer & telemetry dashboard
│
├── pipeline/
│   ├── __init__.py           # Package initialization
│   ├── contracts.py          # Pydantic output schemas
│   ├── loader.py             # Document layout parser
│   ├── chunker.py            # Section-aware Markdown state-machine splitter
│   ├── embedder.py           # Dual dense/sparse ONNX embedding layer
│   ├── vectorstore.py        # Multi-tenant Qdrant client manager
│   └── retriever.py          # Parallel RRF prefetch + Cross-Encoder reranker
│
└── data/
    ├── qdrant_storage/       # Local vector DB persistence
    └── flashrank_cache/      # Quantized INT8 ONNX cross-encoder model cache
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/)
- A [Qdrant Cloud cluster](https://cloud.qdrant.io/) (or local Qdrant instance)

### 1. Clone & Install

```bash
git clone https://github.com/your-username/scamshield-ai-core.git
cd scamshield-ai-core

python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install --no-cache-dir -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_secure_high_speed_inference_token_here
QDRANT_URL=https://your-managed-cluster-id.gcp.qdrant.tech:6333
QDRANT_API_KEY=your_secure_cloud_database_token_here
```

### 3. Launch

```bash
streamlit run app/streamlit_app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Demo Scenarios

The following sequence is designed to validate the platform's core guarantees end-to-end:

**Step 1 · Ingest a Compliance Document**

Set the sidebar Workspace ID to `reliance_jio_compliance`. Upload a regulatory file (e.g., the TRAI February 2025 anti-phishing circular). Click **Execute Ingestion Loop** and observe parse latency and chunk density metrics in the telemetry panel.

**Step 2 · Run a Threat Audit**

Paste a banking phishing template from an unverified 10-digit sender header into the input box. Execute the analysis. The platform returns a `SCAM` verdict alongside extraction traces and explicit regulatory rule citations sourced from the ingested document.

**Step 3 · Verify Hallucination Interception**

Check the Hallucination Audit block in the telemetry panel. If the model attempts to reference an outdated compliance clause from its pre-training weights that does not exist in the uploaded document, the dashboard surfaces a red `FAILED` alert — demonstrating the application-layer grounding guardrail in action.

**Step 4 · Prove Tenant Isolation**

Switch the Workspace ID to `sbi_banking_analyst` and re-run the same threat payload. The system bypasses the `reliance_jio_compliance` context entirely and returns a `SAFE` verdict with `0.00` risk severity — confirming hard multi-tenant isolation at the vector index layer.

---

## 📊 Telemetry Dashboard

Every inference run exposes a full engineering-level breakdown:

| Metric | Description |
|---|---|
| **Total Pipeline Latency** | Monotonic start-to-finish processing time (ms) |
| **Qdrant Vector Engine** | Dense/sparse prefetch and RRF fusion speed |
| **Cross-Encoder Latency** | Local CPU cross-attention reranking time |
| **70B Inference Speed** | Groq token generation + JSON grammar compilation time |
| **Context Compaction** | Candidate compression ratio (e.g., `8 raw → 4 nodes`) |
| **Hallucination Audit** | Programmatic citation validation result (`PASSED` / `FAILED`) |

---

## 📄 License

Distributed under the [MIT License](LICENSE).

---

<div align="center">
Built with precision for compliance intelligence · TRAI · RBI · CERT-In
</div>
