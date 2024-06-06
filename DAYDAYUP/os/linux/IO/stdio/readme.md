## stdio
1. FILE *fopen(const char *path, const char *mode);
2. fclose()
3. fgetc()
4. int fputc(int c, FILE *stream);
5. char *fgets(char *str, int size, FILE *stream);
6. int fputs(const char *restrict s, FILE *restrict stream);
7. fread()
8. fwrite()
9. printf()
10. scanf()
11. fseek()
12. int fseeko(FILE *stream, off_t offset, int whence);
13. ftell()
14. off_t ftello(FILE *stream);
15. rewind()
16. fflush()
17. getline()
18. char *tmpnam(char *s); 
19. FILE *tmpfile(void);