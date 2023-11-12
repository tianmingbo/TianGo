package com.atguigu06.project.teamManager.util;


import com.atguigu06.project.teamManager.property.*;

import java.util.Scanner;

import static com.atguigu06.project.model.service.Data.EMPLOYEES;
import static com.atguigu06.project.teamManager.property.Config.*;

/**
 * @author tianmingbo
 */
public class Util {
    private static final Scanner SCANNER = new Scanner(System.in);

    public static char readMenuSelection() {
        char c;
        for (; ; ) {
            String str = readKeyBoard(1, false);
            c = str.charAt(0);
            if (c != '1' && c != '2' &&
                    c != '3' && c != '4') {
                System.out.print("选择错误，请重新输入：");
            } else {
                break;
            }
        }
        return c;
    }

    public static void readReturn() {
        System.out.print("按回车键继续...");
        readKeyBoard(100, true);
    }

    public static int readInt() {
        int n;
        for (; ; ) {
            String str = readKeyBoard(2, false);
            try {
                n = Integer.parseInt(str);
                break;
            } catch (NumberFormatException e) {
                System.out.print("数字输入错误，请重新输入：");
            }
        }
        return n;
    }

    public static char readConfirmSelection() {
        char c;
        for (; ; ) {
            String str = readKeyBoard(1, false).toUpperCase();
            c = str.charAt(0);
            if (c == 'Y' || c == 'N') {
                break;
            } else {
                System.out.print("选择错误，请重新输入：");
            }
        }
        return c;
    }

    private static String readKeyBoard(int limit, boolean blankReturn) {
        String line = "";

        while (SCANNER.hasNextLine()) {
            line = SCANNER.nextLine();
            if (line.length() == 0) {
                if (blankReturn) {
                    return line;
                } else {
                    continue;
                }
            }

            if (line.length() < 1 || line.length() > limit) {
                System.out.print("输入长度（不大于" + limit + "）错误，请重新输入：");
                continue;
            }
            break;
        }

        return line;
    }
}

class ConfigLoad {
    private Employee[] employees;

    private ConfigLoad() {
        employees = new Employee[EMPLOYEES.length];
        for (int i = 0; i < employees.length; i++) {
            int type = Integer.parseInt(EMPLOYEES[i][0]);
            int id = Integer.parseInt(EMPLOYEES[i][1]);
            String name = EMPLOYEES[i][2];
            int age = Integer.parseInt(EMPLOYEES[i][3]);
            double salary = Double.parseDouble(EMPLOYEES[i][4]);

            Equipment eq;
            double bonus;
            int stock;

            switch (type) {
                case EMPLOYEE:
                    employees[i] = new Employee(id, name, age, salary);
                    break;
                case PROGRAMMER:
                    eq = createEquipment(i);
                    employees[i] = new Programmer(id, name, age, salary, eq);
                    break;
                case DESIGNER:
                    eq = createEquipment(i);
                    bonus = Integer.parseInt(EMPLOYEES[i][5]);

            }
        }
    }

    private Equipment createEquipment(int index) {
        int type = Integer.parseInt(EQUIPMENTS[index][0]);
        switch (type) {
            case PC:
                return new PC(EQUIPMENTS[index][1], EQUIPMENTS[index][2]);
            case NOTEBOOK:
                int price = Integer.parseInt(EQUIPMENTS[index][2]);
                return new NoteBook(EQUIPMENTS[index][1], price);
            case PRINTER:
                return new Printer(EQUIPMENTS[index][1], EQUIPMENTS[index][2]);

        }
        return null;
    }
}