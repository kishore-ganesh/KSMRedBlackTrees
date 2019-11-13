class Node:
    def __init__(self, data, left, right, parent, color=0):
        self.data = data
        self.right = right
        self.left = left
        self.color = color  # 1: Red, 0: Black
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_grandparent(self):
        if self.parent:
            return self.parent.get_parent()
        else:
            return None

    def get_sibling(self):
        if self.parent:
            if self == self.parent.right:
                return self.parent.left
            return self.parent.right
        return None

    def rotate_right(self):  # Right rotate rooted at
        node_left = self.left
        node_left.parent = self.parent
        self.left = node_left.right
        if self.parent is not None:
            if self.parent.right == self:
                self.parent.right = node_left
            else:
                self.parent.left = node_left
        self.parent = node_left

    def rotate_left(self):
        node_right = self.right
        node_right.parent = self.parent
        self.right = node_right.left
        if self.parent is not None:
            if self.parent.left == self:
                self.parent.left = node_right
            else:
                self.parent.right = node_right
        self.parent = node_right

    def get_uncle(self):
        if self.parent is not None:
            return self.parent.get_sibling()
        return None


class RedBlackTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def is_leaf(root):
        if root.right is None and root.left is None:
            return True
        return False

    @staticmethod
    def create_leaf():
        return Node(None, None, None, None, color=0)

    def add_node_recursively(self, data, root):
        if data > root.data:
            if self.is_leaf(root.right):
                left_leaf = self.create_leaf()
                right_leaf = self.create_leaf()
                root.right = Node(data, left_leaf, right_leaf, root)
                left_leaf.parent = root.right
                right_leaf.parent = root.right
                return root.right
            else:
                return self.add_node_recursively(data, root.right)
        else:
            if self.is_leaf(root.left):
                left_leaf = self.create_leaf()
                right_leaf = self.create_leaf()
                root.left = Node(data, left_leaf, right_leaf, root)
                left_leaf.parent = root.left
                right_leaf.parent = root.left
                return root.left
            else:
                return self.add_node_recursively(data, root.left)

    def add_node(self, data):
        if self.root is None:
            left_leaf = self.create_leaf()
            right_leaf = self.create_leaf()
            self.root = Node(data, left_leaf, right_leaf, None)
            left_leaf.parent = self.root
            right_leaf.parent = self.root
            self.root.color = 0
            return
        current = self.add_node_recursively(data, self.root)
        self.correct_insertion(current)

    @staticmethod
    def correct_insertion(node):
        print(node.data)
        parent = node.get_parent()
        uncle = node.get_uncle()
        if uncle is not None:
            print(uncle.color)
        if parent.color == 0:
            return
        elif parent.color == 1 and uncle.color == 1:
            # Case 3 insertion
            grandparent = parent.get_parent()
            parent.color = 0
            uncle.color = 0
            grandparent.color = 1
        elif parent.color == 1 and uncle.color == 0:
            grandparent = parent.get_parent()
            if node == parent.right and parent == grandparent.left:
                parent.rotate_left()
            elif node == parent.left and parent == grandparent.right:
                parent.rotate_right()
            if node == parent.right:
                node.rotate_left()
            else:
                node.rotate_right()
            parent.color = 0
            grandparent.color = 1

    def search_recursive(self, root, data):
        if root is None:
            return None
        if self.is_leaf(root):
            return None
        if data > root.data:
            return self.search_recursive(root.right, data)
        elif data == root.data:
            return root
        else:
            return self.search_recursive(root.left, data)

    def search(self, data):
        return self.search_recursive(self.root, data)


if __name__ == "__main__":
    tree = RedBlackTree()
    tree.add_node(10)
    tree.add_node(20)
    tree.add_node(30)
    # print(tree)
