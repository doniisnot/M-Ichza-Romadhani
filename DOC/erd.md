# ERD — AI Credit Scoring Engine Koperasi

```mermaid
erDiagram
    USERS ||--o| MEMBERS : "memiliki"
    MEMBERS ||--o{ LOAN_APPLICATIONS : "mengajukan"
    LOAN_APPLICATIONS ||--o| AI_SCORING_ATTRIBUTES : "memiliki atribut"
    LOAN_APPLICATIONS ||--o{ AI_SCORING_RESULTS : "memiliki hasil"
    USERS ||--o{ ANALYST_DECISIONS : "membuat"
    LOAN_APPLICATIONS ||--o{ ANALYST_DECISIONS : "mendapat keputusan"
    USERS ||--o{ AUDIT_LOGS : "menjadi actor"

    USERS {
        BIGINT id PK
        VARCHAR email UK
        VARCHAR password_hash
        ENUM role
    }

    MEMBERS {
        BIGINT id PK
        VARCHAR member_number UK
        VARCHAR full_name
    }

    LOAN_APPLICATIONS {
        BIGINT id PK
        BIGINT member_id FK
        DECIMAL amount
        ENUM status
        DATETIME created_at
    }

    AI_SCORING_ATTRIBUTES {
        BIGINT id PK
        BIGINT loan_application_id FK UK
        VARCHAR job
        VARCHAR education
        ENUM housing
        ENUM loan
    }

    AI_SCORING_RESULTS {
        BIGINT id PK
        BIGINT loan_application_id FK
        BOOLEAN success
        ENUM prediction
        ENUM recommendation
        INT processing_time_ms
        VARCHAR model_name
        VARCHAR algorithm
        VARCHAR model_version
        BOOLEAN fallback
        VARCHAR fallback_reason NULL
        BOOLEAN loan_status_unchanged
    }

    ANALYST_DECISIONS {
        BIGINT id PK
        BIGINT loan_application_id FK
        BIGINT analyst_user_id FK
        ENUM decision
        TEXT notes NULL
        BOOLEAN is_override
    }

    AUDIT_LOGS {
        BIGINT id PK
        VARCHAR action
        TEXT details
        DATETIME created_at
        BIGINT actor_user_id FK NULL
    }
```

## Constraint dan aturan bisnis

- `users.email` unik.
- `members.member_number` unik.
- `ai_scoring_attributes.loan_application_id` unik karena satu pengajuan mempunyai satu set atribut input aktif.
- `loan_applications.status` hanya `Pending Review`, `Diterima`, atau `Ditolak`.
- `housing` dan `loan` hanya `yes` atau `no`.
- `prediction` hanya `Yes` atau `No`.
- `recommendation` hanya `Diterima` atau `Ditolak`.
- `analyst_decisions.decision` hanya `approved` atau `rejected`.
- Pengajuan baru berstatus `Pending Review`.
- AI tidak mengubah status resmi pengajuan.
- `approved` menghasilkan status resmi `Diterima`; `rejected` menghasilkan `Ditolak`.
- `is_override = true` apabila keputusan analis berbeda dari recommendation AI.
- Jika AI timeout > 5 detik atau service error, sistem menggunakan fallback dan status tetap `Pending Review`.
- `ai_scoring_results` bersifat historis sehingga satu pengajuan dapat memiliki lebih dari satu hasil scoring.

## Asumsi

- **[ASUMSI-01]** Relasi `users` ke `members` adalah 1:0..1; tidak semua user harus menjadi anggota.
- **[ASUMSI-02]** `audit_logs.actor_user_id` dapat null untuk event sistem/service.
- **[ASUMSI-03]** `fallback`, `fallback_reason`, dan `loan_status_unchanged` merupakan field tambahan untuk memperjelas perilaku fail-safe AI.
- **[ASUMSI-04]** `password_hash` hanya persistence field dan tidak pernah dikembalikan API.
- **[ASUMSI-05]** Keputusan analis setelah fallback AI tidak dianggap override karena tidak ada recommendation AI yang valid.
- **[ASUMSI-06]** Email user dan nomor anggota harus unik.
- **[ASUMSI-07]** Hasil scoring disimpan 1:N untuk mendukung retry/history.
