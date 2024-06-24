package encrypt;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

/**
 * DES算法明文按照64位进行分组加密,iv长度也是64位;
 * 要复现DES,需要有明文,key,iv,mode,padding;
 * 如果是ECB模式,则不需要iv,加了会报错;
 * 如果明文中有两个分组的内容相同,ECB会得到完全一样的密文,CBC不会;
 * <p>
 * NOPadding填充方式,加密的明文必须等于分组长度倍数,否则报错;
 * PKCS5Padding会对加密的铭文填充1字节 ~ 1个分组的长度;
 * 没有指定加密模式和填充方式,则默认使用DES/ECB/PKCS5Padding
 */
public class DES {
    public static void main(String[] args) {
        try {
            SecretKeySpec deskey = new SecretKeySpec("12345678".getBytes(), "DES");
//            Cipher des = Cipher.getInstance("DES/ECB/PKCS5Padding");
            IvParameterSpec ivParameterSpec = new IvParameterSpec("12345678".getBytes());  //IV向量的长度对应算法的分组长度，8个
            Cipher des = Cipher.getInstance("DES/CBC/PKCS5Padding"); //CBC先异或，再加密。PKCS5Padding是填充方式
//            des.init(Cipher.ENCRYPT_MODE, deskey);
            des.init(Cipher.ENCRYPT_MODE, deskey, ivParameterSpec); //CBC模式添加iv向量
            byte[] res = des.doFinal("tian666666".getBytes()); //加密结果
            System.out.println(Base64.getEncoder().encodeToString(res));

//            des.init(Cipher.DECRYPT_MODE, deskey); //解密
            des.init(Cipher.DECRYPT_MODE, deskey, ivParameterSpec); //解密
            byte[] res2 = des.doFinal(res);
            System.out.println(new String(res2));
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
