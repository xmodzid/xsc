#!/system/bin/sh

set -e

if [ $# -ne 1 ]; then
    echo "Usage: ./run.sh script.sh"
    exit 1
fi

INPUT="$1"

if [ ! -f "$INPUT" ]; then
    echo "File tidak ditemukan!"
    exit 1
fi

NAME=$(basename "$INPUT" .sh)
BUILD=build
OUT_C="$BUILD/$NAME.c"
OUT_BIN="$BUILD/$NAME"

mkdir -p "$BUILD"

echo "[+] Encoding payload..."

# encode base64
PAYLOAD=$(base64 "$INPUT")

echo "[+] Generating loader..."

cat > "$OUT_C" <<EOF
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char payload[] =
"$PAYLOAD";

int main() {

    FILE *fp = popen("base64 -d | sh", "w");
    if (!fp) return 1;

    fwrite(payload, 1, strlen(payload), fp);

    pclose(fp);
    return 0;
}
EOF

echo "[+] Compiling..."

clang "$OUT_C" -o "$OUT_BIN" -Oz -s -fPIE -pie

chmod 777 "$OUT_BIN"

echo "[✓] Done -> $OUT_BIN"