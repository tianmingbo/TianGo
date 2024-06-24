package encrypt;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

/**
 * DESede也称3DES，密钥长度为24字节
 * 1、des加密 前8个字节加密
 * 2、des解密 中间8个字节解密
 * 3、des加密 最后8个字节再加密
 */

public class DESede {
    public static void main(String[] args) {
        try {
            SecretKeySpec deskey = new SecretKeySpec("123456781234567812345678".getBytes(), "DESede");
//            Cipher des = Cipher.getInstance("DES/ECB/PKCS5Padding");
            IvParameterSpec ivParameterSpec = new IvParameterSpec("12345678".getBytes());  //IV向量的长度对应算法的分组长度，8个
            Cipher des = Cipher.getInstance("DESede/CBC/PKCS5Padding"); //CBC先异或，再加密。PKCS5Padding是填充方式
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
