/**
 * 当你拨打长途电话时,电话公司所保存的信息包括你拨打电话的日期和时间。它还包括三个电话号码:你使用的那个电话、你呼叫的那个电话以及你付账的那个电话。
 * 这些电话号码的每一个都由三个部分组成:区号、交换台和站号码。请为这些记账信息编写一个结构声明。
 *
 * */

struct Phone {
    short area;
    short exchange;
    short station;
};
struct Record {
    short year;
    short month;
    short day;
    int time;
    struct Phone called;
    struct Phone calling;
    struct Phone billed;
};