package Object.useInterface;

interface Product {
    int getProduceTime();
}

/**
 * Printer实现了Output和Product接口，
 * 所以Printer对象既可以赋给Output变量,也可以赋给Product变量
 * */
public class Printer implements Output, Product {
    private String[] printData = new String[MAX_CACHE_LINE];
    private int dataNum = 0;

    public void out() {
        while (dataNum > 0) {
            System.out.println("打印:" + printData[0]);
            //把数组整体向前移一位
            System.arraycopy(printData, 1, printData, 0, --dataNum);
        }
    }

    public void getData(String msg) {
        if (dataNum >= MAX_CACHE_LINE) {
            System.out.println("队列已满，添加失败");
        } else {
            //把打印数据添加到队列里，已保存的数量加1
            printData[dataNum++] = msg;
        }
    }

    public int getProduceTime() {
        return 45;
    }

    public static void main(String[] args) {
        Output o = new Printer();
        o.getData("java");
        o.getData("Python");
        o.out();
        o.print("tian", "chen", "dali");
        o.test();
        Product p = new Printer();
        System.out.println(p.getProduceTime());
        //所有接口类型的引用变量都可以直接赋给Object类型的变量
        Object tmp = p;
    }
}
