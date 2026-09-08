# DRAF USE CASE DETAIL — UC-01

## 1. DETAIL USE CASE

### 1.1 Identitas Use Case

| Elemen                | Detail                                                                                                                                                                                                                                 |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Use Case ID**       | **UC-01**                                                                                                                                                                                                                              |
| **Nama Use Case**     | **Penilaian Kelayakan Kredit Menggunakan AI Credit Scoring Engine dan Pengambilan Keputusan Final**                                                                                                                                    |
| **Aktor Utama**       | Analis Kredit / Pengambil Keputusan                                                                                                                                                                                                    |
| **Aktor Pendukung**   | Credit Scoring Engine (Python ID3 Service), System Logging Service (Audit Trail)                                                                                                                                                       |
| **Platform**          | Web Application                                                                                                                                                                                                                        |
| **Deskripsi Singkat** | Use case menggambarkan proses Analis menginput empat atribut kredit, menjalankan AI Credit Scoring Engine berbasis Decision Tree (ID3), menerima rekomendasi AI, kemudian menetapkan keputusan final melalui konfirmasi atau override. |
| **Traceability**      | FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-10, FR-11, FR-14, NFR-05, BR-01, BR-02, BR-05                                                                                                                                             |

### 1.2 Pre-condition

1. Analis telah login ke sistem menggunakan **Role Analis Kredit**.
2. Terdapat pengajuan pinjaman anggota dengan status **`Pending Review`**.
3. Analis memiliki akses untuk melakukan proses penilaian terhadap pengajuan tersebut.

### 1.3 Post-condition

1. Empat atribut AI (**Job, Education, Housing, Loan**) tersimpan dan dapat ditampilkan.
2. Rekomendasi AI tersimpan dan ditampilkan **terpisah** dari keputusan final.
3. Keputusan final Analis tersimpan sebagai status resmi pengajuan, yaitu:

   * **`Diterima`**, atau
   * **`Ditolak`**.
4. Aktivitas proses scoring dan keputusan tercatat dalam **Audit Trail**.
5. Rekomendasi AI **tidak secara otomatis mengubah status keputusan**.

---

## 1.4 Input dan Output Use Case

### Input

| Parameter            | Ketentuan                          |
| -------------------- | ---------------------------------- |
| **Job**              | Wajib diisi, tipe nominal          |
| **Education**        | Wajib diisi, tipe nominal          |
| **Housing**          | Wajib diisi dengan `Yes` atau `No` |
| **Loan**             | Wajib diisi dengan `Yes` atau `No` |
| **Status Pengajuan** | Harus `Pending Review`             |

### Output

| Output              | Nilai                                                  |
| ------------------- | ------------------------------------------------------ |
| **Rekomendasi AI**  | `Yes/Diterima` atau `No/Ditolak`                       |
| **Keputusan Final** | `Diterima` atau `Ditolak` berdasarkan keputusan Analis |
| **Audit Trail**     | Catatan aktivitas scoring dan keputusan                |

---

# 1.5 Skenario Utama — Happy Flow

### Alur Sekuensial

|    No. | Aktor/Komponen         | Aktivitas                                                                                                       |
| -----: | ---------------------- | --------------------------------------------------------------------------------------------------------------- |
|  **1** | Analis                 | Membuka pengajuan dengan status **`Pending Review`**.                                                           |
|  **2** | Sistem Web             | Menampilkan data pengajuan dan form empat atribut AI: **Job, Education, Housing, Loan**.                        |
|  **3** | Analis                 | Mengisi keempat atribut dengan data yang valid.                                                                 |
|  **4** | Sistem Web             | Melakukan validasi kelengkapan dan validitas keempat atribut.                                                   |
|  **5** | Sistem Web             | Jika seluruh atribut valid, sistem mengirimkan data ke **Credit Scoring Engine**.                               |
|  **6** | Credit Scoring Engine  | Memproses data menggunakan **Decision Tree (ID3)**.                                                             |
|  **7** | Credit Scoring Engine  | Menghasilkan rekomendasi klasifikasi **`Yes/Diterima`** atau **`No/Ditolak`**.                                  |
|  **8** | Sistem Web             | Menerima hasil scoring dari ML Service.                                                                         |
|  **9** | Sistem Web             | Mengukur waktu pemrosesan dan memastikan latensi scoring **≤ 5 detik**.                                         |
| **10** | Sistem Web             | Menampilkan rekomendasi AI kepada Analis beserta empat atribut dasar yang digunakan.                            |
| **11** | System Logging Service | Mencatat aktivitas proses scoring ke Audit Trail.                                                               |
| **12** | Analis                 | Meninjau rekomendasi AI dan atribut yang digunakan.                                                             |
| **13** | Analis                 | Memilih keputusan final berdasarkan hasil review, misalnya **`Diterima`** untuk rekomendasi `Yes/Diterima`.     |
| **14** | Sistem Web             | Menyimpan keputusan Analis sebagai **keputusan final** dan mempertahankan rekomendasi AI sebagai data terpisah. |
| **15** | Sistem Web             | Memperbarui status pengajuan menjadi **`Diterima`** atau **`Ditolak`** sesuai keputusan Analis.                 |
| **16** | System Logging Service | Mencatat keputusan final Analis pada Audit Trail.                                                               |
| **17** | Sistem Web             | Menampilkan bahwa proses penilaian dan keputusan final telah selesai.                                           |

### Prinsip penting pada Happy Flow

**AI → memberikan rekomendasi → Analis melakukan review → Analis menetapkan keputusan final.**

Dengan demikian, meskipun AI menghasilkan `Yes/Diterima`, sistem **tidak boleh langsung mengubah status pengajuan menjadi `Diterima`** sebelum Analis melakukan konfirmasi.

---

# 1.6 Skenario Alternatif / Flow Eksepsi

## Alur A — Input 4 Atribut Tidak Lengkap / Invalid

**Kondisi:** Salah satu atau lebih atribut AI tidak diisi atau memiliki nilai tidak valid.

| No. | Aktor/Komponen | Aktivitas                                                                  |
| --: | -------------- | -------------------------------------------------------------------------- |
|  A1 | Analis         | Mengisi data Job, Education, Housing, dan Loan.                            |
|  A2 | Sistem Web     | Memvalidasi seluruh atribut.                                               |
|  A3 | Sistem Web     | Menemukan minimal satu atribut kosong atau invalid.                        |
|  A4 | Sistem Web     | Menampilkan pesan validasi dan meminta Analis melengkapi/memperbaiki data. |
|  A5 | Sistem Web     | **Tidak mengirim data ke ML Service.**                                     |
|  A6 | Sistem Web     | **Tidak mengubah keputusan/status final pengajuan secara otomatis.**       |

**Aturan:** AI hanya dapat dijalankan apabila **4/4 atribut** telah lengkap dan valid.

---

## Alur B — Analis Melakukan Override

**Kondisi:** AI menghasilkan `No/Ditolak`, tetapi Analis menentukan `Diterima`.

| No. | Aktor/Komponen         | Aktivitas                                                 |
| --: | ---------------------- | --------------------------------------------------------- |
|  B1 | Credit Scoring Engine  | Menghasilkan rekomendasi **`No/Ditolak`**.                |
|  B2 | Sistem Web             | Menampilkan rekomendasi AI kepada Analis.                 |
|  B3 | Analis                 | Meninjau rekomendasi AI.                                  |
|  B4 | Analis                 | Memilih keputusan final **`Diterima`**.                   |
|  B5 | Sistem Web             | Menyimpan rekomendasi AI sebagai **`No/Ditolak`**.        |
|  B6 | Sistem Web             | Menyimpan keputusan Analis sebagai **`Diterima`**.        |
|  B7 | Sistem Web             | Menetapkan status resmi pengajuan menjadi **`Diterima`**. |
|  B8 | System Logging Service | Mencatat aktivitas override pada Audit Trail.             |

**Aturan:** Keputusan final adalah keputusan Analis, sedangkan rekomendasi AI tetap tersimpan sebagai informasi terpisah.

---

## Alur C — ML Engine Timeout / Failure

**Kondisi:** ML Service tidak tersedia atau proses scoring melebihi SLA **5 detik**.

| No. | Aktor/Komponen         | Aktivitas                                                                                   |
| --: | ---------------------- | ------------------------------------------------------------------------------------------- |
|  C1 | Analis                 | Menjalankan proses scoring setelah 4 atribut valid.                                         |
|  C2 | Sistem Web             | Mengirim data scoring ke ML Service.                                                        |
|  C3 | ML Service             | Tidak memberikan respons atau proses melebihi **5 detik**.                                  |
|  C4 | Sistem Web             | Mengidentifikasi kegagalan/timeout scoring.                                                 |
|  C5 | Sistem Web             | Menampilkan pesan bahwa proses scoring AI gagal/timeout dan belum menghasilkan rekomendasi. |
|  C6 | Sistem Web             | **Tidak menetapkan keputusan kredit secara otomatis.**                                      |
|  C7 | System Logging Service | Mencatat kegagalan/timeout pada Audit Trail.                                                |
|  C8 | Analis                 | Dapat melakukan tindak lanjut sesuai proses operasional koperasi.                           |

**Aturan utama:** Kegagalan AI **tidak boleh menghasilkan keputusan `Diterima` atau `Ditolak` secara otomatis**.

---

# 2. ACCEPTANCE CRITERIA

## Skenario 1 — Scoring Berhasil dan Analis Mengonfirmasi Rekomendasi

### AC-01 — Happy Flow

**Given**

* Analis telah login sebagai **Role Analis Kredit**.
* Pengajuan memiliki status **`Pending Review`**.
* **Job, Education, Housing, dan Loan = 4/4 atribut lengkap dan valid**.

**When**

* Analis menjalankan Credit Scoring Engine.
* Decision Tree (ID3) menghasilkan rekomendasi.
* Waktu pemrosesan AI tercatat **≤ 5 detik**.
* Analis mengonfirmasi rekomendasi tersebut sebagai keputusan final.

**Then**

* Sistem menampilkan rekomendasi **`Yes/Diterima`** atau **`No/Ditolak`**.
* Sistem menyimpan rekomendasi AI dan keputusan Analis secara terpisah.
* Status pengajuan berubah sesuai keputusan final Analis.
* Aktivitas scoring dan keputusan tercatat pada Audit Trail.
* AI **tidak menetapkan keputusan final tanpa konfirmasi Analis**.

---

## Skenario 2 — Override Rekomendasi AI

### AC-02 — Override Flow

**Given**

* Analis telah login sebagai **Role Analis Kredit**.
* Pengajuan memiliki status **`Pending Review`**.
* Empat atribut AI **Job, Education, Housing, dan Loan = 4/4 lengkap dan valid**.
* Credit Scoring Engine menghasilkan rekomendasi **`No/Ditolak`**.

**When**

* Analis meninjau rekomendasi tersebut.
* Analis memilih keputusan final **`Diterima`** sebagai override.

**Then**

* Sistem menyimpan rekomendasi AI sebagai **`No/Ditolak`**.
* Sistem menyimpan keputusan final Analis sebagai **`Diterima`**.
* Status resmi pengajuan menjadi **`Diterima`**.
* Sistem mencatat aktivitas override pada Audit Trail.
* Sistem **tidak mengganti rekomendasi AI menjadi `Yes/Diterima`**; rekomendasi dan keputusan final tetap terpisah.

---

## Skenario 3 — Validation & Fallback Flow

### AC-03A — Atribut Tidak Lengkap

**Given**

* Analis telah login.
* Pengajuan berstatus **`Pending Review`**.
* Hanya **3 dari 4 atribut** yang terisi, misalnya Loan belum diisi.

**When**

* Analis mencoba menjalankan Credit Scoring Engine.

**Then**

* Sistem menolak proses scoring.
* Sistem menampilkan pesan bahwa **Loan wajib dilengkapi**.
* Sistem tidak mengirim data scoring ke ML Engine.
* Status keputusan pengajuan tetap **`Pending Review`**.

### AC-03B — ML Service Timeout

**Given**

* Analis telah mengisi **4/4 atribut secara lengkap dan valid**.
* Sistem telah mengirim permintaan scoring ke ML Service.

**When**

* ML Service tidak memberikan hasil dalam waktu **≤ 5 detik** atau service mengalami kegagalan.

**Then**

* Sistem menyatakan proses scoring gagal/timeout.
* Sistem tidak menampilkan hasil `Yes/Diterima` atau `No/Ditolak` sebagai rekomendasi yang valid.
* Sistem **tidak mengubah status pengajuan secara otomatis** dari `Pending Review`.
* Kegagalan tersebut dicatat dalam Audit Trail.

---

# Ringkasan Definition of Done UC-01

UC-01 dinyatakan selesai apabila seluruh kondisi berikut terpenuhi:

| Kriteria                          | Target                                    |
| --------------------------------- | ----------------------------------------- |
| Atribut input                     | **4/4 wajib lengkap dan valid**           |
| Algoritma                         | **Decision Tree (ID3)**                   |
| Output AI                         | `Yes/Diterima` atau `No/Ditolak`          |
| Latensi scoring                   | **≤ 5 detik**                             |
| Keputusan final                   | **Wajib ditetapkan Analis**               |
| Override                          | **Diperbolehkan**                         |
| Rekomendasi AI vs keputusan final | **Tersimpan/ditampilkan terpisah**        |
| Input invalid                     | **Scoring tidak dijalankan**              |
| ML timeout/failure                | **Tidak menghasilkan keputusan otomatis** |
| Audit                             | Aktivitas scoring dan keputusan tercatat  |

**Inti kontrol bisnis UC-01:**

> **4 Atribut Valid → ID3 Scoring → Rekomendasi AI → Review Analis → Konfirmasi/Override → Keputusan Final → Audit Trail**

Model AI berperan sebagai **decision-support tool**, sehingga tidak ada jalur dalam use case ini yang memungkinkan AI menetapkan keputusan kredit final secara mandiri.
