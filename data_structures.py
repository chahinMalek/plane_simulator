from typing import Generic, List, TypeVar

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

    def __repr__(self):
        return str(self.item)


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

    def is_empty(self):
        return self.first is None

    def __del__(self):

        while not self.is_empty():
            self.pop()
        del self

