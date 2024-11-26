graph TD
    %% Define subgraphs for clarity
    subgraph Data Ingestion
        A[RSS Feed Parser] -->|Extracts feeds| B[Content Scraper]
        B -->|Extract articles| C[Raw Data Storage]
        class A,B,C ingestion;
    end

    subgraph Preprocessing
        C -->|Sanitize and Extract| D[Text Processor]
        C -->|Extract Elements| E[Image Processor]
        C -->|Extract Code| F[Code Processor]
        C -->|Extract Tables| G[Table Processor]
        class D,E,F,G preprocessing;
    end

    subgraph Embedding
        D -->|Text embeddings| H[Language Model BERT or GPT]
        E -->|Image embeddings| I[Image Model CLIP]
        F -->|Code embeddings| J[Code Model Codex]
        G -->|Table embeddings| K[Table Parser Custom ML]
        class H,I,J,K embedding;
    end

    subgraph Storage
        H -->|Store text embeddings| L[Embedding Index FAISS or BigQuery]
        I -->|Store image embeddings| L
        J -->|Store code embeddings| L
        K -->|Store table embeddings| L
        C -->|Store raw and processed articles| M[BigQuery or Cloud Storage]
        class L,M storage;
    end

    subgraph Classification
        L -->|Retrieve embeddings| N[Classifier Model Supervised or Zero-shot]
        N -->|Map to MITRE ATT&CK| O[MITRE Ontology Mapper]
        class N,O classification;
    end

    subgraph Query Generation
        O -->|Generate query templates| P[Query Generator]
        P -->|Fill templates| Q[Kestrel Query Builder]
        class P,Q queryGeneration;
    end

    subgraph Orchestration
        A --> R[Orchestrator Airflow or Prefect]
        R --> B
        R --> C
        R --> D
        R --> N
        R --> Q
        class R orchestration;
    end

    subgraph Feedback Loop
        O -->|Validation| S[Human Feedback Interface]
        S -->|Retrain| N
        class S feedback;
    end

    %% Define classes with colors
    classDef ingestion fill:#f9c74f,stroke:#f8961e,stroke-width:2px;
    classDef preprocessing fill:#90be6d,stroke:#43aa8b,stroke-width:2px;
    classDef embedding fill:#577590,stroke:#277da1,stroke-width:2px;
    classDef storage fill:#f94144,stroke:#f3722c,stroke-width:2px;
    classDef classification fill:#9a031e,stroke:#5f0f40,stroke-width:2px;
    classDef queryGeneration fill:#ffafcc,stroke:#b5179e,stroke-width:2px;
    classDef orchestration fill:#7400b8,stroke:#6930c3,stroke-width:2px;
    classDef feedback fill:#06d6a0,stroke:#118ab2,stroke-width:2px;
