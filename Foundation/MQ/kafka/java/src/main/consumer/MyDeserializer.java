package src.main.consumer;

import org.apache.kafka.common.serialization.Deserializer;
import org.codehaus.jackson.map.ObjectMapper;

import java.util.Map;

class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
}

/**
 * @author tianmingbo
 * 自定义解序列化
 */
public class MyDeserializer implements Deserializer {
    private ObjectMapper objectMapper;

    @Override
    public void configure(Map configs, boolean isKey) {
        objectMapper = new ObjectMapper();
    }


    @Override
    public Object deserialize(String topic, byte[] data) {
        Person person = null;
        try {
            person = objectMapper.readValue(data, Person.class);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return person;
    }
}
