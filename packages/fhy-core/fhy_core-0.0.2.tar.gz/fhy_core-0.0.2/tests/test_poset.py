"""Tests the partially ordered set utility."""

import pytest
from fhy_core.utils.lattice import Lattice
from fhy_core.utils.poset import PartiallyOrderedSet


@pytest.fixture()
def basic_non_lattice_poset():
    lattice = Lattice[int]()
    lattice.add_element(1)
    lattice.add_element(2)
    lattice.add_element(3)
    lattice.add_element(4)
    lattice.add_order(1, 3)
    lattice.add_order(1, 4)
    lattice.add_order(2, 3)
    lattice.add_order(2, 4)
    return lattice


def test_basic_non_lattice_poset(basic_non_lattice_poset: Lattice[int]):
    """Test that a basic non-lattice poset is not a lattice."""
    assert basic_non_lattice_poset.is_lattice() is False


def test_basic_non_lattice_has_no_least_upper_bound(
    basic_non_lattice_poset: Lattice[int],
):
    """Test that a basic non-lattice poset has no least upper bound for certain
    elements.
    """
    with pytest.raises(RuntimeError):
        basic_non_lattice_poset.get_least_upper_bound(3, 4)


@pytest.fixture
def basic_poset():
    """Uses the PartiallyOrderedSet class internals to create a poset with two
    elements.

    poset: ({1, 2}, <=)

    """
    poset = PartiallyOrderedSet[int]()
    poset._graph.add_node(1)
    poset._graph.add_node(2)
    poset._graph.add_edge(1, 2)
    return poset


def test_empty_poset_length():
    """Test that an empty poset's length is correctly calculated."""
    poset = PartiallyOrderedSet[int]()

    assert len(poset) == 0


def test_poset_length(basic_poset):
    """Test that the poset's length is correctly calculated."""
    assert len(basic_poset) == 2


def test_element_not_in_empty_poset():
    """Test that an element is not in an empty poset."""
    poset = PartiallyOrderedSet[int]()

    assert 1 not in poset


def test_element_in_poset(basic_poset):
    """Test that an element is in the poset."""
    assert 1 in basic_poset


def test_poset_add_element():
    """Test that elements are correctly added to the poset."""
    poset = PartiallyOrderedSet[int]()
    poset.add_element(1)

    assert len(poset) == 1


def test_poset_add_duplicate_element():
    """Test that adding a duplicate element raises an error."""
    poset = PartiallyOrderedSet[int]()
    poset.add_element(1)

    with pytest.raises(ValueError):
        poset.add_element(1)


def test_poset_is_less_than(basic_poset):
    """Test that the is_less_than method correctly determines if one element is less
    than another.
    """
    assert basic_poset.is_less_than(1, 2)


def test_poset_is_less_than_with_invalid_lower_element(basic_poset):
    """Test that is_less_than raises an error when the lower element is not in the
    poset.
    """
    with pytest.raises(ValueError):
        basic_poset.is_less_than(3, 2)


def test_poset_is_less_than_with_invalid_upper_element(basic_poset):
    """Test that is_less_than raises an error when the upper element is not in the
    poset.
    """
    with pytest.raises(ValueError):
        basic_poset.is_less_than(1, 3)


def test_poset_is_greater_than(basic_poset):
    """Test that the is_greater_than method correctly determines if one element is
    greater than another.
    """
    assert basic_poset.is_greater_than(2, 1)


def test_poset_is_greater_than_with_invalid_lower_element(basic_poset):
    """Test that is_greater_than raises an error when the lower element is not in the
    poset.
    """
    with pytest.raises(ValueError):
        basic_poset.is_greater_than(3, 2)


def test_poset_is_greater_than_with_invalid_upper_element(basic_poset):
    """Test that is_greater_than raises an error when the upper element is not in the
    poset.
    """
    with pytest.raises(ValueError):
        basic_poset.is_greater_than(1, 3)


def test_poset_add_order(basic_poset):
    """Test that order relations are correctly added to the poset."""
    basic_poset.add_element(3)
    basic_poset.add_order(2, 3)

    assert basic_poset.is_less_than(2, 3)
    assert basic_poset.is_greater_than(3, 2)


def test_poset_add_order_with_invalid_lower_element(basic_poset):
    """Test that add_order raises an error when the lower element is not in the
    poset.
    """
    with pytest.raises(ValueError):
        basic_poset.add_order(3, 2)


def test_poset_add_order_with_invalid_upper_element(basic_poset):
    """Test that add_order raises an error when the upper element is not in the
    poset.
    """
    with pytest.raises(ValueError):
        basic_poset.add_order(1, 3)


def test_poset_invalid_order():
    """Test that an invalid order raises an error."""
    poset = PartiallyOrderedSet[int]()
    poset.add_element(1)
    poset.add_element(2)
    poset.add_order(1, 2)

    with pytest.raises(RuntimeError):
        poset.add_order(2, 1)


def test_poset_iter(basic_poset):
    """Test that the poset can be iterated over."""
    assert list(basic_poset) == [1, 2]
    assert list(basic_poset) == [1, 2], "Expected the poset to be iterable \
multiple times."
