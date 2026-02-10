# XSC — XShield Script Compiler

> [!CAUTION]
> **Development Status**  
> XSC masih dalam tahap pengembangan aktif. Fitur, metode proteksi, dan struktur output dapat berubah sewaktu-waktu.

---

## 🛡 Tentang XSC

**XShield Script Compiler (XSC)** adalah compiler yang mengubah **Bash Script** menjadi **binary ELF native** untuk meningkatkan keamanan source code dan distribusi script.

XSC menggunakan kombinasi **GCC + Clang (aarch64)** serta sistem obfuscation untuk melindungi script dari reverse engineering dan analisis statis.

---

## 🚀 Fitur Utama

### 🔄 Bash to Native Binary
Mengubah script `.sh` menjadi executable binary.

- 🔐 Source script tidak dapat dibaca langsung
- ⚡ Eksekusi lebih cepat dibanding interpreter shell
- 📦 Output berupa binary standalone

---

### ⚙️ Dual Compiler Engine

XSC menggunakan toolchain modern:

- 🧰 **GCC** → Stabil dan kompatibel luas
- 🧬 **Clang aarch64** → Optimal untuk ARM64
- 🔀 Auto compiler selection

---

### 🧠 Protection Layer

Lapisan keamanan tambahan:

- 🧩 String obfuscation
- 🧱 Dummy logic injection
- 🌀 Basic anti static analysis
- 🔒 Runtime payload execution (memory only)

---

### 📦 Standalone Output

- ❌ Tidak membutuhkan Bash source saat runtime
- ✅ Binary langsung bisa dijalankan
- ✅ Cocok untuk distribusi script

---

## 🛠 Kompatibilitas

| Spesifikasi | Status |
|------------|---------|
| OS | Linux / Android |
| CPU ABI | arm64-v8a (aarch64) |
| armeabi-v7a | ⚠️ Terbatas |
| Root | ❌ Tidak wajib |

> ⚠️ Direkomendasikan menggunakan perangkat ARM64 untuk performa dan stabilitas terbaik.

---

## 📦 Cara Penggunaan

### ▶️ Compile Script

```bash
./xsc p.sh