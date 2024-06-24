package util;


import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.util.Properties;


/**
 * @author
 */
public class ConfigProperties {

    private String propertyFileName = "";
    private Properties properties = new Properties();


    public ConfigProperties() {

    }

    public ConfigProperties(String fileName) {
        this.propertyFileName = fileName;
    }


    protected void loadFromFile() {
        InputStream in = null;
        InputStreamReader ireader = null;

        try {

            ClassLoader loader = ConfigProperties.class.getClassLoader();
            in = loader.getResourceAsStream(propertyFileName);

            if (null != in) {
                ireader = new InputStreamReader(in, "utf-8");
            } else {
                String filePath = IOUtil.getResourcePath(propertyFileName);
                in = new FileInputStream(filePath);
                //解决读非UTF-8编码的配置文件时，出现的中文乱码问题
                ireader = new InputStreamReader(in, "utf-8");
            }
            properties.load(ireader);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            IOUtil.closeQuietly(ireader);
        }
    }


    /**
     * 按key获取值
     *
     * @param key
     * @return
     */
    public String readProperty(String key) {
        String value = "";

        value = properties.getProperty(key);

        return value;
    }


    public String getValue(String key) {

        return readProperty(key);

    }

    public int getIntValue(String key) {

        return Integer.parseInt((readProperty(key)));

    }

    public static ConfigProperties loadFromFile(Class aClass)
            throws IllegalAccessException {

        ConfigProperties propertiesUtil = null;


        return propertiesUtil;
    }

    public static void loadAnnotations(Class aClass) {

        ConfigProperties configProperties = null;
        try {
            configProperties = loadFromFile(aClass);


            if (null == configProperties) return;

            Field[] fields = aClass.getDeclaredFields();

        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
    }


}