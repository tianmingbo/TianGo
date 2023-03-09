package generic.typeWildcard;


import java.util.ArrayList;
import java.util.List;

class Canvas {
    //? extends Shape 表示List后尖括号里的类型是Shape的子类型即可。
    //Shape称为这个通配符的上限
    public void drawAll(List<? extends Shape> shapes) {
//    public void drawAll(List<Shape> shapes) {  List<Circle> 并不是List<Shape>的子类型
        System.out.println(shapes.size());
        /*
        在shapes中不能add，因为没法确定集合元素是哪个类型
         * */
        for (var s : shapes) {
            s.draw(this);
        }
    }
}

//设定类型通配符的上限
abstract class Shape {
    public abstract void draw(Canvas c);
}

class Circle extends Shape {
    @Override
    public void draw(Canvas c) {
        System.out.println("circle");
    }
}

class Rectangle extends Shape {
    @Override
    public void draw(Canvas c) {
        System.out.println("rectangle");
    }
}


public class Shape_1 {
    public static void main(String[] args) {
        List<Circle> circleList = new ArrayList<>();
        circleList.add(new Circle());
        var c = new Canvas();
        c.drawAll(circleList);
    }

}
