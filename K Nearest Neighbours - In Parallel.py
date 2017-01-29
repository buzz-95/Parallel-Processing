#================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#									K NEAREST NEIGHBOURS
#----------------------------------------------------------------------------------------------------------------
#================================================================================================================

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import multiprocessing as mp
import pandas as pd
import random
from collections import Counter
from sklearn import preprocessing
from itertools import repeat


#for plotting
plt.style.use('ggplot')

class CustomKNN:
	
	def __init__(self):
		self.accurate_predictions = 0
		self.total_predictions = 0
		self.accuracy = 0.0
		
	def distances_for_parallel(self, features, incoming, group):
		return (np.linalg.norm(np.array(features)- np.array(incoming)), group)

	def predict(self, training_data, to_predict, group, k = 3):
		#training_data = dict(item for item in training_data)  # Convert back to a dict
		print(training_data)

		if len(training_data) >= k:
			print("K cannot be smaller than the total voting groups(ie. number of training data points)")
			return
		
		distributions = []
		for group in training_data:
			for features in training_data[group]:
				euclidean_distance = np.linalg.norm(np.array(features)- np.array(to_predict))
				distributions.append([euclidean_distance, group])
		
		results = [i[1] for i in sorted(distributions)[:k]]
		result = Counter(results).most_common(1)[0][0]
		confidence = Counter(results).most_common(1)[0][1]/k
		
		if result == group:
			self.accurate_predictions += 1
		
		else:
			print("Wrong classification with confidence " + str(confidence * 100) + " and class " + str(result))
		
		self.total_predictions += 1

	
	def test(self, test_set, training_data):
		pool = mp.Pool(processes= 8)

		
		for group in test_set:
			training_data = list(training_data.items())
			print(type(training_data))
			pool.starmap(self.predict, zip(training_data, test_set[group], repeat(group), repeat(3)))
		
		self.accuracy = 100*(self.accurate_predictions/self.total_predictions)
		print("\nAcurracy :", str(self.accuracy) + "%")

def mod_data(df):
	df.replace('?', -999999, inplace = True)
	
	df.replace('yes', 4, inplace = True)
	df.replace('no', 2, inplace = True)

	df.replace('notpresent', 4, inplace = True)
	df.replace('present', 2, inplace = True)
	
	df.replace('abnormal', 4, inplace = True)
	df.replace('normal', 2, inplace = True)
	
	df.replace('poor', 4, inplace = True)
	df.replace('good', 2, inplace = True)
	
	df.replace('ckd', 4, inplace = True)
	df.replace('notckd', 2, inplace = True)

def main():
	df = pd.read_csv(r".\data\chronic_kidney_disease.csv")
	mod_data(df)
	dataset = df.astype(float).values.tolist()
	
	#Normalize the data
	x = df.values #returns a numpy array
	min_max_scaler = preprocessing.MinMaxScaler()
	x_scaled = min_max_scaler.fit_transform(x)
	df = pd.DataFrame(x_scaled) #Replace df with normalized values
	
	#Shuffle the dataset
	random.shuffle(dataset)

	#20% of the available data will be used for testing
	test_size = 0.2

	#The keys of the dict are the classes that the data is classfied into
	training_set = {2: [], 4:[]}
	test_set = {2: [], 4:[]}
	
	#Split data into training and test for cross validation
	training_data = dataset[:-int(test_size * len(dataset))]
	test_data = dataset[-int(test_size * len(dataset)):]
	
	#Insert data into the training set
	for record in training_data:
		training_set[record[-1]].append(record[:-1]) # Append the list in the dict will all the elements of the record except the class

	#Insert data into the test set
	for record in training_data:
		test_set[record[-1]].append(record[:-1]) # Append the list in the dict will all the elements of the record except the class

	knn = CustomKNN()
	knn.test(test_set, training_set)

if __name__ == "__main__":
	main()
