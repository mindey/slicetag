import re

class Slicer(object):

    def __init__(self, content=''):
        self.content = content
        self.slices = []

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content

    def parse_cutouts(self, ret=False):
        '''
            Returns a list of cutouts from text. Cutout here is defined
		    as a string starting with {: and and a matching :} in top level of nesting.

			Simple approach doesn't work:

            >>> def re_show(pat, s):
                    print(re.compile(pat, re.M).sub("[\g<0>]", s.rstrip()))
            >>> re_show('{:(.*?):}','Hel{:Wonderful:}rld. And world {:two {: ha :} worlds:}.')

			Wrong: Hel[{:Wonderful:}]rld. And world [{:two {: ha :}] worlds:}.

            The current approach works for me:

            >>> s = Slicer('Hel{:Wonderful:}rld. And world {:two {: ha :} worlds:}.')
            >>> s.parse_cutouts()
            >>> s.slices

            Right: ['{:Wonderful:}', '{:two {: ha :} worlds:}']

        '''
        count = 0
        start = False
        result = []
        findall = lambda x, symbol: [content.start() for content in list(re.finditer(symbol, x))]

        for i in sorted(findall(self.content,'{:') + findall(self.content,':}')):
            if self.content[i:i+2] == '{:':
                count += 1
            if self.content[i:i+2] == ':}':
                count += -1
            if not start and count == 1:
                start = i
            if count == 0:
                result.append(self.content[start:i]+':}')
                start = False

        self.slices = result

        if ret:
            return result
