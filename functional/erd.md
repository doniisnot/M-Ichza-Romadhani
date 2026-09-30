# Entity Relationship Diagram (ERD)
## Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (Credit Scoring Engine)

### 1. Diagram ERD (Mermaid Format)

```mermaid
erDiagram
    USERS ||--o| MEMBERS : "has profile"
    USERS ||--o{ ANALYST_DECISIONS : "makes"
    USERS ||--o{ AUDIT_LOGS : "generates"
    MEMBERS ||--o{ LOAN_APPLICATIONS : "applies"
    LOAN_APPLICATIONS ||--o| AI_SCORING_ATTRIBUTES : "contains"
    LOAN_APPLICATIONS ||--o| AI_SCORING_RESULTS : "evaluated_by"
    LOAN_APPLICATIONS ||--o| ANALYST_DECISIONS : "resolved_by"

    USERS {
        bigint id PK
        string email UK
        string password_hash
        enum role "admin, analyst, member, management, auditor"
        datetime created_at
        datetime updated_at
    }

    MEMBERS {
        bigint id PK
        bigint user_id FK
        string member_number UK
        string full_name
        string phone_number
        datetime created_at
        datetime updated_at
    }

    LOAN_APPLICATIONS {
        bigint id PK
        bigint member_id FK
        decimal amount
        enum status "pending_review, approved, rejected"
        datetime application_date
        datetime created_at
        datetime updated_at
    }

    AI_SCORING_ATTRIBUTES {
        bigint id PK
        bigint loan_application_id FK
        string job
        string education
        enum housing "yes, no"
        enum loan "yes, no"
        datetime created_at
    }

    AI_SCORING_RESULTS {
        bigint id PK
        bigint loan_application_id FK
        enum prediction "yes, no"
        string recommendation "Diterima, Ditolak"
        int processing_time_ms
        string model_name
        string model_version
        datetime evaluated_at
    }

    ANALYST_DECISIONS {
        bigint id PK
        bigint loan_application_id FK
        bigint analyst_id FK
        enum decision "approved, rejected"
        boolean is_override
        text notes
        datetime decided_at
    }

    AUDIT_LOGS {
        bigint id PK
        bigint user_id FK
        string action
        string target_entity
        bigint target_id
        json payload
        datetime created_at
    }