package internet;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class URLDecodeTest_2 {
    public static void main(String[] args) {
        //解码
        String keyword = URLDecoder.decode("%E7%96%AF", StandardCharsets.UTF_8);
        System.out.println(keyword);
        try {
            //编码
            System.out.println(URLEncoder.encode("大力","GBK"));
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }
}
