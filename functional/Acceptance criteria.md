Berikut DRAFT Acceptance Criteria yang disusun dari perspektif **QA Engineer / Test Analyst Senior**, dengan fokus pada kondisi yang dapat diverifikasi melalui database, API, UI, role/authorization, serta integrasi ML.

**Catatan penting:** daftar User Story yang diberikan hanya sampai **US-14**. Tidak ada definisi **US-15** pada input, sehingga saya tidak membuat acceptance criteria fiktif untuk US-15.

# DRAFT ACCEPTANCE CRITERIA

## Sistem Informasi Koperasi Simpan Pinjam Berbasis AI

### Konvensi Pengujian

* **Latensi AI:** ≤ 5 detik sejak request scoring diterima Web sampai response model diterima.
* **Latensi UI normal:** ≤ 3 detik untuk validasi dan operasi UI non-ML.
* **Akurasi baseline ID3:** 80%.
* **Sensitivitas baseline ID3:** 71,42%.
* **Spesifisitas baseline ID3:** 90,90%.
* **Input AI wajib:** Job, Education, Housing, Loan.
* **Housing:** hanya `Yes` atau `No`.
* **Loan:** hanya `Yes` atau `No`.
* **Keputusan final:** hanya dapat ditetapkan oleh Analis Kredit.
* **Status awal pengajuan:** `Pending Review`.
* **Hasil AI dan keputusan final:** wajib disimpan/ditampilkan sebagai dua informasi yang berbeda.

---

# EPIK 1 — MANAJEMEN ANGGOTA

## US-01 — Pengelolaan Data Anggota oleh Admin

**Prioritas:** MUST

**Keterlacakan:** FR-01 / NFR-08 / NFR-09

**Usulan Metode Uji:** UI-End-to-End Test + System Testing

### Scenario 01 — Admin berhasil menambahkan anggota baru

```gherkin
Scenario: Admin berhasil menambahkan data anggota dengan data valid
  Given pengguna telah login dengan role "Admin"
  And form tambah anggota tersedia
  And nomor identitas anggota belum terdaftar di database
  When Admin mengisi seluruh field wajib dengan data valid
  And Admin menekan tombol "Simpan"
  Then sistem menyimpan 1 record anggota baru ke database
  And response penyimpanan menghasilkan HTTP 200 atau 201
  And data anggota baru tampil pada daftar anggota
  And operasi penyimpanan selesai dalam waktu <= 3 detik
```

### Scenario 02 — Admin tidak dapat membuat anggota dengan identitas duplikat

```gherkin
Scenario: Sistem menolak identitas anggota yang sudah terdaftar
  Given pengguna telah login sebagai "Admin"
  And terdapat anggota dengan nomor identitas "ID001" di database
  When Admin membuat anggota baru menggunakan nomor identitas "ID001"
  And Admin menekan tombol "Simpan"
  Then sistem menolak penyimpanan data
  And tidak terdapat record anggota baru dengan nomor identitas "ID001"
  And pesan "Nomor identitas sudah terdaftar" ditampilkan
  And pesan validasi tampil dalam waktu <= 3 detik
```

### Scenario 03 — Pengguna tanpa role Admin tidak dapat mengelola anggota

```gherkin
Scenario: Anggota tidak dapat mengakses fungsi pengelolaan anggota
  Given pengguna telah login dengan role "Anggota"
  When pengguna mengakses endpoint atau halaman pengelolaan anggota
  Then sistem menolak akses
  And sistem mengembalikan HTTP 403 atau mengarahkan pengguna ke halaman unauthorized
  And pengguna tidak dapat membuat, mengubah, atau menghapus data anggota
```

---

# EPIK 2 — PENGAJUAN PINJAMAN

## US-02 — Pengajuan Pinjaman oleh Anggota

**Prioritas:** MUST

**Keterlacakan:** FR-02 / NFR-08 / NFR-11 / BR-03

**Usulan Metode Uji:** UI-End-to-End Test + System Testing

### Scenario 01 — Anggota berhasil mengajukan pinjaman

```gherkin
Scenario: Anggota mengirim pengajuan pinjaman dengan data valid
  Given pengguna telah login dengan role "Anggota"
  And data profil anggota telah tersedia
  And form pengajuan pinjaman tersedia
  When Anggota mengisi seluruh field wajib dengan data valid
  And Anggota menekan tombol "Ajukan Pinjaman"
  Then sistem membuat 1 record pengajuan pinjaman baru
  And pemilik pengajuan disimpan menggunakan ID anggota yang sedang login
  And status pengajuan tersimpan sebagai "Pending Review"
  And pengajuan tampil pada riwayat pengajuan anggota
  And proses penyimpanan selesai dalam waktu <= 3 detik
```

### Scenario 02 — Pengajuan ditolak jika field wajib kosong

```gherkin
Scenario: Sistem menolak pengajuan dengan field wajib kosong
  Given pengguna telah login sebagai "Anggota"
  And form pengajuan pinjaman sedang terbuka
  When Anggota mengosongkan minimal 1 field wajib
  And Anggota menekan tombol "Ajukan Pinjaman"
  Then sistem tidak membuat record pengajuan baru
  And field yang kosong mendapatkan pesan validasi
  And pesan validasi tampil dalam waktu <= 3 detik
```

### Scenario 03 — Anggota tidak dapat membuat pengajuan atas nama anggota lain

```gherkin
Scenario: Sistem mencegah manipulasi pemilik pengajuan
  Given pengguna telah login sebagai "Anggota"
  And ID anggota yang sedang login adalah "A001"
  When pengguna mengirim request pengajuan dengan owner_id "A002"
  Then sistem menolak request tersebut
  And tidak ada pengajuan baru yang tersimpan atas nama "A002"
  And sistem mengembalikan HTTP 403 atau 422 sesuai mekanisme validasi authorization
```

---

## US-03 — Melihat Daftar Pengajuan oleh Admin

**Prioritas:** MUST

**Keterlacakan:** FR-03 / NFR-09 / NFR-10

**Usulan Metode Uji:** UI-End-to-End Test + System Testing

### Scenario 01 — Admin melihat daftar pengajuan

```gherkin
Scenario: Admin dapat melihat daftar pengajuan yang tersedia
  Given pengguna telah login dengan role "Admin"
  And database memiliki minimal 3 data pengajuan
  When Admin membuka halaman "Daftar Pengajuan"
  Then sistem menampilkan daftar pengajuan
  And setiap record menampilkan minimal ID pengajuan, anggota, tanggal, dan status
  And data yang ditampilkan sesuai dengan database
  And halaman selesai dimuat dalam waktu <= 3 detik
```

### Scenario 02 — Admin melihat perubahan status pengajuan

```gherkin
Scenario: Daftar pengajuan menampilkan status terbaru
  Given terdapat pengajuan dengan status "Pending Review"
  When status pengajuan pada database berubah menjadi "Diterima"
  And Admin memuat ulang halaman daftar pengajuan
  Then pengajuan tersebut ditampilkan dengan status "Diterima"
  And status lama "Pending Review" tidak lagi ditampilkan sebagai status aktif
```

---

# EPIK 3 — AI CREDIT SCORING ENGINE ★

## US-04 — Input 4 Atribut AI (Job, Education, Housing, Loan)

**Prioritas:** MUST

**Keterlacakan:** FR-04 / NFR-01 / NFR-06 / BR-02

**Usulan Metode Uji:** UI-End-to-End Test + Integration Test

### Scenario 01 — Happy Path: seluruh atribut AI valid

```gherkin
Scenario: Analis mengisi seluruh 4 atribut AI dengan nilai valid
  Given pengguna telah login dengan role "Analis Kredit"
  And pengajuan memiliki status "Pending Review"
  And form atribut AI tersedia
  When Analis mengisi Job dengan nilai valid
  And Analis mengisi Education dengan nilai valid
  And Analis memilih Housing "Yes" atau "No"
  And Analis memilih Loan "Yes" atau "No"
  Then sistem menandai seluruh 4 atribut sebagai valid
  And form mengizinkan proses scoring AI
  And tidak terdapat pesan error validasi pada keempat atribut
```

### Scenario 02 — Edge Case: satu atribut AI kosong

```gherkin
Scenario: Sistem menolak scoring ketika atribut Loan kosong
  Given pengguna telah login sebagai "Analis Kredit"
  And Job telah diisi dengan nilai valid
  And Education telah diisi dengan nilai valid
  And Housing telah diisi dengan "Yes"
  And Loan bernilai null atau kosong
  When Analis menekan tombol "Jalankan Scoring"
  Then sistem menolak submission
  And pesan "Atribut Loan wajib diisi" tampil dalam waktu <= 3 detik
  And request scoring tidak dikirim ke ML Engine
  And status pengajuan tetap "Pending Review"
```

### Scenario 03 — Sistem menolak nilai enum yang tidak valid

```gherkin
Scenario: Sistem menolak nilai Housing selain Yes atau No
  Given pengguna telah login sebagai "Analis Kredit"
  And data Housing dikirim dengan nilai "Maybe"
  When Analis mengirim form atribut AI
  Then sistem menolak data tersebut
  And request scoring tidak dikirim ke ML Engine
  And sistem menampilkan pesan validasi bahwa Housing hanya menerima "Yes" atau "No"
  And status pengajuan tetap "Pending Review"
```

### Scenario 04 — Empat atribut berhasil disimpan

```gherkin
Scenario: Sistem menyimpan empat atribut AI yang valid
  Given pengguna telah login sebagai "Analis Kredit"
  And pengajuan memiliki status "Pending Review"
  When Analis menyimpan Job, Education, Housing, dan Loan dengan nilai valid
  Then keempat atribut tersimpan pada record pengajuan atau tabel atribut AI terkait
  And nilai yang tersimpan sama dengan nilai yang dikirim pengguna
  And tidak ada atribut mandatory yang bernilai null
```

---

## US-05 — Menjalankan Credit Scoring Engine (ID3)

**Prioritas:** MUST

**Keterlacakan:** FR-05 / FR-06 / NFR-01 / NFR-02 / NFR-03 / NFR-04 / NFR-05 / BR-02

**Usulan Metode Uji:** Integration Test + System Testing

### Scenario 01 ★ — Happy Path: ID3 berhasil melakukan scoring

```gherkin
Scenario: Credit Scoring Engine ID3 berhasil memproses input valid
  Given pengguna telah login sebagai "Analis Kredit"
  And pengajuan berstatus "Pending Review"
  And Job, Education, Housing, dan Loan telah terisi valid
  And ML Engine ID3 dalam kondisi tersedia
  When Analis menekan "Jalankan Scoring"
  Then Web Application mengirim keempat atribut ke ML Engine
  And ML Engine memproses data menggunakan model Decision Tree ID3
  And ML Engine mengembalikan hasil "Yes" atau "No"
  And total waktu pemrosesan scoring <= 5 detik
  And response scoring berhasil diterima oleh Web Application
```

### Scenario 02 ★ — Edge Case: input tidak lengkap tidak dikirim ke ML

```gherkin
Scenario: Sistem menghentikan scoring ketika satu atribut kosong
  Given pengguna telah login sebagai "Analis Kredit"
  And Job, Education, dan Housing valid
  And Loan bernilai null
  When Analis menekan "Jalankan Scoring"
  Then sistem menolak proses scoring sebelum request ML dibuat
  And ML Engine tidak menerima request scoring
  And pesan "Atribut Loan wajib diisi" tampil dalam waktu <= 3 detik
  And status pengajuan tetap "Pending Review"
```

### Scenario 03 ★ — Fallback: ML Engine timeout lebih dari 5 detik

```gherkin
Scenario: Sistem menangani timeout ML Engine
  Given pengguna telah login sebagai "Analis Kredit"
  And seluruh 4 atribut AI valid
  And ML Engine tidak memberikan response selama > 5 detik
  When Analis menjalankan scoring
  Then Web Application menghentikan atau menandai request sebagai timeout
  And pesan "Proses scoring AI mengalami batas waktu/gagal" ditampilkan
  And sistem tidak menetapkan keputusan final secara otomatis
  And status pengajuan tetap "Pending Review"
  And tidak ada status "Diterima" atau "Ditolak" yang dibuat sebagai keputusan final
```

### Scenario 04 ★ — Fallback: ML Engine mengembalikan HTTP 500

```gherkin
Scenario: Sistem menangani Internal Server Error dari ML Engine
  Given seluruh 4 atribut AI valid
  And ML Engine mengembalikan HTTP 500 Internal Server Error
  When Analis menjalankan scoring
  Then Web Application menangkap error tersebut
  And pesan "Proses scoring AI mengalami batas waktu/gagal" ditampilkan
  And status pengajuan tetap "Pending Review"
  And keputusan final tidak dibuat otomatis
  And error tercatat pada mekanisme audit atau logging sistem
```

---

## US-06 — Menampilkan Rekomendasi AI

**Prioritas:** MUST

**Keterlacakan:** FR-07 / NFR-01 / NFR-06 / BR-01 / BR-06

**Usulan Metode Uji:** Integration Test + UI-End-to-End Test

### Scenario 01 ★ — Rekomendasi AI ditampilkan terpisah dari keputusan final

```gherkin
Scenario: Sistem menampilkan hasil rekomendasi AI setelah scoring berhasil
  Given pengguna telah login sebagai "Analis Kredit"
  And 4 atribut AI telah valid
  And ML Engine mengembalikan hasil "Yes"
  When Web Application menerima response scoring
  Then sistem menampilkan "Rekomendasi AI: Diterima"
  And rekomendasi AI ditampilkan sebagai informasi terpisah dari "Keputusan Final Analis"
  And keputusan final analis belum berubah menjadi "Diterima"
  And status pengajuan tetap "Pending Review" sampai analis menetapkan keputusan
  And hasil rekomendasi diterima dalam waktu <= 5 detik sejak request scoring
```

### Scenario 02 ★ — Rekomendasi No ditampilkan sebagai Ditolak

```gherkin
Scenario: Sistem menampilkan rekomendasi No sebagai Ditolak
  Given 4 atribut AI valid
  And ML Engine mengembalikan hasil "No"
  When response scoring diterima Web Application
  Then sistem menampilkan "Rekomendasi AI: Ditolak"
  And sistem tidak mengubah status pengajuan menjadi "Ditolak" secara otomatis
  And field "Keputusan Final Analis" tetap belum ditetapkan
```

### Scenario 03 ★ — Timeout tidak menghasilkan rekomendasi

```gherkin
Scenario: Sistem tidak menampilkan keputusan AI ketika scoring timeout
  Given 4 atribut AI valid
  And ML Engine tidak memberikan response selama > 5 detik
  When Web Application menerima kondisi timeout
  Then sistem menampilkan pesan fallback "Proses scoring AI mengalami batas waktu/gagal"
  And sistem tidak menampilkan rekomendasi "Diterima" atau "Ditolak" sebagai hasil scoring yang valid
  And status pengajuan tetap "Pending Review"
```

---

## US-07 — Transparansi Dasar Rekomendasi AI

**Prioritas:** SHOULD

**Keterlacakan:** FR-08 / NFR-06 / NFR-07 / BR-04

**Usulan Metode Uji:** UI-End-to-End Test + UAT

### Scenario 01 ★ — Atribut dasar yang digunakan model ditampilkan

```gherkin
Scenario: Sistem menampilkan empat atribut dasar scoring
  Given scoring AI berhasil dilakukan
  And rekomendasi AI telah tersedia
  When Analis membuka detail hasil scoring
  Then sistem menampilkan Job
  And sistem menampilkan Education
  And sistem menampilkan Housing
  And sistem menampilkan Loan
  And nilai yang ditampilkan sama dengan nilai yang dikirim ke ML Engine
```

### Scenario 02 ★ — Atribut transparansi tidak dapat mengubah hasil yang sudah tersimpan

```gherkin
Scenario: Informasi atribut AI hanya berfungsi sebagai informasi transparansi
  Given rekomendasi AI telah tersimpan
  When Analis melihat empat atribut dasar model
  Then sistem menampilkan atribut sebagai data input/model information
  And perubahan keputusan tidak terjadi hanya karena Analis membuka informasi atribut
  And keputusan final tetap membutuhkan tindakan eksplisit dari Analis
```

### Scenario 03 — Rekomendasi AI dan keputusan final terlihat berbeda

```gherkin
Scenario: UI membedakan rekomendasi AI dengan keputusan final
  Given rekomendasi AI telah tersedia
  And keputusan final Analis belum ditetapkan
  When Analis membuka detail pengajuan
  Then sistem menampilkan bagian "Rekomendasi AI"
  And sistem menampilkan bagian "Keputusan Final Analis"
  And kedua nilai tersebut tidak menggunakan field atau label status yang sama
```

---

# EPIK 4 — KEPUTUSAN KREDIT OLEH ANALIS

## US-08 — Konfirmasi Keputusan Kredit oleh Analis

**Prioritas:** MUST

**Keterlacakan:** FR-09 / NFR-14 / BR-01 / BR-06

**Usulan Metode Uji:** UI-End-to-End Test + UAT

### Scenario 01 — Analis mengonfirmasi rekomendasi Diterima

```gherkin
Scenario: Analis mengonfirmasi rekomendasi AI Diterima
  Given pengguna telah login sebagai "Analis Kredit"
  And rekomendasi AI adalah "Diterima"
  And status pengajuan adalah "Pending Review"
  When Analis memilih keputusan final "Diterima"
  And Analis menekan tombol "Konfirmasi"
  Then sistem menyimpan keputusan final sebagai "Diterima"
  And keputusan final tersimpan pada database
  And status pengajuan berubah menjadi "Diterima"
  And keputusan tersebut tercatat sebagai tindakan Analis
```

### Scenario 02 — Analis mengonfirmasi rekomendasi Ditolak

```gherkin
Scenario: Analis mengonfirmasi rekomendasi AI Ditolak
  Given pengguna telah login sebagai "Analis Kredit"
  And rekomendasi AI adalah "Ditolak"
  And status pengajuan adalah "Pending Review"
  When Analis memilih keputusan final "Ditolak"
  And Analis menekan tombol "Konfirmasi"
  Then sistem menyimpan keputusan final sebagai "Ditolak"
  And status pengajuan berubah menjadi "Ditolak"
  And keputusan final tidak dicatat sebagai keputusan otomatis AI
  And aktivitas Analis tercatat pada audit trail
```

### Scenario 03 — AI tidak dapat menetapkan keputusan final sendiri

```gherkin
Scenario: Sistem mencegah perubahan status final hanya berdasarkan hasil AI
  Given rekomendasi AI telah tersedia
  And belum ada tindakan konfirmasi dari Analis
  When sistem menerima hasil AI "Diterima" atau "Ditolak"
  Then status pengajuan tetap "Pending Review"
  And field keputusan final Analis tetap belum ditetapkan
  And tidak ada keputusan final yang dibuat tanpa tindakan Analis
```

---

## US-09 — Override Rekomendasi AI oleh Analis

**Prioritas:** MUST

**Keterlacakan:** FR-10 / NFR-14 / BR-01 / BR-05 / BR-06

**Usulan Metode Uji:** UI-End-to-End Test + UAT

### Scenario 01 — Analis melakukan override No menjadi Diterima

```gherkin
Scenario: Analis melakukan override rekomendasi Ditolak menjadi Diterima
  Given pengguna telah login sebagai "Analis Kredit"
  And rekomendasi AI adalah "Ditolak"
  And status pengajuan adalah "Pending Review"
  When Analis memilih keputusan final "Diterima"
  And Analis melakukan aksi "Override"
  Then sistem menyimpan rekomendasi AI tetap sebagai "Ditolak"
  And sistem menyimpan keputusan final Analis sebagai "Diterima"
  And status pengajuan berubah menjadi "Diterima"
  And audit trail mencatat bahwa keputusan final merupakan hasil override Analis
```

### Scenario 02 — Analis melakukan override Yes menjadi Ditolak

```gherkin
Scenario: Analis melakukan override rekomendasi Diterima menjadi Ditolak
  Given pengguna telah login sebagai "Analis Kredit"
  And rekomendasi AI adalah "Diterima"
  And status pengajuan adalah "Pending Review"
  When Analis memilih keputusan final "Ditolak"
  And Analis melakukan aksi "Override"
  Then rekomendasi AI tetap tersimpan sebagai "Diterima"
  And keputusan final Analis tersimpan sebagai "Ditolak"
  And status pengajuan berubah menjadi "Ditolak"
  And aktivitas override tercatat pada audit trail
```

### Scenario 03 — Override tanpa keputusan final tidak diperbolehkan

```gherkin
Scenario: Sistem menolak override tanpa pilihan keputusan final
  Given rekomendasi AI telah tersedia
  And keputusan final Analis belum dipilih
  When Analis mencoba menyimpan override tanpa memilih "Diterima" atau "Ditolak"
  Then sistem menolak penyimpanan
  And status pengajuan tetap "Pending Review"
  And pesan validasi keputusan final ditampilkan dalam waktu <= 3 detik
```

---

# EPIK 5 — TRACKING STATUS PENGAJUAN

## US-10 — Pembaruan Status Pengajuan

**Prioritas:** MUST

**Keterlacakan:** FR-11 / NFR-13

**Usulan Metode Uji:** Integration Test + System Testing

### Scenario 01 — Status berubah setelah keputusan final

```gherkin
Scenario: Sistem memperbarui status setelah keputusan Analis disimpan
  Given pengajuan memiliki status "Pending Review"
  And pengguna telah login sebagai "Analis Kredit"
  When Analis menyimpan keputusan final "Diterima"
  Then status database pengajuan berubah menjadi "Diterima"
  And status yang ditampilkan pada UI adalah "Diterima"
  And status tidak kembali ke "Pending Review" setelah halaman dimuat ulang
```

### Scenario 02 — Status tidak berubah ketika scoring gagal

```gherkin
Scenario: Status tetap Pending Review ketika AI gagal
  Given pengajuan memiliki status "Pending Review"
  And ML Engine mengalami timeout atau HTTP 500
  When Analis menjalankan scoring
  Then sistem menampilkan pesan fallback
  And status pengajuan tetap "Pending Review"
  And database tidak menyimpan keputusan final "Diterima" atau "Ditolak"
```

### Scenario 03 — Status hanya menggunakan nilai yang valid

```gherkin
Scenario: Sistem menolak nilai status yang tidak didefinisikan
  Given terdapat pengajuan dengan status "Pending Review"
  When request perubahan status dikirim dengan nilai "SelesaiX"
  Then sistem menolak perubahan tersebut
  And status database tetap "Pending Review"
  And response menunjukkan validation error
```

---

## US-11 — Melihat Status Pengajuan Milik Sendiri oleh Anggota

**Prioritas:** MUST

**Keterlacakan:** FR-12 / NFR-09 / NFR-10 / NFR-12 / BR-03

**Usulan Metode Uji:** UI-End-to-End Test + System Testing + Security Testing

### Scenario 01 — Anggota melihat pengajuan miliknya

```gherkin
Scenario: Anggota hanya melihat pengajuan milik sendiri
  Given pengguna login sebagai "Anggota"
  And ID anggota adalah "A001"
  And database memiliki pengajuan milik "A001"
  When Anggota membuka halaman "Pengajuan Saya"
  Then sistem hanya menampilkan pengajuan dengan owner_id "A001"
  And data anggota lain tidak ditampilkan
  And halaman selesai dimuat dalam waktu <= 3 detik
```

### Scenario 02 — Anggota tidak dapat mengakses pengajuan anggota lain

```gherkin
Scenario: Anggota mencoba mengakses ID pengajuan milik anggota lain
  Given pengguna login sebagai "Anggota A001"
  And pengajuan "P002" dimiliki oleh "A002"
  When Anggota A001 mengakses detail pengajuan "P002"
  Then sistem menolak akses
  And sistem mengembalikan HTTP 403 atau 404 sesuai mekanisme keamanan
  And data pengajuan P002 tidak ditampilkan
```

### Scenario 03 — Status terbaru ditampilkan

```gherkin
Scenario: Anggota melihat status terbaru pengajuannya
  Given anggota memiliki pengajuan dengan status "Diterima"
  When Anggota membuka detail pengajuan
  Then sistem menampilkan status "Diterima"
  And status yang ditampilkan sama dengan status pada database
  And Anggota tidak memiliki kontrol untuk mengubah status tersebut
```

---

## US-12 — Melihat Seluruh Pengajuan oleh Analis

**Prioritas:** MUST

**Keterlacakan:** FR-13 / NFR-09 / NFR-10

**Usulan Metode Uji:** UI-End-to-End Test + System Testing

### Scenario 01 — Analis dapat melihat seluruh pengajuan kewenangannya

```gherkin
Scenario: Analis melihat daftar seluruh pengajuan yang menjadi kewenangannya
  Given pengguna login dengan role "Analis Kredit"
  And terdapat minimal 3 pengajuan pada database dalam kewenangan Analis
  When Analis membuka daftar pengajuan
  Then sistem menampilkan seluruh pengajuan yang berada dalam kewenangan Analis
  And setiap pengajuan menampilkan ID, anggota, tanggal, dan status
  And data selesai dimuat dalam waktu <= 3 detik
```

### Scenario 02 — Analis dapat membuka detail pengajuan

```gherkin
Scenario: Analis membuka detail pengajuan
  Given Analis telah login
  And terdapat pengajuan "P001" dalam kewenangannya
  When Analis membuka detail P001
  Then sistem menampilkan data pengajuan P001
  And sistem menampilkan status terbaru
  And jika tersedia, sistem menampilkan rekomendasi AI dan keputusan final secara terpisah
```

### Scenario 03 — Pengajuan di luar kewenangan tidak dapat diakses

```gherkin
Scenario: Analis tidak dapat mengakses pengajuan di luar kewenangannya
  Given Analis A tidak memiliki kewenangan terhadap pengajuan P999
  When Analis A meminta detail P999
  Then sistem menolak akses
  And sistem mengembalikan HTTP 403 atau 404
  And data P999 tidak dikirimkan kepada client
```

---

# EPIK 6 — AUDIT TRAIL

## US-13 — Pencatatan Aktivitas Sistem ke Audit Trail

**Prioritas:** MUST

**Keterlacakan:** FR-14 / NFR-13 / NFR-14

**Usulan Metode Uji:** Integration Test + System Testing

### Scenario 01 — Aktivitas scoring tercatat

```gherkin
Scenario: Sistem mencatat aktivitas scoring AI ke audit trail
  Given Analis telah login
  And pengajuan memiliki 4 atribut AI valid
  When Analis menjalankan Credit Scoring Engine
  Then sistem membuat record audit untuk aktivitas scoring
  And record audit memuat minimal user/actor, ID pengajuan, aktivitas, timestamp, dan hasil/status proses
  And record audit dapat ditemukan setelah proses selesai
```

### Scenario 02 — Aktivitas override tercatat

```gherkin
Scenario: Sistem mencatat aktivitas override keputusan AI
  Given rekomendasi AI adalah "Ditolak"
  And Analis melakukan override menjadi "Diterima"
  When keputusan final disimpan
  Then sistem membuat record audit override
  And audit mencatat rekomendasi AI "Ditolak"
  And audit mencatat keputusan final "Diterima"
  And audit mencatat identitas Analis
  And audit mencatat timestamp aktivitas
```

### Scenario 03 — Kegagalan ML tercatat

```gherkin
Scenario: Sistem mencatat kegagalan ML Engine
  Given seluruh atribut AI valid
  And ML Engine mengembalikan HTTP 500 atau timeout > 5 detik
  When Analis menjalankan scoring
  Then sistem mencatat aktivitas kegagalan pada audit trail atau error log
  And record memuat ID pengajuan
  And record memuat jenis kegagalan
  And status pengajuan tetap "Pending Review"
```

### Scenario 04 — Audit trail tidak berubah ketika keputusan AI gagal

```gherkin
Scenario: Kegagalan scoring tidak menghasilkan keputusan final pada audit
  Given pengajuan berstatus "Pending Review"
  And ML Engine mengalami timeout
  When timeout ditangani sistem
  Then audit mencatat kegagalan scoring
  And audit tidak mencatat keputusan final "Diterima" atau "Ditolak" sebagai keputusan Analis
  And status pengajuan tetap "Pending Review"
```

---

# EPIK 7 — REPORTING

## US-14 — Laporan Pengajuan dan Penilaian

**Prioritas:** SHOULD

**Keterlacakan:** FR-15 / NFR-09 / NFR-10

**Usulan Metode Uji:** System Testing + UI-End-to-End Test + UAT

### Scenario 01 — Admin/Analis menghasilkan laporan

```gherkin
Scenario: Pengguna berwenang menghasilkan laporan pengajuan
  Given pengguna telah login dengan role yang memiliki hak akses laporan
  And database memiliki minimal 3 pengajuan
  When pengguna membuka menu "Laporan Pengajuan"
  And pengguna memilih periode laporan yang valid
  Then sistem menampilkan data pengajuan sesuai periode
  And setiap data menampilkan minimal ID pengajuan, anggota, status, dan keputusan
  And halaman laporan selesai dimuat dalam waktu <= 3 detik
```

### Scenario 02 — Laporan hanya berisi data sesuai filter

```gherkin
Scenario: Sistem menghasilkan laporan berdasarkan periode yang dipilih
  Given database memiliki pengajuan pada Januari dan Februari
  When pengguna memilih periode Januari
  And pengguna menjalankan laporan
  Then laporan hanya menampilkan pengajuan pada periode Januari
  And pengajuan pada Februari tidak ditampilkan
  And jumlah record laporan sesuai dengan hasil query database untuk periode Januari
```

### Scenario 03 — Rekomendasi AI dan keputusan final dibedakan dalam laporan

```gherkin
Scenario: Laporan membedakan rekomendasi AI dengan keputusan final
  Given terdapat pengajuan dengan rekomendasi AI "Ditolak"
  And keputusan final Analis adalah "Diterima" melalui override
  When pengguna menghasilkan laporan
  Then laporan menampilkan rekomendasi AI sebagai "Ditolak"
  And laporan menampilkan keputusan final sebagai "Diterima"
  And kedua nilai tidak digabung menjadi satu field keputusan
```

### Scenario 04 — Pengguna tanpa hak akses tidak dapat membuka laporan

```gherkin
Scenario: Sistem menolak akses laporan kepada role yang tidak memiliki izin
  Given pengguna login dengan role yang tidak memiliki permission laporan
  When pengguna membuka halaman atau endpoint laporan
  Then sistem menolak akses
  And sistem mengembalikan HTTP 403 atau mengarahkan ke halaman unauthorized
  And data laporan tidak dikirimkan kepada client
```

---

# MATRIX VALIDASI KHUSUS AI

| User Story | Happy Path | Incomplete Input | Timeout/500 | ≤5 detik | AI ≠ Keputusan Final |
| ---------- | ---------: | ---------------: | ----------: | -------: | -------------------: |
| US-04      |          ✓ |                ✓ |           — |        — |                    ✓ |
| US-05      |          ✓ |                ✓ |           ✓ |        ✓ |                    ✓ |
| US-06      |          ✓ |               ✓* |           ✓ |        ✓ |                    ✓ |
| US-07      |          ✓ |               ✓* |          ✓* |       ✓* |                    ✓ |

`*` skenario tersebut dapat diuji melalui hasil dari US-04/US-05 dan diverifikasi pada layer UI.

---

# MATRIX ACCEPTANCE CRITERIA UTAMA

| ID       | Acceptance Criteria Kritis          | Expected Result                               |
| -------- | ----------------------------------- | --------------------------------------------- |
| AC-AI-01 | 4 atribut valid                     | Scoring dapat dijalankan                      |
| AC-AI-02 | 1 dari 4 atribut kosong             | Scoring ditolak                               |
| AC-AI-03 | Request dengan input incomplete     | Tidak dikirim ke ML Engine                    |
| AC-AI-04 | ML berhasil                         | Response Yes/No diterima                      |
| AC-AI-05 | Latensi ML                          | ≤ 5 detik                                     |
| AC-AI-06 | UI validation                       | ≤ 3 detik                                     |
| AC-AI-07 | ML timeout >5 detik                 | Fallback ditampilkan                          |
| AC-AI-08 | ML HTTP 500                         | Fallback ditampilkan                          |
| AC-AI-09 | AI menghasilkan Yes                 | Rekomendasi "Diterima", bukan keputusan final |
| AC-AI-10 | AI menghasilkan No                  | Rekomendasi "Ditolak", bukan keputusan final  |
| AC-AI-11 | Tidak ada tindakan Analis           | Status tetap "Pending Review"                 |
| AC-AI-12 | Analis konfirmasi                   | Keputusan final tersimpan                     |
| AC-AI-13 | Analis override                     | Rekomendasi AI tetap, keputusan final berubah |
| AC-AI-14 | Override                            | Audit trail tercatat                          |
| AC-AI-15 | Anggota mengakses data anggota lain | HTTP 403/404                                  |
| AC-AI-16 | ML failure                          | Tidak boleh menghasilkan keputusan otomatis   |

---

# CATATAN QA TERKAIT METRIK MODEL

Metrik **akurasi 80%, sensitivitas 71,42%, dan spesifisitas 90,90%** sebaiknya diperlakukan sebagai **baseline hasil riset/model**, bukan acceptance criterion bahwa setiap eksekusi individual harus menghasilkan akurasi 80%.

Validasi metrik tersebut dilakukan melalui **model evaluation test** menggunakan dataset dan pembagian data yang telah ditetapkan:

* Total sampel: 50
* Training: 25 sampel
* Testing: 25 sampel
* Accuracy baseline: 80%
* Sensitivity baseline: 71,42%
* Specificity baseline: 90,90%

Contoh acceptance test untuk evaluasi model:

```gherkin
Scenario: Model ID3 memenuhi baseline evaluasi penelitian
  Given dataset pengujian terdiri dari 50 sampel
  And 25 sampel digunakan sebagai data training
  And 25 sampel digunakan sebagai data testing
  And preprocessing dataset menggunakan prosedur yang telah ditetapkan
  When model Decision Tree ID3 dievaluasi menggunakan data testing
  Then nilai accuracy tercatat dan dapat dibandingkan dengan baseline 80%
  And nilai sensitivity tercatat dan dapat dibandingkan dengan baseline 71.42%
  And nilai specificity tercatat dan dapat dibandingkan dengan baseline 90.90%
  And hasil evaluasi disimpan sebagai evidence pengujian model
```

**Catatan:** baseline tersebut tidak boleh diterjemahkan menjadi aturan seperti *"setiap 10 transaksi harus menghasilkan 8 prediksi benar"*. Metrik adalah hasil evaluasi terhadap **dataset**, bukan SLA setiap transaksi.

---

# CATATAN US-15

Daftar input yang diberikan berakhir pada **US-14 — Laporan Pengajuan dan Penilaian**. Tidak terdapat definisi:

> **US-15 (ID, nama, prioritas, FR/NFR, BR)**

Karena acceptance criteria harus memiliki keterlacakan yang jelas, **US-15 tidak dibuat secara asumtif**. Setelah definisi US-15 tersedia, acceptance criteria dapat mengikuti pola yang sama dengan US-01 sampai US-14.

Dokumen di atas sudah bisa dijadikan dasar **test case QA**, terutama untuk mengubah setiap `Scenario` menjadi kolom *Test Case ID, Precondition, Test Steps, Expected Result, Actual Result, Status,* dan *Evidence*.
