"""
create on 17-03-14
@author: Koprvhdix
"""


class LoadPingShuiYun(object):
    """ Load PingShuiYun file for rhyming and tonal pattern.
    It only remove the blank line and tab.
    """

    def __init__(self):
        pingshuiyun_path = 'PingShuiYun'
        open_pingshuiyun_file = open(pingshuiyun_path, "r", encoding="utf8")
        pingshuiyun_all_lines = open_pingshuiyun_file.readlines()

        self.pingshuiyun_dict = dict()

        # P and Z
        tonal = 0
        rhyming = 0

        for line in pingshuiyun_all_lines:
            if len(line) == 3:
                tonal += 1
                continue
            if len(line) < 10:
                rhyming += 1
                continue
            not_stop = True
            for character in line[:-1]:
                # delete noise
                if character == '<' or character == '[':
                    not_stop = False
                elif character == '>' or character == ']':
                    not_stop = True
                    continue

                if not_stop:
                    if character not in self.pingshuiyun_dict:
                        self.pingshuiyun_dict[character] = list()
                    self.pingshuiyun_dict[character].append(['P' if tonal < 3 else 'Z', rhyming])
