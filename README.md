# XShield Compiler Tools

```
╭────────────────────────────────╮
      XShield Compiler v7.1      
           (Plus Edition)        

      Copyright (C) 2026         
      XShield Team Project       
╰────────────────────────────────╯
```

> **XShield** adalah tools untuk mengkompilasi dan mengobfuskasi script Shell (`.sh`) maupun program C (`.c`) menjadi binary terenkripsi yang dilindungi berbagai lapisan proteksi.

---

## Fitur

- Enkripsi payload dengan XOR multi-round + key & salt acak
- Obfuskasi loader: junk functions, random arrays, padding blobs, chunking
- Proteksi Anti-Debug, Anti-VM, Anti-Reverse
- Self-Delete setelah eksekusi
- Expiry date (binary otomatis mati setelah tanggal tertentu)
- Kompresi UPX (--lzma -9) + strip otomatis di mode release
- Mendukung compiler: `gcc`, `clang`, `tcc`, atau auto-detect

---

## Requirements

Pastikan tools berikut tersedia di sistem sebelum kompilasi:

| Tools | Fungsi | Install |
|-------|--------|---------|
| `gcc` / `clang` / `tcc` | Compiler utama | `pkg install gcc` / `apt install gcc` |
| `make` | Build system | `pkg install make` |
| `upx` | Kompresi binary (opsional) | `pkg install upx` |
| `strip` | Strip simbol (opsional) | sudah include di `binutils` |

---

## Cara Compile XShield

### 1. Clone Repository

```bash
git clone https://github.com/aetherdev22/XShield.git
cd XShield
```

### 3. (Opsional) Install Global

```bash
cp xc /usr/local/bin/xc
chmod +x /usr/local/bin/xc
```

---

## Cara Pakai

### Sintaks

```
./xc <script.sh | program.c> [options]
```

### Options

| Flag | Keterangan | Default |
|------|-----------|---------|
| `-m release\|debug` | Build mode | `release` |
| `-o OUTPUT` | Nama output binary | basename dari input |
| `-c auto\|gcc\|clang\|tcc` | Pilih compiler | `auto` |
| `--anti-debug` | Aktifkan anti-debug traps | off |
| `--anti-vm` | Aktifkan deteksi anti-VM | off |
| `--anti-reverse` | Aktifkan anti-reverse constructor | off |
| `--self-delete` | Binary hapus diri setelah eksekusi | off |
| `--expire YYYY-MM-DD` | Set tanggal kedaluwarsa binary | none |
| `--no-upx` | Skip kompresi UPX | off |
| `--no-strip` | Skip strip binary | off |
| `--save-c` | Simpan generated `.c` source | off |
| `-q` / `--quiet` | Sembunyikan semua output | off |

---

## Contoh Penggunaan

**Compile script shell dasar:**
```bash
./xc script.sh
```

**Compile program C:**
```bash
./xc program.c
```

**Mode release dengan nama output custom:**
```bash
./xc script.sh -m release -o mybin
```

**Full proteksi:**
```bash
./xc script.sh -m release --anti-debug --anti-vm --anti-reverse --self-delete
```

**Dengan expiry date:**
```bash
./xc script.sh --expire 2026-12-31 --self-delete
```

**Ganti compiler ke tcc:**
```bash
./xc script.sh -c tcc -m release -o output
```

**Simpan generated source C:**
```bash
./xc script.sh --save-c
```

**Mode debug (tanpa strip & upx):**
```bash
./xc script.sh -m debug -o test_bin
```

**Self-compile:**
```bash
./xc xc.c -o xc
```

**Help Instruction:**
```bash
./xc -h
```

---

## Compile di Android (Termux)

```bash
# Install dependencies
pkg update && pkg install -y gcc tcc upx binutils

# Clone & compile
git clone https://github.com/aetherdev22/XShield.git
cd XShield

# Jalankan
./xc script.sh -m release --anti-debug --anti-vm
```

---

## Output Build

Setelah kompilasi berhasil, terminal menampilkan summary seperti berikut:

```
╭────────────────────────────────────────────────╮
│  ▸ XShield BUILDER  Payload Obfuscator & Compiler
│  ──────────────────────────────────────────────│
│  [*] Input
│       Path  : /sdcard/script.sh
│       Size  : 34962 bytes
│       Type  : Shell script
│  ──────────────────────────────────────────────│
│  ✔ BUILD SUCCESS
│  ──────────────────────────────────────────────│
│    Output File : /sdcard/mybin
│    File Size   : 345.29 KB
│    Anti-Debug  : ✔ ENABLED
│    Anti-VM     : ✔ ENABLED
╰────────────────────────────────────────────────╯
```

---

## Struktur File

```
XShield/
├── xc.c            # Source utama compiler
├── xc              # Binary hasil compile
└── README.md       # Dokumentasi ini
```

---

## Notes

- Mode `release` otomatis menjalankan `strip` dan `upx` jika tersedia di sistem
- Mode `debug` menonaktifkan strip, upx, dan optimasi — cocok untuk testing
- Flag `--save-c` menyimpan generated loader sebagai file `.c` di direktori yang sama dengan output
- Binary yang sudah di-compile tidak membutuhkan dependency apapun (standalone)
- Flag `--expire` menggunakan format `YYYY-MM-DD` dan binary akan menolak eksekusi setelah tanggal tersebut

---

## License

Copyright (C) 2026 XShield Team Project. All rights reserved.
