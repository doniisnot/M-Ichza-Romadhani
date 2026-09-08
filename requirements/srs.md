# DRAF SRS

## Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (*Credit Scoring Engine*)

**Status:** Draft
**Platform:** Web Application
**Metode AI:** Decision Tree — ID3
**Prinsip prioritas:** MoSCoW
**Acuan kualitas:** ISO/IEC 25010
**Batasan:** AI sebagai *decision-support tool*, keputusan final oleh analis/pengambil keputusan manusia.

---

# 1. TUJUAN, SCOPE, DAN DEFINISI ISTILAH

## 1.1 Tujuan Dokumen SRS

Dokumen ini mendefinisikan kebutuhan perangkat lunak untuk **Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (*Credit Scoring Engine*)**.

SRS digunakan sebagai acuan bagi pengembang, analis sistem, penguji, dan stakeholder dalam memahami **fungsi, batasan, kebutuhan kualitas, data minimum, serta aturan bisnis** sistem.

Dokumen ini tidak membahas rancangan arsitektur secara mendalam, desain antarmuka, maupun struktur database tingkat detail.

---

## 1.2 Scope Sistem

Sistem mencakup:

1. Manajemen data anggota koperasi.
2. Pengajuan pinjaman oleh anggota.
3. Pengelolaan data pengajuan pinjaman.
4. Input empat atribut yang digunakan oleh model AI:

   * Job
   * Education
   * Housing
   * Loan
5. ★ Proses *Automatic Credit Scoring Engine* menggunakan Decision Tree (ID3).
6. ★ Penampilan rekomendasi hasil model kepada analis.
7. Konfirmasi/override keputusan oleh analis.
8. Pelacakan status pengajuan.
9. Audit trail aktivitas terkait pengajuan dan keputusan.
10. Pelaporan pengajuan dan hasil penilaian.

Sistem **tidak menjadikan AI sebagai pengambil keputusan kredit secara mandiri**.

---

## 1.3 Definisi Istilah dan Singkatan

| Istilah                   | Definisi                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| **SRS**                   | *Software Requirements Specification*, dokumen spesifikasi kebutuhan perangkat lunak.        |
| **AI**                    | *Artificial Intelligence*, teknologi kecerdasan buatan.                                      |
| **Credit Scoring**        | Proses penilaian kelayakan kredit berdasarkan data tertentu.                                 |
| **Decision Tree**         | Metode klasifikasi berbentuk struktur percabangan berdasarkan atribut input.                 |
| **ID3**                   | *Iterative Dichotomiser 3*, algoritma pembentukan Decision Tree berbasis *information gain*. |
| **ML**                    | *Machine Learning*, metode pembelajaran mesin dari data.                                     |
| **TP**                    | *True Positive*, data positif yang diklasifikasikan positif dengan benar.                    |
| **TN**                    | *True Negative*, data negatif yang diklasifikasikan negatif dengan benar.                    |
| **FP**                    | *False Positive*, data negatif yang diklasifikasikan positif.                                |
| **FN**                    | *False Negative*, data positif yang diklasifikasikan negatif.                                |
| **Akurasi**               | Proporsi prediksi model yang benar dari seluruh data pengujian.                              |
| **Sensitivitas**          | Kemampuan model mengidentifikasi kelas positif dengan benar.                                 |
| **Spesifikasi**           | Kemampuan model mengidentifikasi kelas negatif dengan benar.                                 |
| **MoSCoW**                | Metode prioritas kebutuhan: Must, Should, Could, Won't.                                      |
| **Scoring Engine**        | Komponen sistem yang menghasilkan klasifikasi/rekomendasi kelayakan berdasarkan model AI.    |
| **Decision-support tool** | Alat bantu yang memberikan rekomendasi kepada manusia, bukan menggantikan keputusan manusia. |
| **Override**              | Tindakan analis untuk menetapkan keputusan akhir yang berbeda dari rekomendasi AI.           |
| **Audit Trail**           | Catatan aktivitas atau perubahan yang dapat digunakan untuk penelusuran proses.              |

---

# 2. KEBUTUHAN UMUM & LINGKUNGAN OPERASI

## 2.1 Target User & Stakeholder

| Peran                                 | Kebutuhan Sistem                                                      | Pengaruh      |
| ------------------------------------- | --------------------------------------------------------------------- | ------------- |
| **Anggota/Nasabah**                   | Mengajukan pinjaman dan melihat status pengajuan sendiri              | Tinggi        |
| **Admin/Pengelola**                   | Mengelola data anggota dan pengajuan                                  | Tinggi        |
| **Analis Kredit/Pengambil Keputusan** | Memproses pengajuan dan menggunakan rekomendasi AI sebagai alat bantu | Sangat Tinggi |
| **Ketua/Manajemen Koperasi**          | Memantau proses dan hasil pengajuan                                   | Tinggi        |
| **Tim Engineer/Data Analyst**         | Mengelola dan mengembangkan sistem/model                              | Sedang–Tinggi |
| **Auditor Keuangan**                  | Menelusuri proses dan hasil pengajuan                                 | Sedang        |

---

## 2.2 Lingkungan Operasi

| Komponen               | Kebutuhan                                                                   |
| ---------------------- | --------------------------------------------------------------------------- |
| **Platform**           | Web Application                                                             |
| **Web Browser**        | Browser web yang mendukung aplikasi web modern — **[ASUMSI-SRS-01]**        |
| **Web Server**         | PHP/Laravel                                                                 |
| **Database**           | MySQL                                                                       |
| **ML Engine Service**  | Python dengan Scikit-Learn dan Decision Tree/ID3                            |
| **Perangkat pengguna** | Komputer/perangkat yang dapat menjalankan web browser — **[ASUMSI-SRS-02]** |

Detail konfigurasi server, topologi jaringan, API internal, dan struktur database **tidak termasuk dalam SRS ringkas ini**.

---

## 2.3 Asumsi & Dependensi Operasional

1. **[ASUMSI-SRS-03]** Pengguna memiliki akses ke browser dan jaringan yang diperlukan untuk mengakses aplikasi.
2. Sistem bergantung pada ketersediaan database MySQL.
3. Sistem bergantung pada ketersediaan ML Engine Service ketika proses scoring dilakukan.
4. Data yang digunakan untuk scoring harus memenuhi format atribut yang ditentukan.
5. Dataset baseline yang digunakan dalam konteks riset terdiri dari 50 sampel, dengan 25 data latih dan 25 data uji.
6. Performa baseline tidak dianggap sebagai jaminan performa sistem pada kondisi produksi.

---

# 3. KEBUTUHAN FUNGSIONAL (*FUNCTIONAL REQUIREMENTS*)

| ID FR     | Prioritas | Pernyataan Kebutuhan                                                                                                                                                   | Metode Verifikasi |
| --------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| **FR-01** | MUST      | Sistem harus dapat mengelola data anggota saat admin melakukan proses manajemen anggota → data anggota tersimpan/terbarui.                                             | Test              |
| **FR-02** | MUST      | Sistem harus dapat menerima pengajuan pinjaman saat anggota mengisi data pengajuan → pengajuan tercatat dengan status awal.                                            | Test              |
| **FR-03** | MUST      | Sistem harus dapat menampilkan daftar pengajuan saat admin/analis mengakses modul pengajuan → daftar pengajuan yang dapat diakses ditampilkan.                         | Demonstration     |
| **FR-04** | MUST      | Sistem harus dapat menerima empat atribut AI saat analis melakukan proses penilaian → Job, Education, Housing, dan Loan tersimpan sebagai input scoring.               | Test              |
| **FR-05** | MUST ★    | Sistem harus dapat menjalankan *Credit Scoring Engine* saat keempat atribut AI telah lengkap dan valid → model Decision Tree (ID3) menghasilkan klasifikasi kelayakan. | Test              |
| **FR-06** | MUST ★    | Sistem harus dapat mengirimkan data empat atribut ke proses scoring saat analis menjalankan penilaian → hasil scoring diterima oleh sistem.                            | Test              |
| **FR-07** | MUST ★    | Sistem harus dapat menampilkan rekomendasi AI saat proses scoring berhasil → rekomendasi **Yes/Diterima** atau **No/Ditolak** ditampilkan kepada analis.               | Demonstration     |
| **FR-08** | SHOULD ★  | Sistem harus dapat menampilkan atribut dasar yang digunakan model saat rekomendasi AI diberikan → analis dapat mengetahui dasar atribut yang digunakan.                | Demonstration     |
| **FR-09** | MUST      | Sistem harus dapat menerima keputusan analis saat analis melakukan konfirmasi hasil pengajuan → keputusan akhir tersimpan.                                             | Test              |
| **FR-10** | MUST      | Sistem harus dapat menerima override terhadap rekomendasi AI saat analis menetapkan keputusan yang berbeda → keputusan analis menjadi keputusan akhir.                 | Test              |
| **FR-11** | MUST      | Sistem harus dapat memperbarui status pengajuan saat keputusan pengajuan ditetapkan → status pengajuan diperbarui sesuai keputusan.                                    | Test              |
| **FR-12** | MUST      | Sistem harus dapat menampilkan status pengajuan saat anggota melihat riwayat pengajuannya → hanya status pengajuan milik anggota tersebut ditampilkan.                 | Test              |
| **FR-13** | MUST      | Sistem harus dapat menampilkan seluruh pengajuan saat analis mengakses daftar pengajuan → seluruh pengajuan yang menjadi kewenangannya ditampilkan.                    | Demonstration     |
| **FR-14** | MUST      | Sistem harus dapat mencatat aktivitas penting saat proses pengajuan, scoring, atau keputusan dilakukan → aktivitas tercatat dalam audit trail.                         | Inspection        |
| **FR-15** | SHOULD    | Sistem harus dapat menghasilkan laporan pengajuan saat pengguna berwenang meminta laporan → laporan pengajuan dan hasil penilaian ditampilkan.                         | Demonstration     |
| **FR-16** | COULD     | Sistem harus dapat menampilkan metrik performa model saat pengguna berwenang membuka informasi performa AI → metrik baseline ditampilkan.                              | Demonstration     |
| **FR-17** | COULD     | Sistem harus dapat menyediakan pencarian pengajuan saat pengguna berwenang mencari pengajuan → pengajuan yang sesuai kriteria pencarian ditampilkan.                   | Test              |

### Catatan Prioritas

* **MUST:** fungsi minimum agar sistem dapat menjalankan proses koperasi dan credit scoring.
* **SHOULD:** penting untuk meningkatkan transparansi dan operasional, tetapi tidak menghambat fungsi utama prototype.
* **COULD:** fitur tambahan yang dapat dikembangkan jika waktu 3 bulan memungkinkan.
* **WON'T:** tidak terdapat dalam scope prototype saat ini.

---

# 4. KEBUTUHAN NON-FUNGSIONAL (*NON-FUNCTIONAL REQUIREMENTS*)

| ID NFR     | Kategori ISO/IEC 25010         | Metrik & Target Terukur                                                                                                                              | Kondisi Pengukuran                                                       |
| ---------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **NFR-01** | Functional Suitability         | Model menghasilkan klasifikasi berdasarkan 4 atribut yang ditentukan                                                                                 | Pengujian fungsi scoring                                                 |
| **NFR-02** | Functional Suitability         | **Baseline akurasi AI = 80%**                                                                                                                        | Dataset baseline 50 sampel dengan 25 data latih dan 25 data uji          |
| **NFR-03** | Functional Suitability         | **Baseline sensitivitas = 71,42%**                                                                                                                   | Evaluasi terhadap dataset uji                                            |
| **NFR-04** | Functional Suitability         | **Baseline spesifikasi = 90,90%**                                                                                                                    | Evaluasi terhadap dataset uji                                            |
| **NFR-05** | Performance Efficiency         | Latensi AI Engine **≤ 5 detik/scoring**                                                                                                              | Diukur sejak permintaan scoring dijalankan sampai hasil scoring diterima |
| **NFR-06** | Usability                      | Analis dapat memahami hasil rekomendasi dan atribut dasar yang digunakan model                                                                       | Pengujian penggunaan oleh analis — **[ASUMSI-SRS-04]**                   |
| **NFR-07** | Usability                      | Indikator rekomendasi menggunakan istilah yang dapat dipahami pengguna target                                                                        | Inspection/Demonstration                                                 |
| **NFR-08** | Security                       | Sistem menyediakan autentikasi pengguna                                                                                                              | Test                                                                     |
| **NFR-09** | Security                       | Akses sistem dibatasi berdasarkan role pengguna                                                                                                      | Test role-based access                                                   |
| **NFR-10** | Security                       | Data pengajuan kredit hanya dapat diakses oleh pengguna sesuai kewenangannya                                                                         | Test                                                                     |
| **NFR-11** | Data Privacy & Confidentiality | Data pribadi dan finansial anggota harus dilindungi menggunakan enkripsi — **[ASUMSI-SRS-05: metode/standar enkripsi ditentukan pada tahap desain]** | Inspection/Test                                                          |
| **NFR-12** | Data Privacy & Confidentiality | Anggota tidak dapat mengakses data pengajuan anggota lain                                                                                            | Test                                                                     |
| **NFR-13** | Reliability                    | Sistem mempertahankan data pengajuan dan hasil keputusan setelah proses berhasil — **[ASUMSI-SRS-06]**                                               | Test                                                                     |
| **NFR-14** | Reliability                    | Kegagalan proses scoring tidak boleh mengubah keputusan final secara otomatis                                                                        | Test                                                                     |
| **NFR-15** | Maintainability                | Model dan aplikasi dapat diperbarui tanpa mengubah tujuan fungsional utama sistem — **[ASUMSI-SRS-07]**                                              | Inspection                                                               |
| **NFR-16** | Maintainability                | Perubahan model dapat dibedakan dari keputusan analis — **[ASUMSI-SRS-08]**                                                                          | Inspection                                                               |

> **Catatan:** ISO/IEC 25010 digunakan sebagai kerangka karakteristik kualitas. Target yang belum diberikan dalam konteks ditandai `[ASUMSI-SRS-XX]` dan harus divalidasi sebelum menjadi acceptance criteria final.

---

# 5. KEBUTUHAN DATA MINIMUM FITUR AI

## 5.1 Struktur Input Model

Model menggunakan **empat atribut utama**:

| Atribut       | Tipe    | Nilai/Keterangan           |
| ------------- | ------- | -------------------------- |
| **Job**       | Nominal | Jenis pekerjaan anggota    |
| **Education** | Nominal | Tingkat pendidikan anggota |
| **Housing**   | Enum    | `Yes` / `No`               |
| **Loan**      | Enum    | `Yes` / `No`               |

Keempat atribut tersebut wajib tersedia sebelum proses scoring dapat dijalankan.

---

## 5.2 Output Model

Output minimum:

| Output                    | Nilai                                |
| ------------------------- | ------------------------------------ |
| **Klasifikasi Kelayakan** | `Yes / Diterima` atau `No / Ditolak` |

Persentase/skor relevansi **tidak ditetapkan dalam konteks riset**.

Oleh karena itu:

> **[ASUMSI-SRS-09]** Jika sistem menampilkan skor/persentase relevansi, format dan interpretasinya harus ditentukan melalui validasi model sebelum digunakan sebagai dasar keputusan.

---

## 5.3 Validasi Input

Sistem harus:

1. Memastikan **Job** terisi.
2. Memastikan **Education** terisi.
3. Memastikan **Housing** memiliki nilai `Yes` atau `No`.
4. Memastikan **Loan** memiliki nilai `Yes` atau `No`.
5. Menolak proses scoring apabila salah satu atribut tidak lengkap atau tidak valid.
6. Memberikan informasi bahwa data harus diperbaiki sebelum scoring dapat dijalankan.

Hal tersebut selaras dengan **BR-02**.

---

# 6. ATURAN BISNIS (*BUSINESS RULES*)

### BR-01 — Keputusan Final

**Sistem tidak boleh menyetujui atau menolak pinjaman secara otomatis berdasarkan output AI tanpa konfirmasi manusia.**

Output AI hanya merupakan rekomendasi.

**Keputusan final = keputusan analis/pengambil keputusan.**

---

### BR-02 — Kelengkapan Atribut

**Proses scoring AI hanya dapat dijalankan jika Job, Education, Housing, dan Loan telah terisi lengkap dan valid.**

Jika salah satu atribut tidak memenuhi validasi, proses scoring tidak dijalankan.

---

### BR-03 — Aksesibilitas Data

* Anggota hanya dapat melihat **status pengajuan miliknya sendiri**.
* Analis dapat melihat pengajuan yang menjadi kewenangannya, sesuai kebutuhan sistem yang ditetapkan.

---

### BR-04 — Transparansi Aturan

**Sistem harus menampilkan atribut dasar yang digunakan model saat memberikan rekomendasi.**

Hal ini bertujuan agar rekomendasi AI dapat dipahami sebagai hasil evaluasi berdasarkan data yang dimasukkan, bukan sebagai keputusan yang muncul tanpa dasar.

---

### BR-05 — Override Keputusan

**Analis dapat menetapkan keputusan akhir yang berbeda dari rekomendasi AI.**

Keputusan analis menjadi keputusan final sistem.

---

### BR-06 — Pemisahan Rekomendasi dan Keputusan

**Sistem harus membedakan hasil rekomendasi AI dengan keputusan final analis.**

Dengan demikian, rekomendasi `Yes/Diterima` dari AI tidak secara otomatis berarti pinjaman telah disetujui.

---

# 7. MATRIKS TRACEABILITY

| ID FR/NFR     | Fitur PRD / Bukti Riset Terkait                       | Target User                    |
| ------------- | ----------------------------------------------------- | ------------------------------ |
| **FR-01**     | Manajemen anggota                                     | Admin, Anggota                 |
| **FR-02**     | Pengajuan pinjaman                                    | Anggota                        |
| **FR-03**     | Pengelolaan pengajuan                                 | Admin, Analis                  |
| **FR-04**     | Empat atribut AI: Job, Education, Housing, Loan       | Analis                         |
| **FR-05**     | ★ Automatic Credit Scoring Engine — Decision Tree ID3 | Analis                         |
| **FR-06**     | ★ Proses scoring menggunakan atribut riset            | Analis                         |
| **FR-07**     | ★ Display rekomendasi AI                              | Analis                         |
| **FR-08**     | Transparansi atribut/model                            | Analis, Auditor                |
| **FR-09**     | Keputusan final oleh manusia                          | Analis/Pengambil Keputusan     |
| **FR-10**     | Override keputusan AI                                 | Analis/Pengambil Keputusan     |
| **FR-11**     | Tracking status pengajuan                             | Anggota, Analis                |
| **FR-12**     | Anggota melihat status pengajuan sendiri              | Anggota                        |
| **FR-13**     | Analis melihat pengajuan                              | Analis                         |
| **FR-14**     | Audit trail                                           | Analis, Manajemen, Auditor     |
| **FR-15**     | Reporting                                             | Manajemen, Auditor             |
| **FR-16**     | Baseline performa AI                                  | Tim IT/Data Analyst, Manajemen |
| **FR-17**     | Pengelolaan/pencarian pengajuan                       | Admin, Analis                  |
| **NFR-01**    | Fungsi Credit Scoring berbasis 4 atribut              | Analis                         |
| **NFR-02**    | Baseline akurasi **80%**                              | Analis, Tim Data Analyst       |
| **NFR-03**    | Baseline sensitivitas **71,42%**                      | Tim Data Analyst               |
| **NFR-04**    | Baseline spesifikasi **90,90%**                       | Tim Data Analyst               |
| **NFR-05**    | Latensi AI ≤ **5 detik/scoring**                      | Analis                         |
| **NFR-06–07** | Kemudahan memahami rekomendasi                        | Analis                         |
| **NFR-08–10** | Autentikasi, otorisasi, proteksi data kredit          | Semua pengguna                 |
| **NFR-11–12** | Data Privacy & Confidentiality                        | Anggota, Admin, Analis         |
| **NFR-13–14** | Reliability                                           | Admin, Analis, Manajemen       |
| **NFR-15–16** | Maintainability                                       | Tim IT/Data Analyst            |

---

## Ringkasan Acceptance Scope Prototype

Secara ringkas, prototype SRS ini dianggap memenuhi **scope utama** apabila alur berikut dapat berjalan:

**Anggota → Pengajuan Pinjaman → Pengisian 4 Atribut → ★ ID3 Credit Scoring → Rekomendasi AI → Review Analis → Keputusan Final → Tracking Status → Audit/Reporting**

Dengan ketentuan paling penting:

> **AI memberikan rekomendasi, sedangkan keputusan kredit tetap dibuat dan dikonfirmasi oleh manusia.**

Baseline model yang digunakan adalah **akurasi 80%, sensitivitas 71,42%, dan spesifikasi 90,90%** berdasarkan 50 sampel dengan pembagian 25 data latih dan 25 data uji. Nilai tersebut merupakan **baseline riset**, bukan klaim performa produksi.
