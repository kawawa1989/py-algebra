from itertools import permutations
from permutation_group import PermutationGroup
from permutation_group_element import PermutationGroupElement


class SymmetricGroup(PermutationGroup):
    def __init__(self, n: int) -> None:
        super().__init__()
        sequence = []
        for i in range(n):
            sequence.append(i + 1)
        self.root = self
        self.identity = tuple(sequence)
        self.__alternating_group: PermutationGroup = None

        # 全ての組み合わせパターンを生成
        swapped_sequences = list(permutations(self.identity))
        i = 0
        for c in swapped_sequences:
            element = PermutationGroupElement(self.identity, c)
            key = element.sequence
            self.elements[key] = element
            i += 1

    @property
    def alternating_group(self) -> PermutationGroup:
        if self.__alternating_group:
            return self.__alternating_group

        elements: dict[str, PermutationGroupElement] = {}
        for e in self:
            if e.is_even:
                elements[e.sequence] = e
        self.__alternating_group = PermutationGroup.create_child_group(
            self, elements)
        return self.__alternating_group
