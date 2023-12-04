from __future__ import annotations
from algebra_structure.operator.group import Element, IElementProvider

# permuted_set の値を解析してサイクルの積を求める
def parse_cycle_products(permuted_set: tuple, identity_set: tuple):
    cycles = []
    identity_index = 0
    temp_set = list(permuted_set)
    for value in identity_set:
        permuted_index = temp_set.index(value)
        # インデックスが一致しないのであれば identity_index にある要素と入れ替えを行う
        if permuted_index != identity_index:
            cycles.append([temp_set[permuted_index], temp_set[identity_index]])
            temp_set[permuted_index], temp_set[identity_index] = temp_set[identity_index], temp_set[permuted_index]

        identity_index += 1
    return cycles


# 置換前 → 置換後のサイクルを求める。
# 例えば identity_set が (1 2 3) で permuted_set が (2 3 1) である場合、
# 1 → 2 → 3 → 1 という置換になるので計算結果は (1 2 3) になる。
# identity_set が (1 2 3 4) で permuted_set が (2 1 4 3) の場合、
# 「1 と 2 の交換」と 「3 と 4 の交換」という操作になる(循環しないので別々の操作と扱う) ので
# (1 2)(3 4) となる
def scan_cycle(identity_set: tuple, permuted_set: tuple) -> tuple[tuple]:
    cycle_value: list[tuple] = []

    def has_scanned(value):
        for cycle in cycle_value:
            if value in cycle:
                return True
        return False

    # value が identity_set の何番目に存在するのかをチェックし、 identity_set にセットされている場所の permuted_set の値をチェックする。
    # 走査済みではないのであれば cycle に perm_value を登録し、今度は perm_value の値を使って再帰的に同様のチェックを行う。
    def find_cycle(value, cycle: list[int]):
        id_index = identity_set.index(value)
        perm_value = permuted_set[id_index]
        if perm_value in cycle or has_scanned(perm_value):
            return
        cycle.append(perm_value)
        find_cycle(perm_value, cycle)

    for index in range(len(identity_set)):
        id_value = identity_set[index]
        if has_scanned(id_value):
            continue
        perm_value = permuted_set[index]
        if id_value != perm_value:
            cycle = [id_value, perm_value]
            find_cycle(perm_value, cycle)
            cycle_value.append(tuple(cycle))

    if len(cycle_value) == 0:
        cycle_value.append(tuple([]))
    return tuple(cycle_value)


# 対称群の元を定義する
class PermutationGroupElement(Element):
    # identity_set ... 恒等元の役割を持つ、 (1,2,3,...n) の集合
    #              この値をもとに置換操作を行う
    # permuted_set ... identity_set を置換した後の数列
    def __init__(self, provider: IElementProvider, identity_set: tuple, permuted_set: tuple) -> None:
        super().__init__(provider)
        self.identity_set = identity_set
        self.permuted_set = permuted_set
        self.permutations = parse_cycle_products(self.permuted_set, identity_set)
        self.cycle_value = scan_cycle(self.identity_set, self.permuted_set)

    # 置換回数
    @property
    def permutations_count(self):
        return len(self.permutations)
    
    # 識別子
    @property
    def id(self):
        return self.permuted_set

    # 偶置換であるか
    @property
    def is_even(self):
        return self.permutations_count % 2 == 0

    # 置換操作のログを出力する
    @property
    def print_permutation_flow(self):
        temp = list(self.identity_set)
        s = "------------------------------------\n"
        s += f"{self.cycle_value}\n"
        s += "------------------------------------\n"
        s += f"{self.identity_set}\n"
        s += f"{self.permuted_set}\n"
        for permutation in reversed(self.permutations):
            i = temp.index(permutation[0])
            j = temp.index(permutation[1])
            temp[i], temp[j] = temp[j], temp[i]
            s += f"permutation ({permutation[0]}, {permutation[1]}) -> {temp}\n"
        return s

    def __str__(self):
        s = ""
        for cycle in self.cycle_value:
            s += str(cycle)
        if not s:
            s = "()"
        return s

    def pow(self, p: int) -> PermutationGroupElement:
        temp_set = self.identity_set
        for _ in range(p):
            temp_set = self.mul(temp_set)
        return self.provider.provide(temp_set)

    def __mul__(self, value: any) -> PermutationGroupElement:
        return self.provider.provide(self.mul(value))

    def mul(self, value) -> tuple:
        temp_set = None
        if isinstance(value, tuple):
            temp_set = list(value)
        else:
            temp_set = list(value.permuted_set)

        for swap in reversed(self.permutations):
            i = temp_set.index(swap[0])
            j = temp_set.index(swap[1])
            temp_set[i], temp_set[j] = temp_set[j], temp_set[i]
        return tuple(temp_set)
