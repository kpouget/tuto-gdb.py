#include <time.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

#define NB_ITER 100

int is_profiling = 0;

void bug(int i) {
  printf("BUG BUG BUG (i=%d)\n", i);
}

int run(int i) {
  if (!is_profiling) bug(i);

  return is_profiling;
}

void start_profiling(void) {
  assert(!is_profiling);
  is_profiling = 1;
}

void stop_profiling(void) {
  assert(is_profiling);
  is_profiling = 0;
}

int main() {
  int i;

  srand(time(NULL));
  int bad = rand() % NB_ITER;
  
  for(i = 0; i < NB_ITER; i++) {
    if (i != bad) start_profiling();
    run(i);
    if (i != bad) stop_profiling();
  }
}
