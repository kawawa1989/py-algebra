from permutation_group import PermutationGroup
S4 = PermutationGroup.create_symmetric_group(4)


print("-------------------------------")
print(f"S4 (length={S4.order}):")
print("-------------------------------")
print(S4)
print("Cyclic Group:")
for e in S4:
    cyclic_group = S4.create_cyclic_group(e)
    print("-------------------------------")
    print(f"{e} len: {cyclic_group.order}")
    print("-------------------------------")
    print(cyclic_group)


A4 = S4.alternating_group
print("-------------------------------")
print(f"A4 (length={A4.order}):")
print("-------------------------------")
print(A4)

KleinsGroup = S4[(((),), ((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3)))]

print("-------------------------------")
print(f"KleinsGroup (length={KleinsGroup.order}):")
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
    for e in group:
        g = PermutationGroup.create_group(group, [e])
        print(KleinsGroup.mul(g))
