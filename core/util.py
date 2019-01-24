
def unexpression_adder(appendable):
    def dec(unexpression):
        appendable.append(unexpression.__name__)
        return unexpression

    return appendable, dec

def pairfmt(pair):
    return '{},{}'.format(*pair)

def pairsfmt(pairs):
    return ' '.join(map(pairfmt, pairs))

def attrs_to_xml(dct):
    return ' '.join(['{}="{}"'.format(k, int(v) if
        isinstance(v, bool) else v) for k,v in dct.items()])
