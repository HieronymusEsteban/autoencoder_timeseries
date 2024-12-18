import pandas as pd
import numpy as np


def load_data(files):
    data_raw = {}
    for filename in files:
        print(filename)
        file_name_first_part = filename.split(".tsv")[0]
        number_string = file_name_first_part.split('NM')[1]
        print(int(number_string))
        group_number = int(number_string)
        data_raw[group_number] = pd.read_csv(filename, delimiter='\t', encoding='utf-8', skiprows=10, low_memory=False)
        #print(nm_data_raw[group_number].columns)
        column_names = data_raw[group_number].columns
        data_raw[group_number].drop(column_names[len(column_names)-1], axis=1, inplace=True)
        #print(nm_data_raw[group_number].columns)
    return data_raw


def attribute_sound_track_labels(sound_track_order, data_dict):
    for number in sound_track_order.groups:

        # Select the row corresponding to one groups: 
        selection_bools = sound_track_order.groups == number
        song_order_group = sound_track_order[selection_bools]
        #print(song_order[selection_bools].iloc[0,:])
        # Make an empty list to store all the labels in: 
        song_labels = []
        # Loop through all the elements in the row corresponding to one group:
        for song_number in song_order_group.iloc[0,1:]:
    
            # Make a list with the label of the corresponding
            # sound track of the same length as the corresponding
            # time series:
            labels = [song_number]*6000
    
            # Add the list with the one label to the list
            # that is going to contain all labels:
            song_labels.extend(labels)
    
        # Add the list with all labels to the data frame of
        # one experimental group as a target column:
        data_dict[number]['target'] = song_labels
    return data_dict



def take_data_with_label_or_not(data_dict, label, with_label = True):
    #frames_to_stack = []
    output_dictionary = {}
    for key, data_group in data_dict.items():
        if with_label == True:
            selection_bools = data_group.target == label
        else:
            selection_bools = data_group.target != label
        normal_data_group = data_group[selection_bools]

        x_columns = []
        for element in normal_data_group.columns:
            if 'X' in element:
                #print(element)
                x_columns.append(element)
        columns_to_select = x_columns + ['target']

        normal_data_group_1d = normal_data_group.loc[:,columns_to_select]
        print(normal_data_group_1d.shape)
        #frames_to_stack.append(normal_data_group_1d)
        output_dictionary[key] = normal_data_group_1d
    #normal_data_all_1d = pd.concat(frames_to_stack) 
    
    return output_dictionary



def transpose_by_minute(data):
    '''Transpose the data frame by sound track length 
    (each batch of data corresponding to one sound 
    track has to be transposed individually because one row should 
    contain the time series corresponding to one sound track:'''
    indices = list(np.arange(0, data.shape[0]+1, 6000))
    indices
    list_of_frames = []
    for num in range(0, len(indices)-1):
        data_num = data.iloc[indices[num]:indices[num+1],:]
        data_values = data_num.iloc[:,:-1]
        data_t = data_values.T
        data_t.columns = list(range(0, 6000))
        #print(data.iloc[:,:])
        list_of_frames.append(data_t.iloc[:,:])
    data_t = pd.concat(list_of_frames, axis=0)
    return data_t


def choose_columns_no_corner(data_dict):
    for key, df in data_dict.items(): 
        data_dict[key] = df.loc[:, ~df.columns.str.startswith('C')]