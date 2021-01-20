# This is an example showing how to use the ns-3 SimulationExecutionManager to
# get from compilation to result visualization.

import sem
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Create the campaign #
#######################

script = 'wifi-multi-tos'
ns_path = 'ns-3'
campaign_dir = "/tmp/sem-test/wifi-plotting-example"

campaign = sem.CampaignManager.new(ns_path, script, campaign_dir,
                                   runner_type='ParallelRunner',
                                   max_parallel_processes=8)

print(campaign)  # This prints out the campaign settings

###################
# Run simulations #
###################

# These are the available parameters
# We specify each parameter as an array containing the desired values
params = {
    'nWifi': [1],  # Number of STAs
    'distance': list(range(0, 110, 10)),  # Distance from AP
    'useRts': [True],  # Enable RTS/CTS
    'useShortGuardInterval': [True],  # Use the short guard interval
    'mcs': list(range(0, 8, 2)),  # Modulation Coding Scheme to use
    'channelWidth': [20],  # Channel width
    'simulationTime': [4],  # How long to simulate for
}
runs = 10  # Number of runs to perform for each combination

# Actually run the simulations
# This will also print a progress bar
campaign.run_missing_simulations(params, runs=runs)

##################################
# Exporting and plotting results #
##################################

# We need to define a function to parse the results. This function will then be
# passed to get_results_as_dataframe, that will call it on every result it needs
# to export.
def get_average_throughput(result):
    if result['meta']['exitcode'] == 0:
        throughput = float(result['output']['stdout'].split(" ")[-2])
    else:
        throughput = 0
    return [throughput]
throughput_labels = ['Throughput']

# Use the parsing function to create a Pandas dataframe
results = campaign.get_results_as_dataframe(get_average_throughput,
                                            throughput_labels,
                                            drop_columns=True)

# Plot contents of the dataframe using Seaborn
sns.catplot(x='distance',
            y='Throughput',
            hue='mcs',
            data=results,
            kind='point')
plt.show()
