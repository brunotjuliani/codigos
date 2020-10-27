import spotpy                                                # Load the SPOT package into your working storage
from spotpy import analyser                                  # Load the Plotting extension
from spotpy.examples.spot_setup_rosenbrock import spot_setup # Import the two dimensional Rosenbrock example

help(spot_setup)

# Give Monte Carlo algorithm the example setup and saves results in a RosenMC.csv file
sampler = spotpy.algorithms.mc(spot_setup(), dbname='RosenMC', dbformat='csv')

sampler.sample(100000)                # Sample 100.000 parameter combinations
results=sampler.getdata()             # Get the results of the sampler

spotpy.analyser.plot_parameterInteraction(results)     # Use the analyser to show the parameter interaction

posterior=spotpy.analyser.get_posterior(results, percentage=10)
spotpy.analyser.plot_parameterInteraction(posterior)

print(spotpy.analyser.get_best_parameterset(results))
