package com.atguigu06.project.teamManager.property;

import com.atguigu06.project.teamManager.service.Status;

/**
 * @author tianmingbo
 */
public class Programmer extends Employee {
    private int memId;
    private Status status = Status.FREE;
    private Equipment equipment;

    public Programmer() {
    }

    public Programmer(int id, String name, int age,
                      double salary, Equipment equipment) {
        super(id, name, age, salary);
        this.equipment = equipment;
    }

    public int getMemId() {
        return memId;
    }

    public void setMemId(int memId) {
        this.memId = memId;
    }

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public Equipment getEquipment() {
        return equipment;
    }

    public void setEquipment(Equipment equipment) {
        this.equipment = equipment;
    }

    protected String getMemberDetails() {
        return getMemId() + "/" + getDetails();
    }

    public String getDetailsForTeam() {
        return getMemberDetails() + "\t程序员";
    }

    @Override
    public String toString() {
        return getDetails() + "\t程序员\t" + status + "\t\t\t\t\t" + equipment.desc();
    }

}
