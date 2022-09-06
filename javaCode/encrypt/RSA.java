package encrypt;

import javax.crypto.Cipher;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Arrays;
import java.util.Base64;
import java.security.spec.X509EncodedKeySpec;

public class RSA {
    public static void main(String[] args) {
        try {
            String pubKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvaBFb3z1B8zMt3mEHZUi" +
                    "oNM0pPIBmGMijXTxmRAqvo/0mJruocnXivBWH6JYksqjGg3zO9ZxxwOcx1TsVs0X" +
                    "R2/ZkH6junvDMaNayWmtAMOWTalyGf+eaqd5MpnWY8dglvfWCJKEDOnlOl/9jdoP" +
                    "faRM3DTsBBvus3ynvOIAIWOlMaHIOguyKepNSkh3MAsc3qXtNGP8MZ5m9pg/ot5p" +
                    "ApohaE06yA9/ysYAxoz9chPmeCArcpG+nbM7oVXdTAIiPXVyalZmuu0XcUwVnonQ" +
                    "APv/t+wuKofQcl24zDUZ9rpMWnERUE4YzodDhTOGp8TSsy4eRav0GYUaa4vSSG28" +
                    "ZQIDAQAB";
            byte[] keyBytes = Base64.getDecoder().decode(pubKey);
            X509EncodedKeySpec keySpec = new X509EncodedKeySpec(keyBytes);
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            PublicKey publicKey = keyFactory.generatePublic(keySpec);
            System.out.println(Arrays.toString(publicKey.getEncoded()));

            String privateKey = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC9oEVvfPUHzMy3" +
                    "eYQdlSKg0zSk8gGYYyKNdPGZECq+j/SYmu6hydeK8FYfoliSyqMaDfM71nHHA5zH" +
                    "VOxWzRdHb9mQfqO6e8Mxo1rJaa0Aw5ZNqXIZ/55qp3kymdZjx2CW99YIkoQM6eU6" +
                    "X/2N2g99pEzcNOwEG+6zfKe84gAhY6Uxocg6C7Ip6k1KSHcwCxzepe00Y/wxnmb2" +
                    "mD+i3mkCmiFoTTrID3/KxgDGjP1yE+Z4ICtykb6dszuhVd1MAiI9dXJqVma67Rdx" +
                    "TBWeidAA+/+37C4qh9ByXbjMNRn2ukxacRFQThjOh0OFM4anxNKzLh5Fq/QZhRpr" +
                    "i9JIbbxlAgMBAAECggEAG4ljq+38czaFX/tweQ9IKQyir3VJUATNZrddwjl7y5KC" +
                    "FYsiLjJub4m5J/zeWeq9RrJR6RWaDilzIesuKui7ga83a+lIA3Ong9TSAT+sVNkS" +
                    "QZLis+3P5nMNgZCfdnvkhefVmAcWz/1DQXfhDTFmYHt0geHZiDs6Laxje2ViWXar" +
                    "cpVxXNVWKuzdFqNsnaw2Oq9jUFYW4ysoCZ8aSePvj737IO75y6MwXpl7rH0IuY8+" +
                    "uTGEOHCt/gnKrYHA7jrRb7oolcKG8wH1ge8Kzc73J3cXqBiOqFoHVS/09rzcQcWV" +
                    "JYgYxh3L9tUR0Q5LmNwHsZNbqqHQ7uDssNJYubrqAQKBgQD5T16mBdMdrUzEPjJP" +
                    "GpaLeuPjXoSy89X1FB8wC45R8mqhE0in9gfPPp3tBJyuN6bl4p+QkdQsnLFx4tZL" +
                    "8Jzkng7Wj437forkRV5riY5E4BypN7W9kxNihK2dAurxbl7YkoPBWoGN4WIJssky" +
                    "PW3JKwFczkPkG2VRhJ//apHx5QKBgQDCtudT9cvFyTk6TLYsW7Ghv0eKEk3PHKRX" +
                    "LgCOBISIDHV4PNwLLZGMSwK08ERdJWQy2Mw8CEj6OBo4X2XeBTCwR4grr+Am3tuA" +
                    "ZvUYev2dn51udoXvBT0v1te6H5ZPaXRPMedHWL701q8DX+AamtKLK4FtkWeylHDe" +
                    "4rJu04n4gQKBgQC5tI5rGrGcTId/MlklJUf4U6zGo5Qy/IBmUvu8PQ9hKTKWExgu" +
                    "zIwaqqjWcXYIK7otSPbUqFukc3+VtoMsA+nKPZYN6ta2/BaXXLitX8RSt6GBxtag" +
                    "hJqO6werig3Zkv4hUlnEQBd6yOTPFpbZznolu9wC9j4J/wIki6bmicp2pQKBgQCD" +
                    "ldl0yvnfeuH6vRarmXfMiBiPfVkp6wBAjiz/zJvH2SuViwNlZnEi7xowLuL0U62I" +
                    "EyzKMQsoVbuadxW/WaCSsHScmWmQuzB5cJqX5Z345IIewWg3pEG6T6VP+cK5fdmF" +
                    "H4NdmuLJUT/KtwMa16ALPuZjpkz+yQQSC/9rl/d4gQKBgHGWr4u+V3NgoLPZuydX" +
                    "ctbmULsM+9HUfsMnVr8GM2whaD2iuNpHScKizr6fjwXnV5eAocpq145+mg7JcEkO" +
                    "8D4qX9yoBOWrAGkMYX95gdavYjbpHq02pnDZsK2asIDaJhkuqMUPfREuVWxhdJfl" +
                    "MIiEAdMVxIOHU+iNAFv34VT7";
            byte[] privateKeyBytes = Base64.getDecoder().decode(privateKey);
            PKCS8EncodedKeySpec privateKeySpec = new PKCS8EncodedKeySpec(privateKeyBytes);
            PrivateKey privateKeys = keyFactory.generatePrivate(privateKeySpec);

            byte[] privateBytes = privateKeys.getEncoded();
            System.out.println(Arrays.toString(privateBytes));

            Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
            cipher.init(Cipher.ENCRYPT_MODE, publicKey);
            byte[] bt_encrypted = cipher.doFinal("chendali666".getBytes()); //密文加密
            System.out.println(Base64.getEncoder().encodeToString(bt_encrypted));

            cipher.init(Cipher.DECRYPT_MODE, privateKeys);
            byte[] bt_original = cipher.doFinal(bt_encrypted);//用私钥解密
            System.out.println(new String(bt_original));
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
