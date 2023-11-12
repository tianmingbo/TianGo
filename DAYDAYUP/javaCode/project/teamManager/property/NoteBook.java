package com.atguigu06.project.teamManager.property;

public class NoteBook extends Equipment {
    private String model;//机器的型号
    private double price;//价格


    public NoteBook(String model, double price) {
        this.model = model;
        this.price = price;
    }


    public String getModel() {
        return model;
    }


    public void setModel(String model) {
        this.model = model;
    }


    public double getPrice() {
        return price;
    }


    public void setPrice(double price) {
        this.price = price;
    }


    @Override
    String desc() {
        return model + "(" + price + ")";
    }
}
