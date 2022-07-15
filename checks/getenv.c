#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
  const char *v = getenv("MYGETENVTEST");
  if (NULL == v) return 1;
  if (0 != strcmp(v, "GETENVWORKS")) {
    puts(v);
    return 2;
  }
  return 0;
}
