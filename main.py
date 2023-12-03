from permutation_group import PermutationGroup
S4 = PermutationGroup.create_symmetric_group(4)


print("-------------------------------")
print(f"S4 (length={len(S4.elements)}):")
print("-------------------------------")
print(S4)
print("Cyclic Group:")
for e in S4.elements.values():
    cyclic_group = S4.create_cyclic_group(e)
    print("-------------------------------")
    print(f"{e} len: {len(cyclic_group.elements)}")
    print("-------------------------------")
    print(cyclic_group)


A4 = S4.alternating_group
print("-------------------------------")
print(f"A4 (length={len(A4.elements)}):")
print("-------------------------------")
print(A4)

KleinsGroup = S4[(((),), ((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3)))]

print("-------------------------------")
print(f"KleinsGroup (length={len(KleinsGroup.elements)}):")
print("-------------------------------")
print(KleinsGroup)

SA_q = S4.quat(KleinsGroup)

print("-------------------------------")
print(f"S4/A4 (length={len(SA_q)}):")
print("-------------------------------")
for index, group in enumerate(SA_q):
    if index == 0:
        continue
    print("-------------------------------")
    print(f"[{index}]")
    print("-------------------------------")
    print(group)
    for e in group.elements.values():
        g = PermutationGroup.create_group(group, [e])
        print(KleinsGroup.mul(g))


"""
print(klein2)

print(g)
sub = g.get_subset([[(3, 4)]])
print(sub)
print(sub.mul(klein))

sub = g.get_subset([[(1, 2)]])
print(sub)
print(sub.mul(klein))

sub = g.get_subset([[(1, 3, 2, 4)]])
print(sub)
print(sub.mul(klein))

PermutationGroup.symmetric_group(4)
"""
