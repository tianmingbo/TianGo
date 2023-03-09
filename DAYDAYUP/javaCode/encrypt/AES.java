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
public class AES {
    public static void main(String[] args) {
        try {
            SecretKeySpec aeskey = new SecretKeySpec("12345678qwertyui".getBytes(), "AES");
            IvParameterSpec ivParameterSpec = new IvParameterSpec("12345678qwertyui".getBytes());
            Cipher aes = Cipher.getInstance("AES/CBC/PKCS5Padding");
            aes.init(Cipher.ENCRYPT_MODE, aeskey, ivParameterSpec);
            byte[] res = aes.doFinal("tian666666".getBytes());
            System.out.println(Base64.getEncoder().encodeToString(res));

            aes.init(Cipher.DECRYPT_MODE, aeskey, ivParameterSpec); //解密
            byte[] res2 = aes.doFinal(res);
            System.out.println(new String(res2));
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
