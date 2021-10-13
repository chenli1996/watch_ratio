import json
from easydict import EasyDict
import os
import _pickle as cp
# import cPickle as cp
from os import listdir


def get_config_from_json(json_file):
    """
    Get the config from a json file
    :param json_file:
    :return: config(namespace) or config(dictionary)
    """
    # parse the configurations from the config json file provided
    with open(json_file, 'rb') as config_file:
        config_dict = json.load(config_file)

    # convert the dictionary to a namespace using bunch lib
    config = EasyDict(config_dict)

    return config, config_dict

def choose_group(data_dir):
    config, _ = get_config_from_json("../configs/config_RL.json")
    filename = data_dir + 'target_group.txt'
    if os.path.exists(filename):
        ff = open(filename,'rb')
        return ff.readlines()[0]
    else:
        f = sorted(os.listdir(data_dir))[0]
        with open(data_dir + f, 'rb') as infile:
            reqlist = cp.load(infile,encoding='utf-8')
        d = {}
        length = len(reqlist)
        for i,req in enumerate(reqlist):
            print("count and choose:",i, length)
            if req[1][:config.PREFIX] not in d:
                d[req[1][:config.PREFIX]] = 1
            else:
                d[req[1][:config.PREFIX]] += 1

        # target_group = sorted(d.items(), key=lambda x: x[1])[-1][0]
        target_group = sorted(d.items(), key=lambda x: x[1],reverse=True)
        for pair in target_group:
            print(pair)
        # print (target_group)
        # ff = open(filename,'wb')
        # ff.write(target_group)
        # choose group with most reqs in first day
        return target_group
def choose_group_from_txt(data_dir):
    # config, _ = get_config_from_json("../configs/config_RL.json")
    config_PREFIX = 18
    filename = data_dir + str(config_PREFIX)+'target_group.txt'
    if os.path.exists(filename):
        ff = open(filename,'rb')
        return ff.readlines()[0]
    else:
        f = sorted(os.listdir(data_dir))[0]
        with open(data_dir + f, 'r') as infile:
            reqlist = infile.readlines()
            reqlist.sort()
            # reqlist = cp.load(infile,encoding='utf-8')
        d = {}
        length = len(reqlist)
        for i,req in enumerate(reqlist):
            req = req.split('\t')
            print("count and choose:",i, length)
            if req[1][:config_PREFIX] not in d:
                d[req[1][:config_PREFIX]] = 1
            else:
                d[req[1][:config_PREFIX]] += 1

        # target_group = sorted(d.items(), key=lambda x: x[1])[-1][0]
        target_group = sorted(d.items(), key=lambda x: x[1],reverse=True)
        ff = open(filename, 'w')

        for pair in target_group:
            print(pair)
            ff.write(str(pair))
            ff.write('\n')

        # print (target_group)

        # choose group with most reqs in first day
        return target_group
def index_contents(dir):
    in_dir = '../data/req/'
    out_dir = '../data/req_index/'
    index = 0
    d = {}

    for f in sorted(listdir(in_dir)):
        if not f.endswith('cp'):
            continue
        with open(in_dir + f, 'rb') as infile:
            reqlist = cp.load(infile)

        req_list_indexed = []
        cnt = 0
        total = len(reqlist)
        for req in reqlist:
            cnt += 1
            print('indexing contents : ' + str(cnt) + '/'+str(total))
            if req[2] not in d:
                d[req[2]] = index
                index += 1
            req_list_indexed.append([req[0], req[1], d[req[2]]])

        with open(out_dir + f, 'wb') as outfile:
            cp.dump(req_list_indexed, outfile)
    with open(out_dir + 'title_map.cp', 'wb') as outfile:
        cp.dump(d, outfile)


def get_subdataset(datadir):

    # config, _ = get_config_from_json("../configs/config_RL.json")
    #('01111011', 130796), ('11011110', 106591), ('01101111', 91989), ('00111011', 83750)

    # ('011101111111111100', 3051)
    # ('011101101101010000', 3043)
    # ('011110110111110100', 3042)

    # ('110010100110', 27969)
    # ('110111001011', 27177)
    # ('001110100001', 27025)

    prefix_ip = '00111011'
    output_filepath = '/home/chenli/research/caching/dataset/prefix/prefix8/sub4/'
    fp_list = sorted(os.listdir(datadir))
    for fp in fp_list:
        infile = open(datadir+fp,'rb')
        outfile = open(output_filepath+fp,'w')
        reqlist = cp.load(infile, encoding='utf-8')
        reqlist.sort()
        for req in reqlist:
            if req[1][:config_PREFIX] == prefix_ip:
                outfile.write(req[0])
                outfile.write('\t')
                outfile.write(req[1])
                outfile.write('\t')
                outfile.write(req[2])
                outfile.write('\n')
        print(fp)
        infile.close()
        outfile.close()


def get_subdataset_test(datadir):
    history = {}
    config, _ = get_config_from_json("../configs/config_RL.json")
    # ('01111011', 130796), ('11011110', 106591), ('01101111', 91989), ('00111011', 83750)
    prefix_ip = '011101111111111100'
    output_filepath = '/home/chenli/research/caching/dataset/'
    fp_list = sorted(os.listdir(datadir))
    for fp in fp_list:
        infile = open(datadir + fp, 'rb')
        outfile = open(output_filepath + fp, 'w')
        reqlist = cp.load(infile, encoding='utf-8')
        reqlist.sort()
        for req in reqlist:
            if req[1][:config.PREFIX] == prefix_ip:
                if req[2] not in history:
                    history[req[2]] = []
                else:
                    history[req[2]].append(req[0])
                outfile.write(req[0])
                outfile.write('\t')
                outfile.write(req[1])
                outfile.write('\t')
                outfile.write(req[2])
                outfile.write('\n')
        print(fp)
        infile.close()
        outfile.close()

if __name__ == '__main__':
    choose_group('/home/chenli/research/caching/dataset/req/day2to9/')
    # choose_group_from_txt('/home/chenli/research/caching/proactive/dataset/series_txt/')
    # get_subdataset('/home/chenli/research/caching/dataset/req/day2to9/')

