import json
import random
import os
from pathlib import Path

# Setup folder output
BASE_DIR = Path(__file__).resolve().parent / 'data'
BASE_DIR.mkdir(exist_ok=True)

def save_to_json(filename, data):
    filepath = BASE_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] File berhasil dibuat: {filepath}")

def make_nqueens_instance(n=12, instance_id=1):
    """
    Membuat instance N-Queens dengan 1 Ratu terkunci (Fixed Queen).
    Posisi Ratu ditentukan secara acak berdasarkan instance_id sebagai seed.
    """
    # Gunakan ID instance sebagai basis seed atau 'kunci' agar hasil unik per file
    seed = 100 + instance_id
    rnd = random.Random(seed)

    # Kunci ratu di baris 0, pada Kolom Acak.
    row_position = 0
    col_position = rnd.randint(0, n - 1)

    instance_data = {
        "project": "n_queens",
        "description": f"N-Queens N = {n} dengan 1 Ratu terkunci (Varian {instance_id})",
        "n": n,
        "fixed_queens": [[row_position, col_position]],
        "seed_used": seed,
        "instance_id": instance_id
    }
    
    return instance_data

def main():
    # Loop untuk membuat 15 variasi data (instance)
    for i in range(1, 16):
        N_SIZE = 12  # Ukuran papan
        
        # Buat data instance ke-i
        data = make_nqueens_instance(n=N_SIZE, instance_id=i)
        
        # Format nama file: nqueens_N12_Inst01.json, Inst02.json, dst.
        filename = f"nqueens_N{N_SIZE}_Inst{i:02d}.json"

        # Simpan ke file
        save_to_json(filename, data)

    print("\n--- Selesai generate 15 instance ---")

if __name__ == '__main__':

    main()
