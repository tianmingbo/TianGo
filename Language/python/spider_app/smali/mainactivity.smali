.class public Lcom/xjb/demo02/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;   #.super 后跟的是父类
.source "MainActivity.java"   #文件名


#V  void
#Z  boolean
#B  byte
#S  short
#C  char
#I  int
#J  long
#F  float
#D  double

# instance fields
.field private total:Ljava/lang/String;   # .field声明变量，和java一样有类型修饰符


# direct methods
# .method声明函数，以.end method关键词结束
.method public constructor <init>()V
    .locals 1

    .line 10
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 11
    const-string v0, "hello"

    iput-object v0, p0, Lcom/xjb/demo02/MainActivity;->total:Ljava/lang/String;

    return-void
.end method

.method static staticSecret()V
    .locals 2

    .line 42
    const-string v0, "tian"

    const-string v1, "this is a static method"

    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 43
    return-void
.end method


# virtual methods
.method fun(Ljava/lang/String;)Ljava/lang/String;
    .locals 1
    .param p1, "x"    # Ljava/lang/String;

    .line 33
    sget-object v0, Ljava/util/Locale;->ROOT:Ljava/util/Locale;

    invoke-virtual {p1, v0}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method fun(II)V
    .locals 2
    .param p1, "x"    # I
    .param p2, "y"    # I

    .line 29
    add-int v0, p1, p2

    invoke-static {v0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v0

    const-string v1, "tian"
    #静态函数一个参数不在是指针
    invoke-static {v1, v0}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 30
    return-void
.end method


#无返回值的protected修饰的onCreate方法
#invoke[static|virtual|super] 分别表示调用静态函数/正常函数/父类函数
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 2   #表示非参数的变量有多少
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;  .param用于声明方法中的参数名

    .line 15 #表示在java源文件中的位置
    #调用父类函数,p0代表this指针,p1是参数savedInstanceState
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 16
    const v0, 0x7f0b001c

    invoke-virtual {p0, v0}, Lcom/xjb/demo02/MainActivity;->setContentView(I)V

    .line 19
    :goto_0
    const-wide/16 v0, 0x3e8

    :try_start_0
    invoke-static {v0, v1}, Ljava/lang/Thread;->sleep(J)V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    .line 22
    goto :goto_1

    .line 20
    :catch_0
    move-exception v0

    .line 21
    .local v0, "e":Ljava/lang/InterruptedException;
    invoke-virtual {v0}, Ljava/lang/InterruptedException;->printStackTrace()V

    .line 23
    .end local v0    # "e":Ljava/lang/InterruptedException;
    :goto_1
    const/16 v0, 0x32

    const/16 v1, 0x1e   #定义一个数据宽度为16位的数据常量0X1e保存在V1寄存器中

    invoke-virtual {p0, v0, v1}, Lcom/xjb/demo02/MainActivity;->fun(II)V

    .line 24
    const-string v0, "run Me"

    invoke-virtual {p0, v0}, Lcom/xjb/demo02/MainActivity;->fun(Ljava/lang/String;)Ljava/lang/String; #调用fun,返回String类型

    move-result-object v0 #把上一步的返回值赋给vo寄存器

    const-string v1, "tian"   #定义一个字符串并保存在V1寄存器中

    invoke-static {v1, v0}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_0
.end method

.method secret()V
    .locals 2

    .line 37
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    iget-object v1, p0, Lcom/xjb/demo02/MainActivity;->total:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "secret"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, Lcom/xjb/demo02/MainActivity;->total:Ljava/lang/String;

    .line 38
    const-string v0, "tian secret"

    const-string v1, "this is a secret"

    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 39
    return-void
.end method

.method testIf(I)V
    .locals 3
    .param p1, "b"    # I

    .line 46
    const/4 v0, 0x1

    .line 47
    .local v0, "a":I
    const-string v1, "tian"

    if-ge p1, v0, :cond_0   #如果p1寄存器中的值大于V0寄存器中的值,则跳转到:cond_0的位置

    .line 48
    const-string v2, "a is greater than b"

    invoke-static {v1, v2}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    goto :goto_0

    .line 50
    :cond_0
    const-string v2, "a is less than or equal b"

    invoke-static {v1, v2}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 52
    :goto_0
    return-void
.end method