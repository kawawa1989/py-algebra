from __future__ import annotations
from abc import abstractmethod


class IElement:
    pass

class IElementProvider:
    @abstractmethod
    def provide(self, id: any) -> IElement:
        pass

class Element(IElement):
    def __init__(self, provider: IElementProvider) -> None:
        self.provider = provider
        pass

    # 群の要素同士の演算
    @abstractmethod
    def __mul__(self, value: any) -> Element:
        pass

    
class Group:
    def __init__(self, elements) -> None:
        self.elements = elements
        pass

    @abstractmethod
    def operator_mul_g_and_e(self, e: Element) -> Group:
        pass

    @abstractmethod
    def operate_mul_g_and_h(self, h: Group) -> Group:
        pass

    # 群同士の積を求めて新しい群を作成する
    def __mul__(self, x) -> Group:
         # 群・要素での演算
        if isinstance(x, Element):
            return self.operator_mul_g_and_e(x)
         # 群同士の演算
        elif isinstance(x, Group):
            return self.operate_mul_g_and_h(x)
        raise ValueError(f"群の演算に失敗しました。 引数の型がサポート対象外です。 型: {type(x)}")


