package Object.innerClass.EnumDemo;

public class EnumTest {
    public void judge(SeasonEnum s) {
        switch (s) {
            case FALL:
                System.out.println("qiu");
                break;
            case WINTER:
                System.out.println("dong");
                break;
            case SUMMER:
                System.out.println("xia");
                break;
            case SPRING:
                System.out.println("chun");
                break;
        }
    }

    public static void main(String[] args) {
        //默认有values()方法,返回所有实例
        for (var s : SeasonEnum.values()) {
            System.out.println(s);
        }
        //SeasonEnum.SPRING访问实例
        new EnumTest().judge(SeasonEnum.SPRING);
    }
}
