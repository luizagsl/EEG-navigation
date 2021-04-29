import matplotlib
import matplotlib.pyplot as plt
from numpy import add
from time import sleep
matplotlib.use('TkAgg')

# LayoutNavigation constants

CONNECTIONS = dict({'yrd': ['liv'],
                    'liv': ['yrd', 'ktc', 'bed'],
                    'ktc': ['liv'],
                    'bed': ['bat', 'liv'],
                    'bat': ['bed']
                   })
COORDINATES = dict({'yrd': [5, -2],
                    'liv': [3, 2.5],
                    'ktc': [8, 2.5],
                    'bed': [6.5, 7.5],
                    'bat': [1.5, 8.5]
                   })
SIGNAL_DICT = dict({0: 'no',
                    1: 'yes'})

# DirectionNavigation constants

DIRECTIONS = dict({'up': [0, 1],
                   'down': [0, -1],
                   'right': [1, 0,],
                   'left': [-1, 0]
                   })
SIGNAL_DICT = dict({0: 'no',
                    1: 'yes'})


class LayoutNavigation():
    
    def __init__(self):
        pass

    def plot_plant(self, wall_color='grey', door_color='lightgrey', **kwargs):
        fig, ax = plt.subplots(figsize=(5,5))
        # Walls
        ax.plot([0,10], [0,0], color=wall_color, **kwargs)
        ax.plot([0,0], [0,10], color=wall_color, **kwargs)
        ax.plot([0,10], [10,10], color=wall_color, **kwargs)
        ax.plot([10,10], [0,10], color=wall_color, **kwargs)
        ax.plot([3,3], [7,10], color=wall_color, **kwargs)
        ax.plot([0,3], [7,7], color=wall_color, **kwargs)
        ax.plot([3,3], [5,10], color=wall_color, **kwargs)
        ax.plot([3,10], [5,5], color=wall_color, **kwargs)
        ax.plot([6]*2, [7,7], color=wall_color, **kwargs)
        ax.plot([6]*2, [0,5], color=wall_color, **kwargs)
        ax.plot([0]*2, [0,-4], color=wall_color, **kwargs)
        ax.plot([10]*2, [0,-4], color=wall_color, **kwargs)
        ax.plot([0, 10], [-4]*2, color=wall_color, **kwargs)
        # Doors' free space
        ax.plot([2, 3], [0]*2, color='white', **kwargs) # yard/living room
        ax.plot([6]*2, [2, 3], color='white', **kwargs) # kitchen
        ax.plot([4, 5], [5]*2, color='white', **kwargs) # bedroom
        ax.plot([3]*2, [8, 9], color='white', **kwargs) # bathroom
        # Doors
        ax.plot([2]*2, [0, 1], color=door_color, **kwargs) # yard/living room
        ax.plot([6, 7], [3]*2, color=door_color, **kwargs) # kitchen
        ax.plot([4]*2, [5, 6], color=door_color, **kwargs) # bedroom
        ax.plot([2, 3], [8]*2, color=door_color, **kwargs) # bathroom
        #  Opening line
        ax.plot([2, 3], [1, 0], color=door_color) # yard/living room
        ax.plot([7, 6], [3, 2], color=door_color) # kitchen
        ax.plot([4, 5], [6, 5], color=door_color) # bedroom
        ax.plot([3, 2], [9, 8], color=door_color) # bathroom
        # Coordinates
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        return fig, ax

    def navigate(self, start_point, input_signal):
        '''
            Plots the layout and the position of the subject.
            
            Arguments:
                start_point: initial spot on layout
                input_signal: binary sequence, generated from EEG data
        '''
        plt.ion()
        fig, ax = self.plot_plant(wall_color='grey', door_color='lightgrey', linewidth=5)
        px, = ax.plot(COORDINATES[start_point][0], COORDINATES[start_point][1], 'bo')
        current_spot = start_point
        navigation = 0
        while navigation <= len(input_signal):
            px.set_xdata(COORDINATES[current_spot][0])
            px.set_ydata(COORDINATES[current_spot][1])
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(2)
            try:
                current_spot, navigation = self.decision(current_spot, navigation, input_signal)
            except IndexError:
                navigation += 1
                pass
        sleep(5)
        plt.close()

    def decision(self, current_spot, navigation, input_signal):
        '''
            Updates the navigation step and the position of the subject based on the input signal.
            
            Arguments:
                current_spot: current spot on layout
                navigation: current step of the navigation
                input_signal: binary sequence, generated from EEG data
            Returns:
                current_spot, new_spot: following spot on layout
                navigation: step of the navigation after decision
        '''
        for new_spot in CONNECTIONS[current_spot]:
            print('Step {} in navigation, in {}, answer is {} for {}'.format(navigation+1,
                                                                             current_spot,
                                                                             SIGNAL_DICT[input_signal[navigation]],
                                                                             new_spot))
            if input_signal[navigation] == 1:
                return new_spot, navigation + 1
            navigation+=1
            sleep(2)
        return current_spot, navigation


class DirectionNavigation():
    
    def __init__(self):
        pass
    
    def plot_plant(self):
        fig, ax = plt.subplots(figsize=(5,5))
        for i in range(0,11):
            for j in range(0,11):
                ax.scatter(i, j, color='grey', alpha=0.3)
        # COORDINATES
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        return fig, ax
    
    def navigate(self, start_point, input_signal):
        '''
            Plots the layout and the position of the subject.
            
            Arguments:
                start_point: initial coordinates
                input_signal: binary sequence, generated from EEG data
        '''
        plt.ion()
        fig, ax = self.plot_plant()
        px, = ax.plot(start_point[0], start_point[1], 'bo')
        current_spot = start_point
        navigation = 0
        while navigation <= len(input_signal):
            px.set_xdata(current_spot[0])
            px.set_ydata(current_spot[1])
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(1)
            try:
                current_spot, navigation = self.decision(current_spot, navigation, input_signal)
            except IndexError:
                navigation+=1
                pass
        sleep(5)
        plt.close()

    def decision(self, current_spot, navigation, input_signal):
        '''
            Updates the navigation step and the coordinates of the subject based on the input signal.
            
            Arguments:
                current_spot: current coordinates
                navigation: current step of the navigation
                input_signal: binary sequence, generated from EEG data
            Returns:
                current_spot, new_spot: following coordinates
                navigation: step of the navigation after decision
        '''
        for change_direction in list(DIRECTIONS.keys()):
            print('Step {} in navigation, in {}, answer is {} for {}'.format(navigation+1,
                                                                             current_spot,
                                                                             SIGNAL_DICT[input_signal[navigation]],
                                                                             change_direction))
            if input_signal[navigation] == 1:
                new_spot = add(current_spot, DIRECTIONS[change_direction])
                if new_spot[0] in range(0,11) and new_spot[0] in range(0,11):
                    return new_spot, navigation + 1
                else:
                    print('\tOff-limits point, current position maintained.')
            navigation+=1
            sleep(1)
        return current_spot, navigation