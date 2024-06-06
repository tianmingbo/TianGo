## 文件IO

1. int open(const char *pathname, int flags);
   int open(const char *pathname, int flags, mode_t mode);
2. int close(int fd);
3. ssize_t read(int fildes, void *buf, size_t nbyte);
4. ssize_t write(int fildes, const void *buf, size_t nbyte);
5. off_t lseek(int fildes, off_t offset, int whence);
6. int dup(int fildes);
7. dup2()
8. sync()
9. fsync()
10. fdatasync()
11. fcntl()
12. ioctl()

文件IO和标准IO不可混用
转换: fileno(),fdopen()