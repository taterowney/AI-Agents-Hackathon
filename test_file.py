
import random
import statistics

# Generate a list of 10 random numbers between 1 and 100
numbers = [random.randint(1, 100) for _ in range(10)]

print("Random List: ", numbers)

# Calculate the mean value of the list
mean_value = statistics.mean(numbers)

print("Mean Value: ", mean_value)
