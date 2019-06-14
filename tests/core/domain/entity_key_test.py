import pytest

from gumo.core.domain.entity_key import KeyPair
from gumo.core.domain.entity_key import NoneKey
from gumo.core.domain.entity_key import EntityKey
from gumo.core.domain.entity_key import EntityKeyFactory


class TestKeyPair:
    def test_invalid_name(self):
        with pytest.raises(ValueError, match='kind must be an instance of str,'):
            KeyPair(kind=12345, name='name')
        with pytest.raises(ValueError, match='name must be an instance of str or int'):
            KeyPair(kind='Kind', name={'key': 'value'})


class TestKeyPairWithStr:
    key_pair = KeyPair(kind='Kind', name='name')

    def test_valid_name(self):
        assert isinstance(self.key_pair, KeyPair)
        assert self.key_pair == KeyPair(kind='Kind', name='name')

        assert self.key_pair.is_name()
        assert not self.key_pair.is_id()

    def test_invalid_kind_or_name(self):
        with pytest.raises(ValueError, match='do not include quotes'):
            KeyPair(kind='Kind', name='name"')

        with pytest.raises(ValueError, match='do not include quotes'):
            KeyPair(kind='Kind', name="name'with-single-quote")

        with pytest.raises(ValueError, match='do not include quotes'):
            KeyPair(kind='Kind"with-double-quote', name='name')

        with pytest.raises(ValueError, match='do not include quotes'):
            KeyPair(kind="Kind-with-'single-quote", name='name')

    def test_key_pair_literal(self):
        assert self.key_pair.key_pair_literal() == "'Kind', 'name'"


class TestKeyPairWithID:
    id_key_pair = KeyPair(kind='Kind', name=1234567)

    def test_valid_name_int(self):
        assert isinstance(self.id_key_pair, KeyPair)
        assert self.id_key_pair == KeyPair(kind='Kind', name=self.id_key_pair.name)
        assert self.id_key_pair != KeyPair(kind='Kind', name=str(self.id_key_pair.name))

        assert self.id_key_pair.is_id()
        assert not self.id_key_pair.is_name()

    def test_key_pair_literal(self):
        assert self.id_key_pair.key_pair_literal() == "'Kind', 1234567"

    def test_build_implicit_id_str_convert(self):
        assert KeyPair(kind='Kind', name=12345) == KeyPair.build(kind='Kind', name='12345', implicit_id_str=True)
        assert KeyPair(kind='Kind', name=12345) != KeyPair.build(kind='Kind', name='12345', implicit_id_str=False)

        assert KeyPair.build(kind='Kind', name='1234567').key_pair_literal() == "'Kind', 1234567"


class TestNoneKey:
    def test_eq_none(self):
        assert NoneKey() == NoneKey()

    def test_parent(self):
        assert NoneKey().parent() == NoneKey()
        assert not NoneKey().has_parent()

    def test_values(self):
        o = NoneKey()

        assert o.kind() is None
        assert o.name() is None
        assert o.flat_pairs() == []
        assert o.pairs() == []

        assert o.key_literal() is None
        assert o.key_path() is None
        assert o.key_path_urlsafe() is None


class TestEntityKeyWithStringName:
    factory = EntityKeyFactory()
    sample_key_pairs = [
        ('Book', 'name'),
        ('BookComment', 'comment'),
    ]

    def test_zero_length_pairs(self):
        with pytest.raises(ValueError):
            self.factory.build_from_pairs(pairs=[])

    def test_pairs_to_key(self):
        key = self.factory.build_from_pairs(pairs=self.sample_key_pairs)
        assert isinstance(key, EntityKey)
        assert len(key.pairs()) == 2
        assert key.kind() == 'BookComment'
        assert key.name() == 'comment'
        assert key.has_parent()

        parent = key.parent()
        assert isinstance(parent, EntityKey)
        assert len(parent.pairs()) == 1
        assert parent.kind() == 'Book'
        assert parent.name() == 'name'
        assert not parent.has_parent()

        none = parent.parent()
        assert isinstance(none, NoneKey)
        assert len(none.pairs()) == 0
        assert none.kind() is None
        assert none.name() is None
        assert none.parent() == none

    def test_dict_pairs_to_key(self):
        key = self.factory.build_from_pairs(pairs=[
            {'kind': 'Book', 'name': 'name'},
            {'kind': 'BookComment', 'name': 'comment'},
        ])
        assert isinstance(key, EntityKey)
        assert key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']

    def test_flat_pairs(self):
        key = self.factory.build_from_pairs(pairs=self.sample_key_pairs)
        assert key.flat_pairs() == ['Book', 'name', 'BookComment', 'comment']

    def test_build(self):
        key = EntityKeyFactory().build(kind='Book', name='name')
        assert key.kind() == 'Book'
        assert key.name() == 'name'
        assert isinstance(key.parent(), NoneKey)

    def test_build_for_new(self):
        key = self.factory.build_for_new(kind='Book')
        assert key.kind() == 'Book'
        assert isinstance(key.name(), str)
        assert len(key.name()) == 26
        assert isinstance(key.parent(), NoneKey)

    def test_entity_key_literal(self):
        key = self.factory.build(kind='Book', name='name')
        assert key.key_literal() == "Key('Book', 'name')"

    def test_entity_key_path(self):
        key = self.factory.build(kind='Book', name='name')
        child = self.factory.build(kind='Comment', name='comment', parent=key)

        assert key.key_path() == 'Book:name'
        assert key.key_path_urlsafe() == 'Book%3Aname'
        assert child.key_path() == 'Book:name/Comment:comment'
        assert child.key_path_urlsafe() == 'Book%3Aname%2FComment%3Acomment'

        assert self.factory.build_from_key_path(key.key_path()) == key
        assert self.factory.build_from_key_path(key.key_path_urlsafe()) == key
        assert self.factory.build_from_key_path(child.key_path()) == child
        assert self.factory.build_from_key_path(child.key_path_urlsafe()) == child

    def test_entity_key_url(self):
        key = self.factory.build(kind='Book', name='name')
        child = self.factory.build(kind='Comment', name='comment', parent=key)

        assert key.key_url() == 'Book/name'
        assert child.key_url() == 'Book/name/Comment/comment'

        assert self.factory.build_from_key_url(key.key_url()) == key
        assert self.factory.build_from_key_url(child.key_url()) == child


class TestEntityKeyWithIntID:
    factory = EntityKeyFactory()
    sample_key_pairs = [
        ('Book', 1234567890),
        ('BookComment', 9991234567890999)
    ]

    def test_pairs_to_key(self):
        key = self.factory.build_from_pairs(pairs=self.sample_key_pairs)
        assert isinstance(key, EntityKey)
        assert len(key.pairs()) == 2
        assert key.kind() == 'BookComment'
        assert key.name() == 9991234567890999

        parent = key.parent()
        assert isinstance(parent, EntityKey)
        assert len(parent.pairs()) == 1
        assert parent.kind() == 'Book'
        assert parent.name() == 1234567890

        grand_parent = parent.parent()
        assert isinstance(grand_parent, NoneKey)
        assert grand_parent == NoneKey()

    def test_entity_key_literal(self):
        key = self.factory.build_from_pairs(pairs=self.sample_key_pairs)
        assert key.key_literal() == "Key('Book', 1234567890, 'BookComment', 9991234567890999)"

    def test_entity_key_path(self):
        key = self.factory.build_from_pairs(pairs=self.sample_key_pairs)
        assert key.key_path() == 'Book:1234567890/BookComment:9991234567890999'
        assert key.key_path_urlsafe() == 'Book%3A1234567890%2FBookComment%3A9991234567890999'

        assert self.factory.build_from_key_path(key.key_path()) == key
        assert self.factory.build_from_key_path(key.key_path_urlsafe()) == key

    def test_entity_key_url(self):
        key = self.factory.build_from_pairs(pairs=self.sample_key_pairs)
        assert key.key_url() == 'Book/1234567890/BookComment/9991234567890999'

        assert self.factory.build_from_key_url(key_url=key.key_url()) == key
