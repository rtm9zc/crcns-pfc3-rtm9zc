import src.io as projectio
import matplotlib.pyplot as plt

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

def subject_process(subject, trial_index, start_index, end_index, spikes_index):
	file_list = files_by_subject[subject]

	neuron_dict = {}

	for file in file_list:
		neuron = int(file.split('_')[-1][:-4])
		if neuron in neuron_dict:
			trial_dict = neuron_dict[neuron].trial_dict
		else:
			trial_dict = {}
		trials = projectio.file_to_trials(base_dir + file)
		for trial in trials:
			trial_num = trial[trial_index][0][0]
			trial_start = trial[start_index][0][0]
			trial_end = trial[end_index][0][0]
			spike_ct = 0
			# case where no spikes recorded has only one layer
			if len(trial[spikes_index]) != 0:
				for spike in trial[spikes_index][0]:
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

	fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6, 3))
	axes.plot(trial_list, rate_list)
	axes.set_xlabel('Trial Number')
	axes.set_ylabel('Normalized Average Spike Rate')
	axes.set_title('PFC Activity over time for subject ' + subject)
	plt.show()

subject_process(subject='SCR', trial_index=3, start_index=0, end_index=2, spikes_index=4)
subject_process(subject='ADR', trial_index=2, start_index=0, end_index=10, spikes_index=3)
subject_process(subject='BEN', trial_index=2, start_index=0, end_index=10, spikes_index=3)