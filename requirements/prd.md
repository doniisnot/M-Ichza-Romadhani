# DRAF PRD — Sistem Informasi Koperasi Simpan Pinjam Berbasis AI

### *Credit Scoring Engine*

> **Status:** Draft PRD
> **Horizon:** Prototype 3 bulan
> **Platform:** Web Application
> **Fokus utama:** Otomatisasi dan konsistensi penilaian kelayakan kredit menggunakan Decision Tree (ID3)

---

## 1. Ringkasan Eksekutif

Sistem Informasi Koperasi Simpan Pinjam Berbasis AI (*Credit Scoring Engine*) merupakan aplikasi berbasis web yang dirancang untuk membantu pengurus dan analis kredit koperasi melakukan **penilaian kelayakan pengajuan pinjaman secara lebih cepat, objektif, dan konsisten**.

Masalah utama yang ingin diselesaikan adalah proses penilaian kredit secara manual yang membutuhkan waktu, berpotensi menimbulkan *human error*, dan dapat menghasilkan keputusan yang subjektif.

Fitur utama produk adalah **★ Automatic Credit Scoring & Risk Assessment Engine** menggunakan algoritma **Decision Tree (ID3)** dengan empat atribut utama:

* **Job** — pekerjaan
* **Education** — pendidikan
* **Housing** — status cicilan rumah
* **Loan** — status hutang/pinjaman lain

Berdasarkan bukti riset yang diberikan, pengujian pada 50 dataset Bank Marketing UCI dengan 25 data latih dan 25 data uji menghasilkan **akurasi 80%, spesifikasi 90,90%, dan sensitivitas 71,42%**.

Namun, hasil tersebut masih merupakan **bukti awal**, bukan validasi bahwa model sudah siap digunakan sebagai pengambil keputusan kredit secara mandiri pada kondisi produksi.

---

# 2. Problem Statement & Bukti

### Problem Statement

> **Pengurus dan analis kredit koperasi membutuhkan cara yang lebih cepat, konsisten, dan terukur untuk menilai kelayakan pengajuan pinjaman karena proses manual berpotensi memakan waktu, menimbulkan kesalahan perhitungan, dan menghasilkan keputusan yang subjektif.**

### Fakta vs Asumsi

| Jenis             | Pernyataan                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **FAKTA — Riset** | Pengujian Decision Tree (ID3) pada 50 dataset Bank Marketing UCI menggunakan 25 data latih dan 25 data uji menghasilkan akurasi 80%. |
| **FAKTA — Riset** | Spesifikasi model sebesar 90,90%.                                                                                                    |
| **FAKTA — Riset** | Sensitivitas model sebesar 71,42%.                                                                                                   |
| **FAKTA — Riset** | Penilaian berbasis aturan Decision Tree dinyatakan lebih akurat dan konsisten dibandingkan perkiraan penilaian individu/manual.      |
| **FAKTA — Riset** | Empat atribut yang digunakan adalah Job, Education, Housing, dan Loan.                                                               |
| **ASUMSI-01**     | Penggunaan sistem akan mengurangi waktu yang diperlukan analis dalam melakukan penilaian kredit.                                     |
| **ASUMSI-02**     | Pengurus koperasi bersedia menggunakan rekomendasi AI sebagai alat bantu pengambilan keputusan.                                      |
| **ASUMSI-03**     | Data pengajuan anggota dapat diperoleh dan diinput secara konsisten ke dalam sistem.                                                 |
| **ASUMSI-04**     | Empat atribut tersebut cukup relevan untuk membangun prototype penilaian kelayakan kredit.                                           |
| **ASUMSI-05**     | Hasil model dapat ditampilkan dengan cara yang mudah dipahami oleh analis kredit.                                                    |

**Catatan Product Management:**
Akurasi 80% pada dataset kecil tidak boleh diterjemahkan sebagai “sistem memiliki jaminan keputusan kredit 80% benar di koperasi”. Validasi dengan data koperasi yang lebih relevan masih diperlukan.

---

# 3. Target User & Stakeholder

| Peran                                 | Kebutuhan                                                                       | Pengaruh      |
| ------------------------------------- | ------------------------------------------------------------------------------- | ------------- |
| **Pengelola/Admin — Pak Budi**        | Validasi pengajuan lebih cepat dan mengurangi perhitungan manual                | Tinggi        |
| **Analis Kredit/Pengambil Keputusan** | Mendapatkan penilaian dan rekomendasi yang konsisten                            | Tinggi        |
| **Anggota/Nasabah — Mbak Siti**       | Mengetahui status pengajuan dan memperoleh kepastian hasil dengan lebih cepat   | Tinggi        |
| **Ketua/Manajemen Koperasi**          | Memastikan proses kredit berjalan konsisten dan mendukung pengambilan keputusan | Tinggi        |
| **Tim IT/Engineer/Data Analyst**      | Menjaga sistem dan mengembangkan model berdasarkan kebutuhan produk             | Sedang–Tinggi |
| **Auditor Keuangan**                  | Mendapatkan informasi proses dan hasil penilaian yang dapat ditelusuri          | Sedang        |

---

# 4. Value Proposition

### A. Pain yang Dikurangi

**Untuk pengurus/analis:**

* Mengurangi pekerjaan penilaian secara manual.
* Mengurangi risiko kesalahan perhitungan.
* Mengurangi ketergantungan pada perkiraan individu.
* Mengurangi ketidakkonsistenan dalam proses penilaian.

**Untuk anggota:**

* Mengurangi ketidakpastian mengenai status pengajuan.
* Mempercepat proses memperoleh informasi hasil pengajuan.
* Meningkatkan transparansi proses.

### B. Gain yang Diciptakan

* Penilaian kelayakan dapat dilakukan secara lebih terstruktur.
* Analis mendapatkan rekomendasi berbasis aturan/model.
* Keputusan dapat menggunakan kriteria yang sama antar pengajuan.
* Status pengajuan dapat dipantau anggota.
* Manajemen mendapatkan proses penilaian yang lebih terdokumentasi.

### C. Mengapa Decision Tree bukan sekadar gimmick?

Decision Tree memiliki hubungan langsung dengan masalah bisnis karena **mengubah atribut pengajuan menjadi aturan penilaian yang dapat digunakan secara konsisten**.

Dalam konteks prototype ini, AI bukan hanya ditampilkan sebagai fitur tambahan, tetapi digunakan untuk:

> **Input data anggota → evaluasi berdasarkan atribut → menghasilkan penilaian/rekomendasi kelayakan → membantu analis mengambil keputusan.**

Selain itu, hasil riset menunjukkan performa awal **akurasi 80%**, sehingga terdapat bukti awal bahwa pendekatan tersebut dapat digunakan sebagai *decision-support tool*.

**Posisi produk:** AI berfungsi sebagai **alat bantu keputusan**, bukan pengganti pengambil keputusan manusia.

---

# 5. Tujuan Produk & KPI Terukur

| Tujuan                                                        | KPI                                                                        |           Target Prototype | Cara Mengukur                                            |
| ------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------: | -------------------------------------------------------- |
| Mempercepat proses penilaian                                  | Waktu rata-rata dari pengajuan hingga rekomendasi AI                       |  **[ASUMSI-06] ≤ 5 menit** | Catat timestamp mulai dan selesai proses penilaian       |
| Mengurangi kesalahan manual                                   | Persentase penilaian yang membutuhkan koreksi akibat kesalahan perhitungan | **[ASUMSI-07] Turun ≥20%** | Bandingkan proses manual dengan proses berbantuan sistem |
| Meningkatkan konsistensi                                      | Persentase pengajuan yang dinilai menggunakan kriteria yang sama           |       **[ASUMSI-08] ≥95%** | Audit data dan aturan penilaian                          |
| Mengukur performa model                                       | Akurasi                                                                    |           **Baseline 80%** | Evaluasi dataset pengujian                               |
| Mengukur kemampuan mendeteksi kelas tertentu                  | Sensitivitas                                                               |        **Baseline 71,42%** | Evaluasi hasil klasifikasi                               |
| Mengukur kemampuan menghindari klasifikasi positif yang salah | Spesifikasi                                                                |        **Baseline 90,90%** | Evaluasi hasil klasifikasi                               |
| Meningkatkan transparansi anggota                             | Persentase anggota yang dapat melihat status pengajuan                     |       **[ASUMSI-09] ≥95%** | Pengujian fungsional sistem                              |
| Mengukur penggunaan AI                                        | Persentase pengajuan yang berhasil memperoleh hasil penilaian AI           |       **[ASUMSI-10] ≥90%** | Log penggunaan fitur AI                                  |

> **Catatan:** Target yang diberi `[ASUMSI]` adalah target produk awal yang perlu divalidasi dengan koperasi. Angka performa model 80%, 90,90%, dan 71,42% merupakan **baseline dari bukti riset**, bukan target produksi.

---

# 6. Scope Fitur 3 Bulan — MoSCoW

| Prioritas           | Fitur                                      | Deskripsi                                                                                   |
| ------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| **MUST**            | ★ **Automatic Credit Scoring Engine**      | Menghasilkan rekomendasi penilaian kredit berdasarkan Decision Tree (ID3).                  |
| **MUST**            | ★ Input atribut kredit                     | Input Job, Education, Housing, dan Loan sebagai atribut model.                              |
| **MUST**            | Manajemen anggota                          | Admin dapat mengelola data anggota/nasabah.                                                 |
| **MUST**            | Pengajuan pinjaman                         | Anggota dapat mengajukan pinjaman melalui sistem.                                           |
| **MUST**            | Status pengajuan                           | Anggota dapat mengetahui status pengajuan pinjaman.                                         |
| **MUST**            | Dashboard analis                           | Analis dapat melihat pengajuan yang membutuhkan penilaian.                                  |
| **MUST**            | Hasil/rekomendasi AI                       | Sistem menampilkan hasil penilaian sebagai bantuan keputusan.                               |
| **MUST**            | Keputusan analis                           | Pengambil keputusan tetap dapat menentukan keputusan akhir.                                 |
| **MUST**            | Riwayat pengajuan                          | Data pengajuan dan hasil keputusan dapat ditelusuri.                                        |
| **SHOULD**          | ★ Informasi faktor penilaian               | Menampilkan atribut yang digunakan sebagai dasar penilaian agar hasil lebih mudah dipahami. |
| **SHOULD**          | Laporan penilaian                          | Rekap pengajuan dan hasil penilaian untuk pengurus.                                         |
| **SHOULD**          | Audit trail                                | Riwayat perubahan/status pengajuan untuk membantu kebutuhan audit.                          |
| **COULD**           | ★ Dashboard performa model                 | Menampilkan metrik seperti akurasi, sensitivitas, dan spesifikasi.                          |
| **COULD**           | Filter dan pencarian pengajuan             | Mempermudah analis menemukan pengajuan tertentu.                                            |
| **COULD**           | Notifikasi status                          | Memberikan informasi ketika status pengajuan berubah.                                       |
| **WON'T — 3 bulan** | AI yang mengambil keputusan secara mandiri | Keputusan akhir tetap berada pada pengambil keputusan manusia.                              |
| **WON'T — 3 bulan** | Model Deep Learning                        | Tidak diperlukan untuk prototype karena fokus pada Decision Tree ringan.                    |
| **WON'T — 3 bulan** | Prediksi risiko skala produksi masif       | Belum menjadi target karena validasi data masih terbatas.                                   |
| **WON'T — 3 bulan** | Integrasi sistem keuangan eksternal        | Tidak termasuk scope prototype.                                                             |
| **WON'T — 3 bulan** | Pengembangan model dengan dataset besar    | Di luar batasan prototype 3 bulan.                                                          |

---

# 7. Non-Goals Eksplisit

Produk **tidak bertujuan** untuk:

1. Menggantikan analis kredit atau pengambil keputusan manusia.
2. Memberikan jaminan bahwa setiap keputusan AI pasti benar.
3. Menjadi sistem penilaian kredit skala produksi masif dalam prototype 3 bulan.
4. Mengembangkan model AI kompleks seperti Deep Learning.
5. Mengklaim performa produksi berdasarkan dataset 50 data saja.
6. Menentukan kebijakan kredit koperasi secara otomatis.
7. Menjadi sistem akuntansi atau sistem keuangan koperasi secara menyeluruh.
8. Menyediakan validasi risiko kredit yang telah terbukti secara statistik pada populasi anggota koperasi.
9. Menggunakan atribut di luar Job, Education, Housing, dan Loan sebagai bagian dari model awal tanpa validasi lebih lanjut.

---

# 8. Asumsi & Risiko Utama + Mitigasi

| Asumsi/Risiko                               | Dampak                                                                                                           | Mitigasi                                                                                          |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Dataset pelatihan hanya 25 data**         | Model berpotensi belum merepresentasikan kondisi sebenarnya                                                      | Nyatakan sebagai prototype dan lakukan validasi menggunakan data yang lebih relevan jika tersedia |
| **Dataset berasal dari Bank Marketing UCI** | Karakteristik data dapat berbeda dengan anggota koperasi                                                         | Jangan menganggap performa 80% sebagai performa produksi                                          |
| **Hanya 4 atribut digunakan**               | Informasi untuk penilaian mungkin terbatas                                                                       | Jadikan empat atribut sebagai baseline dan evaluasi kebutuhan atribut tambahan                    |
| **Sensitivitas 71,42%**                     | Sebagian kasus positif dapat tidak teridentifikasi oleh model                                                    | Hasil AI harus ditinjau analis sebelum keputusan akhir                                            |
| **Spesifikasi 90,90%**                      | Model memiliki kemampuan yang baik pada metrik tersebut, tetapi belum cukup untuk membuktikan kelayakan produksi | Evaluasi menggunakan dataset yang lebih besar dan relevan                                         |
| **Asumsi pengguna menerima AI**             | Fitur AI dapat tidak digunakan secara optimal                                                                    | Libatkan analis dalam pengujian prototype                                                         |
| **Data anggota tidak konsisten**            | Hasil penilaian dapat menjadi tidak akurat                                                                       | Tetapkan format input dan validasi data                                                           |
| **Interpretasi hasil AI tidak jelas**       | Analis sulit mempercayai rekomendasi                                                                             | Tampilkan atribut/faktor yang menjadi dasar rekomendasi                                           |
| **AI dianggap sebagai keputusan final**     | Risiko keputusan kredit yang tidak tepat                                                                         | Tegaskan bahwa AI merupakan **decision-support**, bukan *decision-maker*                          |
| **Waktu pengembangan hanya 3 bulan**        | Scope terlalu besar dapat menghambat prototype                                                                   | Prioritaskan fitur MUST dan batasi fitur AI pada Decision Tree                                    |
| **Keterbatasan biaya komputasi**            | Model kompleks sulit digunakan                                                                                   | Gunakan Decision Tree sebagai model ringan sesuai scope riset                                     |

---

## Kesimpulan Product Direction

**MVP 3 bulan** sebaiknya difokuskan pada satu alur utama:

> **Anggota mengajukan pinjaman → Admin/Analis memvalidasi data → ★ Credit Scoring Engine menilai berdasarkan Job, Education, Housing & Loan → AI memberikan rekomendasi → Analis melakukan review → Keputusan → Anggota melihat status.**

Dengan positioning tersebut, produk tidak menjual “AI” sebagai gimmick, tetapi menjadikan **Decision Tree sebagai alat bantu standardisasi proses penilaian kredit**. Sementara itu, keterbatasan dataset dan hasil evaluasi awal harus dinyatakan secara eksplisit agar klaim produk tetap sesuai dengan bukti riset yang tersedia.
