# This is an example showing how to use the ns-3 SimulationExecutionManager to
# get from compilation to result visualization.

# Plots thoughput vs time for different tcp-variants using wifi-tcp.cc

import sem
import os
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():

    script = 'wifi-tcp'
    ns_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ns-3')
    campaign_dir = "/tmp/sem-test/wifi-tcp"

    campaign = sem.CampaignManager.new(ns_path, script, campaign_dir,
                                       runner_type='ParallelRunner',
                                       overwrite=True)

    print(campaign) 

    ###################
    # Run simulations #
    ###################


    params = {
        'payloadSize': [1472],
        'dataRate': ['100Mbps'],
        'tcpVariant': ['TcpNewReno','TcpWestwood','TcpLinuxReno'],
        'phyRate': ['HtMcs7'],
        'simulationTime': [10],
        'pcap': [False],
    }
    runs = 1  
    
    campaign.run_missing_simulations(
        sem.list_param_combinations(params),
        runs=runs)

    ##################################
    # Exporting and plotting results #
    ##################################
    # Create a folder for the figures
    figure_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'figures')
    if not os.path.isdir(figure_path):
        os.makedirs(figure_path)


    def get_throughput(result):
        stdout = result['output']['stdout']
        lines = stdout.split('\n')
        ret_dir = {}
        for line in lines:
            if (len(line.split())==3):
                ret_dir[line.split('s')[0]] = line.split()[1]
        return ret_dir

    # Reduce multiple runs to a single value (or tuple)
    results = campaign.get_results_as_xarray(params,
                                             get_throughput,
                                             'Throughput', runs)

    # We can then visualize the object that is returned by the function
    print(results)

    timeList = []

    plt.figure(figsize=[35,25], dpi=300)
    for tcp in params['tcpVariant']:
        result = results.sel(tcpVariant=tcp).stack(st_params=('phyRate','simulationTime','payloadSize','dataRate','pcap','runs'))
        dic = result.to_dict(data=True)
        plot_list = []

        if not timeList:
            for k,v in dic['data'][0].items():
                timeList.append(k)
        
        for k,v in dic['data'][0].items():
            plot_list.append(v)
        plt.plot(timeList,plot_list,label = "TCP: %s"%tcp)
    plt.legend()
    plt.savefig(os.path.join(figure_path, 'throughputComparison.png'))

if __name__ == "__main__":
    main()
