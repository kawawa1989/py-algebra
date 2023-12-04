from itertools import permutations
from algebra_structure.group.permutation_group import PermutationGroup
from algebra_structure.group.permutation_group_element import PermutationGroupElement

class SymmetricGroup(PermutationGroup):
    def __init__(self, n: int) -> None:
        super().__init__()
        identity_set = []
        for i in range(n):
            identity_set.append(i + 1)
        self.root = self
        self.identity_set = tuple(identity_set)
        self.__alternating_group: PermutationGroup = None

        # 全ての組み合わせパターンを生成
        permuted_sets = list(permutations(self.identity_set))
        for permuted_set in permuted_sets:
            element = PermutationGroupElement(self, self.identity_set, permuted_set)
            self.elements[element.id] = element

    @property
    def alternating_group(self) -> PermutationGroup:
        if self.__alternating_group:
            return self.__alternating_group

        elements: dict[str, PermutationGroupElement] = {}
        for e in self:
            if e.is_even:
                elements[e.permuted_set] = e
        self.__alternating_group = PermutationGroup.create_group_by_dict(
            self, elements)
        return self.__alternating_group
