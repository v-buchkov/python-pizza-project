import pytest
from main import Pizza, Margherita, Pepperoni, Hawaiian, order, menu, baking_time, delivery_time, \
    pickup_time, bake, delivery, pickup
from click.testing import CliRunner
import random

# Fix random for tests
random.seed(1)


@pytest.mark.parametrize('pizza,size',
                         [(Pizza, 'L'),
                          (Margherita, 'xl'),
                          (Pepperoni, 'XL'),
                          (Hawaiian, 'l')])
def test_pizza_size(pizza, size: str):
    """Test that size attribute is set correctly."""
    pizza_size = pizza(size=size).size
    assert pizza_size == size.upper(), f'input: {size}, expected: {size}, got: {pizza_size}'


@pytest.mark.parametrize('pizza,expected_size',
                         [(Hawaiian, 'L'),
                          (Pepperoni, 'L'),
                          (Margherita, 'L')])
def test_pizza_default_size(pizza, expected_size):
    """Test that default size is L."""
    pizza_size = pizza().size
    assert pizza_size == expected_size.upper(), f'input: {pizza}, expected: {expected_size}, got: {pizza_size}'


def test_basic_pizza_requires_size():
    """Test that basic Pizza class requires size to be specified."""
    with pytest.raises(TypeError):
        Pizza()


@pytest.mark.parametrize('pizza,size',
                         [(Pizza, 'X'),
                          (Pepperoni, 'HAHA'),
                          (Margherita, 'XXX')])
def test_pizza_incorrect_size(pizza, size):
    """Test that only L & XL sizes are allowed."""
    with pytest.raises(AssertionError):
        pizza(size=size)


@pytest.mark.parametrize('pizza,size',
                         [(Pizza, 3),
                          (Pepperoni, True),
                          (Margherita, bake)])
def test_pizza_incorrect_type(pizza, size):
    """Test that size allows only str."""
    with pytest.raises(AttributeError):
        pizza(size=size)


@pytest.mark.parametrize('pizza,expected_recipe',
                         [(Pizza, ['tomato sauce', 'mozzarella']),
                          (Margherita, ['tomato sauce', 'mozzarella', 'tomatoes']),
                          (Pepperoni, ['tomato sauce', 'mozzarella', 'pepperoni']),
                          (Hawaiian, ['tomato sauce', 'mozzarella', 'chicken', 'pineapples'])])
def test_pizza_recipe(pizza, expected_recipe: list):
    """Test that recipes are correct."""
    # Use any size => take XL
    pizza_recipe = pizza(size='XL').recipe
    assert sorted(pizza_recipe) == sorted(expected_recipe), f'input: {pizza}, ' \
                                                            f'expected: {expected_recipe}, got: {pizza_recipe}'


@pytest.mark.parametrize('pizza,expected_dict',
                         [(Pizza, {'Pizza': ['tomato sauce', 'mozzarella']}),
                          (Margherita, {'Margherita': ['tomato sauce', 'mozzarella', 'tomatoes']}),
                          (Pepperoni, {'Pepperoni': ['tomato sauce', 'mozzarella', 'pepperoni']}),
                          (Hawaiian, {'Hawaiian': ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']})])
def test_pizza_dict(pizza, expected_dict: dict):
    """Test that dict() method works correctly."""
    # Use any size => take XL
    pizza_dict = pizza(size='XL').dict()
    assert pizza_dict == expected_dict, f'input: {pizza}, expected: {expected_dict}, got: {pizza_dict}'


@pytest.mark.parametrize('pizza1,pizza2',
                         [(Margherita(size='L'), Margherita(size='L')),
                          (Pepperoni(size='L'), Pepperoni(size='L')),
                          (Hawaiian(size='XL'), Hawaiian(size='XL'))])
def test_pizza_eq(pizza1, pizza2):
    """Test that __eq__() method works correctly for True."""
    assert pizza1.__eq__(pizza2), f'input: {pizza1, pizza2}, expected: True, got: False'


@pytest.mark.parametrize('pizza1,pizza2',
                         [(Margherita(size='L'), Margherita(size='XL')),
                          (Pepperoni(size='XL'), Pepperoni(size='L')),
                          (Hawaiian(size='XL'), Hawaiian(size='L')),
                          (Pepperoni(size='L'), Margherita(size='L')),
                          (Hawaiian(size='XL'), Pepperoni(size='XL'))])
def test_pizza_not_eq(pizza1, pizza2):
    """Test that __eq__() method works correctly for False."""
    assert not pizza1.__eq__(pizza2), f'input: {pizza1, pizza2}, expected: False, got: True'


def test_baking_time():
    """Test that backing_time() function returns integer"""
    time = baking_time(Margherita())
    assert isinstance(time, int), f'expected: int, got: {type(time)}'


def test_delivery_time():
    """Test that delivery_time() function returns integer"""
    time = delivery_time()
    assert isinstance(time, int), f'expected: int, got: {type(time)}'


def test_pickup_time():
    """Test that pickup_time() function returns integer"""
    time = pickup_time()
    assert isinstance(time, int), f'expected: int, got: {type(time)}'


def test_bake(capfd):
    """Test that bake() function (with decorator) produces correct output."""
    bake(Margherita())

    # Read print output
    out, err = capfd.readouterr()

    try:
        # Split output to strip from x minutes, produced by random function (to not depend on "seed")
        out = out.split(' - ')
        out[1] = out[1].split(' ')[1]
        expected_output = ['bake', 'мин!\n']
    except IndexError:
        # If split is unsuccessful, then error in function => test is not passed
        raise AssertionError(f'expected: "bake - x мин!", got: {out}')

    assert out == expected_output, f'expected: "bake - x мин!", got: {out}'


def test_delivery(capfd):
    """Test that delivery() function (with decorator) produces correct output."""
    delivery(Margherita())

    out, err = capfd.readouterr()

    expected_output = ['\U0001F69A' + 'Доставили', 'мин!\n']

    try:
        # Split output to strip from x minutes, produced by random function (to not depend on "seed")
        out = out.split(' за ')
        out[1] = out[1].split(' ')[1]
    except IndexError:
        # If split is unsuccessful, then error in function => test is not passed
        raise AssertionError(f'expected: "\U0001F69AДоставили за x мин!", got: {out}')

    assert out == expected_output, f'expected: "\U0001F69AДоставили за x мин!", got: {out}'


def test_pickup(capfd):
    """Test that pickup() function (with decorator) produces correct output."""
    pickup(Margherita())

    out, err = capfd.readouterr()

    expected_output = ['\U0001F3E0' + 'Забрали', 'мин!\n']

    try:
        # Split output to strip from x minutes, produced by random function (to not depend on "seed")
        out = out.split(' за ')
        out[1] = out[1].split(' ')[1]
    except IndexError:
        # If split is unsuccessful, then error in function => test is not passed
        raise AssertionError(f'expected: "\U0001F3E0Забрали за x мин!", got: {out}')

    assert out == expected_output, f'expected: "\U0001F3E0Забрали за x мин!", got: {out}'


def test_bake_without_decorator():
    """Test that bake() function (without decorator) produces correct output."""
    original_bake = bake.__wrapped__
    assert isinstance(original_bake(Margherita()), int)


def test_delivery_without_decorator():
    """Test that delivery() function (without decorator) produces correct output."""
    original_delivery = delivery.__wrapped__
    assert isinstance(original_delivery(Margherita()), int)


def test_pickup_without_decorator():
    """Test that pickup() function (without decorator) produces correct output."""
    original_pickup = pickup.__wrapped__
    assert isinstance(original_pickup(Margherita()), int)


def test_order_basic():
    """Test that basic (not flagged) order produces correct output."""
    runner = CliRunner()
    result = runner.invoke(order, ['pepperoni'])

    expected_output = ['\U0001F373' + 'Приготовили', 'мин!\n']

    out = result.output
    try:
        # Split output to strip from x minutes, produced by random function (to not depend on "seed")
        out = out.split(' за ')
        out[1] = out[1].split(' ')[1]
    except IndexError:
        # If split is unsuccessful, then error in function => test is not passed
        raise AssertionError(f'expected: "\U0001F373Приготовили за x мин!", got: {out}')

    assert out == expected_output, f'expected: "\U0001F373Приготовили за x мин!", got: {out}'


def test_order_delivery():
    """Test that order with delivery produces correct output."""
    runner = CliRunner()
    result = runner.invoke(order, ['pepperoni', '--delivery'])

    expected_output = ['\U0001F373' + 'Приготовили', 'мин!', '\U0001F69A' + 'Доставили', 'мин!']

    # Inner function for splitting a line
    def split_line(line):
        line = line.split(' за ')
        line[1] = line[1].split(' ')[1]
        return line

    out = result.output
    lines = out.split('\n')
    try:
        # Split output by lines, then strip each from x minutes, produced by random function (to not depend on "seed")
        out = sum([split_line(line) for line in lines[:-1]], [])
    except IndexError:
        # If split is unsuccessful, then error in function => test is not passed
        raise AssertionError(f'expected: "\U0001F373Приготовили за x мин!\n\U0001F69AДоставили за x мин!", '
                             f'got: {out}')

    assert out == expected_output, f'expected: "\U0001F373Приготовили за x мин!\n\U0001F69AДоставили за x мин!", ' \
                                   f'got: {out}'


def test_menu_delivery():
    """Test that menu produces correct output."""
    runner = CliRunner()
    result = runner.invoke(menu)

    expected_output = ['- Margherita 🧀: tomato sauce, mozzarella, tomatoes',
                       '- Pepperoni 🍕: tomato sauce, mozzarella, pepperoni',
                       '- Hawaiian 🍍: tomato sauce, mozzarella, chicken, pineapples']

    out = result.output

    # Split by lines, drop the last (empty)
    out = out.split('\n')[:-1]

    assert out == expected_output, f'expected: {expected_output}, got: {out}'
