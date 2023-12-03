class PermutationGroupElement:
    def __init__(self, original_sequence: tuple[int, ...], own_sequence: tuple[int, ...],  swap_seqs: list[list[int]]) -> None:
        self.original_sequence = original_sequence
        self.own_sequence = own_sequence
        self.swap_seqs = swap_seqs

    @property
    def sequence_key(self):
        return str(self.own_sequence)

    @property
    def swap_count(self):
        return len(self.swap_seqs)

    @property
    def is_even(self):
        return self.swap_count % 2 == 0

    @property
    def print_swap_flow(self):
        sequence = list(self.original_sequence)
        s = "------------------------------------\n"
        s += f"{self.cycle_values}\n"
        s += "------------------------------------\n"
        s += f"{self.original_sequence}\n"
        s += f"{self.own_sequence}\n"
        for swap in reversed(self.swap_seqs):
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
            i = self.original_sequence.index(value)
            a = self.original_sequence[i]
            b = self.own_sequence[i]
            if b in group or has_been_marked(b):
                return

            group.append(b)
            find_cyclic(b, group)

        for i in range(len(self.original_sequence)):
            a = self.original_sequence[i]
            if has_been_marked(a):
                continue
            b = self.own_sequence[i]
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

    def mul(self, value: tuple[int, ...]) -> tuple[int, ...]:
        sequence = list(value)
        for swap in reversed(self.swap_seqs):
            i = sequence.index(swap[0])
            j = sequence.index(swap[1])
            sequence[i], sequence[j] = sequence[j], sequence[i]
        return tuple(sequence)
