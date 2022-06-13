package Object.useInterface.factoryMode;

import Object.useInterface.Output;

public class Computer {
    private Output out;

    public Computer(Output out) {
        this.out = out;
    }
    public void keyIn(String msg){
        out.getData(msg);
    }
    public void print(){
        out.out();
    }
}
