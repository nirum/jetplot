"""
Tests for the capsules module

"""

from jetpack.capsules import FuzzyDict
from nose.tools import assert_raises


def generate_fruits():
    """Generates a FuzzyDict of fruits"""
    fruits = FuzzyDict(threshold=0.7)
    fruits['apple'] = 1
    fruits['banana'] = 2
    fruits['pear'] = 3
    return fruits


def test_fuzzydict():
    """Tests the fuzzydict class"""

    fruits = generate_fruits()

    # get set of keys
    keys = {'apple', 'banana', 'pear'}

    # number of elements
    assert len(fruits) == 3

    # keys match
    assert set(fruits.keys()) == keys

    # iterable
    for f in iter(fruits):
        assert f in keys

    # get a key (exact)
    assert fruits['apple'] == 1

    # get a key (fuzzy)
    assert fruits['banannna'] == 2
    assert fruits['bannna'] == 2
    assert fruits['abannna'] == 2
    assert fruits['per'] == 3
    assert fruits['peer'] == 3
    assert fruits['ear'] == 3
    assert fruits['pple'] == 1
    assert fruits['app'] == 1
    assert fruits['apale'] == 1

    # key not found
    for faulty_key in ('foo', 'bnnnaeaa', 'apeer', 'xyz'):
        with assert_raises(KeyError) as context:
            fruits[faulty_key]
            assert 'Match not found for ' + faulty_key in str(context.exception)

    # set a new key
    fruits['strawberry'] = 4
    assert len(fruits) == 4

    # check values
    for val in fruits.values():
        assert val in (1, 2, 3, 4)

    # update a key
    fruits['apple'] += 4
    assert fruits['apple'] == 5

    fruits['bnnana'] -= 1
    assert fruits['banana'] == 1

    fruits['peer'] = 'NULL'
    assert fruits['pear'] == 'NULL'

    # delete a key
    del fruits['peer']
    assert len(fruits) == 3
    for key in fruits:
        assert key in {'apple', 'banana', 'strawberry'}

    with assert_raises(KeyError) as context:
        del fruits['orange']
        assert 'Match not found for orange' in str(context.exception)
