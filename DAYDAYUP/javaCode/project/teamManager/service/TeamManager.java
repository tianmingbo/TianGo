package com.atguigu06.project.teamManager.service;

import com.atguigu06.project.teamManager.property.Architect;
import com.atguigu06.project.teamManager.property.Designer;
import com.atguigu06.project.teamManager.property.Employee;
import com.atguigu06.project.teamManager.property.Programmer;
import com.atguigu06.project.teamManager.util.Util;

public class TeamManager {
    private static int uid = 1;
    private final int MAX_MEMBER = 5;
    private Programmer[] team = new Programmer[MAX_MEMBER];
    private int total = 0;

    public Programmer[] getTeam() {
        Programmer[] team = new Programmer[total];
        for (int i = 0; i < total; i++) {
            team[i] = this.team[i];
        }
        return team;
    }

    private boolean isExist(Programmer p) {
        for (int i = 0; i < total; i++) {
            if (team[i].getId() == p.getId()) {
                return true;
            }
        }
        return false;
    }

    public void addMember(Employee e) throws TeamException {
        if (total > MAX_MEMBER) {
            throw new TeamException("成员已满,无法添加");
        }
        if (!(e instanceof Programmer)) {
            throw new TeamException("该成员不是开发人员，无法添加");
        }
        Programmer p = (Programmer) e;
        switch (p.getStatus()) {
            case BUSY:
                throw new TeamException("该员工已是某团队成员");
            case VOCATION:
                throw new TeamException("该员正在休假，无法添加");
        }
        if (isExist(p)) {
            throw new TeamException("该员工已在本团队中");
        }
        int numArch = 0, numDesi = 0, numPrg = 0;
        for (int i = 0; i < total; i++) {
            if (team[i] instanceof Architect) {
                numArch++;
            } else if (team[i] instanceof Designer) {
                numDesi++;
            } else if (team[i] != null) {
                numPrg++;
            }
        }
        if (p instanceof Architect && numArch >= 1) {
            throw new TeamException("团队中至多只能有一名架构师");
        }
        if (p instanceof Designer && numDesi >= 2) {
            throw new TeamException("团队中至多只能有两名设计师");
        }
        if (p instanceof Programmer && numPrg >= 3) {
            throw new TeamException("团队中至多只能有三名程序员");
        }
        p.setStatus(Status.BUSY);
        p.setMemId(uid++);
        team[total++] = p;
    }

    public void removeMember(int id) throws TeamException {
        int n = 0;
        for (; n < total; n++) {
            if (team[n].getId() == id) {
                team[n].setStatus(Status.FREE);
                break;
            }
        }
        if (n == total) {
            throw new TeamException("找不到该成员，无法删除");
        }
        for (int i = n + 1; i < total; i++) {
            team[i - 1] = team[i];
        }
        team[--total] = null;
    }
}