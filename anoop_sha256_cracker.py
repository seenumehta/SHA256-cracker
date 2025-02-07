import hashlib
import os
import threading
import subprocess
from queue import Queue

NUM_THREADS = 8  
RAINBOW_TABLE_FILE = "sha256_rainbow_table.txt"

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def load_wordlist(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return []
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read().splitlines()

def lookup_rainbow_table(target_hash, table_file):
    if not os.path.exists(table_file):
        print("No Rainbow Table found.")
        return None
    
    with open(table_file, "r") as f:
        for line in f:
            try:
                hash_value, word = line.strip().split(":")
                if hash_value == target_hash:
                    return word
            except ValueError:
                continue
    return None

def worker(queue, target_hash, found_flag):
    while not queue.empty() and not found_flag.is_set():
        word = queue.get()
        if sha256_hash(word) == target_hash:
            print(f"Match found: {word}")
            found_flag.set()
            return

def crack_sha256_multithreaded(target_hash, wordlist):
    queue = Queue()
    for word in wordlist:
        queue.put(word)

    found_flag = threading.Event()
    threads = []

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(queue, target_hash, found_flag))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if not found_flag.is_set():
        print("No match found.")

def run_hashcat(target_hash, wordlist_file):
    print("Running Hashcat...")
    
    hash_file = "hash_to_crack.txt"
    with open(hash_file, "w") as f:
        f.write(target_hash)
    
    cmd = ["hashcat", "-m", "1400", "-a", "0", hash_file, wordlist_file, "--force"]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except FileNotFoundError:
        print("Hashcat not found.")
    except subprocess.CalledProcessError:
        print("Hashcat failed.")

hash_to_crack = input("Enter SHA-256 hash: ").strip()
wordlist_file = input("Enter wordlist file: ").strip()

wordlist = load_wordlist(wordlist_file)

if wordlist:
    print("Choose method:")
    print("1. Multithreading")
    print("2. Hashcat")
    print("3. Rainbow Table")

    choice = input("Select method: ").strip()

    if choice == "1":
        crack_sha256_multithreaded(hash_to_crack, wordlist)
    elif choice == "2":
        run_hashcat(hash_to_crack, wordlist_file)
    elif choice == "3":
        match = lookup_rainbow_table(hash_to_crack, RAINBOW_TABLE_FILE)
        if match:
            print(f"Found: {match}")
        else:
            print("Not found in Rainbow Table.")
    else:
        print("Invalid choice.")
