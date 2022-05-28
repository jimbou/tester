#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*void print(char str[])
{
    printf("String Output: ");
    puts(str);
}*/




void hello() {
   printf("hello world\n");
    return;
}



/*void read_rapl() {
    char *path = "" ; // sublirose to me to sosto path 
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    unsigned long long int old ,data;

    FILE *fd = fopen(path, "r");

    if (fd == NULL)
      exit(EXIT_FAILURE);

    while ((read = getline(&line, &len, fd)) != -1) {
      //Do nothing.
    }
    old = strtoull(line, NULL, 10);
    printf("old %llu", old);
    while (data == old ){
      data = strtoull(line, NULL, 10);  
    }



    if (line)
      free(line);

    fclose(fd);
    printf("%llu", data);
    return ;  
}
*/
int main() {
    int a;
    scanf("%d", &a);
    if (a>2){
    hello();   
    }
    else{
      printf("hello world_2\n");   
    }
    return 0;
}


void print(char *s) {
    printf("%s\n", s);
}