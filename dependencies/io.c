#include <stdio.h>

void __write_int(int ni) {
  printf("%d\n", ni);
}

void __write_float(float nf) {
  printf("%f\n", nf);
}

int __read_int() {
  int num;
  scanf("%d", &num);
  return num;
}

float __read_float() {
  float num;
  scanf("%f", &num);
  return num;
}
