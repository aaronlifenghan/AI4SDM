import pickle

with open('/data/MBESLIS/MBESLIS.pkl', 'rb') as file:
   loaded_data = pickle.load(file)
   
   
print(len(loaded_data))
print(loaded_data[0][0])