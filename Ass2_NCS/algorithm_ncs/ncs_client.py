import json

from algorithm_ncs import ncs_c as ncs
import argparse
import time

parser = argparse.ArgumentParser(description="This is a NCS solver")
parser.add_argument("-c", "--config", default="algorithm_ncs/parameter.json", type=str, help="a json file that contains parameter")
parser.add_argument("-d", "--data", default="6", type=int, help="the problem dataset that need to be solved")
args = parser.parse_args()

"""
how to use it?
example:
    python3 -m algorithm_ncs.ncs_client -d 12 -c algorithm_ncs/parameter.json
    
good luck!
"""
if __name__ == '__main__':
    config_file = args.config
    p = args.data
    with open(config_file) as file:
        try:
            ncs_para = json.loads(file.read())
        except:
            raise Exception("not a json format file")

    _lambda = ncs_para["lambda"]
    r = ncs_para["r"]
    epoch = ncs_para["epoch"]
    n = ncs_para["n"]
    ncs_para = ncs.NCS_CParameter(tmax=300000, lambda_exp=_lambda, r=r, epoch=epoch, N=n)
    begin = time.time()
    print("************ start problem %d **********" % p)
    ncs_c = ncs.NCS_C(ncs_para, p)
    ncs_res = ncs_c.loop(quiet=False, seeds=0)
    print(ncs_res)
    cost_of_time=time.time() - begin
    print("time cost is {}".format(cost_of_time))
    store_datas_name = "store_datas_{}.txt".format(str(p))
    store_datas_name_2 = "store_datas_{}_copy.txt".format(str(p))
    store_datas = open(store_datas_name,mode="a+")
    store_datas_2 = open(store_datas_name_2,mode="a+")
    store_datas.writelines("\"lambda\":{},\"r\":{},\"epoch\":{},\"n\":{},cost_time={},result={}\r\n".format(\
    _lambda,r,epoch,n,cost_of_time,ncs_res))
    store_datas_2.writelines("\"lambda\":{},\"r\":{},\"epoch\":{},\"n\":{},cost_time={},result={}\r\n".format(\
    _lambda,r,epoch,n,cost_of_time,ncs_res))
    store_datas.close()
    store_datas_2.close()