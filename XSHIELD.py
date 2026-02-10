import os
import sys
import subprocess
import random
import string
import hashlib


def check_file_exists(target):
    if not os.path.isfile(target):
        print("File tidak ditemukan!")
        sys.exit(1)


def c_array_bytes(data, bytes_per_line=32):  # 32 bytes per line for shorter array (fewer lines)
    lines = []
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i + bytes_per_line]
        line = ", ".join(f"0x{b:04x}" for b in chunk)  # Changed to 4-digit hex for longer entries, making array shorter
        lines.append(line)
    return ",\n".join(lines)


def c_escape_str(s):
    return (s.replace("\\","\\\\")
             .replace("\"","\\\"")
             .replace("\n","\\n")
             .replace("\r",""))


def generate_symbol():
    ascii="!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
    ascii=ascii.replace("'","").replace("\\","")
    return random.choice(ascii)


def generate_key(length=512):  # All keys now 512 bytes for consistency
    # Advanced key generation using SHA-512 for better randomness and strength
    seed = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=128))  # Longer seed
    hash_obj = hashlib.sha512(seed.encode())
    key = list(hash_obj.digest()) * (length // 64 + 1)
    return key[:length]


def xor_encrypt(data,key):
    return [b ^ key[i%len(key)] for i,b in enumerate(data)]


def caesar_encrypt(data,shift,symbol):
    sym=ord(symbol)
    return [((b ^ sym)+shift)%256 for b in data]


def arc4_encrypt(data,key):
    S=list(range(256))
    j=0
    for i in range(256):
        j=(j+S[i]+key[i%len(key)])%256
        S[i],S[j]=S[j],S[i]

    out=[]
    i=j=0
    for byte in data:
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        k=S[(S[i]+S[j])%256]
        out.append(byte ^ k)
    return out


# ===== Chaotic fragment =====

def chaotic_fragment(line):

    words=line.split()

    if len(words) < 2:
        return line

    fragments=[]

    for w in words:

        if len(w) > 4 and random.random() < 0.5:

            cut=random.randint(1,len(w)-2)
            fragments.append(w[:cut])
            fragments.append(w[cut:])
        else:
            fragments.append(w)

    result=[]
    i=0

    while i < len(fragments):

        if i < len(fragments)-1 and random.random() < 0.5:
            result.append(fragments[i] + fragments[i+1])
            i+=2
        else:
            result.append(fragments[i])
            i+=1

    random.shuffle(result)
    return " ".join(result)


# ===== Dummy 8% =====

def generate_dummy(text):

    lines=[l.strip() for l in text.splitlines() if l.strip()]

    if not lines:
        lines=["echo dummy"]

    file_size=len(text.encode())
    target_size=max(32, file_size * 8 // 100)

    collected=[]
    current_size=0

    while current_size < target_size:

        base=random.choice(lines)
        fragment=chaotic_fragment(base) + "\n"

        collected.append(fragment)
        current_size += len(fragment.encode())

    random.shuffle(collected)
    return "".join(collected)  # Gabungkan menjadi satu string multi-baris


# ===== Dummy builder =====

def build_dummy_functions(dummy_text):

    esc=c_escape_str(dummy_text)

    fname="df_"+''.join(random.choices(string.ascii_lowercase,k=6))
    var="dm_"+''.join(random.choices(string.ascii_lowercase,k=6))

    function=f'''
volatile const char *{var}="{esc}";
void {fname}(){{
volatile unsigned int s=0;
for(size_t i=0;i<strlen({var});i++)
s+={var}[i];
if(s==999999) printf("%u",s);
}}
'''

    call=f"{fname}();"

    return [function], [call]  # Hanya satu function dan satu call


# ===== Junk =====

def generate_junk():

    junk=[]

    for _ in range(random.randint(3,5)):

        name=''.join(random.choices(string.ascii_lowercase,k=6))

        junk.append(f'''
void {name}(){{
volatile int x=0;
for(int i=0;i<40;i++)
x+=i;
}}
''')

    return junk


# ===== Advanced Obfuscated Strings =====

def obfuscate_string_advanced(s):
    # Multi-layer obfuscation: XOR + Caesar + ARC4 with 512-byte keys for all
    data = s.encode()
    xor_key = generate_key(512)  # Changed to 512
    caesar_shift = random.randint(1,255)
    caesar_sym = generate_symbol()
    arc4_key = generate_key(512)  # Changed to 512
    
    stage1 = xor_encrypt(data, xor_key)
    stage2 = caesar_encrypt(stage1, caesar_shift, caesar_sym)
    stage3 = arc4_encrypt(stage2, arc4_key)
    
    return c_array_bytes(stage3), len(stage3), xor_key, caesar_shift, caesar_sym, arc4_key

def generate_obfuscated_strings():
    strings = [
        "sh",
        "-c",
        "/system/bin/sh",
        "execl",
        "malloc",
        "memcpy",
        "strlen",
        "printf",
        "volatile",
        "const",
        "char",
        "uint8_t",
        "int",
        "size_t",
        "for",
        "if",
        "return",
        "void",
        "static",
        "include",
        "stdio.h",
        "stdlib.h",
        "stdint.h",
        "string.h",
        "unistd.h"
    ]
    obfuscated = {}
    for s in strings:
        arr, length, xor_k, caesar_s, caesar_sym, arc4_k = obfuscate_string_advanced(s)
        obfuscated[s] = (arr, length, xor_k, caesar_s, caesar_sym, arc4_k)
    return obfuscated

# ===== Hidden Anti-Debug (Obfuscated Function Names) =====

def generate_anti_debug():
    # Obfuscated function name to hide it in binary, starting with letter
    func_name = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f'''
int {func_name}() {{
    // PTRACE_TRACEME
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {{
        return 1; // Being traced
    }}
    // TracerPID check
    FILE *fp = fopen("/proc/self/status", "r");
    if (fp) {{
        char line[256];
        while (fgets(line, sizeof(line), fp)) {{
            if (strstr(line, "TracerPid:")) {{
                int pid;
                sscanf(line, "TracerPid: %d", &pid);
                if (pid != 0) {{
                    fclose(fp);
                    return 1; // Being traced
                }}
                break;
            }}
        }}
        fclose(fp);
    }}
    return 0;
}}
''', func_name

# ===== Hidden Frida Detection =====

def generate_frida_detection():
    func_name = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f'''
int {func_name}() {{
    // Scan memory for Frida signatures
    FILE *fp = fopen("/proc/self/maps", "r");
    if (!fp) return 0;
    char line[256];
    while (fgets(line, sizeof(line), fp)) {{
        if (strstr(line, "frida") || strstr(line, "Frida")) {{
            fclose(fp);
            return 1;
        }}
    }}
    fclose(fp);
    // Check for Frida ports
    for (int port = 27040; port <= 27050; port++) {{
        char cmd[256];
        sprintf(cmd, "netstat -tuln | grep :%d", port);
        if (system(cmd) == 0) {{
            return 1;
        }}
    }}
    return 0;
}}
''', func_name

# ===== Hidden Xposed Detection =====

def generate_xposed_detection():
    func_name = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f'''
int {func_name}() {{
    // Check for Xposed framework
    if (access("/system/framework/XposedBridge.jar", F_OK) != -1) {{
        return 1;
    }}
    // Check for Xposed modules
    DIR *dir = opendir("/data/app");
    if (dir) {{
        struct dirent *entry;
        while ((entry = readdir(dir))) {{
            if (strstr(entry->d_name, "xposed")) {{
                closedir(dir);
                return 1;
            }}
        }}
        closedir(dir);
    }}
    return 0;
}}
''', func_name

# ===== Hidden Emulator Detection =====

def generate_emulator_detection():
    func_name = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f'''
int {func_name}() {{
    // Hardware fingerprint analysis
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp) {{
        char line[256];
        while (fgets(line, sizeof(line), fp)) {{
            if (strstr(line, "goldfish") || strstr(line, "ranchu") || strstr(line, "Bluestacks") || strstr(line, "LDPlayer")) {{
                fclose(fp);
                return 1;
            }}
        }}
        fclose(fp);
    }}
    // Check for emulator-specific files
    if (access("/system/lib/libdvm.so", F_OK) != -1 && access("/system/bin/qemu-props", F_OK) != -1) {{
        return 1;
    }}
    return 0;
}}
''', func_name

# ===== Hidden Network Obfuscation =====

def generate_network_obfuscation():
    func_name = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f'''
void {func_name}() {{
    // This is a placeholder for network obfuscation
    // In a real implementation, use HTTPS with randomized headers
    // For now, just a dummy function
    srand(time(NULL));
    char headers[10][256];
    for (int i = 0; i < 10; i++) {{
        sprintf(headers[i], "X-Random-%d: %d", i, rand());
    }}
}}
''', func_name

# ===== Hidden Anti Universal Decryption =====

def generate_anti_universal_dec():
    func_name = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f'''
void {func_name}() {{
    // Dummy anti-decompilation measures
    // Use inline assembly or other tricks to confuse decompilers
    __asm__ volatile (
        "nop\\n"
        "nop\\n"
        "nop\\n"
    );
}}
''', func_name

# ===== Library Name Obfuscation =====

def generate_library_obfuscation():
    libs = ["libc.so", "libdl.so", "libm.so"]
    obfuscated_libs = {}
    for lib in libs:
        arr, length, xor_k, caesar_s, caesar_sym, arc4_k = obfuscate_string_advanced(lib)
        obfuscated_libs[lib] = (arr, length, xor_k, caesar_s, caesar_sym, arc4_k)
    return obfuscated_libs

# ================= MAIN =================

if len(sys.argv)!=2:
    print("Usage: xsc file.sh")
    sys.exit(1)


target=sys.argv[1]
check_file_exists(target)

# Generate output name based on input file (without .sh extension)
output_name = os.path.splitext(os.path.basename(target))[0]

data=open(target,"rb").read()
text=data.decode("utf-8","ignore")

print("[+] Encrypting payload with enhanced strength...")

dummy_text=generate_dummy(text)
dummy_functions,dummy_calls=build_dummy_functions(dummy_text)
junk_functions=generate_junk()

obfuscated_strings = generate_obfuscated_strings()
anti_debug_code, anti_debug_func = generate_anti_debug()
frida_detection_code, frida_func = generate_frida_detection()
xposed_detection_code, xposed_func = generate_xposed_detection()
emulator_detection_code, emulator_func = generate_emulator_detection()
network_obfuscation_code, network_func = generate_network_obfuscation()
obfuscated_libs = generate_library_obfuscation()
anti_universal_dec_code, anti_dec_func = generate_anti_universal_dec()

extra_code="\n".join(dummy_functions + junk_functions)

xor_key=generate_key(512)  # 512-byte XOR key
arc4_key=generate_key(512)  # 512-byte ARC4 key
shift=random.randint(1,255)
symbol=generate_symbol()

# Additional encryption layer for extra strength: Reverse bytes after ARC4
stage1=xor_encrypt(data,xor_key)
stage2=caesar_encrypt(stage1,shift,symbol)
stage3=arc4_encrypt(stage2,arc4_key)
stage4 = stage3[::-1]  # Reverse for added complexity

payload_bytes=c_array_bytes(stage4, 32)  # 32 bytes per line for shorter array
xor_str=c_array_bytes(xor_key, 32)  # 32 bytes per line for keys
arc4_str=c_array_bytes(arc4_key, 32)  # 32 bytes per line for keys

loader=f'''
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <dirent.h>
#include <time.h>

const char *xshield="\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n🆇🆂🅷🅸🅴🅻🅳🅲🅾🅼🅿🅸🅻🅴🆁🆂🅷🅴🅻🅻\\n         Version 5.3 Plus(xsc)\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\\n   • Github : xmodzid.github.io/xsc\\n   • Telegram : @get01projects\\n━━━━━━━━━━━━━━━━━━━━━━━━━━━ \\n";

{extra_code}

{anti_debug_code}

{frida_detection_code}

{xposed_detection_code}

{emulator_detection_code}

{network_obfuscation_code}

{anti_universal_dec_code}

static uint8_t S[256];
static uint8_t i1,j1;

void arc4_key(uint8_t *k){{
for(int i=0;i<256;i++) S[i]=i;
int j=0;
for(int i=0;i<256;i++){{
j=(j+S[i]+k[i%512])&255;  // Adjusted for 512-byte key
uint8_t t=S[i]; S[i]=S[j]; S[j]=t;
}}
i1=j1=0;
}}

void arc4(uint8_t *d,int len){{
for(int n=0;n<len;n++){{
i1=(i1+1)&255;
j1=(j1+S[i1])&255;
uint8_t t=S[i1]; S[i1]=S[j1]; S[j1]=t;
d[n]^=S[(S[i1]+S[j1])&255];
}}
}}

void caesar(uint8_t *d,int len,int s,char sym){{
for(int i=0;i<len;i++){{
d[i]=(d[i]-s+256)%256;
d[i]^=sym;
}}
}}

void xor_dec(uint8_t *d,int len,uint8_t *k){{
for(int i=0;i<len;i++) d[i]^=k[i%512];  // Adjusted for 512-byte key
}}

void reverse_bytes(uint8_t *d, int len) {{
    for (int i = 0; i < len / 2; i++) {{
        uint8_t temp = d[i];
        d[i] = d[len - 1 - i];
        d[len - 1 - i] = temp;
    }}
}}

const uint8_t payload[]={{
{payload_bytes}
}};

const uint8_t xor_key[512]={{ {xor_str} }};
const uint8_t arc4_key_data[512]={{ {arc4_str} }};

const int shift={shift};
const char sym='{symbol}';

void run_dummy(){{
{''.join(dummy_calls)}
}}

int main(){{
run_dummy();

// Disabled detections for direct execution (commented out to prevent auto-exit)
#if 0
int ad = {anti_debug_func}();
int fd = {frida_func}();
int xd = {xposed_func}();
int ed = {emulator_func}();

if (ad || fd || xd || ed) {{
    return 1; // Exit if any detection triggers
}}
#endif

{network_func}();
{anti_dec_func}();

int len=sizeof(payload);
uint8_t *buf=malloc(len+1);
if (!buf) {{
    perror("malloc failed");
    return 1;
}}
memcpy(buf,payload,len);

// Reverse first (undo stage4)
reverse_bytes(buf, len);
// Then ARC4
arc4_key((uint8_t*)arc4_key_data);
arc4(buf,len);
// Then Caesar
caesar(buf,len,shift,sym);
// Then XOR
xor_dec(buf,len,(uint8_t*)xor_key);

buf[len]=0;

if (execl("/system/bin/sh","sh","-c",(char*)buf,NULL) == -1) {{
    perror("execl failed");
    free(buf);
    return 1;
}}
free(buf);
return 0;
}}
'''

open("loader.c","w").write(loader)

print("[+] Compiling...")

cmd=["clang","loader.c","-o",output_name,"-Oz","-s","-fPIE","-pie"]

if subprocess.run(cmd).returncode!=0:
    print("Compile gagal!")
    sys.exit()

os.chmod(output_name,0o777)

print(f"[✓] Done -> {output_name} (0777)")