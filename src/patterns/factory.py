"""
Factory Pattern
- defines an interface (AbsFactory) for creating an object (Product),
  but lets subclass (Factory1 and Factory2) decide which class to instantiate
- lets class defer class instantiation to subclass
"""
from abc import ABC
from abc import abstractmethod

class AbsProduct(ABC):

    @abstractmethod
    def product(self):
        pass

class ProductA1(AbsProduct):

    def product(self):
        print('Product A1')

class ProductA2(AbsProduct):

    def product(self):
        print('Product A2')

class ProductB1(AbsProduct):

    def product(self):
        print('Product B1')

class ProductB2(AbsProduct):

    def product(self):
        print('Product B2')

class AbsFactory(ABC):

    @abstractmethod
    def create_product_A(self):
        pass

    @abstractmethod
    def create_product_B(self):
        pass

class Factory1(AbsFactory):

    def create_product_A(self):
        return ProductA1()

    def create_product_B(self):
        return ProductB1()

class Factory2(AbsFactory):

    def create_product_A(self):
        return ProductA2()

    def create_product_B(self):
        return ProductB2()


class Main(object):
    """
    $ python src/patterns/factory.py

    Factory 1
    =========
    Product A1
    Product B1


    Factory 2
    =========
    Product A2
    Product B2
    """

    def main(self):
        print('Factory 1')
        print('=========')
        factory1 = Factory1()
        factory1.create_product_A().product()
        factory1.create_product_B().product()
        print('\n')

        print('Factory 2')
        print('=========')
        factory2 = Factory2()
        factory2.create_product_A().product()
        factory2.create_product_B().product()

if __name__ == '__main__':
    Main().main()