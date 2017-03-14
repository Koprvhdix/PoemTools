# coding: utf-8

from loadPingShuiYun import LoadPingShuiYun


if __name__ == '__main__':
    pingshuiyun_dict = LoadPingShuiYun().pingshuiyun_dict
    print(pingshuiyun_dict['吴'])
    print(pingshuiyun_dict['凯'])
    print(pingshuiyun_dict['床'])
    print(pingshuiyun_dict['前'])
    print(pingshuiyun_dict['明'])
    print(pingshuiyun_dict['月'])
    print(pingshuiyun_dict['光'])

    # the characters has more pronunciation
    for key in pingshuiyun_dict:
        if len(pingshuiyun_dict[key]) > 1:
            print(key)
            print(pingshuiyun_dict[key])
