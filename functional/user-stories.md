# DRAF USER STORIES

## Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (*Credit Scoring Engine*)

User Stories berikut diturunkan langsung dari **FR-01 sampai FR-15** pada SRS. Fitur **Could Have (FR-16, FR-17)** dan **Won't Have** tidak dimasukkan.

---

# EPIK 1 — Manajemen Anggota

### US-01 — Pengelolaan Data Anggota

**Sebagai Admin/Pengelola Koperasi, Saya ingin mengelola data anggota, Sehingga data anggota yang digunakan dalam proses layanan koperasi dapat tersimpan dan diperbarui secara terstruktur.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-01; NFR-08, NFR-09

**Acceptance Criteria:**

* **Given** Admin telah memiliki akses sistem, **When** Admin melakukan penambahan atau pembaruan data anggota, **Then** sistem menyimpan data anggota yang telah diproses.
* **Given** data anggota telah tersimpan, **When** Admin memperbarui data tersebut, **Then** sistem menampilkan data anggota yang telah diperbarui.
* **Given** pengguna bukan Admin, **When** pengguna mencoba melakukan pengelolaan data anggota tanpa kewenangan, **Then** sistem menolak akses sesuai role.

---

# EPIK 2 — Pengajuan Pinjaman

### US-02 — Pengajuan Pinjaman Anggota

**Sebagai Anggota/Nasabah, Saya ingin mengajukan pinjaman melalui sistem, Sehingga pengajuan saya dapat tercatat dan diproses oleh koperasi.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-02; NFR-08, NFR-11

**Acceptance Criteria:**

* **Given** Anggota memiliki akses sistem, **When** Anggota mengisi dan mengirimkan pengajuan pinjaman, **Then** sistem mencatat pengajuan tersebut dengan status awal.
* **Given** pengajuan berhasil dicatat, **When** Anggota melihat pengajuan tersebut, **Then** sistem menampilkan informasi pengajuan dan status awalnya.

---

### US-03 — Melihat Daftar Pengajuan oleh Admin

**Sebagai Admin/Pengelola Koperasi, Saya ingin melihat daftar pengajuan pinjaman, Sehingga saya dapat memantau pengajuan yang masuk untuk diproses.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-03; NFR-09, NFR-10

**Acceptance Criteria:**

* **Given** Admin telah memiliki akses, **When** Admin membuka modul pengajuan, **Then** sistem menampilkan daftar pengajuan yang menjadi kewenangannya.
* **Given** terdapat pengajuan yang telah masuk, **When** Admin mengakses daftar pengajuan, **Then** informasi pengajuan dapat ditampilkan untuk proses selanjutnya.

---

# EPIK 3 — AI Credit Scoring Engine

### US-04 — Input Atribut AI

**Sebagai Analis Kredit, Saya ingin memasukkan empat atribut Job, Education, Housing, dan Loan, Sehingga data yang diperlukan untuk proses credit scoring tersedia secara lengkap.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-04; NFR-01, NFR-06
* **Business Rule:** BR-02

**Acceptance Criteria:**

* **Given** Analis sedang melakukan penilaian pengajuan, **When** Analis mengisi Job, Education, Housing, dan Loan, **Then** sistem menyimpan keempat atribut sebagai input scoring.
* **Given** salah satu dari empat atribut belum lengkap atau tidak valid, **When** Analis mencoba menjalankan scoring, **Then** sistem tidak menjalankan proses scoring dan meminta data dilengkapi/diperbaiki.

---

### US-05 — Menjalankan Credit Scoring Engine

**Sebagai Analis Kredit, Saya ingin menjalankan Credit Scoring Engine berbasis Decision Tree (ID3), Sehingga saya memperoleh rekomendasi kelayakan kredit berdasarkan empat atribut yang telah diinput.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-05, FR-06; NFR-01, NFR-02, NFR-03, NFR-04, NFR-05
* **Business Rule:** BR-02

**Acceptance Criteria:**

* **Given** Job, Education, Housing, dan Loan telah lengkap dan valid, **When** Analis menjalankan scoring, **Then** sistem memproses data menggunakan Decision Tree (ID3).
* **Given** proses scoring berhasil, **When** engine mengembalikan hasil, **Then** sistem menerima hasil klasifikasi kelayakan.
* **Given** proses scoring dijalankan, **When** sistem mengukur waktu pemrosesan, **Then** latensi AI Engine tidak melebihi **5 detik per scoring**.

---

### US-06 — Menampilkan Rekomendasi AI

**Sebagai Analis Kredit, Saya ingin melihat hasil rekomendasi AI, Sehingga saya dapat menggunakan hasil tersebut sebagai pertimbangan dalam menentukan keputusan kredit.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-07; NFR-01, NFR-06
* **Business Rule:** BR-01, BR-06

**Acceptance Criteria:**

* **Given** Credit Scoring Engine berhasil melakukan klasifikasi, **When** hasil scoring tersedia, **Then** sistem menampilkan rekomendasi **Yes/Diterima** atau **No/Ditolak**.
* **Given** rekomendasi AI telah ditampilkan, **When** Analis melihat hasil tersebut, **Then** rekomendasi ditampilkan sebagai **alat bantu keputusan**, bukan keputusan final otomatis.

---

### US-07 — Transparansi Dasar Rekomendasi AI

**Sebagai Analis Kredit, Saya ingin melihat atribut dasar yang digunakan AI dalam menghasilkan rekomendasi, Sehingga saya dapat memahami dasar penilaian yang diberikan oleh model.**

* **Prioritas:** SHOULD Have
* **Keterlacakan:** FR-08; NFR-06, NFR-07
* **Business Rule:** BR-04

**Acceptance Criteria:**

* **Given** rekomendasi AI telah tersedia, **When** Analis melihat hasil scoring, **Then** sistem menampilkan atribut dasar yang digunakan model.
* **Given** atribut dasar ditampilkan, **When** Analis meninjau rekomendasi, **Then** informasi tersebut dapat dipahami sebagai dasar pertimbangan penilaian.

---

# EPIK 4 — Keputusan Kredit oleh Analis

### US-08 — Konfirmasi Keputusan Kredit

**Sebagai Analis Kredit/Pengambil Keputusan, Saya ingin mengonfirmasi keputusan pengajuan setelah meninjau rekomendasi AI, Sehingga keputusan final kredit tetap berada pada pihak yang berwenang.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-09; NFR-14
* **Business Rule:** BR-01, BR-06

**Acceptance Criteria:**

* **Given** rekomendasi AI telah tersedia, **When** Analis melakukan konfirmasi keputusan, **Then** sistem menyimpan keputusan analis sebagai keputusan final.
* **Given** rekomendasi AI tersedia, **When** belum ada konfirmasi dari Analis, **Then** sistem tidak menetapkan rekomendasi AI sebagai keputusan final secara otomatis.

---

### US-09 — Override Rekomendasi AI

**Sebagai Analis Kredit/Pengambil Keputusan, Saya ingin melakukan override terhadap rekomendasi AI, Sehingga saya dapat menetapkan keputusan final berdasarkan pertimbangan manusia apabila diperlukan.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-10; NFR-14
* **Business Rule:** BR-01, BR-05, BR-06

**Acceptance Criteria:**

* **Given** AI memberikan rekomendasi, **When** Analis menetapkan keputusan yang berbeda, **Then** sistem menyimpan keputusan Analis sebagai keputusan final.
* **Given** Analis melakukan override, **When** keputusan disimpan, **Then** rekomendasi AI tetap terpisah dari keputusan final Analis.
* **Given** tidak ada tindakan dari Analis, **When** rekomendasi AI tersedia, **Then** sistem tidak mengubahnya menjadi keputusan final secara otomatis.

---

# EPIK 5 — Tracking Status Pengajuan

### US-10 — Pembaruan Status Pengajuan

**Sebagai Analis Kredit/Pengambil Keputusan, Saya ingin memperbarui status pengajuan berdasarkan keputusan yang telah ditetapkan, Sehingga status pengajuan mencerminkan keputusan terbaru.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-11; NFR-13

**Acceptance Criteria:**

* **Given** keputusan final telah ditetapkan oleh Analis, **When** keputusan diproses, **Then** sistem memperbarui status pengajuan sesuai keputusan.
* **Given** status telah diperbarui, **When** data pengajuan ditampilkan kembali, **Then** sistem menampilkan status terbaru.

---

### US-11 — Melihat Status Pengajuan oleh Anggota

**Sebagai Anggota/Nasabah, Saya ingin melihat status pengajuan pinjaman saya, Sehingga saya dapat mengetahui perkembangan dan hasil pengajuan tanpa harus mengakses data anggota lain.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-12; NFR-09, NFR-10, NFR-12
* **Business Rule:** BR-03

**Acceptance Criteria:**

* **Given** Anggota memiliki pengajuan pinjaman, **When** Anggota membuka riwayat pengajuan, **Then** sistem menampilkan status pengajuan miliknya.
* **Given** Anggota mencoba mengakses pengajuan milik anggota lain, **When** permintaan akses dilakukan, **Then** sistem menolak akses tersebut.

---

### US-12 — Melihat Seluruh Pengajuan oleh Analis

**Sebagai Analis Kredit/Pengambil Keputusan, Saya ingin melihat seluruh pengajuan yang menjadi kewenangan saya, Sehingga saya dapat melakukan proses penilaian dan pengambilan keputusan kredit.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-13; NFR-09, NFR-10

**Acceptance Criteria:**

* **Given** Analis telah terautentikasi, **When** Analis membuka daftar pengajuan, **Then** sistem menampilkan pengajuan yang menjadi kewenangannya.
* **Given** terdapat pengajuan yang membutuhkan penilaian, **When** Analis mengakses daftar tersebut, **Then** data pengajuan tersedia untuk proses penilaian.

---

# EPIK 6 — Audit Trail

### US-13 — Pencatatan Aktivitas Sistem

**Sebagai Auditor Keuangan, Saya ingin aktivitas penting terkait pengajuan, scoring, dan keputusan tercatat dalam audit trail, Sehingga proses pengajuan dan keputusan dapat ditelusuri.**

* **Prioritas:** MUST Have
* **Keterlacakan:** FR-14; NFR-13, NFR-14

**Acceptance Criteria:**

* **Given** terjadi aktivitas penting pada pengajuan, scoring, atau keputusan, **When** aktivitas tersebut diproses sistem, **Then** aktivitas tercatat dalam audit trail.
* **Given** terdapat catatan aktivitas, **When** pihak yang berwenang melakukan penelusuran, **Then** catatan aktivitas dapat digunakan untuk mengetahui riwayat proses.

---

# EPIK 7 — Reporting

### US-14 — Laporan Pengajuan dan Penilaian

**Sebagai Ketua/Manajemen Koperasi, Saya ingin menghasilkan laporan pengajuan dan hasil penilaian, Sehingga saya dapat memantau proses dan hasil pengajuan kredit secara terstruktur.**

* **Prioritas:** SHOULD Have
* **Keterlacakan:** FR-15; NFR-09, NFR-10

**Acceptance Criteria:**

* **Given** pengguna memiliki kewenangan untuk melihat laporan, **When** pengguna meminta laporan pengajuan, **Then** sistem menampilkan laporan pengajuan dan hasil penilaian.
* **Given** terdapat data pengajuan dan hasil penilaian, **When** laporan dibuat, **Then** informasi yang ditampilkan berasal dari data pengajuan yang tersedia pada sistem.

---

# Ringkasan Product Backlog User Stories

| ID        | EPIK               | User Story                                       | Prioritas | FR           |
| --------- | ------------------ | ------------------------------------------------ | --------- | ------------ |
| **US-01** | Manajemen Anggota  | Mengelola data anggota                           | MUST      | FR-01        |
| **US-02** | Pengajuan Pinjaman | Mengajukan pinjaman                              | MUST      | FR-02        |
| **US-03** | Pengajuan Pinjaman | Melihat daftar pengajuan oleh Admin              | MUST      | FR-03        |
| **US-04** | AI Scoring         | Input 4 atribut AI                               | MUST      | FR-04        |
| **US-05** | AI Scoring         | Menjalankan Decision Tree ID3                    | MUST      | FR-05, FR-06 |
| **US-06** | AI Scoring         | Melihat rekomendasi AI                           | MUST      | FR-07        |
| **US-07** | AI Scoring         | Melihat dasar rekomendasi AI                     | SHOULD    | FR-08        |
| **US-08** | Keputusan Kredit   | Konfirmasi keputusan                             | MUST      | FR-09        |
| **US-09** | Keputusan Kredit   | Override rekomendasi AI                          | MUST      | FR-10        |
| **US-10** | Tracking Status    | Memperbarui status pengajuan                     | MUST      | FR-11        |
| **US-11** | Tracking Status    | Melihat status pengajuan sendiri                 | MUST      | FR-12        |
| **US-12** | Tracking Status    | Melihat pengajuan yang menjadi kewenangan analis | MUST      | FR-13        |
| **US-13** | Audit Trail        | Mencatat aktivitas penting                       | MUST      | FR-14        |
| **US-14** | Reporting          | Menghasilkan laporan pengajuan dan penilaian     | SHOULD    | FR-15        |

### Alur Utama User Story

**US-02 → US-03 → US-04 → US-05 ★ → US-06 ★ → US-07 ★ → US-08/US-09 → US-10 → US-11**

Dengan prinsip utama:

> **Decision Tree (ID3) menghasilkan REKOMENDASI → Analis melakukan REVIEW → Analis menetapkan KEPUTUSAN FINAL.**

Jadi, pada seluruh User Story AI (**US-05 sampai US-07**), sistem tidak boleh diposisikan sebagai pihak yang mengambil keputusan kredit secara mandiri.
