package javaSet.queue;

import java.util.ArrayDeque;
import java.util.LinkedList;
import java.util.PriorityQueue;

//queue的实现
public class QueueDemo {
    //优先队列
    static void priorityQueue() {
        var pq = new PriorityQueue();
        pq.offer(6);
        pq.offer(-6);
        pq.offer(69);
        pq.offer(65);
        pq.offer(16);
        System.out.println(pq);
        System.out.println(pq.poll());
    }

    //栈的实现
    static void arrayQueueStack() {
        var stack = new ArrayDeque();
        stack.push("java");
        stack.push("py");
        stack.push("c");
        System.out.println(stack);
        var a = stack.pollFirst();
        System.out.println(a);
        System.out.println(stack);
    }

    //队列
    static void queue() {
        var queue = new ArrayDeque();
        queue.offer("java");
        queue.offer("c");
        queue.offer("py");
        System.out.println(queue.pop());
    }

    static void linkedList() {
        //这个是使用链表来实现的，插入删除时性能更好
        //LinkedList实现了Deque接口
        var books = new LinkedList();
        books.add("java");
        books.add("c");
        books.add("py");
        System.out.println(books.pollLast());
    }

    public static void main(String[] args) {
//        QueueDemo.priorityQueue();
//        QueueDemo.arrayQueueStack();
//        QueueDemo.queue();
        QueueDemo.linkedList();
    }
}
