# PTM-05 Prompt Log — AI Credit Scoring Engine Koperasi

## Identitas Artefak

- Praktikum: PTM-05 — REST API & Database
- Proyek: AI Credit Scoring Engine Koperasi
- Tool AI: ChatGPT — GPT-5.6 Luna
- Stack: Laravel 11 / PHP 11 + Python 3.11 / FastAPI + Pydantic v2
- Database: MySQL 8.0 / PostgreSQL
- Model: Decision Tree — ID3

## 1. Sesi D.1 — OpenAPI

**Target:** `openapi.yaml`

**Tujuan prompt:** menghasilkan spesifikasi REST API berdasarkan LLD/user story,
dengan resource noun jamak, schema request/response, error response, dan penandaan
endpoint AI.

**Output awal yang diperoleh:**
- resource dan endpoint utama teridentifikasi,
- endpoint `/scoring/predict` ditandai sebagai AI,
- schema `ScoringPredictRequest` memuat `job`, `education`, `housing`, `loan`,
- response AI memuat prediction, recommendation, processing time, dan model info.

**Revisi manual:**
- menegaskan AI tidak boleh mengubah status resmi pinjaman,
- menambahkan fallback timeout >5 detik,
- menambahkan HTTP 504 untuk timeout,
- memperketat input AI dengan `additionalProperties: false`,
- menambahkan endpoint keputusan analis sebagai satu-satunya perubahan status resmi.

**Kualitas output:** 4/5.

## 2. Sesi D.2 — ERD / Pydantic

**Target:** `erd.md` dan `models.py`

**Tujuan prompt:** menyinkronkan ERD dan skema Pydantic dengan components/schemas
OpenAPI, termasuk PK/FK, enum, unique constraint, validator, dan relasi.

**Output utama:**
- tujuh entitas utama,
- relasi member → loan application,
- relasi loan → scoring attributes,
- relasi loan → scoring results,
- relasi analyst decision dan audit log,
- enum untuk role, status, input AI, prediction, recommendation, dan analyst decision.

**Revisi manual:**
- `ScoringPredictRequest` dibuat strict dengan `extra="forbid"`,
- validator string ditambahkan untuk `job` dan `education`,
- hasil scoring dibuat historis 1:N,
- field persistence `password_hash` dipisahkan dari response publik,
- fallback dan `loan_status_unchanged` disinkronkan dengan kontrak API.

**Kualitas output:** 4/5.

## 3. Sesi Iterasi Lanjutan

**Target:** sinkronisasi D.1 + D.2 + dokumentasi

**Masalah yang diperiksa:**
1. AI berpotensi disalahartikan sebagai pemberi keputusan final.
2. Fallback belum cukup eksplisit.
3. Validasi input AI harus menghasilkan 422.
4. ERD, OpenAPI, dan Pydantic harus memakai nilai enum yang sama.

**Perbaikan:**
- status resmi hanya berubah melalui `/loans/{id}/decision`,
- fallback mempertahankan `Pending Review`,
- `extra="forbid"` dan `additionalProperties: false`,
- enum disamakan pada tiga artefak,
- `is_override` didokumentasikan pada persistence model.

**Kualitas output:** 5/5 setelah revisi.

## 4. Asumsi yang dibuat

| Kode | Asumsi | Verifikasi |
|---|---|---|
| ASUMSI-01 | users → members = 1:0..1 | Benar |
| ASUMSI-02 | actor_user_id pada audit log nullable | Benar |
| ASUMSI-03 | field fallback merupakan ekstensi kontrak | Benar |
| ASUMSI-04 | password_hash persistence-only | Benar |
| ASUMSI-05 | fallback + keputusan analis bukan override | Benar |
| ASUMSI-06 | email/member_number unique | Benar |
| ASUMSI-07 | hasil scoring disimpan 1:N | Benar |

## 5. Evaluasi

AI digunakan sebagai co-pilot penyusunan. Hasil akhir ditinjau dan direvisi agar
sinkron dengan D.1, D.2, aturan Human-in-the-Loop, validasi 422, dan fail-safe.
Pemahaman serta keputusan desain tetap berada pada tim.
