from algebra_structure.group.permutation_group import PermutationGroup
from algebra_structure.group.symmetric_group import SymmetricGroup


S4 = SymmetricGroup(4)
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
KleinsGroup = S4["(),(1 2)(3 4),(1 3)(2 4),(1 4)(2 3)"]
print("-------------------------------")
print(f"KleinsGroup (length={KleinsGroup.order}):")
print("-------------------------------")
print(KleinsGroup)

SA_q = S4 / KleinsGroup
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
    print("-------------------------------")
    for e in group:
        g = PermutationGroup.create_group(group, [e])

V1 = KleinsGroup * S4["(3 4)"]
print("-------------------------------")
print(f"V1")
print("-------------------------------")
print(V1)