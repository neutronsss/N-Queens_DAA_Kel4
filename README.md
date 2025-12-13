# N-Queens_DAA_Kel4

Proyek ini merupakan implementasi dan eksperimen algoritma **Backtracking (Algoritma A)** dan  
**Backtracking + Forward Checking (Algoritma B)** untuk menyelesaikan masalah **N-Queens (N = 12)**  
dengan **1 Ratu Terkunci (Fixed Queen)** pada setiap instance.  
Total instance: **15 file JSON unik**, dibangkitkan otomatis oleh generator.

---

## 1) Struktur Folder

N-Queens_DAA_Kel4/
│

├── data/ # berisi 15 instance JSON

│ ├── nqueens_N12_Inst01.json

│ ├── ...

│ └── nqueens_N12_Inst15.json

│
├── generate_instances.py # membangkitkan 15 instance unik

├── run.py # menjalankan Algo A & B

└── README.md # dokumen panduan proyek

---

## 2) Penjelasan Skrip Eksekusi (run.py)

File **run.py** melakukan:

- Membaca file instance (JSON)
- Menjalankan:
  - **Algo A** → Backtracking biasa  
  - **Algo B** → Backtracking + Forward Checking
- Mengukur:
  - waktu eksekusi dalam milidetik
  - jumlah node yang dieksplorasi
  - skor solusi (0–1)
- Mencetak tabel performa seperti:

Inst | Fixed Q | Algo A (ms) | Nodes A | Score A | Algo B (ms) | Nodes B | Score B
1 | [0, 4] | 28.02 | 481 | 1.00 | 5.91 | 198 | 1.00


---

## 3) Generator Instance (generate_instances.py)

File ini digunakan untuk menghasilkan **15 instance unik**:

- Ukuran papan: `n = 12`
- Fixed queen: di baris 0, kolom acak berdasarkan **seed**
- Seed = `100 + instance_id`  
- Format file otomatis:  

Untuk membuat ulang instance:

```bash
python generate_instances.py

```

## 4) Format Instance (JSON)

Contoh isi file instance:

{
  "project": "n_queens",
  
  "description": "N-Queens N = 12 dengan 1 Ratu terkunci (Varian X)",
  
  "n": 12,
  
  "fixed_queens": [[0, 3]],
  
  "seed_used": 103,
  
  "instance_id": 3
}

Keterangan:

- fixed_queens → ratu wajib yang posisinya tidak boleh dilanggar
- seed_used → menjamin hasil unik & reproducible
- instance_id → nomor varian 1–15

## 5) Cara Menjalankan Eksperimen
- Jalankan Algoritma A
  - python run.py --instance data/nqueens_N12_Inst01.json --algo A

- Jalankan Algoritma B
  - python run.py --instance data/nqueens_N12_Inst01.json --algo B

- Jalankan seluruh 15 instance sekaligus
  - python run.py

## 6) Evaluator Solusi

Skor dihitung berdasarkan:
- Konflik vertikal dan diagonal
- Kepatuhan terhadap fixed queen
- Kelengkapan ratu
- Formula:
    - final_score = conflict_score × completeness_score

Evaluator otomatis melalui fungsi evaluate_solution().

## 7) Ketergantungan

Tidak menggunakan library eksternal.
Hanya membutuhkan Python 3.x dengan modul builtin:
- json
- time
- random
- pathlib

## 8) Reproducibility Guide

Untuk menjalankan ulang seluruh eksperimen dari awal:
- python generate_instances.py
- python run.py

Semua hasil akan identik karena seed dikunci pada setiap instance.

## 9) Kontribusi Anggota
- Ibrahim Syauqi
  - Membuat readme
- Jimly Syahbatin
  - Programming dan visualisasi program
- Zaki Elias Al Haqqani Kudus
  - Penyusunan laporan dan menambah visualisasi
