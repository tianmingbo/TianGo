package Object.useInterface.factoryMode;

import Object.useInterface.Output;

public class BatterPrinter implements Output {
    private final String[] printData = new String[MAX_CACHE_LINE * 2];
    private int dataNum = 0;

    public void out() {
        while (dataNum > 0) {
            System.out.println("打印:" + printData[0]);
            //把数组整体向前移一位
            System.arraycopy(printData, 1, printData, 0, --dataNum);
        }
    }

    public void getData(String msg) {
        if (dataNum >= MAX_CACHE_LINE * 2) {
            System.out.println("队列已满，添加失败");
        } else {
            //把打印数据添加到队列里，已保存的数量加1
            printData[dataNum++] = msg;
        }
    }
}
