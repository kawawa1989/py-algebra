from itertools import permutations
from algebra_structure.group.permutation_group import PermutationGroup
from algebra_structure.group.permutation_group_element import PermutationGroupElement
from algebra_structure.group.symmetric_group import SymmetricGroup


S4 = SymmetricGroup(4)
print("-------------------------------")
print(f"S4 (length={S4.order}):")
print("-------------------------------")
print(S4)


#for e in S4:
#    print(e.print_permutation_flow)
    