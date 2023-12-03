from __future__ import annotations
from itertools import permutations
from permutation_group_element import PermutationGroupElement


def generate_key(value: tuple[int, ...]):
    return str(value)


class PermutationGroup:
    @classmethod
    def create_symmetric_group(cls, n):
        sequence = []
        for i in range(n):
            sequence.append(i + 1)

        inst: PermutationGroup = cls()
        inst.root = inst
        inst.original_sequence = tuple(sequence)

        # 全ての組み合わせパターンを生成
        swapped_sequences = list(permutations(inst.original_sequence))
        i = 0
        for c in swapped_sequences:
            swap_seqs = inst.find_swap_sequence(c, inst.original_sequence)
            element = PermutationGroupElement(
                inst.original_sequence,
                c,
                swap_seqs)

            key = generate_key(element.own_sequence)
            inst.elements[key] = element
            i += 1
        return inst

    @classmethod
    def create_group(cls, parent: PermutationGroup, elements: list[PermutationGroupElement]):
        dic = {}
        for e in elements:
            dic[generate_key(e.own_sequence)] = e
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.original_sequence = parent.original_sequence
        inst.elements = dic
        return inst

    @classmethod
    def create_child_group(cls, parent: PermutationGroup, elements: dict[str, PermutationGroupElement]):
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.original_sequence = parent.original_sequence
        inst.elements = elements
        return inst

    def __init__(self) -> None:
        self.root: PermutationGroup = None
        self.original_sequence: tuple[int, ...] = ()
        self.elements: dict[str, PermutationGroupElement] = {}

    def get_element_by_sequence(self, sequence: tuple):
        return self.elements[generate_key(sequence)]

    def get_element_by_cycle(self, cycle_values: tuple):
        for e in self.elements.values():
            if e.cycle_values == cycle_values:
                return e
        return None

    def element_op_pow(self, element: PermutationGroupElement, p: int):
        return self.get_element_by_sequence(element.pow(p))

    def create_cyclic_group(self, element: PermutationGroupElement):
        current_seq = element.own_sequence
        cyclic_group_elements = []
        while current_seq != self.original_sequence:
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
                gh = g.mul(h.mul(self.original_sequence))
                k = generate_key(gh)
                elements[k] = self.root.elements[k]
        return PermutationGroup.create_child_group(self.root, elements=elements)

    # 引数は部分群 H とし、 gH の左剰余類を求める
    def quat(self, H: PermutationGroup) -> list[PermutationGroup]:
        G = self
        quatients: dict[str, dict[str, PermutationGroupElement]] = {}
        for g in G.elements.values():
            coset: list[PermutationGroupElement] = []
            for h in H.elements.values():
                gh = g.mul(h.mul(self.original_sequence))
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
                elements[generate_key(e.own_sequence)] = e
        return PermutationGroup.create_child_group(self, elements)

    def find_swap_sequence(self, combination: tuple, original_sequence: list[int]):
        swap_seqs = []
        origin = 0
        n_seq = list(combination)
        for value in original_sequence:
            i = n_seq.index(value)
            # インデックスが一致しないのであれば origin にある要素と入れ替えを行う
            if i != origin:
                swap_seqs.append([n_seq[i], n_seq[origin]])
                n_seq[i], n_seq[origin] = n_seq[origin], n_seq[i]

            origin += 1
        return swap_seqs

    def __str__(self):
        s = ""
        for k, e in self.elements.items():
            s += f"{e}\n"
        return s

    def to_sorted_string(self):
        s = ""
        for k, e in sorted(self.elements.items()):
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
                        self.get_element_by_sequence(e.own_sequence))

        return PermutationGroup.create_group(self, elements)
