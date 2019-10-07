# 定义二叉树的节点类
class Node(object):
    def __init__(self, item, lchild=None, rchild=None):  # 通过添加参数 lchild=None, rchild=None，使得Node类的泛化能力更好
        self.elem = item
        self.lchild = lchild
        self.rchild = rchild


class Tree(object):
    def __init__(self, root=None):
        self.root = root

    def add(self, item):
        """完全二叉树添加新的节点item"""
        # 将item封装成一个node
        node = Node(item)

        # 判断根节点是否为空
        if self.root is None:
            self.root = node
            return

        # 使用队列来广度遍历树
        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)  # !注意：这里可以直接用pop(0)弹出第一个元素
            if cur_node.lchild is None:
                cur_node.lchild = node
                return
            elif cur_node.rchild is None:
                cur_node.rchild = node
                return
            else:
                queue.append(cur_node.lchild)
                queue.append(cur_node.rchild)

    #                 queue.pop(0)

    def breath_travel(self):
        """二叉树的广度优先遍历,队列实现"""
        if self.root is None:
            return
        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)
            print(cur_node.elem)
            if cur_node.lchild is None:
                return
            elif cur_node.rchild is None:
                return
            else:
                queue.append(cur_node.lchild)
                queue.append(cur_node.rchild)

    def preorder(self):
        pass

    def inorder(self):
        pass

    def postorder(self):
        pass


if __name__ == '__main__':
    # 先建节点，再将节点添加到tree
    #     node = Node('A')
    #     tree = Tree(node)

    # 先实例化一个控树，再添加节点
    tree = Tree()
    tree.add('A')
    tree.add('B')
    tree.add('C')
    tree.add('D')
    tree.add('E')
    tree.add('F')
    tree.add('G')
    tree.add('H')


    # 定义二叉树的节点类
    class Node(object):
        def __init__(self, item, lchild=None, rchild=None):  # 通过添加参数 lchild=None, rchild=None，使得Node类的泛化能力更好
            self.elem = item
            self.lchild = lchild
            self.rchild = rchild


    class Tree(object):
        def __init__(self, root=None):
            self.root = root

        def add(self, item):
            """完全二叉树添加新的节点item"""
            # 将item封装成一个node
            node = Node(item)

            # 判断根节点是否为空
            if self.root is None:
                self.root = node
                return

            # 使用队列来广度遍历树
            queue = [self.root]
            while queue:
                cur_node = queue.pop(0)  # !注意：这里可以直接用pop(0)弹出第一个元素
                if cur_node.lchild is None:
                    cur_node.lchild = node
                    return
                elif cur_node.rchild is None:
                    cur_node.rchild = node
                    return
                else:
                    queue.append(cur_node.lchild)
                    queue.append(cur_node.rchild)

        #                 queue.pop(0)

        def breath_travel(self):
            """二叉树的广度优先遍历,队列实现"""
            if self.root is None:
                return
            queue = [self.root]
            while queue:
                cur_node = queue.pop(0)
                print(cur_node.elem)
                if cur_node.lchild is None:
                    break
                elif cur_node.rchild is None:
                    break
                else:
                    queue.append(cur_node.lchild)
                    queue.append(cur_node.rchild)
            [print(cur_node.elem) for cur_node in queue]

        def preorder(self):
            pass

        def inorder(self):
            pass

        def postorder(self):
            pass


    if __name__ == '__main__':
        # 先建节点，再将节点添加到tree
        #     node = Node('A')
        #     tree = Tree(node)

        # 先实例化一个控树，再添加节点
        tree = Tree()
        tree.add('A')
        tree.add('B')
        tree.add('C')
        tree.add('D')
        tree.add('E')
        tree.add('F')
        tree.add('G')
        tree.add('H')
        tree.breath_travel()