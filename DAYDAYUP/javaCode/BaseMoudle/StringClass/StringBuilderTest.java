package BaseMoudle.StringClass;

public class StringBuilderTest {
    public static void main(String[] args) {
        StringBuilder str = new StringBuilder();
        str.append("java");
        str.insert(0, "hello ");
        str.replace(5,6,",");
        str.delete(5,6);
        str.reverse();
        System.out.println(str.capacity());
        System.out.println(str.length());
        System.out.println(str);
    }
}
