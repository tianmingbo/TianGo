#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node *createNode(int data) {
    Node *newNode = (Node *) malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void insertNode(Node *head, int data) {
    Node *newNode = createNode(data);
    Node *current = head;

    while (current->next != NULL) {
        current = current->next;
    }
    current->next = newNode;
}

void deleteNode(Node *head, int data) {
    Node *current = head;
    Node *prev = NULL;

    while (current != NULL && current->data != data) {
        prev = current;
        current = current->next;
    }

    if (current != NULL) {
        if (prev != NULL) {
            prev->next = current->next;
        }
        free(current);
    }
}

void displayList(Node *head) {
    Node *current = head->next;

    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

void sortList(Node *head) {
    Node *current = head->next;
    Node *index = NULL;
    int temp;

    if (head->next == NULL) {
        return;
    }

    while (current != NULL) {
        index = current->next;

        while (index != NULL) {
            if (current->data > index->data) {
                temp = current->data;
                current->data = index->data;
                index->data = temp;
            }
            index = index->next;
        }
        current = current->next;
    }
}

int main() {
    Node *head = createNode(0);

    insertNode(head, 2);
    insertNode(head, 3);
    insertNode(head, 1);
    sortList(head);
    displayList(head);

    deleteNode(head, 2);
    displayList(head);

    return 0;
}
