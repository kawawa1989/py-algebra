from __future__ import annotations
import re
from algebra_structure.group.permutation_group_element import PermutationGroupElement
from algebra_structure.operator.group import Element, Group, IElementProvider

class PermutationGroup(Group, IElementProvider):
    @classmethod
    def create_group(cls, parent: PermutationGroup, elements: list[PermutationGroupElement]):
        dic = {}
        for e in elements:
            dic[e.permuted_set] = e
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.identity_set = parent.identity_set
        inst.elements = dic
        return inst

    @classmethod
    def create_group_by_dict(cls, parent: PermutationGroup, elements: dict[tuple, PermutationGroupElement]):
        inst: PermutationGroup = cls()
        inst.root = parent
        inst.identity_set = parent.identity_set
        inst.elements = elements
        return inst

    def __init__(self) -> None:
        self.root: PermutationGroup = None
        self.identity_set: tuple[int, ...] = ()
        self.elements: dict[tuple, PermutationGroupElement] = {}
        self.inverse_map: dict[tuple, PermutationGroupElement] = None
        self.cyclic_group_map: dict[tuple, PermutationGroupElement] = None

    @property
    def order(self) -> int:
        return len(self.elements)

    def provide(self, id: any) -> PermutationGroupElement:
        element = self.get_element_by_id(id)
        if element:
            return element
        return self.get_element_by_cycle(id)

    def operator_mul_g_and_e(self, e: Element):
        return self.mul(PermutationGroup.create_group(self, [e]))

    def operate_mul_g_and_h(self, h: Group):
        return self.mul(h)
    
    def operate_truediv_g_and_h(self, h: Group):
        return self.quat(h)

    def get_element_by_id(self, id: tuple):
        if not id in self.elements:
            return None
        return self.elements[id]

    def get_element_by_cycle(self, cycle_value: tuple):
        for e in self:
            if e.cycle_value == cycle_value:
                return e
        return None

    def create_cyclic_group(self, element: PermutationGroupElement):
        cyclic_group_elements = []
        elem = element
        while elem.permuted_set != self.identity_set:
            cyclic_group_elements.append(elem)
            elem = element * elem

        cyclic_group_elements.append(elem)
        return PermutationGroup.create_group(self, cyclic_group_elements)

    # 群同士の積を求めて新しい群を作成する
    def mul(self, H: PermutationGroup) -> PermutationGroup:
        G = self
        elements: dict[str, PermutationGroupElement] = {}
        for g in G:
            for h in H:
                gh = g * h * self.identity_set
                elements[gh.id] = gh
        return PermutationGroup.create_group_by_dict(self.root, elements=elements)

    # 引数は部分群 H とし、 gH の左剰余類を求める
    def quat(self, H: PermutationGroup) -> list[PermutationGroup]:
        G = self
        quatients: dict[str, dict[str, PermutationGroupElement]] = {}
        for g in G:
            coset: list[PermutationGroupElement] = []
            for h in H:
                gh = g * h
                coset.append(gh)

            sorted_keys = tuple(sorted(e.cycle_value for e in coset))
            if not sorted_keys in quatients:
                quatients[sorted_keys] = {}
            quatients[sorted_keys][g.id] = g

        quatient_list: list[PermutationGroup] = []
        for elements in quatients.values():
            group = PermutationGroup.create_group_by_dict(self, elements)
            quatient_list.append(group)

        return quatient_list
    
    # 共役類を探し、リスト形式に変換して返す
    def get_conjugacy_classes(self):
        G = self
        N = self
        conjugacy_classes: dict[tuple, list[PermutationGroupElement]] = {}
        for n in N:
            elements = [g * n * g.inverse() for g in G]
            sorted_keys = tuple(sorted(e.cycle_value for e in elements))
            conjugacy_classes.setdefault(sorted_keys, []).append(n)
        return [PermutationGroup.create_group(self, values) for values in conjugacy_classes.values()]

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
            elements = sorted(elements, key=lambda x: x.cycle_value)
        s = ""
        for e in elements:
            s += f"{e}\n"
        return s

    def __getitem__(self, query: str):
        elements = []
        splitted_query = query.split(",")
        for q in splitted_query:
            cycle_value = []
            for match in re.findall(r"\(([\d\s]*)\)", q.strip()):
                numbers_str = match.split(" ")
                cycle = []
                for num in numbers_str:
                    if not num:
                        continue
                    cycle.append(int(num))
                cycle_value.append(tuple(cycle))
            element = self.get_element_by_cycle(tuple(cycle_value))
            elements.append(element)
        if len(elements) == 1:
            return elements[0]
        return PermutationGroup.create_group(self, elements)

