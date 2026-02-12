#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static const char payload[] =
"__PAYLOAD__";

int main() {

    FILE *fp = popen("base64 -d | sh", "w");
    if (!fp) return 1;

    fwrite(payload, 1, strlen(payload), fp);

    pclose(fp);
    return 0;
}