//
// Created by 田明博 on 2024/6/27.
//

#include <syslog.h>

int main() {
    // 打开系统日志，使用LOG_PID标志将程序的PID包含在每条日志消息中
    openlog("myprogram", LOG_PID, LOG_USER);

    // 记录不同级别的日志消息
    syslog(LOG_INFO, "This is an informational message.");
    syslog(LOG_WARNING, "This is a warning message.");
    syslog(LOG_ERR, "This is an error message.");

    // 关闭系统日志
    closelog();

    return 0;
}
