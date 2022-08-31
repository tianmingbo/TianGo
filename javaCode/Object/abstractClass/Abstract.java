package Object.abstractClass;

abstract class Shape {
    {
        System.out.println("init");
    }

    private String color;

    //抽象方法，没有方法体
    public abstract double calPerimeter();

    public abstract String getType();

    //用来被子类调用
    public Shape() {
    }

    public Shape(String color) {
        System.out.println("generate");
        this.color = color;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }
}

class Triangle extends Shape {
    private double a;
    private double b;
    private double c;

    public Triangle(String color, double a, double b, double c) {
        super(color);
        this.setSides(a, b, c);
    }

    public void setSides(double a, double b, double c) {
        this.a = a;
        this.b = b;
        this.c = c;
    }

    //重写抽象方法
    public double calPerimeter() {
        return a + b + c;
    }

    public String getType() {
        return "三角形";
    }
}

class Circle extends Shape {
    private double radius;

    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }

    public void setRadius(double radius) {
        this.radius = radius;
    }

    //重写抽象方法
    public double calPerimeter() {
        return 2 * Math.PI * radius;
    }

    public String getType() {
        return getColor() + "圆形";
    }
}

public class Abstract {
    public static void main(String[] args) {
        Shape s1 = new Triangle("black", 3, 4, 5);
        Shape s2 = new Circle("yellow", 3);
        System.out.println(s1.getType());
        System.out.println(s1.calPerimeter());
    }
}
