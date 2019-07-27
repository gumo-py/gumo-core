from typing import List
from typing import Union
from typing import Optional

import copy
import base64
import uuid

from gumo.core.domain.entity_key.key import EntityKey
from gumo.core.domain.entity_key.key import KeyPair
from gumo.core.domain.entity_key.key import NoneKey  # noqa: F401
from gumo.core.domain.entity_key.key import IncompleteKey


class EntityKeyFactory:
    def __init__(self):
        pass

    def build_from_pairs(self, pairs: List[Union[tuple, dict, KeyPair]]) -> EntityKey:
        key = None

        if len(pairs) == 0:
            raise ValueError('pairs must have at least one element.')

        for pair in pairs:
            if isinstance(pair, dict):
                key_pair = KeyPair.build_from_dict(doc=pair)
            elif isinstance(pair, tuple) or isinstance(pair, list):
                key_pair = KeyPair(pair[0], pair[1])
            elif isinstance(pair, KeyPair):
                key_pair = pair
            else:
                raise ValueError(f'Unknown object type: {type(pair)}, got: {pair}')

            key = EntityKey(
                _kind=key_pair.kind,
                _name=key_pair.name,
                _parent=key
            )

        return key

    def build(self, kind: str, name: Union[str, int], parent: Optional[EntityKey] = None) -> EntityKey:
        return EntityKey(
            _kind=kind,
            _name=name,
            _parent=parent
        )

    def build_incomplete_key(self, kind: str, parent: Optional[EntityKey] = None) -> IncompleteKey:
        return IncompleteKey(kind=kind, parent=parent)

    def build_for_new(self, kind: str, parent: Optional[EntityKey] = None) -> EntityKey:
        """(deprecated) Please use gumo.core.application.EntityKeyGenerator."""
        name = self._generate_new_uuid()
        return self.build(kind=kind, name=name, parent=parent)

    def _generate_new_uuid(self) -> str:
        s = base64.b32encode(uuid.uuid4().bytes).decode('utf-8')
        return s.replace('======', '').lower()

    def build_from_key_path(self, key_path: str) -> EntityKey:
        pairs = []
        for pair in key_path.replace('%2F', '/').replace('%3A', ':').split('/'):
            kind, name = pair.split(':')
            pairs.append(KeyPair.build(kind=kind, name=name, implicit_id_str=True))

        return self.build_from_pairs(pairs=pairs)

    @staticmethod
    def _split_list(l, n):
        """
        list divided by n items.
        :param l: list
        :param n: item size of sub-list
        :return:
        """
        for idx in range(0, len(l), n):
            yield l[idx:idx + n]

    def build_from_key_url(self, key_url: str) -> EntityKey:
        pairs = []

        key_elements = key_url.replace('%2F', '/').split('/')
        key_pairs = list(self._split_list(key_elements, 2))

        for pair in key_pairs:
            kind, name = pair
            pairs.append(KeyPair.build(kind=kind, name=name, implicit_id_str=True))

        return self.build_from_pairs(pairs=pairs)
