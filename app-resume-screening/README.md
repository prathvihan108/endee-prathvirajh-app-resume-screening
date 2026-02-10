# AI Resume Screening System

This project is a high-performance resume screening tool built during my internship. It leverages the Endee Labs Vector Engine as a local database service to store and search candidate resumes using semantic AI embeddings..

---

<div align="center">
  <h3>🎥 Brief Demo</h3>
  <video 
    src="https://github.com/user-attachments/assets/2054a014-49a3-415e-8369-d3d7b1a5f447" 
    poster="https://github.com/user-attachments/assets/76e640b0-342b-4cfb-8e21-0a8400681880" 
    width="100%" 
    style="max-width: 600px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" 
    controls 
    muted>
    <p>Your browser does not support HTML5 video.</p>
  </video>
  <br />
  <p><em>Semantic Search & Batch Ingestion powered by Endee Engine</em></p>
</div>

---

## 🚀 Overview

**Resume-Screening AI** is a full-stack, vector-native recruitment platform designed to solve a fundamental problem in modern talent acquisition:

> Keywords describe history — vectors describe capability..

Traditional hiring tools rely on manual filtering and exact string matching. Resume-Screening AI provides:

- **Semantic Talent Discovery:** Identifying candidates based on the conceptual meaning of their skills.
- **Privacy-Preserving Ingestion:** Intelligent redaction of sensitive PII (Personally Identifiable Information) during the parsing phase.
- **High-Density Vector Storage:** Leveraging the Endee Engine for efficient, sub-millisecond candidate retrieval.
- **Batch Intelligence:** Processing entire departments of resumes simultaneously to build a searchable talent pool.

---

## 🎯 Problem Statement

Recruiters are currently trapped in a "Keyword Arms Race" where:

- **Talent is Overlooked:** Qualified candidates are rejected simply because their resume uses "Golang" while the search used "Go."

- **Data Bloat:** Storing unencrypted, unredacted PDFs in searchable databases creates significant privacy and compliance liabilities.

- **Fragmented Analysis:** Resumes are treated as isolated documents rather than a connected network of skills and experiences.

-**Navigate information intuitively:** Standard search engines find words — Resume-Screening AI finds the right person.

---

## 💡 Solution

**Resume-Screening AI** creates a vector-native intelligence layer over the hiring pipeline, transforming static documents into searchable semantic profiles.

### Workflow

1️⃣ **Intelligent Ingestion:** Batch upload of multi-format resumes via FastAPI

2️⃣ **Heuristic Extraction:** Segmenting raw PDF data into structured Skill and Experience blocks

3️⃣ **CSemantic Embedding:** Transforming candidate profiles into 384-dimensional vectors using transformer-based models.

4️⃣ **Endee Integration:** Storing vectors with int8d precision for optimized local performance

5️⃣ **Contextual Search:** Ranking candidates using cosine similarity to map job descriptions to the talent pool

6️⃣ **Database Lifecycle Management:** Full administrative control for re-indexing and clearing the vector space.

Result: A lean, high-speed recruitment engine that prioritizes skill context over keyword frequency.

---

## 🧰 Technology Stack

### Frontend

- **React 18** Modern UI library using Functional Components and Hooks.

- **Vite** - Next-generation frontend tooling for optimized development.

- **Tailwind CSS** - Utility-first styling for a clean, responsive "Recruiter Dashboard.

- **Axios** - Promise-based HTTP client for seamless communication with the FastAPI gateway.

- **Lucide React** - Icons

---

### Backend

- **FastAPI** - Powering your asynchronous API endpoints (/upload-batch, /search, /stats).

- **Python-3** - Running within your endee_venv on Ubuntu

- **Sentence-Transformers** - Embedding generation (all-MiniLM-L6-v2, 384 dims)

- **Requests** - Used for the check_health and get_version calls to the Dockerized engine.

- **UUID** - For generating unique identifiers to prevent candidate ID collisions in the vector space.

- **Dotenv** - Managing your HF_TOKEN and environment variables securely.

- **PyPDF2** - PDF parsing

---

### Vector Database

### Endee

- High-performance C++ vector database
- HNSW algorithm for approximate nearest neighbor search
- Sub-10ms query latency
- Cosine similarity metric
- Batch vector insertion

Used for:

- Embedding storage
- Semantic retrieval
- Relationship discovery

---

## 🏗️ Project Architecture

The system follows a modular architecture that prioritizes data privacy and local high-speed vector search.

- **`endee`**: The core Vector Database (C++ engine) used for local storage of semantic embeddings.
  **app-resume-screening/:**: The custom application layer. It handles PDF text extraction, AI embedding generation (NLP), and provides a REST API for the frontend.

  ```
  .
  ├── backend
  │   ├── core
  │   │   ├── embedder.py
  │   │   ├── parser.py
  │   │   └── __pycache__
  │   │       ├── embedder.cpython-310.pyc
  │   │       └── parser.cpython-310.pyc
  │   ├── main.py
  │   ├── processor.py
  │   ├── __pycache__
  │   │   └── main.cpython-310.pyc
  │   └── services
  │       ├── endee_client.py
  │       └── __pycache__
  │           └── endee_client.cpython-310.pyc
  ├── frontend
  │   ├── eslint.config.js
  │   ├── index.html
  │   ├── package.json
  │   ├── package-lock.json
  │   ├── public
  │   │   └── vite.svg
  │   ├── README.md
  │   ├── src
  │   │   ├── App.css
  │   │   ├── App.jsx
  │   │   ├── assets
  │   │   │   └── react.svg
  │   │   ├── components
  │   │   │   ├── CandidateCard.jsx
  │   │   │   ├── DatabaseStats.jsx
  │   │   │   ├── FileUpload.jsx
  │   │   │   └── SearchBar.jsx
  │   │   ├── index.css
  │   │   ├── main.jsx
  │   │   ├── pages
  │   │   │   └── Dashboard.jsx
  │   │   └── services
  │   │       └── api.js
  │   └── vite.config.js
  ├── README.md
  ├── requirements.txt
  └── structure.txt


  ```

---

## 🚀 Setup & Installation

### 1. Workspace Initialization

Clone your forked repository which contains both the Endee core and the internship project..

Using HTTP:

```
git clone https://github.com/prathvihan108/endee-prathvirajh-app-resume-screening.git
```

Using SSH:

```
git clone git@github.com:prathvihan108/endee-prathvirajh-app-resume-screening.git
```

### 2. Set up Endee Vector DB

Change dir

```
cd endee

```

**Start Endee**

```
docker compose up -d
```

**Verify the Server is Running**

```
docker ps

```

You should see a container named endee-server

### 3. Setting Up the Application

We use a Python Virtual Environment (endee_venv) to manage dependencies for the FastAPI backend located in the internship folder.

Step 1: Create the Virtual Environment This isolates your project libraries from the system-wide Python installation.

```
python3 -m venv endee_venv
```

Step 2: Activate the Environment

```
source venv/bin/activate
```

Step 3: Install Project Requirements

```
pip install -r app-resume-screening/requirements.txt
```

**Configure Environment Variables**
Create the .env file:

```
cd app-resume-screening
touch .env
```

Add your Hugging Face token to the file. Open it with your preferred editor and insert the following line:

```
HF_TOKEN="your_hugging_face_token_here"
```

How to Obtain Your Hugging Face Token
Follow these brief steps to generate your access key:

1.  Login: Sign in to your account at huggingface.co.

2.  Settings: Click your profile icon in the top-right corner and select Settings.

3.  Access Tokens: Select Access Tokens from the left-side navigation menu.

4.  Generate: Click New token, provide a name, and select the Read role

5.  Copy: Copy the token and paste it into the .env file you created.

### 4. Running the Application

Step 1: Activate the Environment from the root(i.e endee)

```
source endee_venv/bin/activate
```

Step 2: Ensure your Hugging Face Token is set in .env file we created in /internship-project-harshitha

Step 3: Start the server on port 8000

Note:virtual Environment(HG_venv) should be active while u run the "uvicorn" command or app

```
cd iapp-resume-screening
uvicorn backend.main:app --reload --port 8000
```

Verification: Open http://localhost:8000/docs. If you see the Swagger UI, your backend is alive and ready.

Step 4: Start the Vite Frontend(Terminal 2)

```
#Open new terminal
# Navitage to the frontend directory(/prathvirajh-app-resume-screening/app-resume-screening/frontend)

# Install dependencies
npm install

# Start the Vite development server
npm run dev

```
