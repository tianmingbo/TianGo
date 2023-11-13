package com.atguigu06.project.teamManager.menu;

import com.atguigu06.project.teamManager.property.Employee;
import com.atguigu06.project.teamManager.property.Programmer;
import com.atguigu06.project.teamManager.service.TeamException;
import com.atguigu06.project.teamManager.service.TeamManager;
import com.atguigu06.project.teamManager.util.ConfigLoad;
import com.atguigu06.project.teamManager.util.Util;

public class Menu {
    private ConfigLoad config = new ConfigLoad();
    private TeamManager tm = new TeamManager();

    public void enterMainMenu() {
        boolean stopFlag = false;
        char key = 0;
        do {
            if (key != '1') {
                getAllEmployees();
            }
            System.out.print("1-团队列表  2-添加团队成员  3-删除团队成员 4-退出   请选择(1-4)：");
            key = Util.readMenuSelection();
            System.out.println();
            switch (key) {
                case '1':
                    listTeam();
                    break;
                case '2':
                    addMember();
                    break;
                case '3':
                    deleteMember();
                    break;
                case '4':
                    System.out.print("确认是否退出(Y/N)：");
                    char yn = Util.readConfirmSelection();
                    if (yn == 'Y') {
                        stopFlag = true;
                    }
                    break;
            }
        } while (!stopFlag);
    }

    private void listTeam() {
        System.out.println("\n--------------------团队成员列表---------------------");
        Programmer[] team = tm.getTeam();
        if (team.length == 0) {
            System.out.println("开发团队目前没有成员！");
        } else {
            System.out.println("TID/ID\t姓名\t\t年龄\t工资\t\t职位\t\t奖金\t\t股票");
        }
        for (int i = 0; i < team.length; i++) {
            System.out.println(" " + team[i].getDetailsForTeam());
        }
        System.out.println("-----------------------------------------------------");
    }

    public void getAllEmployees() {
        System.out.println("\n-------------------------------开发团队调度系统--------------------------------");
        Employee[] employees = config.getEmployees();
        if (employees.length == 0) {
            System.out.println("没有员工记录！");
        } else {
            System.out.println("ID\t姓名\t\t年龄\t工资\t\t职位\t\t状态\t\t奖金\t\t股票\t\t领用设备");
        }
        for (int i = 0; i < employees.length; i++) {
            System.out.println(employees[i]);
        }
        System.out.println("-------------------------------------------------------------------------------");
    }

    private void addMember() {
        System.out.println("---------------------添加成员---------------------");
        System.out.print("请输入要添加的员工ID：");
        int id = Util.readInt();
        try {
            Employee e = config.getEmployee(id);
            tm.addMember(e);
            System.out.println("添加成功");
        } catch (TeamException e) {
            System.out.println("添加失败，原因：" + e.getMessage());
        }
        Util.readReturn();
    }

    private void deleteMember() {
        System.out.println("---------------------删除成员---------------------");
        System.out.print("请输入要删除员工的TID：");
        int id = Util.readInt();
        System.out.print("确认是否删除(Y/N)：");
        char yn = Util.readConfirmSelection();
        if (yn == 'N') {
            return;
        }
        try {
            tm.removeMember(id);
            System.out.println("删除成功");
        } catch (TeamException e) {
            System.out.println("删除失败，原因：" + e.getMessage());
        }
        Util.readReturn();
    }

    public static void main(String[] args) {
        Menu menu = new Menu();
        menu.enterMainMenu();

    }
}
