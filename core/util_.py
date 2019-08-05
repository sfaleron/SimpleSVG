
# the old way still feels like it could be better..
# also, path elements are not handled.

class KeywordToAttr(object):
    __slots__ = ()
    def __init__(self, **kw):
        for k,v in kw.items():
            setattr(self, k, v)

class AttrSerializer(KeywordToAttr):
    __slots__ = ( 'priority', 'chain', 'longDesc',
        'shortDesc', 'predicate', 'transformer' )

_serializers = []

def add_attrSerializer(shortDesc, predicate, transformer,
    priority=0.0, chain=False, longDesc=None):

    _serializers.append(AttrSerializer(
        shortDesc=shortDesc, predicate=predicate, transformer=transformer,
        priority=priority, chain=chain, longDesc=longDesc ))
