import json
import time
from pathlib import Path

# BAGIAN 1: EVALUATOR
def evaluate_solution(sol, instance):
    """
    Mengembalikan skor kualitas solusi (0.0 - 1.0).
    1.0 = Sempurna (Valid).
    < 1.0 = Ada pelanggaran (conflict).
    """
    # Jika solusi kosong atau format salah, skor 0
    if not isinstance(sol, list) or len(sol) != instance['n']:
        return 0.0

    n = instance['n']
    
    # 1. Cek Penalti Fixed Queens (Ratu Terkunci)
    # Jika ratu terkunci digeser, skor langsung 0 (pelanggaran fatal)
    fixed_queens = instance.get('fixed_queens', [])
    for r_fix, c_fix in fixed_queens:
        if sol[r_fix] != -1 and sol[r_fix] != c_fix:
            return 0.0 

    # 2. Hitung Konflik Antar Ratu
    # Kumpulkan posisi ratu yang sudah terpasang (abaikan -1/kosong)
    queens = [(r, c) for r, c in enumerate(sol) if c != -1]
    
    num_queens = len(queens)
    if num_queens < 2:
        # Jika cuma ada 0 atau 1 ratu, tidak ada konflik, tapi bukan solusi lengkap
        return num_queens / n if n > 0 else 0.0

    # Total pasangan yang mungkin: kombinasi nC2 = n * (n-1) / 2
    total_pairs = num_queens * (num_queens - 1) / 2
    
    attacking_pairs = 0
    for i in range(num_queens):
        for j in range(i + 1, num_queens):
            r1, c1 = queens[i]
            r2, c2 = queens[j]

            # Cek serangan Vertikal (Kolom sama)
            if c1 == c2:
                attacking_pairs += 1
                continue
            
            # Cek serangan Diagonal
            if abs(r1 - r2) == abs(c1 - c2):
                attacking_pairs += 1
                continue

    # 3. Hitung Skor Akhir
    # Skor dasar berdasarkan konflik
    safe_pairs = total_pairs - attacking_pairs
    conflict_score = safe_pairs / total_pairs if total_pairs > 0 else 1.0
    
    # Penyesuaian: Skor harus juga memperhitungkan kelengkapan papan
    completeness_score = num_queens / n
    
    # Weighted score: Conflict Score * Completeness Score
    final_score = conflict_score * completeness_score
    
    return final_score

# BAGIAN 2: ALGORITMA
# --- Helper: Cek Keamanan Standar (Untuk Algo A) ---
def is_safe(board, row, col, n):
    for i in range(n):
        if board[i] != -1:
            if board[i] == col: return False
            if abs(board[i] - col) == abs(i - row): return False
    return True

# --- ALGORITMA A: BASELINE (Backtracking Biasa) ---
def algo_A(instance):
    n = instance['n']
    fixed_queens = instance['fixed_queens']
    board = [-1] * n
    nodes_explored = 0 

    # 1. Pasang Fixed Queens
    for r, c in fixed_queens:
        board[r] = c

    def solve(row):
        nonlocal nodes_explored
        nodes_explored += 1
        
        if row == n:
            return True
        
        # Jika baris ini sudah diisi Fixed Queen, skip
        if board[row] != -1:
            return solve(row + 1)

        # Coba kolom 0 sampai N-1
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row] = col
                if solve(row + 1):
                    return True
                board[row] = -1
        return False

    if solve(0):
        return board, nodes_explored
    else:
        # Kembalikan papan parsial
        return board, nodes_explored


# --- ALGORITMA B: FORWARD CHECKING (Look Ahead) ---
def algo_B(instance):
    n = instance['n']
    fixed_queens = instance['fixed_queens']
    board = [-1] * n
    nodes_explored = 0

    # Inisialisasi Domain
    initial_domains = {r: set(range(n)) for r in range(n)}

    # Pasang Fixed Queens & Update Domain Awal
    for r, c in fixed_queens:
        board[r] = c
        initial_domains[r] = {c} 

    # Fungsi Pruning
    def prune_domains(current_domains, r_placed, c_placed):
        new_domains = {}
        for r in range(n):
            if r <= r_placed:
                new_domains[r] = current_domains[r]
                continue
            
            allowed_cols = set()
            for c in current_domains[r]:
                # Cek Vertikal & Diagonal
                if c == c_placed: continue
                if abs(r - r_placed) == abs(c - c_placed): continue
                allowed_cols.add(c)
            
            # Jika domain kosong, backtrack
            if not allowed_cols:
                return None 
            
            new_domains[r] = allowed_cols
        return new_domains

    # Pruning awal berdasarkan Fixed Queens
    start_domains = initial_domains
    valid_start = True
    for r_fix, c_fix in fixed_queens:
        start_domains = prune_domains(start_domains, r_fix, c_fix)
        if start_domains is None:
            valid_start = False; break

    def solve(row, current_domains):
        nonlocal nodes_explored
        nodes_explored += 1
        
        if row == n:
            return True

        if board[row] != -1:
            return solve(row + 1, current_domains)

        # Iterasi hanya pada domain yang tersisa
        possible_cols = list(current_domains[row])
        
        for col in possible_cols:
            board[row] = col
            next_domains = prune_domains(current_domains, row, col)
            
            if next_domains is not None:
                if solve(row + 1, next_domains):
                    return True
            
            board[row] = -1
            
        return False

    if valid_start and solve(0, start_domains):
        return board, nodes_explored
    else:
        # Kembalikan papan parsial
        return board, nodes_explored

# BAGIAN 3: EKSEKUSI (Disesuaikan)
def main():
    # Folder tempat instance disimpan
    data_dir = Path(__file__).parent / 'data'
    
    # Header Tabel: Ditambahkan kolom 'Fixed Q'
    header = f"{'Inst':<5} | {'Fixed Q':<9} | {'Algo A (ms)':<12} | {'Nodes A':<10} | {'Score A':<8} | {'Algo B (ms)':<12} | {'Nodes B':<10} | {'Score B':<8}"
    print(header)
    print("-" * len(header))

    # Loop membaca instance 1 sampai 15
    for i in range(1, 16):
        N_SIZE = 12
        filename = f"nqueens_N{N_SIZE}_Inst{i:02d}.json"
        filepath = data_dir / filename
        
        if not filepath.exists():
            print(f"{i:<5} | {'File not found':<70}")
            continue

        try:
            with open(filepath, 'r') as f:
                instance = json.load(f)

            # --- AMBIL INFO FIXED QUEEN ---
            # Mengambil data fixed queen untuk ditampilkan di tabel
            fq_list = instance.get('fixed_queens', [])
            # Format menjadi string "[r, c]" agar rapi di tabel
            fq_str = str(fq_list[0]) if fq_list else "-"

            # --- RUN ALGO A ---
            t0 = time.time()
            sol_A, nodes_A = algo_A(instance)
            dt_A = (time.time() - t0) * 1000
            score_A = evaluate_solution(sol_A, instance)

            # --- RUN ALGO B ---
            t0 = time.time()
            sol_B, nodes_B = algo_B(instance)
            dt_B = (time.time() - t0) * 1000
            score_B = evaluate_solution(sol_B, instance)

            # Print baris hasil dengan kolom Fixed Q
            print(f"{i:<5} | {fq_str:<9} | {dt_A:<12.4f} | {nodes_A:<10} | {score_A:<8.2f} | {dt_B:<12.4f} | {nodes_B:<10} | {score_B:<8.2f}")

        except Exception as e:
            print(f"Error pada instance {i}: {e}")

    print("-" * len(header))
    print("Selesai eksekusi 15 instance.")

if __name__ == '__main__':

    main()
