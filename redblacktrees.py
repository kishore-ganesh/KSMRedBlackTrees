import queue
import random
import uuid


def gen_checksum(current=None):
    if current is None or random.random() < 0.2:
        return uuid.uuid4().hex
    else:
        return current


class Node:
    def __init__(self, data, left, right, parent, color=1, checksum=gen_checksum(None)):
        self.data = data
        self.right = right
        self.left = left
        self.color = color  # 1: Red, 0: Black
        self.parent = parent
        self.checksum = checksum

    def update_checksum(self):
        self.checksum = gen_checksum(None)

    def random_checksum(self):
        new_checksum = gen_checksum(self.checksum)
        if self.checksum != new_checksum:  # checksum was updated
            return True
        else:
            self.checksum = new_checksum
            return False

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

    def get_red(self):
        if self.left is not None and self.left.color is 1:
            return self.left
        elif self.right is not None and self.right.color is 1:
            return self.right
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
        return Node(None, None, None, None, color=0, checksum=None)

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

    def add_node(self, data, checksum=None):
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
        if checksum is not None:
            current.checksum = checksum
        return current.checksum

    def del_node(self, node, val):
        # node=self.search(val)
        # print(node.data)
        if node is None:
            print("not found")
            return None
        elif node.data is val:
            if node.left.data is None and node.right.data is None:
                self.correct_deletion(node.left, node)
                return None
            elif node.left.data is None and node.right.data is not None:
                self.correct_deletion(node.right, node)
                return node.right
            elif node.left.data is not None and node.right.data is None:
                self.correct_deletion(node.left, node)
                return node.left
            else:
                temp = self.insuc(node.right)
                temp2 = temp.data
                self.del_node(node, temp2)
                node.data = temp2
                return node
        elif node.data > val:
            node.left = self.del_node(node.left, val)
        else:
            node.right = self.del_node(node.right, val)
        return node

    def insuc(self, node):
        if node.left is None:
            return node
        return self.insuc(node.left)

    @staticmethod
    def correct_insertion(node):
        # print("d")
        print(node.data)
        parent = node.get_parent()
        uncle = node.get_uncle()
        if parent.color == 0:
            return None
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

    def correct_deletion(self, u, v):
        if u.color is 1 or v.color is 1:
            u.color = 0
        elif u.color is 0 and v.color is 0:
            if v.parent is not None:
                s = v.get_sibling()
                if s.color is 0 and s.get_red() is None:
                    s.color = 1
                    self.correct_deletion(u, v.parent)
                elif s.color is 0 and s.get_red() is not None:
                    r = s.get_red()
                    if s.parent.right is s and s.right is r:
                        r.color = 0
                        s.parent.rotate_left()
                    elif s.parent.left is s and s.left is r:
                        r.color = 0
                        s.parent.rotate_right()
                    elif s.parent.right is s and s.left is r:
                        r.color = 0
                        s.rotate_right()
                        s.parent.parent.rotate_left()
                    elif s.parent.left is s and s.right is r:
                        r.color = 0
                        s.rotate_left()
                        s.parent.parent.rotate_right()
                elif s.color is 1:
                    s.parent.color = 1
                    s.color = 0
                    if s.parent.left is s:
                        s.parent.rotate_right()
                    else:
                        s.parent.rotate_left()

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

    def search_val(self, data):
        node = self.search_recursive(self.root, data)
        if node is None:
            return False
        else:
            return True

    def level_order_traversal(self):
        q = queue.Queue()
        q.put(self.root)
        while not q.empty():
            top = q.get()
            if top.data is not None:
                print(str(top.data) + " " + str(top.color))
                q.put(top.left)
                q.put(top.right)


def run_scan(_unstable, _stable):
    q = queue.Queue()
    q.put(_unstable.root)
    while not q.empty():
        top = q.get()
        if top.data is not None:
            if top.random_checksum():
                _unstable.del_node(_unstable.root, top.data)
            else:
                _stable.add_node(top.data, checksum=top.checksum)
            q.put(top.left)
            q.put(top.right)


if __name__ == "__main__":
    stable = RedBlackTree()
    unstable = RedBlackTree()
    do_stuff = True
    while do_stuff:
        ch = input("1. Insert page\n2. Update page\n3. Check page\n4. Random update and scan\n5. Print trees\n\n 0. "
                   "Exit\n: ")
        if ch == 0:
            do_stuff = False
            break
        if ch == 1:
            data = int(input("Enter page reference (int): "))
            if stable.search_val(data):
                print('Found page in stable tree!')
            else:
                cs = unstable.add_node(data)
                print('Added page {} with checksum {}.'.format(data, cs))
        elif ch == 2:
            data = int(input("Enter page reference (int): "))
            if stable.search_val(data):
                stable.search(data).update_checksum()
            elif unstable.search_val(data):
                unstable.search(data).update_checksum()
            else:
                print('Data not found! Adding...')
                cs = unstable.add_node(data)
                print('Added page {} with checksum {}.'.format(data, cs))
        elif ch == 3:
            data = int(input("Enter page reference (int): "))
            if stable.search_val(data):
                print('Found stable page {} with checksum {}'.format(data, stable.search(data).checksum))
            elif unstable.search_val(data):
                print('Found unstable page {} with checksum {}'.format(data, unstable.search(data).checksum))
            else:
                print('No such page!')
        elif ch == 4:
            print('Running scan and random update...')
            run_scan(unstable, stable)
            del unstable
            unstable = RedBlackTree()
        elif ch == 5:
            print('Stable:')
            stable.level_order_traversal()
            print('Unstable')
            unstable.level_order_traversal()
    # print(tree)
