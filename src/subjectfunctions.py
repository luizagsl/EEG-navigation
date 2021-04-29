from numpy import where, var, mean
from pandas import read_csv
from os import getcwd
from os.path import join, realpath
import mne

__location__ = realpath(getcwd())
DATABASE_FOLDER = join(__location__, 'Database-EEG')


class subject(object):

    def __init__(self, subject_id):
        self.subject_id = subject_id
        self.cnt_filename = str()
        self.cnt_file = None
        self.ch_names = None
        self.event_filename = str()
        self.event_file = None
        self.event_signals = None
        self.binary_signal = list()

    def load_data(self, selected_file):
        '''
            Call functions to search files for categorization trial/series,
            split series into events and generate binary signal.
            This function is called from the main notebook.
        '''
        self.get_filenames(selected_file)
        self.load_cnt()
        self.load_txt()
        self.split_signals()
        self.generate_binary_signal()

    def get_filenames(self, selected_file):
        self.cnt_filename = join(DATABASE_FOLDER, self.subject_id,
                                         self.subject_id + selected_file + '.cnt')
        self.event_filename = join(DATABASE_FOLDER, self.subject_id,
                                           self.subject_id + selected_file + '.txt')

    def load_cnt(self):
        '''
            Load EEG data (.cnt file).
        '''
        raw = mne.io.read_raw_cnt(self.cnt_filename, preload=True,
                                  verbose=False).filter(l_freq=1, h_freq=30, verbose=False)
        self.ch_names = raw.info.ch_names[0:4]
        data, times = raw.get_data(return_times=True)
        self.cnt_file = (data[0:4, :], times)
        raw.close()
        del raw

    def load_txt(self):
        '''
            Load event file (.txt file).
        '''
        event_txt = read_csv(self.event_filename, delimiter="\t")
        event_txt['latency'] /= 1000
        event_txt = event_txt.drop(columns=['type', 'urevent'])
        self.event_file = event_txt

    def split_signals(self):
        '''
            Split a series (one categorization file) into events (100 per series).
        '''
        file_events = []
        for idx, current_event in enumerate(self.event_file['latency']):
            initial_idx = int(where(self.cnt_file[1] == current_event)[0])
            if idx + 1 == self.event_file.shape[0]:
                final_idx = len(self.cnt_file[1]) - 1
            else:
                final_idx = int(where(self.cnt_file[1] == self.event_file['latency'][idx + 1])[0])
            file_events.append(self.cnt_file[0][:, initial_idx:final_idx])
        self.event_signals = file_events

    def generate_binary_signal(self):
        '''
            Generate binary signal from events. Each event is processed and
            converted to a boolean value.
            By standard, the binary signal will contain 100 elements.
            Processing steps:
                Calculate mean of electrodes' amplitudes over time
                Calculate variance of mean signal
                Compare variance to threshold.
        '''
        for idx_event, event_signal in enumerate(self.event_signals):
            if var(mean(event_signal, axis=0))*10**9 < 0.41:
                signal_bool = 1
            else:
                signal_bool = 0
            self.binary_signal.append(signal_bool)

