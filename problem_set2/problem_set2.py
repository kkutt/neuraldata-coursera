#
#  NAME
#    problem_set2_solutions.py
#
#  DESCRIPTION
#    Open, view, and analyze action potentials recorded during a behavioral
#    task.  In Problem Set 2, you will write create and test your own code to
#    create tuning curves.
#

#Helper code to import some functions we will use
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as mlab
from scipy import optimize
from scipy import stats


def load_experiment(filename):
    """
    load_experiment takes the file name and reads in the data.  It returns a
    two-dimensional array, with the first column containing the direction of
    motion for the trial, and the second column giving you the time the
    animal began movement during thaht trial.
    """
    data = np.load(filename)[()];
    return np.array(data)

def load_neuraldata(filename):
    """
    load_neuraldata takes the file name and reads in the data for that neuron.
    It returns an arary of spike times.
    """
    data = np.load(filename)[()];
    return np.array(data)
    
def bin_spikes(trials, spk_times, time_bin):
    """
    bin_spikes takes the trials array (with directions and times) and the spk_times
    array with spike times and returns the average firing rate for each of the
    eight directions of motion, as calculated within a time_bin before and after
    the trial time (time_bin should be given in seconds).  For example,
    time_bin = .1 will count the spikes from 100ms before to 100ms after the 
    trial began.
    
    dir_rates should be an 8x2 array with the first column containing the directions
    (in degrees from 0-360) and the second column containing the average firing rate
    for each direction
    """
    
    spikes_per_trials = np.zeros( ( np.size(trials,0), np.size(trials,1) ) )
    dir_rates = np.column_stack( ( np.arange(0,360,45), np.zeros(8) ) )
    
    for i in range(np.size(trials,0)):
        i_time = trials[i,1] 
        spikes_per_trials[i] = ( trials[i,0] , np.count_nonzero(np.logical_and(spk_times>i_time-time_bin,spk_times<i_time+time_bin)) )
    
    for dir_i in np.arange(0,360,45):
        sum_for_dir = np.sum(spikes_per_trials[:,1] * (spikes_per_trials[:,0] == dir_i))
        avg_for_dir = sum_for_dir / np.count_nonzero(spikes_per_trials[:,0] == dir_i)
        dir_rate = avg_for_dir / (2 * time_bin)
        dir_rates[ np.where(dir_rates == dir_i)[0][0] ,1] = dir_rate
    
    return dir_rates
    
def plot_tuning_curves(direction_rates, title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates) and plots a histogram and 
    polar representation of the tuning curve. It adds the given title.
    """
    
    #plots
    plt.figure()
    plt.subplot(2,2,1)
    plt.bar(direction_rates[:,0], direction_rates[:,1], width=45, align='center')
    plt.xlim(-22.5,337.5)
    plt.xticks( direction_rates[:,0] )
    plt.xlabel('Direction of Motion [degrees]')
    plt.ylabel('Firing rate [spikes/s]')
    plt.title(title)
    
    plt.subplot(2,2,2,polar=True)
    plt.polar( np.deg2rad( direction_rates[:,0] ), direction_rates[:,1], label='Firing rate [spikes/s]', color='blue' )
    plt.polar( np.deg2rad( np.roll(direction_rates[:,0],1) ), np.roll(direction_rates[:,1],1), color='blue')
    plt.legend(loc=8)
    plt.title(title)

    
def roll_axes(direction_rates):
    """
    roll_axes takes the x-values (directions) and y-values (direction_rates)
    and return new x and y values that have been "rolled" to put the maximum
    direction_rate in the center of the curve. The first and last y-value in the
    returned list should be set to be the same. (See problem set directions)
    Hint: Use np.roll()
    """
   
    
    return new_xs, new_ys, roll_degrees    
    

def normal_fit(x,mu, sigma, A):
    """
    This creates a normal curve over the values in x with mean mu and
    variance sigma.  It is scaled up to height A.
    """
    n = A*mlab.normpdf(x,mu,sigma)
    return n

def fit_tuning_curve(centered_x,centered_y):
    """
    This takes our rolled curve, generates the guesses for the fit function,
    and runs the fit.  It returns the parameters to generate the curve.
    """

    return p
    


def plot_fits(direction_rates,fit_curve,title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates and fit_curve) and plots the 
    actual values with circles, and the curves as lines in both linear and 
    polar plots.
    """
    

def von_mises_fitfunc(x, A, kappa, l, s):
    """
    This creates a scaled Von Mises distrubition.
    """
    return A*stats.vonmises.pdf(x, kappa, loc=l, scale=s)


    
def preferred_direction(fit_curve):
    """
    The function takes a 2-dimensional array with the x-values of the fit curve
    in the first column and the y-values of the fit curve in the second.  
    It returns the preferred direction of the neuron (in degrees).
    """
  
    return pd
    
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    trials = load_experiment('trials.npy')   
    spk_times = load_neuraldata('neuron3.npy')
    time_bin = 0.1
    dir_rates = bin_spikes(trials, spk_times, time_bin)
    
    plot_tuning_curves(dir_rates, 'Neuron 3 Tuning Curve')

    plt.show()

