[Peran]
Kamu adalah requirements analyst senior untuk pengembangan sistem enterprise berbasis web dan Machine Learning.

[Tugas]
Ubah DRAF PRD berikut menjadi DRAF SRS (Software Requirements Specification) ringkas, presisi, dan terstruktur sesuai standar ISO/IEC 25010 dan prinsip MoSCoW.

[Konteks]
  PRD Hasil Revisi :
  - Nama Produk: Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (Credit Scoring Engine).
  - Platform & Stack: Web Application (PHP/Laravel, MySQL DB, Python ML Service untuk ID3 Decision Tree).
  - Fitur AI Inti: Automatic Credit Scoring Engine berbasis Decision Tree (ID3) dengan 4 atribut: Job (pekerjaan), Education (pendidikan), Housing (status cicilan rumah), dan Loan (status hutang lain).
  - Bukti Riset & Baseline: Dataset 50 sampel Bank Marketing UCI (25 data latih, 25 data uji). Performa baseline model: Akurasi 80%, Spesifikasi 90.90%, Sensitivitas 71.42%.
  - Batasan Utama: Decision Tree berfungsi sebagai *decision-support tool* (alat bantu keputusan), BUKAN *decision-maker* mandiri. Keputusan akhir tetap berada di tangan analis/pengambil keputusan manusia.

[Format Output SRS]

1. TUJUAN, SCOPE, DAN DEFINISI ISTILAH
   - Tujuan Dokumen SRS.
   - Scope Sistem (Batas-batas fungsionalitas sistem informasi koperasi simpan pinjam).
   - Tabel Definisi Istilah & Singkatan (misal: ID3, TP, TN, FP, FN, Credit Scoring, Decision Tree, MoSCoW, SRS).

2. KEBUTUHAN UMUM & LINGKUNGAN OPERASI
   - Target User & Stakeholder (Tabel: Peran – Kebutuhan Sistem – Pengaruh).
   - Lingkungan Operasi (Spesifikasi platform Web Browser, Web Server, ML Engine Service, & Database).
   - Asumsi & Dependensi Operasional.

3. KEBUTUHAN FUNGSIONAL (FUNCTIONAL REQUIREMENTS / FR)
   - Gunakan format tabel: ID FR | Prioritas (MoSCoW) | Pernyataan Kebutuhan | Metode Verifikasi (Test/Demonstration/Inspection/Analysis).
   - Gunakan POLA KETAT: "Sistem harus dapat <aksi> <objek> saat <kondisi> → <output>".
   - Sertakan ID FR dari FR-01 hingga FR-n (Mencakup: Manajemen Anggota, Pengajuan Pinjaman, Input Atribut AI, Running Scoring Engine, Display Rekomendasi AI, Override/Keputusan Analis, Tracking Status, Audit Trail, & Reporting).

4. KEBUTUHAN NON-FUNGSIONAL (NON-FUNCTIONAL REQUIREMENTS / NFR)
   - Gunakan format tabel: ID NFR | Kategori ISO/IEC 25010 | Metrik & Target Terukur | Kondisi Pengukuran.
   - WAJIB Memuat Kategori ISO/IEC 25010 berikut:
     * Functional Suitability & Performance Efficiency (Kinerja & Akurasi AI Engine: Baseline Akurasi 80%, Latensi AI Engine ≤ 5 detik per scoring).
     * Usability (Kemudahan pemahaman indikator/faktor penilai bagi analis).
     * Security (Autentikasi, otorisasi role-based access, proteksi data kredit).
     * Data Privacy & Confidentiality (Enkripsi data pribadi & finansial anggota).
     * Reliability & Maintainability.

5. KEBUTUHAN DATA MINIMUM FITUR AI
   - Definisi Struktur Input Model (4 Atribut: Job [Nominal], Education [Nominal], Housing [Enum: Yes/No], Loan [Enum: Yes/No]).
   - Definisi Output Model (Klasifikasi Kelayakan: [Yes / Diterima] atau [No / Ditolak], serta persentase/skor relevansi jika ada).
   - Skema validasi & penanganan data input yang tidak lengkap/invalid.

6. ATURAN BISNIS (BUSINESS RULES / BR)
   - BR-01: Keputusan Final (Sistem tidak boleh menyetujui/menolak pinjaman secara otomatis tanpa konfirmasi manusia).
   - BR-02: Kelengkapan Atribut (Proses scoring AI hanya dapat dijalankan jika ke-4 atribut terisi lengkap).
   - BR-03: Aksesibilitas Data (Anggota hanya dapat melihat status pengajuan milik sendiri; Analis dapat melihat seluruh pengajuan).
   - BR-04: Transparansi Aturan (Sistem harus menampilkan atribut dasar yang digunakan model saat memberikan rekomendasi).

7. MATRIKS TRACEABILITY (KETERATURAN)
   - Tabel pemetaan yang menghubungkan: [ID FR / ID NFR] ↔ [Fitur PRD / Bukti Riset Terkait] ↔ [Target User].

[Aturan Penulisan SRS]
  - DILARANG MENAMBAH KEBUTUHAN DI LUAR CONTEXT/PRD TANPA BUKTI ATAU LABEL [ASUMSI-SRS-XX].
  - Hentikan pembahasan jika mulai masuk ke detail arsitektur teknis/UI design/database schema (karena itu merupakan domain HLD/LLD/SRS Detail).
  - Gunakan Bahasa Indonesia baku, ilmiah, dan format Markdown yang rapi.