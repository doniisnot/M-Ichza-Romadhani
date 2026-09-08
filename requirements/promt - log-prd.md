[Peran]
Kamu adalah Senior Product Manager untuk produk Web-Based Enterprise System berfitur AI/Machine Learning.

[Tugas]
Susun DRAF PRD ringkas untuk "Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (Credit Scoring Engine)" berdasarkan konteks riset di bawah ini.

[Konteks]
  Problem statement : Penilaian pengajuan pinjaman koperasi secara manual memerlukan waktu lama, rentan kesalahan hitung (human error), dan subjektif. Pengambil keputusan kesulitan menentukan kelayakan kredit anggota secara konsisten dan akurat, sehingga berisiko meningkatkan kecacatan/kegagalan kredit (non-performing loan).
  Target user       : Pengurus/Pengelola Koperasi (Admin & Analis Kredit/Pengambil Keputusan) dan Anggota/Nasabah Koperasi.
  Stakeholder lain    : Ketua/Manajemen Koperasi, Tim Pengembang IT (Engineer/Data Analyst), dan Auditor Keuangan.
  Persona ringkas     : 
    1. Pak Budi (50 th, Pengelola/Admin Koperasi): Menginginkan proses validasi pengajuan kredit yang cepat, objektif, dan otomatis tanpa perlu menghitung rasio risik secara manual.
    2. Mbak Siti (32 th, Anggota Koperasi): Menginginkan transparansi status pengajuan pinjaman dan kepastian hasil keputusan yang cepat dan adil.
  Bukti riset         : 
    - Pengujian model Decision Tree (Algoritma ID3) menggunakan 50 dataset Bank Marketing UCI (25 data latih, 25 data uji) menghasilkan performa: Akurasi 80%, Spesifikasi 90.90%, dan Sensitivitas 71.42%.
    - Penilaian berbasis aturan (rule-based Decision Tree) terbukti lebih akurat dan konsisten dibandingkan perkiraan penilaian individu/manual.
    - Evaluasi keputusan didasarkan pada 4 atribut utama: Job (pekerjaan), Education (pendidikan), Housing (status cicilan rumah), dan Loan (status hutang/pinjaman lain).
  Platform & stack    : Website (Web Application) — PHP/Laravel/CodeIgniter, MySQL DB, Python ML Service (Scikit-Learn/ID3 Decision Tree Engine).
  Fitur AI inti       : Engine Penilai Kelayakan Kredit Otomatis (Automatic Credit Scoring & Risk Assessment Engine) berbasis Algoritma Decision Tree (ID3) dengan atribut: Job, Education, Housing, dan Loan.
  Konstrain           : Prototype diproduksi dalam waktu 1 semester; dataset pelatihan awal terbatas (25 data latih); biaya komputasi AI minim (hanya menggunakan ML ringan/Decision Tree tanpa GPU mahal); sistem belum tervalidasi secara penuh di skala produksi masif.

[Format Output]
  1) Ringkasan Eksekutif;
  2) Problem Statement & Bukti (Pisahkan FAKTA dari jurnal vs ASUMSI);
  3) Target User & Stakeholder (Tabel: Peran – Kebutuhan – Pengaruh);
  4) Value Proposition: Pain yang dikurangi, Gain yang diciptakan, Mengapa fitur AI (Decision Tree) bukan sekadar gimmick;
  5) Tujuan Produk & KPI Terukur (+ Cara mengukurnya);
  6) Scope Fitur 3 Bulan: Tabel MoSCoW (Fitur AI diberi tanda ★);
  7) Non-Goals Eksplisit;
  8) Asumsi & Risiko Utama + Mitigasi.

[Aturan]
  - Hanya gunakan data pada [Konteks] di atas; jika ada informasi pendukung yang kurang, tulis [ASUMSI-XX] lalu lanjutkan penjelasannya.
  - JANGAN menulis solusi teknis/arsitektur mendalam seperti HLD/LLD/ERD (itu urusan SRS/Engineering). Focus pada aspek Product Management & Business/User Value.
  - Gunakan Bahasa Indonesia baku dan format Markdown yang rapi.
