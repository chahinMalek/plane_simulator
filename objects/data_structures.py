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
