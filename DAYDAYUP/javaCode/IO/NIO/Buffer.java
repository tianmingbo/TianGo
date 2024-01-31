package IO.NIO;

import java.nio.ByteBuffer;

/**
 * Buffer本质上是一个内存块,既可以写入数据,也可以从中读取数据
 * allocate:创建缓冲区
 * rewind:倒带，就像播放磁带一样倒回去，再重新播放
 * flip:翻转，就像翻转硬币一样，将读取指针移到写入指针的位置
 * clear:清空，将读取指针和写入指针都移到初始位置
 * mark:将当前position的值保存起来放在mark属性中
 * reset: 将mark的值恢复到position中
 *
 * @author tianmingbo
 */
public class Buffer {
    public static void main(String[] args) {
        // 创建一个缓冲区
        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
        System.out.println("初始时-->limit--->" + byteBuffer.limit());
        System.out.println("初始时-->position--->" + byteBuffer.position());
        System.out.println("初始时-->capacity--->" + byteBuffer.capacity());
        System.out.println("初始时-->mark--->" + byteBuffer.mark());

        System.out.println("--------------------------------------");

        // 添加一些数据到缓冲区中
        String s = "大力";
        byteBuffer.put(s.getBytes());

        // 看一下初始时4个核心变量的值
        System.out.println("put完之后-->limit--->" + byteBuffer.limit());
        System.out.println("put完之后-->position--->" + byteBuffer.position());
        System.out.println("put完之后-->capacity--->" + byteBuffer.capacity());
        System.out.println("put完之后-->mark--->" + byteBuffer.mark());
        byteBuffer.flip(); //翻转,写模式变读模式
        // 创建一个limit()大小的字节数组(因为就只有limit这么多个数据可读)
        byte[] bytes = new byte[byteBuffer.limit()];
        // 将读取的数据装进我们的字节数组中
        byteBuffer.get(bytes);
        // 输出数据
        System.out.println(new String(bytes, 0, bytes.length));
        System.out.println(byteBuffer);
        byteBuffer.clear(); //清空缓冲区,并转换为写模式
        System.out.println(byteBuffer);
    }
}
