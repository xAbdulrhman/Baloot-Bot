class Pack(list):
    def __init__(self):
        list.__init__(self)

    def __repr__(self):
        ReprOut = ''
        for i, Card in enumerate(self):
            ReprOut += '{!r}: {!r}\n'.format(i, Card)
        return ReprOut

    def __str__(self):
        if self == []:
            return ''
        ReprOut = ''
        for i, Card in enumerate(self):
            ReprOut += '{!r:>01}: {!s}\n'.format(i, Card)
        return ReprOut