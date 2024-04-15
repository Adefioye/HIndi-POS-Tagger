import os
print ('---- Train for smoothing alpha ---- ')

smoothing_alpha = 0
alpha_step = 0.01
best_accuracy = 0
best_alpha = 0

# Iterate over alpha values
while smoothing_alpha <= 1:
    print ('--- Testing for alpha = ', smoothing_alpha, ' -----')
    # Train the model with the current alpha value
    train_command = f'python3 train.py {smoothing_alpha}'
    os.system(train_command)
    
    # Test the model and get accuracy
    test_command = 'python3 test.py'
    accuracy = os.system(test_command)
    
    # Update best accuracy and alpha if the current accuracy is better
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_alpha = smoothing_alpha
    
    # Move to the next alpha value
    smoothing_alpha += alpha_step

# Print the best alpha and accuracy
print("Best alpha:", best_alpha)
print("Best accuracy:", best_accuracy)

