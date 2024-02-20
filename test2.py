def test(a, b, c):
    d = ""
    e = 0
    f = len(a)
    h = len(b)
    m = len(c)
    k = 187
    l = 187
    e = f if f > h else h
    for g in range(e):
        l = k = 187
        if g >= f:
            l = ord(b[g])
        elif g >= h:
            k = ord(a[g])
        else:
            k = ord(a[g])
            l = ord(b[g])
        d += c[(k ^ l) % m]
    return d


def auth(b):
    c = 'http://falogin.cn/?code=7&asyn=0'
    session = test('4v*XeYkSGH37vPt7', b,
                   '9Pxngv[ubw>,iX3Y$C!7uz|2pf!WOXh0vQaab,U3uO3NbPbbODEs6sCT3x*.><)t8i)0!p*5QEDDvGg94IemjAJk0.t!]9Xutj4L9]C]aBK9[l$hEKE4lBPyzY0BmOD7BvM6K>3Fabec*~61IOu4{V3}0t!Q3^nN0rVm*AEiyH$Ps[~[.vX!5$YrQARYCOw2u0u<edjtx)Q$V3FjHw{]q$[Q8AToAvHuv5tcntqHq8*b*BsqhalC7}eIAsE$v)a')
    c += f'&id+{session}'
    print(session)


if __name__ == '__main__':
    a = test("tianmingbo666", "RDpbLfCPsJZ7fiv",
             "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW")
    print(auth(a))
