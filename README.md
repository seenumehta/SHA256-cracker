# SHA256-cracker
📖 User Guide: Anoop's SHA-256 Cracker

🔹 Step 1: Install Requirements

For Linux (Ubuntu/Debian-based distros):

sudo apt update
sudo apt install python3 python3-pip git hashcat
pip install tqdm

For Android (Termux users):

pkg update && pkg upgrade
pkg install python git
pip install tqdm


---

🔹 Step 2: Clone the Repository

git clone https://github.com/YOUR-USERNAME/SHA256-Cracker.git
cd SHA256-Cracker


---

🔹 Step 3: Run the Script

python3 anoop_sha256_cracker.py


---

🔹 Step 4: Enter Hash & Wordlist

Enter the SHA-256 hash you want to crack.

Provide the path to the wordlist (e.g., rockyou.txt).



---

🔹 Step 5: Choose Cracking Method

1️⃣ Multithreading (CPU-based, fast)
2️⃣ Hashcat (GPU-accelerated, ultra-fast)
3️⃣ Rainbow Table (Precomputed, instant lookup)


---

🔹 Step 6: Get Results

If the hash is found, it will display the cracked password.

If not found, try a larger wordlist or use GPU acceleration with Hashcat.



---

That's it! 🚀 Happy cracking, Anoop! 🔥

