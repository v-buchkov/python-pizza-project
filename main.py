"""
Buchkov Viacheslav, DS Track, Python - Project
"""
import click
import random
from typing import Dict, List
from functools import wraps


class Pizza:
    """
    A class of basic Pizza object.

    ...

    Attributes
    ----------
    size : str
        size of the pizza
    recipe : list
        ingredients (tomato sauce and mozzarella are basic => attributes of all Pizza classes)
    icon : str
        icon for the user-friendly representation (advised by marketing department)

    Methods
    -------
    dict():
        Returns Pizza recipe of {'Pizza type' : ingredients} form.
    """
    # List of all available sizes
    # If some additional size is added for all pizza types, this is the only variable that needs to be changed
    AVAILABLE_SIZES = ['L', 'XL']

    def __init__(self, size: str):
        """
        Initializing Pizza object.

        Parameters
        ----------
            size : str
                size of the pizza

        Returns
        -------
        None
        """
        # If some size is not specified as available, then raise AssertionError
        assert size.upper() in self.AVAILABLE_SIZES, f'Unknown size {size}'
        self.size = size.upper()
        # Basic ingredients for all pizzas - specific recipes JUST ADD ingredients
        self.recipe = ['tomato sauce', 'mozzarella']
        # Basic icon
        self.icon = '\U0001F9C7'

    def dict(self) -> Dict[str, List[str]]:
        """
        Listing the ingredients for the pizza object.

        Returns
        -------
        dict
        """
        return {f'{self.__class__.__name__}': self.recipe}

    def __eq__(self, other) -> bool:
        """
        Checks, if two pizzas are exactly the same.
        Pizzas are assumed to be the same, if their recipes and sizes match.

        Parameters
        ----------
            other
                other pizza to be compared to

        Returns
        -------
        bool
        """
        # If recipes and sizes match fully, then assume to be equal
        if sorted(self.recipe) == sorted(other.recipe) and self.size == other.size:
            return True
        else:
            return False


class Margherita(Pizza):
    """
    Classical version.
    """
    def __init__(self, size: str = Pizza.AVAILABLE_SIZES[0]):
        """
        Initializing Margherita object.

        Parameters
        ----------
            size : str
                size of the pizza

        Returns
        -------
        None
        """
        super().__init__(size)
        # Only tomatoes added
        self.recipe += ['tomatoes']
        self.icon = '\U0001F9C0'


class Pepperoni(Pizza):
    """
    The most popular version.
    """
    def __init__(self, size: str = Pizza.AVAILABLE_SIZES[0]):
        """
        Initializing Pepperoni object.

        Parameters
        ----------
            size : str
                size of the pizza

        Returns
        -------
        None
        """
        super().__init__(size)
        # Only pepperoni added
        self.recipe += ['pepperoni']
        self.icon = '\U0001F355'


class Hawaiian(Pizza):
    """
    Unusual version.
    """
    def __init__(self, size: str = Pizza.AVAILABLE_SIZES[0]):
        """
        Initializing Hawaiian object.

        Parameters
        ----------
            size : str
                size of the pizza

        Returns
        -------
        None
        """
        super().__init__(size)
        # Chicken and pineapples added
        self.recipe += ['chicken', 'pineapples']
        self.icon = '\U0001F34D'


def baking_time(pizza) -> float:
    """
    Calculates time spent for backing a specified pizza.

        Parameters:
            pizza : Pizza object

        Returns:
            time_spent (float): Time in minutes, spent for baking this pizza
    """
    available_sizes = pizza.AVAILABLE_SIZES
    size = pizza.size
    size_index = available_sizes.index(size)

    # Assume that time spent linearly depends on the size (the larger pizza, the more time spent) with coeff = 1
    return random.randint(7 + size_index, 15 + size_index)


def delivery_time() -> float:
    """
    Calculates time spent for delivering the order.

        Returns:
            time_spent (float): Time in minutes, spent for delivering this order
    """
    return random.randint(15, 31)


def pickup_time() -> float:
    """
    Calculates time spent, waiting for self-service pickup.

        Returns:
            time_spent (float): Time in minutes, spent waiting for self-service pickup
    """
    return random.randint(5, 61)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool) -> None:
    """
    Processes the order (baking + optional delivery) for the specified pizza.

        Parameters:
            pizza (str) : Name of the Pizza that we want to cook
            delivery (bool) : Flag, whether the delivery is needed

        Returns:
            time_spent (float): Time in minutes, spent waiting for self-service pickup
    """
    # Get the correct class by the name from globals in this module
    ordered_pizza = globals()[pizza.capitalize()]
    print('\U0001F373' + f'Приготовили за {baking_time(ordered_pizza())} мин!')
    # Prints about the delivery, only if flag is active (nothing for self-service)
    if delivery:
        print('\U0001F69A' + f'Доставили за {delivery_time()} мин!')


@cli.command()
def menu() -> None:
    """
    Prints all available pizzas.
    """
    # All available Pizzas => all classes that inherit basic Pizza class
    available_pizzas = list(Pizza.__subclasses__())
    # For each such class will print required params
    for p in available_pizzas:
        # print( - {Pizza name} {marketing icon}: {ingredients})
        print(f'- {p.__name__} {p().icon}: {", ".join(p().recipe)}')


def log(blueprint):
    """
    Logging decorator.
    If called as "@log" without argument, will use basic representation "func_name - x min!".

        Parameters:
            blueprint : The blueprint for printing the log. Optional.
    """
    # If called as "@log", blueprint will be the function that is being decorated
    # Therefore, apply basic logic for no-argument function
    if callable(blueprint):
        @wraps(blueprint)
        def default_wrapper(pizza):
            # Calling blueprint, because actually in this case blueprint is func
            time_execution = blueprint(pizza)
            # Print log
            print(blueprint.__name__ + f' - {time_execution} мин!')
        return default_wrapper
    # If else, use blueprint as string to print in the specified format
    else:
        def decorator(func):
            @wraps(func)
            def modified_wrapper(pizza):
                # Get time spent for the specified task
                time_execution = func(pizza)
                # Print log
                print(blueprint.format(time_execution))
            return modified_wrapper
        return decorator


@log
def bake(pizza) -> float:
    """
    Bakes pizza and returns the time spent.

        Parameters:
            pizza : Pizza object

        Returns:
            time_spent (float): Time in minutes, spent for baking this pizza
    """
    return baking_time(pizza)


@log('\U0001F69A' + 'Доставили за {} мин!')
def delivery(pizza) -> float:
    """
    Delivers the pizza and returns the time spent for delivering the order.

        Parameters:
            pizza : Pizza object

        Returns:
            time_spent (float): Time in minutes, spent for delivering this order
    """
    return delivery_time()


@log('\U0001F3E0' + 'Забрали за {} мин!')
def pickup(pizza) -> float:
    """
    Sets pizza for self-service pickup and returns the time spent.

        Parameters:
            pizza : Pizza object

        Returns:
            time_spent (float): Time in minutes, spent waiting for self-service pickup
    """
    return pickup_time()


if __name__ == '__main__':
    cli()
