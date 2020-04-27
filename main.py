import src.io as projectio

class NeuronData:
	def __init__(self, trial_dict, average):
		self.trial_dict = trial_dict
		self.average = average

	def normalize(self):
		for trial in self.trial_dict:
			self.trial_dict[trial] = self.trial_dict[trial]/self.average

subjects = ['SCR', 'ELV', 'ADR', 'BEN']
base_dir = 'data/pfc3/data/'

files = projectio.files_from_csv('data/pfc3/SummaryDatabase.csv')

files_by_subject = {}

for subject in subjects:
	s_list = []
	for file in files:
		if file.startswith(subject):
			s_list.append(file)
	files_by_subject[subject] = s_list

test_f = files_by_subject['SCR']

neuron_dict = {}

for file in test_f:
	neuron = int(file.split('_')[-1][:-4])
	if neuron in neuron_dict:
		trial_dict = neuron_dict[neuron].trial_dict
	else:
		trial_dict = {}
	trials = projectio.file_to_trials(base_dir + file)
	for trial in trials:
		trial_num = trial[3][0][0]
		trial_start = trial[0][0][0]
		trial_end = trial[2][0][0]
		spike_ct = 0
		# case where no spikes recorded has only one layer
		if len(trial[4]) != 0:
			for spike in trial[4][0]:
				if spike > trial_start and spike < trial_end:
					spike_ct += 1
		spike_rate = float(spike_ct)/(trial_end-trial_start)

		trial_dict[trial_num] = spike_rate
	#Get average spike rate over all trials
	total_rates = 0
	for trial in trial_dict:
		total_rates += trial_dict[trial]
	average_rate = total_rates/float(len(trial_dict))

	neuron_dict[neuron] = NeuronData(trial_dict, average_rate)

num_trials = 0
for neuron in neuron_dict:
	neuron_dict[neuron].normalize()
	num_trials = max(num_trials, max(neuron_dict[neuron].trial_dict.keys()))
print(num_trials)

trial_list = []
rate_list = []
for i in range(1, num_trials + 1):
	num_neurons = 0
	total_rate = 0
	for neuron in neuron_dict:
		if i in neuron_dict[neuron].trial_dict:
			num_neurons += 1
			total_rate += neuron_dict[neuron].trial_dict[i]
	if num_neurons > 0:
		trial_list.append(i)
		rate_list.append(total_rate/float(num_neurons))
print(trial_list, rate_list)