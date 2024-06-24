package Object.useInterface.factoryMode;

import Object.useInterface.Output;

public class OutputFactory {
    //返回一个Output实例,在工厂类中创建实例，
    public Output getOutput() {
        return new BatterPrinter();
    }

    public static void main(String[] args) {
        var of = new OutputFactory();
        var c = new Computer(of.getOutput());
        c.keyIn("tian");
        c.print();
    }
}
