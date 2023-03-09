package BaseMoudle.SystemClass;

import java.io.FileOutputStream;
import java.util.Map;
import java.util.Properties;

public class SystemTest {
    public static void main(String[] args) throws Exception {
        //获取系统的环境变量
        Map<String, String> env = System.getenv();
        for (var name : env.keySet()) {
            System.out.println(env.get(name));
        }
        System.out.println(System.getenv("JAVA_HOME"));
        //获取所有的系统属性
        Properties prop = System.getProperties();
        prop.store(new FileOutputStream("prop.txt"), "System Properties");
        System.out.println(System.getProperty("os.name"));
    }
}
