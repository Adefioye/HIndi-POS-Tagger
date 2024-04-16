import matplotlib.pyplot as plt
import numpy as np

alphas = [0.004, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 10, 'null']
unknown_accuracy = [55.50, 55.65, 55.45, 56.21, 56.18, 56.17, 55.39, 55.04, 54.79, 54.57, 48.11, 57.24]
known_accuracy = [88.28, 88.33, 88.16, 88.50, 88.49, 88.48, 88.04, 87.66, 87.37, 87.05, 75.12, 93.31]
overall_accuracy = [86.53, 86.58, 86.41, 86.77, 86.76, 86.76, 86.30, 85.92, 85.63, 85.32, 73.68, 91.39]

#Accuracy Breakdown (Overall & Known Words)
plt.figure(figsize=(10, 6))
plt.plot(alphas, known_accuracy, marker='o', color='lightgreen', linestyle='-', label='Known Words Accuracy')
plt.plot(alphas, overall_accuracy, marker='o', color='skyblue', linestyle='-', label='Overall Accuracy')
plt.xlabel('Smoothing Alpha')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy by Smoothing Alpha')
plt.legend()
plt.ylim(85, 95)
plt.grid(True)
plt.show()

#Unknown words
plt.figure(figsize=(10, 6))
plt.plot(alphas, unknown_accuracy, marker='o', color='salmon', linestyle='-', label='Unknown Words Accuracy')
plt.xlabel('Smoothing Alpha')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy by Smoothing Alpha')
plt.legend()
plt.grid(True)
plt.show()
plt.ylim(50, 60)