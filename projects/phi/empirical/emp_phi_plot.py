import matplotlib.pyplot as plt
import numpy as np

from projects.phi.tools.utils import *

phi_awake = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Awake/phi_1.csv')
phi_sum_awake = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Awake/phiSum_1.csv')

phi_mild = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Mild/phi_1.csv')
phi_sum_mild = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Mild/phiSum_1.csv')

phi_deep = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Deep/phi_1.csv')
phi_sum_deep = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Deep/phiSum_1.csv')

phi_recovery = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Recovery/phi_1.csv')
phi_sum_recovery = load_matrix('/home/user/Desktop/data_phi/phi/tests/concat/Recovery/phiSum_1.csv')

phi = [phi_awake,phi_mild,phi_deep,phi_recovery]
phi_sum = [phi_sum_awake,phi_sum_mild,phi_sum_deep,phi_sum_recovery]

states = ['Awake','Mild','Deep','Recovery']
state_pos = np.arange(len(states))

plt.scatter(state_pos,phi)
plt.title('Relation of Phi and Propofol Induced Unconsciousness')
plt.xlabel('Brain State')
plt.ylabel('Phi')
plt.xticks(state_pos,states)
plt.show()

plt.scatter(state_pos,phi_sum)
plt.title('Relation of Phi and Propofol Induced Unconsciousness')
plt.xlabel('Brain State')
plt.ylabel('Phi')
plt.xticks(state_pos,states)
plt.show()