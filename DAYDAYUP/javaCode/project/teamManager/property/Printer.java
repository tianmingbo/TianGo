package com.atguigu06.project.teamManager.property;

public class Printer extends Equipment {
    private String name;
    private String type;

    public Printer(String name, String type) {
        this.name = name;
        this.type = type;
    }

    @Override
    String desc() {
        return name + "(" + type + ")";
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
