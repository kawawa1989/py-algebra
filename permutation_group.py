from __future__ import annotations
from permutation_group_element import PermutationGroupElement


class PermutationGroup:
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
    def create_group_by_dict(cls, parent: PermutationGroup, elements: dict[tuple, PermutationGroupElement]):
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.identity = parent.identity
        inst.elements = elements
        return inst

    def __init__(self) -> None:
        self.root: PermutationGroup = None
        self.identity: tuple[int, ...] = ()
        self.elements: dict[tuple, PermutationGroupElement] = {}
        self.inverse_map: dict[tuple, PermutationGroupElement] = None
        self.cyclic_group_map: dict[tuple, PermutationGroupElement] = None

    @property
    def order(self) -> int:
        return len(self.elements)

    def get_element_by_sequence(self, sequence: tuple):
        return self.elements[sequence]

    def get_element_by_cycle(self, cycle_values: tuple):
        for e in self:
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
        for g in G:
            for h in H:
                gh = g.mul(h.mul(self.identity))
                elements[gh] = self.root.elements[gh]
        return PermutationGroup.create_group_by_dict(self.root, elements=elements)

    # 引数は部分群 H とし、 gH の左剰余類を求める
    def quat(self, H: PermutationGroup) -> list[PermutationGroup]:
        G = self
        quatients: dict[str, dict[str, PermutationGroupElement]] = {}
        for g in G:
            coset: list[PermutationGroupElement] = []
            for h in H:
                gh = g.mul(h.mul(self.identity))
                elem = self.get_element_by_sequence(gh)
                coset.append(elem)

            sorted_keys = tuple(sorted(e.cycle_values for e in coset))
            if not sorted_keys in quatients:
                quatients[sorted_keys] = {}
            quatients[sorted_keys][g.sequence] = g

        quatient_list: list[PermutationGroup] = []
        for elements in quatients.values():
            group = PermutationGroup.create_group_by_dict(self, elements)
            quatient_list.append(group)

        return quatient_list

    def __iter__(self):
        for e in self.elements.values():
            yield e

    def __str__(self):
        s = ""
        for e in self:
            s += f"{e}\n"
        return s

    def to_string(self, sort_elements=True):
        elements = list(self.elements.values())
        if sort_elements:
            elements = sorted(elements, key=lambda x: x.cycle_values)
        s = ""
        for e in elements:
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
            for e in self:
                if equals(e.cycle_values, key):
                    elements.append(
                        self.get_element_by_sequence(e.sequence))

        return PermutationGroup.create_group(self, elements)
