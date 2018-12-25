from typing import Generic, List, TypeVar, Callable

_T = TypeVar('_T')


class BaseNode(Generic[_T]):

    def __init__(self, item: _T):
        self.item = item

    def append(self, item: _T):
        pass

    def add(self, item: _T):
        pass

    def __del__(self):
        del self

    def __repr__(self):
        return str(self.item)


class ListNode(BaseNode):

    def __init__(self, item: _T):
        super().__init__(item)
        self.predecessor = None
        self.successor = None

    def append(self, item: _T):
        next_node = ListNode(item)
        self.successor = next_node
        next_node.predecessor = self

    def __del__(self):
        del self.predecessor
        del self.successor
        super().__del__()


class TreeNode(BaseNode):

    def __init__(self, item: _T):

        super().__init__(item)
        self.right = None
        self.left = None

    def __del__(self):

        del self.right
        del self.left
        super().__del__()

    def __repr__(self):
        return '{} -> {}, {}'.format(
            self.item,
            self.left.item if self.left is not None else None,
            self.right.item if self.right is not None else None
        )


class AVLNode(TreeNode):

    def __init__(self, item: _T):

        super().__init__(item)
        self.height = 0

    def __repr__(self):
        return 'h{} i{} -> l{}, r{}'.format(
            self.height,
            self.item,
            self.left.item if self.left is not None else None,
            self.right.item if self.right is not None else None
        )

    @staticmethod
    def get_height(node: 'AVLNode'):
        return -1 if node is None else node.height


class Queue(Generic[_T]):

    def __init__(self, iterable: List[_T]):

        self.first = None
        self.last = self.first

        for i in iterable:
            self.push(i)

    def push(self, item: _T) -> None:

        if self.first is None:
            self.first = ListNode(item)
            self.last = self.first
        else:
            self.last.append(item)
            self.last = self.last.successor

    def pop(self) -> _T:

        if self.first is self.last:

            if self.first is None:
                raise ValueError('No item to pop from collection!')

            item = self.first.item
            del self.last, self.first
            self.last = None
            self.first = None

        else:
            t: ListNode[_T] = self.first
            self.first = self.first.successor
            item = t.item
            del t

        return item

    def __repr__(self) -> str:

        l: List[_T] = []
        n: ListNode[_T] = self.first

        while n is not None:
            l.append(n.item)
            n = n.successor

        return l.__repr__()

    def is_empty(self) -> bool:
        return self.first is None

    def __del__(self):

        while not self.is_empty():
            self.pop()
        del self


class Stack(Generic[_T]):

    def __init__(self, iterable: List[_T]):

        self.first = None

        for i in iterable:
            self.push(i)

    def push(self, item: _T) -> None:

        if self.first is None:
            self.first = ListNode(item)
        else:
            temp = self.first
            self.first = ListNode(item)
            self.first.successor = temp

    def pop(self) -> _T:

        if self.first is None:
            raise ValueError('No item to pop from collection!')

        temp = self.first
        self.first = self.first.successor
        item = temp.item
        del temp
        return item

    def __repr__(self) -> str:

        l: List[_T] = []
        n: ListNode[_T] = self.first

        while n is not None:
            l.append(n.item)
            n = n.successor

        return l.__repr__()

    def is_empty(self) -> bool:
        return self.first is None

    def __del__(self):

        while not self.is_empty():
            self.pop()
        del self


class Heap(Generic[_T]):

    def __init__(self, iterable: List[_T], comparable: Callable[[_T, _T], int]):

        self.comparable = comparable
        self.heap = list(iterable)

        if len(self.heap) != 0:
            self.__make_heap()

    @staticmethod
    def __get_parent(index: int) -> int:
        return index // 2

    @staticmethod
    def __get_left_child(index: int) -> int:
        return 2 * index + 1

    @staticmethod
    def __get_right_child(index: int) -> int:
        return 2 * index + 2

    def __up_heap(self, index: int) -> int:

        if not 0 <= index < len(self.heap):
            raise IndexError('Index out of bounds exception!')

        if index == 0:
            return index

        if 0 < index < len(self.heap):
            p_index: int = Heap.__get_parent(index)

            if self.comparable(self.heap[index], self.heap[p_index]) > 0:
                self.heap[p_index], self.heap[index] = self.heap[index], self.heap[p_index]

            return self.__up_heap(p_index)

    def __down_heap(self, index: int) -> int:

        if not 0 <= index < len(self.heap):
            raise IndexError('Index out of bounds exception!')

        l_child: int = Heap.__get_left_child(index)

        if len(self.heap) <= l_child:
            return index

        r_child: int = l_child + 1 if l_child + 1 < len(self.heap) else l_child

        if self.comparable(self.heap[r_child], self.heap[l_child]) > 0:
            l_child = r_child

        if self.comparable(self.heap[l_child], self.heap[index]) > 0:

            self.heap[l_child], self.heap[index] = self.heap[index], self.heap[l_child]
            return self.__down_heap(l_child)

        else:
            return index

    def __make_heap(self) -> None:
        index: int = len(self.heap) // 2

        while index >= 0:
            self.__down_heap(index)
            index -= 1

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def add(self, item: _T) -> None:
        self.heap.append(item)
        self.__up_heap(len(self.heap)-1)

    def top(self) -> _T:
        return self.heap[0] if len(self.heap) > 0 else None

    def get(self) -> _T:

        if len(self.heap) == 0:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        item: _T = self.heap.pop()

        if len(self.heap) > 0:
            self.__down_heap(0)

        return item


class Tree(Generic[_T]):

    def __init__(self, iterable: List[_T], comparable: Callable[[_T, _T], int]):

        self.root = None
        self.comparable = comparable

        for i in iterable:
            self.add(i)

    def __add(self, node: TreeNode, item: _T) -> None:

        if self.comparable(item, node.item) < 0:
            if node.left is None:
                node.left = TreeNode(item)
            else:
                self.__add(node.left, item)
        else:
            if node.right is None:
                node.right = TreeNode(item)
            else:
                self.__add(node.right, item)

    def __remove(self, node: TreeNode, item: _T) -> None:

        if node is None:
            return None

        predecessor = None

        while True:

            if self.comparable(item, node.item) < 0:
                predecessor = node
                node = node.left
            elif self.comparable(item, node.item) > 0:
                predecessor = node
                node = node.right

            else:
                if node.right is not None:
                    item = self._min(node.right)
                    node.item = item
                    predecessor = node
                    node = node.right
                elif node.left is not None:
                    item = self._max(node.left)
                    node.item = item
                    predecessor = node
                    node = node.left
                else:
                    if predecessor is None:
                        self.root = None
                    elif predecessor.left is node:
                        predecessor.left = None
                    else:
                        predecessor.right = None
                    del node
                    break

    def _pass_in_order(self, node: TreeNode, func: Callable[[_T], None]) -> None:

        if node.left is not None:
            self._pass_in_order(node.left, func)

        func(node)

        if node.right is not None:
            self._pass_in_order(node.right, func)

    def _max(self, node: TreeNode) -> _T:

        if node is None:
            return None

        if node.right is None:
            return node.item
        else:
            return self._max(node.right)

    def _min(self, node: TreeNode) -> _T:

        if node is None:
            return None
        if node.left is None:
            return node.item
        else:
            return self._min(node.left)

    def add(self, item: _T) -> None:

        if self.root is None:
            self.root = TreeNode(item)
        else:
            self.__add(self.root, item)

    def remove(self, item: _T) -> None:
        return self.__remove(self.root, item)

    def pass_in_order(self, func: Callable[[_T], None]) -> None:

        if self.root is not None:
            self._pass_in_order(self.root, func)


class AVLTree(Tree):

    __ALLOWED_IMBALANCE = 1

    def __ll_rotation(self, node: AVLNode) -> AVLNode:

        temp = node.left
        node.left = temp.right
        temp.right = node

        node.height = max(AVLNode.get_height(node.left), AVLNode.get_height(node.right)) + 1
        temp.height = max(node.height, AVLNode.get_height(temp.left)) + 1

        if node is self.root:
            self.root = temp

        return temp

    def __rr_rotation(self, node: AVLNode) -> AVLNode:

        temp = node.right
        node.right = temp.left
        temp.left = node

        node.height = max(AVLNode.get_height(node.left), AVLNode.get_height(node.right)) + 1
        temp.height = max(node.height, AVLNode.get_height(temp.right)) + 1

        if node is self.root:
            self.root = temp

        return temp

    def __lr_rotation(self, node: AVLNode) -> AVLNode:
        node.left = self.__rr_rotation(node.left)
        return self.__ll_rotation(node)

    def __rl_rotation(self, node: AVLNode) -> AVLNode:
        node.right = self.__ll_rotation(node.right)
        return self.__rr_rotation(node)

    def __balance(self, node: AVLNode) -> AVLNode:

        if node is None:
            return None

        if AVLNode.get_height(node.left) - AVLNode.get_height(node.right) > AVLTree.__ALLOWED_IMBALANCE:
            if AVLNode.get_height(node.left.left) >= AVLNode.get_height(node.left.right):
                node = self.__ll_rotation(node)
            else:
                node = self.__lr_rotation(node)

        elif AVLNode.get_height(node.right) - AVLNode.get_height(node.left) > AVLTree.__ALLOWED_IMBALANCE:
            if AVLNode.get_height(node.right.right) >= AVLNode.get_height(node.right.left):
                node = self.__rr_rotation(node)
            else:
                node = self.__rl_rotation(node)

        node.height = max(AVLNode.get_height(node.left), AVLNode.get_height(node.right)) + 1
        return node

    def __remove(self, node: TreeNode, item: _T) -> None:

        predecessor = None
        s = Stack([])

        while True:

            if node is None:
                return None

            if self.comparable(item, node.item) < 0:
                predecessor = node
                node = node.left
            elif self.comparable(item, node.item) > 0:
                predecessor = node
                node = node.right

            else:
                if node.right is not None:
                    item = self._min(node.right)
                    node.item = item
                    predecessor = node
                    node = node.right
                elif node.left is not None:
                    item = self._max(node.left)
                    node.item = item
                    predecessor = node
                    node = node.left
                else:
                    if predecessor is None:
                        self.root = None
                    elif predecessor.left is node:
                        predecessor.left = None
                    else:
                        predecessor.right = None
                    del node
                    break
            s.push(predecessor)

        temp = self.__balance(s.pop())
        while not s.is_empty():

            predecessor = s.pop()
            if predecessor.right and self.comparable(predecessor.item, temp.item) >= 0:
                predecessor.left = temp
            else:
                predecessor.right = temp

            temp = self.__balance(predecessor)

    def __add(self, node: AVLNode, item: _T) -> None:

        s = Stack([])

        while True:

            if node is None:
                node = AVLNode(item)
                break

            s.push(node)

            if self.comparable(item, node.item) < 0:
                node = node.left
            else:
                node = node.right

        while not s.is_empty():

            temp = s.pop()

            if self.comparable(node.item, temp.item) < 0:
                temp.left = node
            else:
                temp.right = node

            temp = self.__balance(temp)
            node = temp

    def add(self, item: _T) -> None:

        if self.root is None:
            self.root = AVLNode(item)
        else:
            self.__add(self.root, item)

    def remove(self, item: _T) -> None:
        return self.__remove(self.root, item)
