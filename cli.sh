#!/system/bin/sh

set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$APP_DIR/build"

mkdir -p "$BUILD_DIR"

build_cmd() {

    if [ -z "$1" ]; then
        echo "Target script required"
        exit 1
    fi

    TARGET="$1"

    if [ ! -f "$TARGET" ]; then
        echo "File tidak ditemukan!"
        exit 1
    fi

    echo "[+] Running Python compiler..."

    python3 "$APP_DIR/run.py" "$TARGET"

    echo "[✓] Build selesai"
}

encrypt_cmd() {

    if [ -z "$1" ]; then
        echo "File required"
        exit 1
    fi

    "$APP_DIR/encrypt.sh" "$1"
}

case "$1" in
    build)
        shift
        build_cmd "$@"
        ;;
    encrypt)
        shift
        encrypt_cmd "$@"
        ;;
    *)
        echo "Command tidak dikenal"
        ;;
esac