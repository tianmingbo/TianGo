package encrypt;


import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class MACEncrypt {

    public static void main(String[] args) {
        try {
            SecretKeySpec secretKeySpec = new SecretKeySpec("a12324567".getBytes(), "HmacSHA1");
            Mac mac = Mac.getInstance(secretKeySpec.getAlgorithm());
            mac.init(secretKeySpec);
            mac.update("tian".getBytes());
            byte[] res = mac.doFinal();
            System.out.println(new String(res));
            System.out.println(Base64.getEncoder().encodeToString(res));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}