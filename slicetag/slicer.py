import re

class Slicer(object):

    def __init__(self, content=''):
        self.content = content
        self.cuts = []
        self.tree = []

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content

    def get_cuts(self, ret=False):
        '''
            Returns a list of cuts from text. A cut here is defined
            as a string starting with {: and and a matching :} in top level of nesting.

            Simple approach doesn't work:

            >>> import re
            >>> def re_show(pat, s):
                    print(re.compile(pat, re.M).sub("[\g<0>]", s.rstrip()))

            >>> re_show('{:(.*?):}','Hel{:Wonderful:}rld. And world {:two {: ha :} worlds:}.')

            Wrong: Hel[{:Wonderful:}]rld. And world [{:two {: ha :}] worlds:}.

            The current approach works for me:

            >>> s = Slicer('Hel{:Wonderful:}rld. And world {:two {: ha :} worlds:}.')
            >>> s.get_cuts()
            >>> s.slices

            Right: ['{:Wonderful:}', '{:two {: ha :} worlds:}']

        '''
        count = 0
        start = False

        findall = lambda x, symbol: [content.start() for content in list(re.finditer(symbol, x))]

        for i in sorted(findall(self.content,'{:') + findall(self.content,':}')):
            if self.content[i:i+2] == '{:':
                count += 1
            if self.content[i:i+2] == ':}':
                count += -1
            if not start and count == 1:
                start = i
            if count == 0:
                self.cuts.append(self.content[start:i]+':}')
                start = False

    def parse_cuts(self):
        '''
            A cut may have conditions, e.g., {:condition|content:}.
            This method makes a list of tuples from self.cuts: [(condition, content), ...].
        '''
        for ix, cut in enumerate(self.cuts):

            if '|' in cut and '{:' in cut and ':}' in cut:
                self.tree += [ (cut[2:cut.index('|')], cut[cut.index('|')+1:-2]) ]
            elif cut[:2] == '{:' and cut[-2:] == ':}':
                self.tree += [ (False, cut[2:-2]) ]
            else:
                self.tree += [ (False, False) ]
