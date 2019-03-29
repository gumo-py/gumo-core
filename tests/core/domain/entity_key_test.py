import pytest

from gumo.core.domain.entity_key import NoneKey
from gumo.core.domain.entity_key import EntityKey
from gumo.core.domain.entity_key import EntityKeyFactory

sample_key_pairs = [
    ('Book', 'name'),
    ('BookComment', 'comment'),
]


def test_zero_length_pairs():
    with pytest.raises(ValueError):
        EntityKeyFactory().build_from_pairs(pairs=[])


def test_pairs_to_key():
    key = EntityKeyFactory().build_from_pairs(pairs=sample_key_pairs)
    assert isinstance(key, EntityKey)
    assert len(key.pairs()) == 2
    assert key.kind() == 'BookComment'
    assert key.name() == 'comment'

    parent = key.parent()
    assert isinstance(parent, EntityKey)
    assert len(parent.pairs()) == 1
    assert parent.kind() == 'Book'
    assert parent.name() == 'name'

    none = parent.parent()
    assert isinstance(none, NoneKey)
    assert len(none.pairs()) == 0
    assert none.kind() is None
    assert none.name() is None
    assert none.parent() == none


def test_dict_pairs_to_key():
    key = EntityKeyFactory().build_from_pairs(pairs=[
        {'kind': 'Book', 'name': 'name'},
        {'kind': 'BookComment', 'name': 'comment'},
    ])
    assert isinstance(key, EntityKey)
    assert key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']


def test_flat_pairs():
    key = EntityKeyFactory().build_from_pairs(pairs=sample_key_pairs)
    assert key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']


def test_build():
    key = EntityKeyFactory().build(kind='Book', name='name')
    assert key.kind() == 'Book'
    assert key.name() == 'name'
    assert isinstance(key.parent(), NoneKey)


def test_build_for_new():
    key = EntityKeyFactory().build_for_new(kind='Book')
    assert key.kind() == 'Book'
    assert isinstance(key.name(), str)
    assert len(key.name()) == 26
    assert isinstance(key.parent(), NoneKey)


def test_entity_key_literal():
    key = EntityKeyFactory().build(kind='Book', name='name')
    assert key.key_literal() == "Key('Book', 'name')"


def test_entity_key_path():
    factory = EntityKeyFactory()
    key = factory.build(kind='Book', name='name')
    child = factory.build(kind='Comment', name='comment', parent=key)

    assert key.key_path() == 'Book:name'
    assert key.key_path_urlsafe() == 'Book%3Aname'
    assert child.key_path() == 'Book:name/Comment:comment'
    assert child.key_path_urlsafe() == 'Book%3Aname%2FComment%3Acomment'

    assert factory.build_from_key_path(key.key_path()) == key
    assert factory.build_from_key_path(key.key_path_urlsafe()) == key
    assert factory.build_from_key_path(child.key_path()) == child
    assert factory.build_from_key_path(child.key_path_urlsafe()) == child


def test_none_key_eq():
    key1 = NoneKey()
    key2 = NoneKey()

    assert key1 == key2
