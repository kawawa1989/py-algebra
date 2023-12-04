from __future__ import annotations
from algebra_structure.operator.group import Element, IElementProvider

def parse_transpositions(sequence: tuple, identity: list[int]):
    transpositions = []
    origin = 0
    n_seq = list(sequence)
    for value in identity:
        i = n_seq.index(value)
        # インデックスが一致しないのであれば origin にある要素と入れ替えを行う
        if i != origin:
            transpositions.append([n_seq[i], n_seq[origin]])
            n_seq[i], n_seq[origin] = n_seq[origin], n_seq[i]

        origin += 1
    return transpositions


# 置換前 → 置換後のサイクルを求める。
# 例えば identity が (1 2 3) で sequence が (2 3 1) である場合、
# 1 → 2 → 3 → 1 という置換になるので計算結果は (1 2 3) になる。
# identity が (1 2 3 4) で sequence が (2 1 4 3) の場合、
# 「1 と 2 の交換」と 「3 と 4 の交換」という操作になる(循環しないので別々の操作と扱う) ので
# (1 2)(3 4) となる
def parse_cycle_values(identity: tuple, sequence: tuple) -> tuple[tuple]:
    values: list[tuple] = []

    def has_been_marked(item):
        for mark_as_used_item in values:
            if item in mark_as_used_item:
                return True
        return False

    def find_cyclic(value, group: list[int]):
        i = identity.index(value)
        a = identity[i]
        b = sequence[i]
        if b in group or has_been_marked(b):
            return

        group.append(b)
        find_cyclic(b, group)

    for i in range(len(identity)):
        a = identity[i]
        if has_been_marked(a):
            continue
        b = sequence[i]
        if a != b:
            group = [a, b]
            find_cyclic(b, group)
            values.append(tuple(group))

    if len(values) == 0:
        values.append(tuple([]))
    return tuple(values)


# 対称群の元を定義する
class PermutationGroupElement(Element):    
    # identity ... 恒等元の役割を持つ、 (1,2,3,...n) の数列
    #              この値をもとに置換操作を行う
    # sequence ... identity を置換した後の数列
    def __init__(self, provider: IElementProvider, identity: tuple, sequence: tuple) -> None:
        super().__init__(provider)
        self.identity = identity
        self.sequence = sequence
        self.transpositions = parse_transpositions(self.sequence, identity)
        self.cycle_values = parse_cycle_values(self.identity, self.sequence)

    # 置換回数
    @property
    def transposition_count(self):
        return len(self.transpositions)

    # 偶置換であるか
    @property
    def is_even(self):
        return self.transposition_count % 2 == 0

    # 置換操作のログを出力する
    @property
    def print_permutation_flow(self):
        sequence = list(self.identity)
        s = "------------------------------------\n"
        s += f"{self.cycle_values}\n"
        s += "------------------------------------\n"
        s += f"{self.identity}\n"
        s += f"{self.sequence}\n"
        for swap in reversed(self.transpositions):
            i = sequence.index(swap[0])
            j = sequence.index(swap[1])
            sequence[i], sequence[j] = sequence[j], sequence[i]
            s += f"swap ({swap[0]}, {swap[1]}) -> {sequence}\n"
        return s

    def __str__(self):
        s = ""
        for cycle in self.cycle_values:
            s += str(cycle)
        if not s:
            s = "()"
        return s

    def __mul__(self, value: any) -> Element:
        return self.provider.provide(self.mul(value))

    def mul(self, value: any) -> tuple:
        sequence = None
        if isinstance(value, tuple):
            sequence = list(value)
        else:
            sequence = list(value.sequence)

        for swap in reversed(self.transpositions):
            i = sequence.index(swap[0])
            j = sequence.index(swap[1])
            sequence[i], sequence[j] = sequence[j], sequence[i]
        return tuple(sequence)

    def pow(self, p: int):
        seq = self.identity
        for i in range(p):
            seq = self.mul(seq)
        return seq
