from itertools import permutations
from algebra_structure.group.permutation_group import PermutationGroup
from algebra_structure.group.permutation_group_element import PermutationGroupElement
from algebra_structure.group.symmetric_group import SymmetricGroup


def sort_key(x: PermutationGroupElement):
    key1 = 0 if x.is_even else 1
    key2 = 0
    if x.is_even:
        key2 = len(x.cycle_value)
    else:
        key2 = len(x.cycle_value[0])
    return (key1, key2)


def dump_csv(group: SymmetricGroup):
    csv = ","
    for x in sorted(group, key=sort_key):
        x_str = f"{x}".replace(",", "")
        csv += x_str + ","
    csv += "\n"
    for y in sorted(group, key=sort_key):
        y_str = f"{y}".replace(",", "")
        csv += y_str + ","
        for x in sorted(group, key=sort_key):
            x_str = f"{x * y}".replace(",", "")
            csv += x_str + ","
        csv += "\n"
    print(csv)


S4 = SymmetricGroup(4)
A4 = S4.alternating_group


"""
G = S4
N = A4
conjugates: dict[tuple, list[PermutationGroupElement]] = {}

for n in N:
    elements = []
    for g in G:
        inv = g.inverse()
        b = g * n * inv
        elements.append(b)
    sorted_keys = tuple(sorted(e.cycle_value for e in elements))
    if not sorted_keys in conjugates:
        conjugates[sorted_keys] = []
    conjugates[sorted_keys].append(n)
print(len(conjugates))
"""

G = A4
N = A4
conjugacy_classes: dict[tuple, list[PermutationGroupElement]] = {}

for n in N:
    elements = [g * n * g.inverse() for g in G]
    sorted_keys = tuple(sorted(e.cycle_value for e in elements))
    conjugacy_classes.setdefault(sorted_keys, []).append(n)
groups = [PermutationGroup.create_group(G, values) for values in conjugacy_classes.values()]


for i, group in enumerate(groups):
    print("-------------------------------------")
    print(f"Group {i}")
    print("-------------------------------------")
    for element in group:
        print(element)

#for key, elements in conjugacies_dict.items():
#    print(key)
#    print(len(elements))

#SA_q = S4 / A4
#dump_csv(S4)

