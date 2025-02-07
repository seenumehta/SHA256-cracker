# SHA-256 Cracker

## Overview

SHA-256 Cracker is a simple and efficient tool for cracking SHA-256 hashes using multiple methods:

1. **Multithreading** - Uses multiple threads for faster dictionary-based attacks.
2. **Hashcat** - Leverages GPU acceleration for rapid cracking.
3. **Rainbow Table** - Uses precomputed hashes for quick lookups.

## Features

- Supports large wordlists (e.g., `rockyou.txt`).
- Implements multithreading for increased speed.
- Uses Hashcat for GPU acceleration.
- Supports Rainbow Table lookups for precomputed hash matching.

## Installation

### Prerequisites

- Python 3.x
- Hashcat (for GPU-based cracking)

### Install Hashcat (Linux)

```sh
sudo apt update && sudo apt install hashcat -y
```

### Clone the Repository

```sh
git clone https://github.com/seenumehta/sha256-cracker.git
cd sha256-cracker
```

## Usage

Run the script and follow the prompts:

```sh
python sha256_cracker.py
```

### Example Usage

#### Cracking with a Dictionary (Multithreading)

1. Run the script.
2. Enter the SHA-256 hash to crack.
3. Provide the wordlist file (e.g., `rockyou.txt`).
4. Select option `1` for multithreading.

#### Cracking with Hashcat (GPU Acceleration)

1. Run the script.
2. Enter the SHA-256 hash to crack.
3. Provide the wordlist file.
4. Select option `2` to use Hashcat.

#### Using Rainbow Table

1. Run the script.
2. Enter the SHA-256 hash.
3. Select option `3` to search in the Rainbow Table.

If the Rainbow Table is not found, the script provides an option to generate one.

## Contributing

Feel free to fork the repository and submit pull requests for improvements.

## License

This project is open-source under the MIT License.

