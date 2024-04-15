import os
import train
import config 

print ('---- Train for smoothing alpha ---- ')

smoothing_alpha = 0.01
alpha_step = 0.01
output_file = config.experiment_out

# Iterate over alpha values
while smoothing_alpha <= 1:
    print ('--- Testing for alpha = ', smoothing_alpha, ' -----')
    # Train the model with the current alpha value
    train.main(smoothing_alpha)
    
    # Test the model and get accuracy
    test_command = 'python3 test.py'
    output = os.popen(test_command).read()
    appended_output = "Smoothing alpha " + str(smoothing_alpha) + " \n" + output + " \n"
    print (appended_output)
    with open(output_file, "a") as file:
        file.write(appended_output)
 
    #Move to the next alpha value
    smoothing_alpha += alpha_step

