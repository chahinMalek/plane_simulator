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


class Queue(Generic[_T]):

    def __init__(self, *iterable: _T):

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


class Tree(Generic[_T]):

    def __init__(self, iterable: List[_T], comparable: Callable[[_T, _T], int]):

        self.root = None
        self.comparable = comparable

        for i in iterable:
            self.add(i)

    def _add(self, node: TreeNode, item: _T) -> None:

        if self.comparable(item, node.item) < 0:
            if node.left is None:
                node.left = TreeNode(item)
            else:
                self._add(node.left, item)
        else:
            if node.right is None:
                node.right = TreeNode(item)
            else:
                self._add(node.right, item)

    def _remove(self, node: TreeNode, item: _T) -> None:

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
                    del node
                    if predecessor is None:
                        self.root = None
                    elif predecessor.left is node:
                        predecessor.left = None
                    else:
                        predecessor.right = None
                    break

    def _pass_in_order(self, node: TreeNode, func: Callable[[_T], None]) -> None:

        if node.left is not None:
            self._pass_in_order(node.left, func)

        func(node.item)

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
            self._add(self.root, item)

    def remove(self, item: _T) -> None:
        return self._remove(self.root, item)

    def pass_in_order(self, func: Callable[[_T], None]) -> None:

        if self.root is not None:
            self._pass_in_order(self.root, func)


class AVLTree(Tree):
    pass


t = Tree([], comparable=lambda x, y: x-y)
t.add(5)
t.remove(5)
t.pass_in_order(func=lambda x: print(x))
