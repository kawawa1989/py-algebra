from __future__ import annotations
from functools import singledispatch


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


class PermutationGroupElement:
    def __init__(self, identity: tuple, sequence: tuple) -> None:
        self.identity = identity
        self.sequence = sequence
        self.transpositions = parse_transpositions(
            self.sequence, identity)

    @property
    def sequence_key(self):
        return str(self.sequence)

    @property
    def swap_count(self):
        return len(self.transpositions)

    @property
    def is_even(self):
        return self.swap_count % 2 == 0

    @property
    def print_swap_flow(self):
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

    @property
    def cycle_values(self) -> tuple[tuple[int, ...], ...]:
        values: list[tuple[int, ...]] = []

        def has_been_marked(item):
            for mark_as_used_item in values:
                if item in mark_as_used_item:
                    return True
            return False

        def find_cyclic(value, group: list[int]):
            i = self.identity.index(value)
            a = self.identity[i]
            b = self.sequence[i]
            if b in group or has_been_marked(b):
                return

            group.append(b)
            find_cyclic(b, group)

        for i in range(len(self.identity)):
            a = self.identity[i]
            if has_been_marked(a):
                continue
            b = self.sequence[i]
            if a != b:
                group = [a, b]
                find_cyclic(b, group)
                values.append(tuple(group))

        if len(values) == 0:
            values.append(tuple([]))
        return tuple(values)

    def __str__(self):
        s = ""
        for cycle in self.cycle_values:
            s += str(cycle)
        if not s:
            s = "()"
        return s

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
