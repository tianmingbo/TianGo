#ifndef PROTO_H__
#define PROTO_H__

#define KEYPATH "/etc/services"
#define KEYPROJ 'g'
#define NAMESIZE 1024

struct msg_st {
    long mtype;

    struct {
        int id;
        float value;
        char name[NAMESIZE];
        int flag;
    } mtext;
};


#endif
