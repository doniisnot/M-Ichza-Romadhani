[Peran]
Kamu adalah Software Architect Senior untuk aplikasi Web Enterprise berfitur AI/Machine Learning.

[Tugas]
Buat DRAF High-Level Design (HLD) ringkas, komprehensif, dan terstruktur berdasarkan dokumen PRD, SRS, User Stories, dan Acceptance Criteria dari "Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (Credit Scoring Engine)" berikut.

[Konteks & Stack Teknologi Target]
- Platform: Web Application (Single Page Application / Server-Side Rendered Web).
- Stack Usulan:
  * Frontend & Web Application Backend: PHP / Laravel framework (mengelola Auth, Role Management, Pengajuan Pinjaman, Business Logic, dan Database).
  * AI ML Service: Python microservice (FastAPI / Flask) khusus menjalankan Model Decision Tree (ID3 / Scikit-Learn).
  * Data Store: MySQL Database (Relational Storage untuk Data Anggota, Pengajuan, Atribut AI, Hasil Scoring, Keputusan, dan Audit Trail).
- Konstrain Utama: Prototype 1 semester (3 bulan); 1 fitur AI inti (Credit Scoring ID3); Biaya komputasi minim; AI berfungsi sebagai *Decision-Support Tool* (bukan *Decision-Maker* mandiri); SLA Latensi AI Engine ≤ 5 detik.

[Format Output HLD]

1. DIAGRAM ARSITEKTUR SISTEM
   - Sajikan diagram arsitektur tingkat tinggi dalam format kode **Mermaid (`graph TD` atau `architecture-beta`)** atau Diagram ASCII yang menggambarkan hubungan:
     `Client (Web Browser) → Backend API (Laravel) → ML Service (Python ID3) → Database (MySQL) → System Logging (Audit Trail)`.

2. DESKRIPSI KOMPONEN & ARSITEKTUR
   - Peran & Tanggung Jawab masing-masing komponen (Web App Backend, ML Engine Service, Database, Audit Trail).
   - Tabel Trade-Off Keputusan Arsitektur Fitur AI: Bandingkan opsi "Cloud/External API vs Dedicated Python ML Service vs Embedded Engine (In-App Rules)" dengan kriteria: Akurasi, Latensi, Biaya, Privasi Data, dan Effort Pengembangan. Berikan rekomendasi arsitektur terpilih beserta alasannya (1-2 kalimat).

3. ALIRAN DATA END-TO-END FITUR AI (DATA FLOW)
   - Jelaskan alur sekuensial data dari: `Input 4 Atribut (Job, Education, Housing, Loan) → Preprocessing & Validasi → Inference (ID3 Model Execution) → Postprocessing → Output Rekomendasi ("Yes/Diterima" / "No/Ditolak") → Persistence Storage`.
   - Sebutkan titik *Fallback* (jalur cadangan) ketika ML Service mengalami Timeout (> 5 detik) atau Error (HTTP 500) untuk menjamin sistem tetap mempertahankan status "Pending Review" tanpa membuat keputusan otomatis.

4. KONTRAK ANTARKOMPONEN TINGKAT TINGGI (API CONTRACT & INTEGRASI)
   - Endpoint Utama Integrasi Backend Laravel ↔ ML Service Python:
     * Endpoint: `POST /api/v1/scoring/predict`
     * Format Payload Request JSON (4 Atribut Mandatory).
     * Format Payload Response JSON (Prediction Result, Processing Time/Latency, Model Metadata).
     * Error Response Format (Timeout / Validation Error / Service Unavailable).

5. SECURITY & PRIVACY BY DESIGN
   - Autentikasi & Otorisasi: Role-Based Access Control (RBAC) membedakan role Anggota, Admin, Analis Kredit, Manajemen, dan Auditor (NFR-08, NFR-09, BR-03).
   - Privasi Data & Confidentiality: Enkripsi data sensitif anggota/finansial pada Rest & Transit (NFR-11). Isolasi data antar anggota (NFR-12).
   - Audit Trail & Logging: Mekanisme pencatatan aktivitas keputusan manusia vs rekomendasi AI untuk kebutuhan audit (FR-14, NFR-13, NFR-14).

6. LINGKUNGAN DEPLOYMENT RINGKAS
   - Gambaran umum deployment environment (Development / Staging / Production) yang efisien dari segi biaya untuk kebutuhan prototype 1 semester.

[Aturan Penulisan HLD]
- Hanya desain sistem berdasarkan FR-01 s.d. FR-15 dan NFR yang tersedia. Dilarang menambah fitur di luar konteks SRS. Jika terdapat gap arsitektur, tandai dengan `[ASUMSI-HLD-XX]`.
- JANGAN masuk ke detail kelas, metode, skema tabel detail, atau query SQL (karena itu merupakan domain LLD).
- Setiap keputusan besar arsitektur wajib disertai alasan ringkas (1-2 kalimat) dan alternatif yang dipertimbangkan.
- Gunakan Bahasa Indonesia baku, ilmiah, dan format Markdown yang rapi.

---

[Konteks Input Dokumen Ringkas]

1. SCOPE BISNIS & AI (PRD & SRS)
- Produk: Sistem Informasi Koperasi Simpan Pinjam dengan Automatic Credit Scoring Engine berbasis Decision Tree (ID3).
- Input Atribut AI (4 Mandatory): Job (Nominal), Education (Nominal), Housing (Enum: Yes/No), Loan (Enum: Yes/No).
- Output AI: Rekomendasi "Yes/Diterima" atau "No/Ditolak" (Decision-Support Tool).
- Baseline Model (Riset UCI Bank Marketing): Akurasi 80%, Sensitivitas 71.42%, Spesifikasi 90.90% (50 sampel: 25 latih, 25 uji).

2. BUSINESS RULES (BR) KUNCI
- BR-01 & BR-06: Keputusan final kredit WAJIB dikonfirmasi oleh Analis Kredit (manusia). Rekomendasi AI dan Keputusan Analis wajib disimpan/ditampilkan terpisah.
- BR-02: Scoring AI hanya boleh diproses jika 4/4 atribut terisi lengkap dan valid.
- BR-05: Analis berhak melakukan OVERRIDE keputusan (menolak rekomendasi AI).

3. NFR KINERJA & KEAMANAN
- NFR-05: Latensi AI Engine ≤ 5 detik/scoring.
- NFR-08 s.d NFR-10: Autentikasi, Role-Based Access Control (RBAC), Isolasi Akses Data.
- NFR-11 & NFR-12: Enkripsi & Data Privacy anggota.
- NFR-13 & NFR-14: Kegagalan scoring tidak boleh mengubah status keputusan final secara otomatis.

[Peran]
Kamu adalah Senior Software Engineer dan Tech Lead untuk aplikasi Web Enterprise berbasis PHP (Laravel) dan Python (FastAPI/Flask).

[Tugas]
Buat DRAF Low-Level Design (LLD) teknis yang terstruktur, presisi, dan terukur berdasarkan dokumen SRS dan HLD dari "Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (Credit Scoring Engine)" berikut.

[Konteks & Stack Teknisi]
- Framework Utama Backend Web: PHP 11 / Laravel 11 (Clean Architecture/Service-Repository Pattern, Eloquent ORM).
- Framework AI ML Engine: Python 3.11 / FastAPI (Scikit-learn untuk model Decision Tree ID3).
- Database Engine: MySQL 8.0 (Relational Database).
- Komunikasi Inter-Service: Synchronous REST API via Guzzle HTTP Client (Laravel -> FastAPI) dengan mekanisme Retry & Timeout.
- Pola Arsitektur Kode: Clean Architecture / Domain-Driven Design (DDD) ringkas yang memisahkan Controller/Router, Service/Use Case Layer, Repository Data Access Layer, dan DTO/Request Validation.

[Format Output LLD]

1. DESAIN MODUL & CLASS FITUR MUST (OOP / CLASS SPECIFICATION)
   Spesifikasikan desain kelas untuk 3 fitur Must utama:
   - Modul Loan Application Management
   - Modul AI Credit Scoring Orchestrator
   - Modul Analyst Decision & Override Engine
   Sertakan: Nama Class, Responsibilitas/Tanggung Jawab, Key Attributes (dengan tipe data), dan Key Methods (termasuk parameter dan return type).

2. SKEMA DATA PERSISTENSI (DATABASE SCHEMA & RELATIONS)
   - Tuliskan skema database dalam bentuk DDL SQL standar (atau Prisma Schema / ERD Teks) untuk entitas utama: `users`, `members`, `loan_applications`, `ai_scoring_attributes`, `ai_scoring_results`, `analyst_decisions`, dan `audit_logs`.
   - Cantumkan Primary Key, Foreign Key, Enum Constraints, Indexes (terutama pada `loan_application_id` dan `user_id`), serta timestamp fields.

3. SPESIFIKASI REST API DETAIL (INTERNAL INTEGRATION CONTRACT)
   Spesifikasikan detail endpoint internal untuk komunikasi Laravel ↔ Python FastAPI (`POST /api/v1/scoring/predict`):
   - HTTP Method, Request Path, Headers (misal: `X-API-Key`, `Content-Type`).
   - Contoh Request Payload JSON (4 Atribut: `job`, `education`, `housing`, `loan`).
   - Contoh Response Payload JSON Sukses (200 OK) memuat `prediction`, `recommendation`, `processing_time_ms`, dan `model_metadata`.
   - Contoh Response Payload JSON Error Validasi (422 Unprocessable Entity) & Service Error (500 / 503).
   - Daftar Kode Error Sistem Spesifik (misal: `ERR_AI_INCOMPLETE_INPUT`, `ERR_AI_SERVICE_TIMEOUT`, `ERR_AI_INTERNAL_ERROR`).

4. SEQUENCE DIAGRAM & ALUR DETAIL FITUR AI (DETAILED EXECUTION FLOW)
   - Buat Diagram Sekuensial terperinci dalam format kode **Mermaid (`sequenceDiagram`)** yang menggambarkan interaksi hingga level kelas/metode:
     `Analyst UI -> LoanController -> ScoringService -> MLHttpClient -> FastAPI Router -> ID3InferenceEngine -> AuditLogger -> Database`.
   - Sertakan alur eksekusi saat **Happy Path**, **Input Validation Error**, **Timeout Execution (> 5 detik)**, dan **ML Service Failure (500 Error)**.

5. RANCANGAN ERROR HANDLING, RETRY, & FALLBACK
   - Mekanisme Handling Timeout: Konfigurasi Guzzle Client di Laravel (timeout = 4.5 detik untuk menjamin SLA ≤ 5 detik NFR-05).
   - Mekanisme Retry Policy: Aturan Retry (misal: Max 2x retry dengan exponential backoff hanya untuk HTTP 502/503/504, tanpa retry pada HTTP 4xx).
   - Fallback State Logic: Penjelasan logis mengapa status pengajuan TETAP berada pada state `Pending Review` ketika terjadi kegagalan ML Service (BR-01, NFR-14).
   - Opsi Arsitektur Teknis yang Belum Diputus: Jika ada pilihan pustaka/teknologi yang fleksibel (misal: Guzzle vs Http Facade, Pydantic vs Marshmallow), berikan 2 opsi + kriteria pertimbangan, lalu tulis tag `[KEPUTUSAN TIM: ...]` untuk diisi oleh tim teknis.

6. TABEL TRACEABILITY LLD ↔ FR/NFR/BR
   - Matriks pemetaan dari Elemen Desain LLD (Class/Method/Table/Endpoint) ke ID FR (FR-01 s.d FR-15), NFR (NFR-01 s.d NFR-16), dan Business Rules (BR-01 s.d BR-06).

[Aturan Penulisan LLD]
- DILARANG MENGUBAH ATAU MENAMBAH REQUIREMENT BISNIS DARI SRS/HLD.
- Seluruh nama Class, Method, Field Database, dan Parameter wajib menggunakan **Bahasa Inggris** (mengikuti konvensi standar koding profesional).
- Seluruh narasi, penjelasan, dan dokumentasi pendukung wajib menggunakan **Bahasa Indonesia** baku.
- Gunakan Markdown yang rapi dan terstruktur.

---

[Konteks Input SRS & HLD Ringkas]

1. SRS FITUR UTAMA & BR
- FR-04, FR-05, FR-06, FR-07: Input 4 atribut AI (`job`, `education`, `housing`, `loan`), eksekusi Decision Tree ID3, pengiriman data ke ML engine, dan penayangan rekomendasi AI (`Yes/Diterima` atau `No/Ditolak`).
- FR-09, FR-10, FR-11: Konfirmasi dan Override keputusan oleh Analis Kredit, serta pembaruan status pengajuan (`Diterima` / `Ditolak`).
- FR-14: Pencatatan Audit Trail untuk seluruh aktivitas scoring, keputusan, dan override.
- BR-01 & BR-06: AI HANYA sebagai *decision-support tool*. Keputusan final WAJIB oleh Analis Kredit manusia. Rekomendasi AI dan keputusan Analis harus disimpan pada entitas terpisah.
- BR-02: Scoring AI hanya boleh diproses jika 4/4 atribut terisi lengkap dan valid.
- BR-05: Analis berhak melakukan Override (keputusan berbeda dengan rekomendasi AI).

2. NFR UNCI
- NFR-05: Latensi AI Engine ≤ 5 detik per scoring.
- NFR-08 s.d NFR-10: Autentikasi, RBAC (Role-Based Access Control), dan isolasi data kredit.
- NFR-13 & NFR-14: Kegagalan proses scoring AI tidak boleh secara otomatis mengubah status keputusan final.

3. HLD ARCHITECTURE BOUNDARIES
- Web App (Laravel) berkomunikasi dengan ML Service (Python FastAPI) via REST API `POST /api/v1/scoring/predict`.
- Persistence Layer: MySQL 8.0.
- Fallback State: Jika ML Service timeout/error, sistem menampilkan pesan error ramah dan mempertahankan status `Pending Review`.
