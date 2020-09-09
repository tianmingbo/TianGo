# 二叉树的遍历都可以借助栈结构使用DFS算法完成。
# 首先是最简单的先序遍历，父>左>右。见144题 。
# 每次入栈前先将父节点加入结果列表，然后左节点入栈。
# 当左子树遍历完后，再遍历右子树。

class Solution:
    def preorderTraversal(self, root):
        res = []  #结果列表
        stack = []  #辅助栈
        cur = root  #当前节点
        while stack or cur:
            while cur:  #一直遍历到最后一层
                res.append(cur.val)
                stack.append(cur)
                cur = cur.left
            top = stack.pop()  #此时该节点的左子树已经全部遍历完
            cur = top.right  #对右子树遍历
        return res

# 接着来看后序遍历，左>右>父。见145题 。
# 能不能借助先序遍历的思路来呢，我们将上面的顺序翻转过来得到，父>右>左。
# 所以现在可以按照之前的方法遍历，最后把结果翻转一下。

class Solution:
    def postorderTraversal(self, root):
        res = []
        stack = []
        cur = root
        while stack or cur:
            while cur:
                res.append(cur.val)
                stack.append(cur)
                cur = cur.right  #先将右节点压栈
            top = stack.pop()  #此时该节点的右子树已经全部遍历完
            cur = top.left  #对左子树遍历
        return res[::-1]  #结果翻转

# 最后来看下中序遍历， 左>父>右。见94题 。
# 与先序遍历不同的是，出栈时才将结果写入列表。

class Solution:
    def inorderTraversal(self, root):
        res = []
        stack = []
        cur = root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            top = stack.pop() #此时左子树遍历完成
            res.append(top.val)  #将父节点加入列表
            cur = top.right #遍历右子树
        return res

