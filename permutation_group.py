from __future__ import annotations
from itertools import permutations
from permutation_group_element import PermutationGroupElement


class PermutationGroup:
    @classmethod
    def create_symmetric_group(cls, n):
        sequence = []
        for i in range(n):
            sequence.append(i + 1)

        inst: PermutationGroup = cls()
        inst.root = inst
        inst.identity = tuple(sequence)

        # 全ての組み合わせパターンを生成
        swapped_sequences = list(permutations(inst.identity))
        i = 0
        for c in swapped_sequences:
            element = PermutationGroupElement(
                inst.identity,
                c)

            key = element.sequence
            inst.elements[key] = element
            i += 1
        return inst

    @classmethod
    def create_group(cls, parent: PermutationGroup, elements: list[PermutationGroupElement]):
        dic = {}
        for e in elements:
            dic[e.sequence] = e
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.identity = parent.identity
        inst.elements = dic
        return inst

    @classmethod
    def create_child_group(cls, parent: PermutationGroup, elements: dict[str, PermutationGroupElement]):
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.identity = parent.identity
        inst.elements = elements
        return inst

    def __init__(self) -> None:
        self.root: PermutationGroup = None
        self.identity: tuple[int, ...] = ()
        self.elements: dict[tuple, PermutationGroupElement] = {}

    def get_element_by_sequence(self, sequence: tuple):
        return self.elements[sequence]

    def get_element_by_cycle(self, cycle_values: tuple):
        for e in self.elements.values():
            if e.cycle_values == cycle_values:
                return e
        return None

    def element_op_pow(self, element: PermutationGroupElement, p: int):
        return self.get_element_by_sequence(element.pow(p))

    def create_cyclic_group(self, element: PermutationGroupElement):
        current_seq = element.sequence
        cyclic_group_elements = []
        while current_seq != self.identity:
            elem = self.get_element_by_sequence(current_seq)
            cyclic_group_elements.append(elem)
            current_seq = element.mul(current_seq)
        elem = self.get_element_by_sequence(current_seq)
        cyclic_group_elements.append(elem)
        return PermutationGroup.create_group(self, cyclic_group_elements)

    # 群同士の積を求めて新しい群を作成する

    def mul(self, H: PermutationGroup) -> PermutationGroup:
        G = self
        elements: dict[str, PermutationGroupElement] = {}
        for g in G.elements.values():
            for h in H.elements.values():
                gh = g.mul(h.mul(self.identity))
                elements[gh] = self.root.elements[gh]
        return PermutationGroup.create_child_group(self.root, elements=elements)

    # 引数は部分群 H とし、 gH の左剰余類を求める
    def quat(self, H: PermutationGroup) -> list[PermutationGroup]:
        G = self
        quatients: dict[str, dict[str, PermutationGroupElement]] = {}
        for g in G.elements.values():
            coset: list[PermutationGroupElement] = []
            for h in H.elements.values():
                gh = g.mul(h.mul(self.identity))
                elem = self.get_element_by_sequence(gh)
                coset.append(elem)

            sorted_keys = tuple(sorted(e.cycle_values for e in coset))
            if not sorted_keys in quatients:
                quatients[sorted_keys] = {}
            quatients[sorted_keys][g.sequence_key] = g

        quatient_list: list[PermutationGroup] = []
        for elements in quatients.values():
            group = PermutationGroup.create_child_group(self, elements)
            quatient_list.append(group)

        return quatient_list

    @property
    def alternating_group(self) -> PermutationGroup:
        elements: dict[str, PermutationGroupElement] = {}
        for e in self.elements.values():
            if e.is_even:
                elements[e.sequence] = e
        return PermutationGroup.create_child_group(self, elements)

    def to_sorted_string(self):
        s = ""
        for k, e in sorted(self.elements.items()):
            s += f"{e}\n"
        return s

    def __str__(self):
        s = ""
        for k, e in self.elements.items():
            s += f"{e}\n"
        return s

    def __getitem__(self, sequence_query):
        def equals(cycle_values, key):
            if len(cycle_values) != len(key):
                return False
            for cycle in cycle_values:
                if not cycle in key:
                    return False
            return True

        elements: list[PermutationGroupElement] = []
        for key in sequence_query:
            for e in self.elements.values():
                if equals(e.cycle_values, key):
                    elements.append(
                        self.get_element_by_sequence(e.sequence))

        return PermutationGroup.create_group(self, elements)
