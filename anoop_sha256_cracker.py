import hashlib
import os
import threading
import subprocess
from queue import Queue
from tqdm import tqdm  # Progress bar

# Configurable number of threads
NUM_THREADS = 8  
RAINBOW_TABLE_FILE = "sha256_rainbow_table.txt"  # File to store precomputed hashes

# Metasploit-style banner
def show_banner():
    banner = r"""
     █████╗ ███╗   ██╗ ██████╗  ██████╗ ██████╗ 
    ██╔══██╗████╗  ██║██╔════╝ ██╔═══██╗██╔══██╗
    ███████║██╔██╗ ██║██║  ███╗██║   ██║██████╔╝
    ██╔══██║██║╚██╗██║██║   ██║██║   ██║██╔══██╗
    ██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝  
    🔥 SHA-256 Cracker | Created by Anoop 🔥
    """
    print(banner)

def sha256_hash(text):
    """Generate SHA-256 hash of a given text."""
    return hashlib.sha256(text.encode()).hexdigest()

def load_wordlist(file_path):
    """Load words from a dictionary file."""
    if not os.path.exists(file_path):
        print(f"❌ Error: The file '{file_path}' was not found.")
        return []
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return [line.strip() for line in file]

def build_rainbow_table(wordlist, table_file):
    """Precompute hashes and store them in a rainbow table file."""
    print("⚡ Building Rainbow Table... This may take a while.")
    with open(table_file, "w") as f:
        for word in tqdm(wordlist, desc="📜 Generating Hashes", unit=" words"):
            f.write(f"{sha256_hash(word)}:{word}\n")
    print(f"✅ Rainbow table saved to {table_file}")

def lookup_rainbow_table(target_hash, table_file):
    """Check if hash exists in the precomputed rainbow table."""
    if not os.path.exists(table_file):
        print("⚠️ No Rainbow Table found. Please generate one first.")
        return None

    with open(table_file, "r") as f:
        for line in f:
            hash_value, word = line.strip().split(":")
            if hash_value == target_hash:
                return word
    return None

def worker(queue, target_hash, found_flag, progress_bar):
    """Thread worker function that processes words from the queue."""
    while not queue.empty():
        if found_flag.is_set():
            return  # Stop if another thread found the password

        word = queue.get()
        progress_bar.update(1)  # Update progress bar

        if sha256_hash(word) == target_hash:
            print(f"\n✅ Match found! The original text is: **{word}**")
            found_flag.set()  # Stop other threads
            return

def crack_sha256_multithreaded(target_hash, wordlist):
    """Multithreaded SHA-256 cracking function with progress bar."""
    print("\n🔎 Searching for a match using multithreading...\n")

    queue = Queue()
    for word in wordlist:
        queue.put(word)

    found_flag = threading.Event()
    threads = []

    with tqdm(total=len(wordlist), desc="🛠️ Cracking Progress", unit=" words") as progress_bar:
        for _ in range(NUM_THREADS):
            thread = threading.Thread(target=worker, args=(queue, target_hash, found_flag, progress_bar))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    if not found_flag.is_set():
        print("❌ No match found in the given wordlist.")

def run_hashcat(target_hash, wordlist_file):
    """Run Hashcat for GPU-accelerated cracking."""
    print("\n⚡ Running Hashcat for faster cracking...")
    
    hash_file = "hash_to_crack.txt"
    
    # Save hash to a file
    with open(hash_file, "w") as f:
        f.write(target_hash)
    
    # Hashcat command (-m 1400 for SHA-256, -a 0 for dictionary attack)
    cmd = ["hashcat", "-m", "1400", "-a", "0", hash_file, wordlist_file, "--force"]

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("❌ Hashcat not found. Install it with: sudo apt install hashcat")
    except subprocess.CalledProcessError:
        print("⚠️ Hashcat failed. Try manually running the command.")

# --- Main Execution ---
show_banner()

print("🔐 SHA-256 Hash Cracker (Multithreaded + Hashcat + Rainbow Table) 🔐")

hash_to_crack = input("🔹 Enter the SHA-256 hash to crack: ").strip()
wordlist_file = input("📂 Enter the path to the wordlist file (e.g., rockyou.txt): ").strip()

# Load wordlist
wordlist = load_wordlist(wordlist_file)

if wordlist:
    print("\n🌐 Choose Cracking Method:")
    print("1️⃣ Use Python (Multithreading)")
    print("2️⃣ Use Hashcat (GPU-Accelerated)")
    print("3️⃣ Use Rainbow Table (Fastest)")

    choice = input("\n👉 Select method (1, 2, or 3): ").strip()

    if choice == "1":
        crack_sha256_multithreaded(hash_to_crack, wordlist)
    elif choice == "2":
        run_hashcat(hash_to_crack, wordlist_file)
    elif choice == "3":
        match = lookup_rainbow_table(hash_to_crack, RAINBOW_TABLE_FILE)
        if match:
            print(f"\n✅ Found in Rainbow Table! The original text is: **{match}**")
        else:
            print("\n⚠️ Not found in Rainbow Table. You may need to generate one.")
            build_choice = input("🔹 Generate Rainbow Table now? (y/n): ").strip().lower()
            if build_choice == "y":
                build_rainbow_table(wordlist, RAINBOW_TABLE_FILE)
    else:
        print("❌ Invalid choice. Exiting...")
