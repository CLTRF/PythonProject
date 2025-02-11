'''
Created on Dec 9, 2024

@author: clt
date:   10/02/2025
Class VNA created to operation BRO components Check-out
# This is the version of the structure that's supported.

'''

from skrf import Network, COMPONENT_FUNC_DICT
import matplotlib.pyplot as plt
from skrf import plotting
from skrf.plotting import save_all_figs
import os
import numpy as np
import pickle

class VNA():
    '''
    Main Patterns class. An object of this class contains a list of ``VNA`` with each member
    of the list being an ordered dictionary object.
    Attributes:
        adress_hexadecimal     in the case of LNA and LNB includes its adress read by the driver
        serial_number
        create_date
        check_out_date
        temperature_check_out
        NF
        Spurious
        S2P
        Gain_SC
        Gain
        Phase
        WorkingDirectory       Directory where the data files are stored: S2P, screenshots, csv

    '''
    def __init__(self):
        '''
        Initialization method - creates empty structure with no Patterns.

        '''
        self.comment_static_vars = ['//###########################################################',
                                    '//#                   STATIC VARIABLES                      #',
                                    '//###########################################################',
                                    '']

        VNA_VERSION = 1
        self.version = VNA_VERSION

        self.comment_auto_populated = ['//########################################################',
                                       '//#       VARIABLES WILL BE POPULATED WHEN LOADING       #',
                                       '//########################################################',
                                       '']

        self.adress_hexadecimal     =   ''
        self.serial_number          =   ''
        self.create_date            =   ''
        self.check_out_date         =   ''
        self.temperature_check_out  =   ''
        self.NF                     =   []
        self.Spurious               =   []
        self.S2P                    =   []
        self.Gain_SC                =   []
        self.Gain                   =   []
        self.Phase                  =   []
        self.WorkingDirectory       =   []

    def change_name(self, file_name):
        '''
            This method is used to change the name of the S2P file
            Usualy used for postprocessing
        '''
        self.S2P = file_name

    def change_working_directory(self, working_directory_name):
        '''
            This method is used to modify the destination directory where graphs need to be saved
            Usualy used for postprocessing
        '''
        self.WorkingDirectory = working_directory_name


    def concat_rotate(self, _object_1, _object_2, _object_3, _object_4, legend):
        #        if not os.path.exists(self.WorkingDirectory):
        #            os.makedirs(self.WorkingDirectory)

        _device_1 = Network(_object_1.S2P)
        _device_2 = Network(_object_2.S2P)
        _device_3 = Network(_object_3.S2P)
        _device_4 = Network(_object_4.S2P)
        device = Network(self.S2P)
            # device = Network(frequency=_device_1.frequency,COMPONENT_FUNC_DICT= _device_1.COMPONENT_FUNC_DICT, PRIMARY_PROPERTY = _device_1.PRIMARY_PROPERTIES, number_of_ports=2, nports = _device_1.nports ,s11=_device_1.s21, s12=_device_2.s21,s21=_device_3.s21, s22=_device_4.s21,name='VNA1,2,3,4')
        rng = np.random.default_rng()
        s = (_device_1.s_deg[0,1], _device_2.s_deg[0, 1], _device_2.s_deg[0, 1],
                 _device_2.s_deg[0, 1])
            # device = Network(frequency=_device_1.frequency, a_deg_unwrap = s, name='random values 2-port')

            # device.s11 = _device_1.s21
            # device.s12 = _device_2.s21
            # device.s22 = _device_3.s21
            # device.s21 = _device_4.s21

        Phase_LNA_1_table = _device_1.s_deg
        Phase_LNA_2_table = _device_2.s_deg
        Phase_LNA_3_table = _device_3.s_deg
        Phase_LNA_4_table = _device_4.s_deg

        Phase_LNA_1 = Phase_LNA_1_table[:, 1, 0]
        Phase_LNA_2 = Phase_LNA_2_table[:, 1, 0]
        Phase_LNA_3 = Phase_LNA_3_table[:, 1, 0]
        Phase_LNA_4 = Phase_LNA_4_table[:, 1, 0]

        device.s11 = (_device_1.s21) * 1
        device.s12 = (_device_2.s21) * 1
        device.s22 = (_device_3.s21) * 1
        device.s21 = (_device_4.s21) * 1

        return Phase_LNA_1, Phase_LNA_2, Phase_LNA_3, Phase_LNA_4, _device_1.frequency.f

    def concat(self, _object_1, _object_2, _object_3, _object_4, legend):
        '''
            This method is used to extract Phases information for S2P files
            and return it for concatenation
            Usualy used for postprocessing
        '''

#        if not os.path.exists(self.WorkingDirectory):
#            os.makedirs(self.WorkingDirectory)

        _device_1 = Network(_object_1.S2P)
        _device_2 = Network(_object_2.S2P)
        _device_3 = Network(_object_3.S2P)
        _device_4 = Network(_object_4.S2P)
        #device = Network(self.S2P)
        #device = Network(frequency=_device_1.frequency,COMPONENT_FUNC_DICT= _device_1.COMPONENT_FUNC_DICT, PRIMARY_PROPERTY = _device_1.PRIMARY_PROPERTIES, number_of_ports=2, nports = _device_1.nports ,s11=_device_1.s21, s12=_device_2.s21,s21=_device_3.s21, s22=_device_4.s21,name='VNA1,2,3,4')
        rng = np.random.default_rng()
        s = (_device_1.s_deg_unwrap[0,1], _device_2.s_deg_unwrap[0,1], _device_2.s_deg_unwrap[0,1], _device_2.s_deg_unwrap[0,1])
        #device = Network(frequency=_device_1.frequency, s_deg_unwrap = s, name='random values 2-port')

        #device.s11 = _device_1.s21
        #device.s12 = _device_2.s21
        #device.s22 = _device_3.s21
        #device.s21 = _device_4.s21

        Phase_LNA_1_table = _device_1.s_deg_unwrap
        Phase_LNA_2_table = _device_2.s_deg_unwrap
        Phase_LNA_3_table = _device_3.s_deg_unwrap
        Phase_LNA_4_table = _device_4.s_deg_unwrap

        Phase_LNA_1 = Phase_LNA_1_table[:,1,0]
        Phase_LNA_2 = Phase_LNA_2_table[:,1,0]
        Phase_LNA_3 = Phase_LNA_3_table[:,1,0]
        Phase_LNA_4 = Phase_LNA_4_table[:,1,0]

        #device.s11 = (_device_1.s21)*1
        #device.s12 = (_device_2.s21)*1
        #device.s22 = (_device_3.s21)*1
        #device.s21 = (_device_4.s21)*1

        return Phase_LNA_1, Phase_LNA_2, Phase_LNA_3, Phase_LNA_4, _device_1.frequency.f

    def concat_S_parameter_ports(self, _object_1, _object_2, _object_3, _object_4, _object_5, _object_6, legend):
        '''
            This method has been developped for X band Antenna Checkout
            for extracting S parameters with the objective to concatenate those ones
            Usualy used for postprocessing
        '''

#        if not os.path.exists(self.WorkingDirectory):
#            os.makedirs(self.WorkingDirectory)

        _device_1 = Network(_object_1.S2P)
        _device_2 = Network(_object_2.S2P)
        _device_3 = Network(_object_3.S2P)
        _device_4 = Network(_object_4.S2P)
        _device_5 = Network(_object_5.S2P)
        _device_6 = Network(_object_6.S2P)

        rng = np.random.default_rng()

        if (legend == 'gain'):

                Gain_LNA_1_table = _device_1.s_db
                Gain_LNA_2_table = _device_2.s_db
                Gain_LNA_3_table = _device_3.s_db
                Gain_LNA_4_table = _device_4.s_db
                Gain_LNA_5_table = _device_5.s_db
                Gain_LNA_6_table = _device_6.s_db
                Gain_LNA_1 = Gain_LNA_1_table[:, 1, 0]
                Gain_LNA_2 = Gain_LNA_2_table[:, 1, 0]
                Gain_LNA_3 = Gain_LNA_3_table[:, 1, 0]
                Gain_LNA_4 = Gain_LNA_4_table[:, 1, 0]
                Gain_LNA_5 = Gain_LNA_5_table[:, 1, 0]
                Gain_LNA_6 = Gain_LNA_6_table[:, 1, 0]

        if (legend == 's21'):
            s_db_1 = _device_1.s_db
            s_db_2 = _device_2.s_db
            s_db_3 = _device_3.s_db
            s_db_4 = _device_4.s_db
            s_db_5 = _device_5.s_db
            s_db_6 = _device_6.s_db
            _output_1   =   s_db_1[:, 1, 0]
            _output_2   =   s_db_2[:, 1, 0]
            _output_3   =   s_db_3[:, 1, 0]
            _output_4   =   s_db_4[:, 1, 0]
            _output_5   =   s_db_5[:, 1, 0]
            _output_6   =   s_db_6[:, 1, 0]

        if (legend == 's12'):
            s_db_1 = _device_1.s_db
            s_db_2 = _device_2.s_db
            s_db_3 = _device_3.s_db
            s_db_4 = _device_4.s_db
            s_db_5 = _device_5.s_db
            s_db_6 = _device_6.s_db
            _output_1   =   s_db_1[:, 0, 1]
            _output_2   =   s_db_2[:, 0, 1]
            _output_3   =   s_db_3[:, 0, 1]
            _output_4   =   s_db_4[:, 0, 1]
            _output_5   =   s_db_5[:, 0, 1]
            _output_6   =   s_db_6[:, 0, 1]

        if (legend == 's11'):
            s_db_1 = _device_1.s_db
            s_db_2 = _device_2.s_db
            s_db_3 = _device_3.s_db
            s_db_4 = _device_4.s_db
            s_db_5 = _device_5.s_db
            s_db_6 = _device_6.s_db
            _output_1   =   s_db_1[:, 0, 0]
            _output_2   =   s_db_2[:, 0, 0]
            _output_3   =   s_db_3[:, 0, 0]
            _output_4   =   s_db_4[:, 0, 0]
            _output_5   =   s_db_5[:, 0, 0]
            _output_6   =   s_db_6[:, 0, 0]

        if (legend == 's22'):
            s_db_1 = _device_1.s_db
            s_db_2 = _device_2.s_db
            s_db_3 = _device_3.s_db
            s_db_4 = _device_4.s_db
            s_db_5 = _device_5.s_db
            s_db_6 = _device_6.s_db
            _output_1   =   s_db_1[:, 1, 1]
            _output_2   =   s_db_2[:, 1, 1]
            _output_3   =   s_db_3[:, 1, 1]
            _output_4   =   s_db_4[:, 1, 1]
            _output_5   =   s_db_5[:, 1, 1]
            _output_6   =   s_db_6[:, 1, 1]

        return _output_1, _output_2, _output_3, _output_4, _output_5, _output_6, _device_1.frequency.f


    def concat_gain(self, _object_1, _object_2, _object_3, _object_4, legend):

#        if not os.path.exists(self.WorkingDirectory):
#            os.makedirs(self.WorkingDirectory)

        _device_1 = Network(_object_1.S2P)
        _device_2 = Network(_object_2.S2P)
        _device_3 = Network(_object_3.S2P)
        _device_4 = Network(_object_4.S2P)
        #device = Network(self.S2P)
        #device = Network(frequency=_device_1.frequency,COMPONENT_FUNC_DICT= _device_1.COMPONENT_FUNC_DICT, PRIMARY_PROPERTY = _device_1.PRIMARY_PROPERTIES, number_of_ports=2, nports = _device_1.nports ,s11=_device_1.s21, s12=_device_2.s21,s21=_device_3.s21, s22=_device_4.s21,name='VNA1,2,3,4')
        rng = np.random.default_rng()
        #s = (_device_1.s21[0,1], _device_2.s21[0,1], _device_2.s21[0,1], _device_2.s21[0,1])
        #device = Network(frequency=_device_1.frequency, a_deg_unwrap = s, name='random values 2-port')

        #device.s11 = _device_1.s21
        #device.s12 = _device_2.s21
        #device.s22 = _device_3.s21
        #device.s21 = _device_4.s21

        Gain_LNA_1_table = _device_1.s_db
        Gain_LNA_2_table = _device_2.s_db
        Gain_LNA_3_table = _device_3.s_db
        Gain_LNA_4_table = _device_4.s_db

        Gain_LNA_1 = Gain_LNA_1_table[:,1,0]
        Gain_LNA_2 = Gain_LNA_2_table[:,1,0]
        Gain_LNA_3 = Gain_LNA_3_table[:,1,0]
        Gain_LNA_4 = Gain_LNA_4_table[:,1,0]

        #device.s11 = (_device_1.s21)*1
        #device.s12 = (_device_2.s21)*1
        #device.s22 = (_device_3.s21)*1
        #device.s21 = (_device_4.s21)*1

        return Gain_LNA_1, Gain_LNA_2, Gain_LNA_3, Gain_LNA_4, _device_1.frequency.f


        with plt.style.context('grayscale'):
            # ring_slot.plot_s_deg()
            device.frequency.unit = 'ghz'
            plt.legend(loc=5)
            plotting.add_markers_to_lines()
            plt.legend()
            #plt.legend('Phase Unwrap for LNA1, LNA2, LNA3, LNA4')  # have to re-generate legend
            plt.title(legend + ' Phase unwrap')

            device.s11.plot_s_deg_unwrap(m=0, n=0, label='LNA1')
            device.s12.plot_s_deg_unwrap(m=0, n=0, label='LNA2')
            device.s21.plot_s_deg_unwrap(m=0, n=0, label='LNA3')
            device.s22.plot_s_deg_unwrap(m=0, n=0, label='LNA4')

            plt.grid()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            plt.clf()

    def save(self, legend, type_of_plot, s_param, _limit):
        '''
            This method is used to extract, plot and save S parameter data
        '''

        _device = Network(self.S2P)

        if not os.path.exists(self.WorkingDirectory):
            os.makedirs(self.WorkingDirectory)

        # ring_slot.s21.plot_s_db()
        # ring_slot.s22.plot_s_deg_unwrap(m=0,n=0, label='S22 Phase unwrap')

        if (_limit != -3658):
            plt.axhline(y=_limit, color='r', linestyle='dotted')

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S11'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s11.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'All_Phase_United'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_deg_unwrap(lw=3, label='Phase Unwrap for LNA1, LNA2, LNA3, LNA4')
                plotting.add_markers_to_lines()
                plt.legend('Phase Unwrap for LNA1, LNA2, LNA3, LNA4')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S11'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s11.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S11'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s11.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S11'):
            # prepare figure
            fig_1, ax_1 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_1.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s11.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S22'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s22.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S22'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s22.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S22'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s22.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S_PARAM'):
            # prepare figure
            fig_2, ax_2 = plt.subplots(1, 1, figsize=(8, 8))
            #plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_2.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S22'):
            # prepare figure
            fig_2, ax_2 = plt.subplots(1, 1, figsize=(8, 8))
            #plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_2.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S21'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s21.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S21'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s21.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S21'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s21.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S21'):
            # prepare figure
            fig_3, ax_3 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_3.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s21.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S12'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s12.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S12'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s12.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S12'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s12.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S12'):
            # prepare figure
            fig_4, ax_4 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_4.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s12.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'ALL_UNITED'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'ALL_UNITED'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'ALL_UNITED'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'ALL_UNITED'):
            # prepare figure
            fig_5, ax_5 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_5.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s12.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()


    def save_2_ports(self, _object_1, _legend_1, _type_of_plot_1, _s_param_1, _object_2, _legend_2, _type_of_plot_2, _s_param_2, limit):
        '''
            This method is used to extract, plot and save S parameter data
            specificaly developped to X Band Antenna check out task
            Allow comparisons using 2 S2P files
            Typicaly used for comparing results and after before BackPlate was mounted
            Create the directory and safe the plots at this location
        '''

        if not os.path.exists(self.WorkingDirectory):
            os.makedirs(self.WorkingDirectory)

        _device_1 = Network(_object_1.S2P)
        _device_2 = Network(_object_2.S2P)

        rng = np.random.default_rng()
        _device_1.frequency.unit = 'ghz'
        _spec_limit = "Specification"

        with plt.style.context('grayscale'):
            # ring_slot.plot_s_deg()

            legend = _legend_1

            if (_s_param_1 == 'SMITH_S11' or _s_param_1 == 'SMITH_S22'):
                # prepare figure
                    fig_1, ax_1 = plt.subplots(1, 1, figsize=(8, 8))
                    plt.legend(loc=5)
                    plt.title(legend + ' Smith')
                    background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
                    # tweak background position
                    ax_1.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
                    _device_1.s11.plot_s_smith()
                    _device_1.s22.plot_s_smith()
                    save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                    # plt.show()
                    plt.clf()
            else:
                plt.legend(loc=5)
                plt.axhline(y=limit, color='r', linestyle='dotted')
                if (_s_param_1 == 'S11'):
                    _device_1.s11.plot_s_db(m=0, n=0, label='')
                if (_s_param_2 == 'S11'):
                    _device_2.s11.plot_s_db(m=0, n=0, label='')
                if (_s_param_1 == 'S22'):
                    plt.axhline(y=limit, color='r', linestyle='dotted')
                if (_s_param_2 == 'S22'):
                    _device_2.s22.plot_s_db(m=0, n=0, label='')
                if (_s_param_1 == 'S12'):
                    _device_1.s12.plot_s_db(m=0, n=0, label='')
                if (_s_param_2 == 'S12'):
                    _device_2.s12.plot_s_db(m=0, n=0, label='')
                if (_s_param_1 == 'S21'):
                    _device_1.s21.plot_s_db(m=0, n=0, label='')
                if (_s_param_2 == 'S21'):
                    _device_2.s21.plot_s_db(m=0, n=0, label='')
                ## plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.legend([_spec_limit,_legend_1, _legend_2],loc="lower right")
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        Status = True

        return Status

    def save_LNB(self, legend, type_of_plot, s_param, data_ware_house_file_name_S2P):
        '''
            This method is used to extract, plot and save S parameter data
            specificaly developed to X Band Antenna check out task
            Allow comparisons using 2 S2P files
            Typicaly used for comparing reslts and after before Back Plate was mounted
            Create the directory and safe the plots at this location
        '''

        _file_length =  26
        _file_name_S2P  = self.S2P[-_file_length:]
        _reconstructed  =   data_ware_house_file_name_S2P+_file_name_S2P
        ##_device = Network(self.S2P)
        _device = Network(_reconstructed)

        if not os.path.exists(self.WorkingDirectory):
            os.makedirs(self.WorkingDirectory)

        # ring_slot.s21.plot_s_db()
        # ring_slot.s22.plot_s_deg_unwrap(m=0,n=0, label='S22 Phase unwrap')

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S11'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s11.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'All_Phase_United'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_deg_unwrap(lw=3, label='Phase Unwrap for LNA1, LNA2, LNA3, LNA4')
                plotting.add_markers_to_lines()
                plt.legend('Phase Unwrap for LNA1, LNA2, LNA3, LNA4')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S11'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s11.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S11'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s11.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S11'):
            # prepare figure
            fig_1, ax_1 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_1.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s11.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S22'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s22.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S22'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s22.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S22'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s22.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S_PARAM'):
            # prepare figure
            fig_2, ax_2 = plt.subplots(1, 1, figsize=(8, 8))
            #plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_2.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S22'):
            # prepare figure
            fig_2, ax_2 = plt.subplots(1, 1, figsize=(8, 8))
            #plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_2.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S21'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s21.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S21'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s21.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S21'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s21.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S21'):
            # prepare figure
            fig_3, ax_3 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_3.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s21.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'S12'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s12.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'S12'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s12.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'S12'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.s12.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S12'):
            # prepare figure
            fig_4, ax_4 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_4.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s12.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()

        if (type_of_plot == "angle_unwrapped") and (s_param == 'ALL_UNITED'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_deg_unwrap(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase unwrap')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "angle_with_rotations") and (s_param == 'ALL_UNITED'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_deg(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Phase with rotations')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "magnitude_dB") and (s_param == 'ALL_UNITED'):
            with plt.style.context('grayscale'):
                # ring_slot.plot_s_deg()
                _device.frequency.unit = 'ghz'
                plt.legend(loc=5)
                _device.plot_s_db(m=0, n=0, label='')
                plotting.add_markers_to_lines()
                plt.legend('')  # have to re-generate legend
                plt.title(legend + ' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'ALL_UNITED'):
            # prepare figure
            fig_5, ax_5 = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
            # tweak background position
            ax_5.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.s12.plot_s_smith()
            save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            # plt.show()
            plt.clf()
