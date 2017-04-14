#
#  NAME
#    problem_set4.py
#
#  DESCRIPTION
#    In Problem Set 4, you will classify EEG data into NREM sleep stages and
#    create spectrograms and hypnograms.
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m
from numpy import cumsum
from matplotlib.pyplot import xlabel
from __builtin__ import xrange


def load_examples(filename):
    """
    load_examples takes the file name and reads in the data.  It returns an
    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['examples'], int(data['srate'])

def load_eeg(filename):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['eeg'], int(data['srate'])

def load_stages(filename):
    """
    load_stages takes the file name and reads in the stages data.  It returns an
    array containing the correct stages (one for each 30s epoch)
    """
    data = np.load(filename)
    return data['stages']

def plot_example_psds(example,rate):
    """
    This function creates a figure with 4 lines to show the overall psd for 
    the four sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()
    
    labels = ['REM', 'NREM 1', 'NREM 2', 'NREM 3-4']
    
    ##YOUR CODE HERE
    for i in xrange(0,4):
        (Pxx, freqs) = m.psd(example[i], NFFT=256, Fs=rate)
        Pxx = Pxx / sum(Pxx)
        plt.plot(freqs, Pxx, hold=True, label=labels[i], lw=10)
    plt.yscale('log')
    plt.xlim( xmax = 20 )
    plt.legend()
    plt.show()
    
    return

def plot_example_spectrograms(example,rate):
    """
    This function creates a figure with spectrogram sublpots to of the four
    sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()
    
    labels = ['REM', 'NREM 1', 'NREM 2', 'NREM 3-4']
    
    ###YOUR CODE HERE
    for i in xrange(0,4):
        plt.subplot(2,2,i+1)
        plt.specgram(example[i], NFFT=256, Fs=rate, label=labels[i])
        plt.ylim( ymax = 30 )
        plt.legend()
    plt.show()
    
    return
      
            
def classify_epoch(epoch,rate):
    """
    This function returns a sleep stage classification (integers: 1 for NREM
    stage 1, 2 for NREM stage 2, and 3 for NREM stage 3/4) given an epoch of 
    EEG and a sampling rate.
    """
    
    ###YOUR CODE HERE
    (Pxx, freqs) = m.psd(epoch, NFFT=256, Fs=rate)
    Pxx = Pxx / sum(Pxx)
    
    stage = 1
    if sum(Pxx * ( ( freqs > 11 ) & ( freqs < 14 ) )) > sum(Pxx * ( ( freqs > 6.5 ) & ( freqs < 9.5 ) )):
        stage = 2
    elif sum(Pxx * ( ( freqs > 0 ) & ( freqs < 4 ) )) > 0.80:
        stage = 3
    #else:
    #    stage = 1
    
    return stage

def plot_hypnogram(eeg, stages, srate):
    """
    This function takes the eeg, the stages and sampling rate and draws a 
    hypnogram over the spectrogram of the data.
    """
    
    fig,ax1 = plt.subplots()  #Needed for the multiple y-axes
    
    #Use the specgram function to draw the spectrogram as usual
    ax1.specgram(eeg, NFFT=256, Fs=srate)

    #Label your x and y axes and set the y limits for the spectrogram
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_ylim(ymax=30)
    
    ax2 = ax1.twinx() #Necessary for multiple y-axes
    
    #Use ax2.plot to draw the hypnogram.  Be sure your x values are in seconds
    #HINT: Use drawstyle='steps' to allow step functions in your plot
    i = 0
    bin_size = 30*srate
    c = np.zeros(len(eeg)/bin_size)
    while i + bin_size < len(eeg):
        c[i/bin_size] = classify_epoch(eeg[range(i,i+bin_size)],srate)
        i = i + bin_size
    
    xx = range(0, c.size*30, 30)
    ax2.plot(xx,c, drawstyle='steps')
    ax2.set_xlim(xmax=3000)  #max=3000 for Test, max=3600 for Practice

    #Label your right y-axis and change the text color to match your plot
    ax2.set_ylabel('NREM Stage',color='b')
    ax2.set_ylim(0.5,3.5)
    
    #Set the limits for the y-axis 
    
    #Only display the possible values for the stages
    ax2.set_yticks(np.arange(1,4))
    
    #Change the left axis tick color to match your plot
    for t1 in ax2.get_yticklabels():
        t1.set_color('b')
    
    #Title your plot    
    plt.title('Hypnogram and Spectogram for Test Data')
    
    plt.show()

        
def classifier_tester(classifiedEEG, actualEEG):
    """
    returns percent of 30s epochs correctly classified
    """
    epochs = len(classifiedEEG)
    incorrect = np.nonzero(classifiedEEG-actualEEG)[0]
    percorrect = (epochs - len(incorrect))/epochs*100
    
    print 'EEG Classifier Performance: '
    print '     Correct Epochs = ' + str(epochs-len(incorrect))
    print '     Incorrect Epochs = ' + str(len(incorrect))
    print '     Percent Correct= ' + str(percorrect) 
    print 
    return percorrect
  
    
def test_examples(examples, srate):
    """
    This is one example of how you might write the code to test the provided 
    examples.
    """
    i = 0
    bin_size = 30*srate
    c = np.zeros((4,len(examples[1,:])/bin_size))
    while i + bin_size < len(examples[1,:]):
        for j in range(1,4):
            c[j,i/bin_size] = classify_epoch(examples[j,range(i,i+bin_size)],srate)
        i = i + bin_size
    
    totalcorrect = 0
    num_examples = 0
    for j in range(1,4):
        canswers = np.ones(len(c[j,:]))*j
        correct = classifier_tester(c[j,:],canswers)
        totalcorrect = totalcorrect + correct
        num_examples = num_examples + 1
    
    average_percent_correct = totalcorrect/num_examples
    print 'Average Percent Correct= ' + str(average_percent_correct) 
    return average_percent_correct

def classify_eeg(eeg,srate):
    """
    DO NOT MODIFY THIS FUNCTION
    classify_eeg takes an array of eeg amplitude values and a sampling rate and 
    breaks it into 30s epochs for classification with the classify_epoch function.
    It returns an array of the classified stages.
    """
    bin_size_sec = 30
    bin_size_samp = bin_size_sec*srate
    t = 0
    classified = np.zeros(len(eeg)/bin_size_samp)
    while t + bin_size_samp < len(eeg):
       classified[t/bin_size_samp] = classify_epoch(eeg[range(t,t+bin_size_samp)],srate)
       t = t + bin_size_samp
    return classified
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    
    plt.close('all') #Closes old plots.
    
    ##PART 1
    #Load the example data
    #Plot the psds
    #Plot the spectrograms
    
    #Test the examples
    
    #Load the practice data
    #Load the practice answers
    #Classify the practice data
    #Check your performance
    
    #Generate the hypnogram plots



