package encrypt;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

public class MD5 {
    public static void main(String[] args) {
        MessageDigest md5 = null;
        try {
            md5 = MessageDigest.getInstance("MD5");
            md5.update("bo6".getBytes());
            byte[] res = md5.digest();
            System.out.println(Base64.getEncoder().encodeToString(res)); //MD5编码成Base64

        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
}
