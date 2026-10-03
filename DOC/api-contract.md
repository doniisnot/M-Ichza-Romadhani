# API Contract — AI Credit Scoring Engine Koperasi

## 1. Tujuan

Dokumen ini menjelaskan keputusan desain API yang menjadi dasar `openapi.yaml`,
ERD, dan `models.py`. Desain mengikuti D.1 dan D.2 PTM-05.

## 2. Arsitektur

- **Laravel 11 / PHP 11**: System of Record dan Business Authority.
- **Python 3.11 / FastAPI + Pydantic v2**: ML Service / inference engine.
- **Database**: MySQL 8.0 / PostgreSQL.
- **Model AI**: Decision Tree dengan algoritma ID3.
- **Komunikasi**: REST sinkron dari Laravel ke FastAPI menggunakan HTTP client/Guzzle.

AI hanya memberikan rekomendasi. Status resmi pengajuan kredit tetap menjadi kewenangan
Credit Analyst.

## 3. Resource dan endpoint

| Method | Endpoint | Fungsi |
|---|---|---|
| POST | `/users/login` | Autentikasi dan token JWT |
| GET | `/members` | Daftar anggota |
| POST | `/members` | Membuat anggota |
| POST | `/loans` | Membuat pengajuan pinjaman |
| GET | `/loans` | Daftar pengajuan |
| GET | `/loans/my-applications` | Riwayat pengajuan anggota |
| POST | `/loans/{id}/attributes` | Menyimpan empat atribut input AI |
| POST | `/scoring/predict` | Menjalankan inference AI |
| POST | `/loans/{id}/decision` | Menyimpan keputusan resmi analis |
| GET | `/audit-logs` | Audit trail |
| GET | `/reports` | Laporan |

Resource menggunakan noun jamak sesuai aturan D.1.

## 4. Kontrak input AI

Endpoint `/scoring/predict` menerima tepat empat atribut:

1. `job`: string
2. `education`: string
3. `housing`: `yes` / `no`
4. `loan`: `yes` / `no`

`additionalProperties: false` pada OpenAPI dan `extra="forbid"` pada Pydantic
digunakan agar field tambahan ditolak. Input kosong/tidak valid menghasilkan HTTP 422.

## 5. Kontrak output AI

Output utama:

- `success`
- `prediction`: `Yes` / `No`
- `recommendation`: `Diterima` / `Ditolak`
- `processing_time_ms`
- `model.name`
- `model.algorithm`
- `model.version`

Field fail-safe:

- `fallback`
- `fallback_reason`
- `loan_status_unchanged`

Field tersebut membantu memperjelas bahwa hasil inference tidak otomatis mengubah
status resmi pengajuan.

## 6. Human-in-the-Loop

Endpoint `/loans/{id}/decision` adalah satu-satunya endpoint pada kontrak ini yang
mengubah status resmi.

Mapping:

- `approved` → `Diterima`
- `rejected` → `Ditolak`

Jika keputusan analis berbeda dari recommendation AI yang valid, `is_override` dicatat
sebagai `true`.

## 7. Fail-safe

Jika ML Service mengalami timeout lebih dari 5 detik atau error internal:

- inference dianggap gagal/fallback,
- alasan fallback dicatat,
- status pinjaman tetap `Pending Review`,
- keputusan final tetap harus dibuat oleh Credit Analyst.

## 8. Keamanan

- Endpoint aplikasi menggunakan Bearer JWT.
- Endpoint inference AI menggunakan `X-API-Key`.
- `password` hanya diterima sebagai input autentikasi dan `password_hash` hanya berada
  pada model persistence; keduanya tidak dikembalikan pada response anggota/pengajuan.

## 9. HTTP response

Setiap endpoint menyediakan minimal tiga kategori response yang relevan: sukses,
kesalahan 4xx, dan kesalahan 5xx/timeout pada endpoint yang membutuhkan service AI.
Kode khusus yang digunakan antara lain:

- `200`: sukses operasi/query.
- `201`: resource berhasil dibuat.
- `400`: format request tidak sesuai.
- `401`: autentikasi gagal.
- `403`: authorization gagal.
- `404`: resource tidak ditemukan.
- `422`: validasi input gagal.
- `500`: error internal ML service.
- `504`: timeout ML service.

## 10. Sinkronisasi OpenAPI ↔ ERD ↔ Pydantic

Entitas utama:

- `users`
- `members`
- `loan_applications`
- `ai_scoring_attributes`
- `ai_scoring_results`
- `analyst_decisions`
- `audit_logs`

Pydantic enum disinkronkan dengan enum status pada ERD dan OpenAPI.
`ai_scoring_results` dibuat 1:N terhadap pengajuan untuk menyimpan histori/retry.

## 11. Asumsi desain

- **ASUMSI-01**: users → members adalah 1:0..1.
- **ASUMSI-02**: `audit_logs.actor_user_id` nullable.
- **ASUMSI-03**: field fallback merupakan ekstensi kontrak untuk fail-safe.
- **ASUMSI-04**: password hash persistence-only.
- **ASUMSI-05**: keputusan setelah fallback tidak dianggap override.
- **ASUMSI-06**: email dan nomor anggota unik.
- **ASUMSI-07**: hasil scoring disimpan historis 1:N.
