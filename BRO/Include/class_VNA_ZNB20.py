'''
Created on Dec 9, 2024

@author: clt

# For use in serialization and deserialization to json
#from __future__ import division
import sys
#from collections import OrderedDict
import numpy as np
from numpy import inf

import includes.misc
import includes.data_load_store
import includes.field_operations

# This is the version of the structure that's supported.

'''

from skrf import Network
import matplotlib.pyplot as plt
from skrf import plotting
from skrf.plotting import save_all_figs

class VNA():
    '''
    Main Patterns class. An object of this class contains a list of ``VNA`` with each member
    of the list being an ordered dictionary object.
    Attributes:
        self.adress_hexadecimal     =   ''
        self.serial_number          =   ''
        self.create_date            =   ''
        self.check_out_date         =   ''
        self.temperature_check_out  =   temperaure in degrees
        self.NF                     =   file name for Noise Figure measurments Snapshot
        self.Spurious               =   file name for Spurious measurments Snapshot
        self.S2P                    =   file name for S2p file
        self.Gain_SC                =   file name for screen shot
        self.Gain                   =   Gain in dB
        self.Phase                  =   Unwrapped phase in degrees
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

    def __get_raw_field_data(self, pat_ind):
        '''
        Warning:
            This is a private method and is NOT intended for external use.

        This method is used to fetch the raw Etheta and Ephi fields from the imported data and
        applied permanent manipulations. It uses geometric definition of alpha, beta, psi angles or
        yaw, pitch roll angles correspondingly to apply permanent roataion. The fixed XYZ coordinate
        system is the same used to define the radiation pattern in spherical coordinates.

        Arguments:
            pat_ind (int): The pattern index to requested. Permanent rotation is based on the three\
                Euler angles defined in ``rot_offset``.

        Returns:
            ff (array): returns ``ff`` and if there is non-zero rotation offset a rotated ``ff``
        '''
        temp_pat = self.patterns[pat_ind]['ff']
        rot_angles = self.patterns[pat_ind]['rot_offset']
        temp_pat = includes.field_operations.rotate(temp_pat, rot_angles)

        return temp_pat

    def save(self,legend,type_of_plot,s_param):

        _device = Network(self.S2P)
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
                plt.title(legend+' Phase unwrap')
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
                plt.title(legend+' Phase with rotations')
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
                plt.title(legend+' Amplitude_dB')
                plt.grid()
                save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
                plt.clf()

        if (type_of_plot == "smith") and (s_param == 'S11'):
            # prepare figure
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
            plt.legend(loc=5)
            plt.title(legend + ' Smith')
            background = plt.imread('C:/Users/CLT/PycharmProjects/PythonProject/BRO/Include/Smith_Chart.png')
    # tweak background position
            ax.imshow(background, extent=[-1.185, 1.14, -1.13, 1.155])
            _device.plot_s_smith()
            #save_all_figs(self.WorkingDirectory, format=['png', 'eps', 'pdf'])
            #plt.show()
            plt.clf()


    def __get_multiple_raw_fields_data(self, pat_inds):
        '''
        Warning:
            This is a private method and is NOT intended for external use.

        Same as ``__get_raw_field_data`` but ``pat_inds`` is a list and the output is aslo a list

        Arguments:
            pat_ind (int): The pattern index to requested. Permanent rotation is based on the three\
                Euler angles defined in ``rot_offset``.

        Returns:
            ff (array): returns ``ff`` and if there is non-zero rotation offset a rotated ``ff``
        '''
        temp_pat = []
        for curr_p in pat_inds:
            temp_pat.append(self.__get_raw_field_data(curr_p))

        return temp_pat

    def __get_interp_mesh_from_patterns(self, pat_inds):
        '''
        Warning:
            This is a private method and is NOT intended for external use.

        This method scans the Patterns listed under ``pat_inds`` and finds the finest theta and phi\
            angular resolution. From that it defines interpolation parameters so that all Patterns \
            in those indexes can be interpolated to that finest resolution.

        Arguments:
            pat_inds (list): list of indexes of Patterns to be interpolated

        Returns:
            tuple: a tuple consisting of:

            - interp_vth (list): interpolation theta matrix generated with meshgrid. The number of \
                rows is the number of samples from equally dividing the theta angle span with the \
                smallest thera step among all pattern indexes. The number of columns is equal to \
                the number of samples when diving the phi range equally witht eh smallest phi step.

            - interp_vph (list): interpolation phi matrix generted with meshgrid. Same definitions \
                as ``interp_vth``.

            - no_th_samples (int): number of theta samples

            - no_ph_samples (int): number of phi samples
        '''
        min_th_step = np.min([self.patterns[curr_p]['th_step'] for curr_p in pat_inds])
        min_ph_step = np.min([self.patterns[curr_p]['ph_step'] for curr_p in pat_inds])
        interp_vth = np.array(range(0, 180 + min_th_step, min_th_step)) * np.pi / 180
        interp_vph = np.array(range(0, 360 + min_ph_step, min_ph_step)) * np.pi / 180

        return interp_vth, interp_vph

    def __get_interp_mesh(self, resolution = None, pat_inds = None):
        '''
        Creates interpolation mesh based on eitehr a set of input pattern indexes ``pat_inds`` or
        directly specifying the resolution ``resolution``.
        '''
        if resolution is None:
            resolution = 'auto'
            if pat_inds is None:
                sys.exit('If interpolation resolution is empty then pattern indexes MUST be \
                                            specified')

        if resolution == 'auto':
            interp_vth, interp_vph = self.__get_interp_mesh_from_patterns(pat_inds)
        else:
            interp_vth = np.array(range(0, 180 + resolution[0], resolution[1]))\
                                         * np.pi / 180
            interp_vph = np.array(range(0, 360 + resolution[1], resolution[1]))\
                                         * np.pi / 180

        interp_vth, interp_vph = np.meshgrid(interp_vth, interp_vph)

        return [interp_vth, interp_vph]

    def __interpolate(self, pat_inds, interp_resolution = None):
        interp_v = self.__get_interp_mesh(interp_resolution, pat_inds)
        temp_fields = []
        for curr_p in pat_inds:
            far_field = self.__get_raw_field_data(curr_p)
            pat_resolution = [self.patterns[curr_p]['th_step'] , self.patterns[curr_p]['ph_step']]
            far_field = includes.field_operations.interpolate_complex_field(interp_v, \
                                                            far_field,pat_resolution)

            temp_fields.append(far_field)
        return temp_fields

    def __create_legends(self, pat_ind):
        '''
        Creates legend string for the pattern index.
        '''
        context = self.get_context(pat_ind)
        legend = (str(context['Frequency [Hz]'] / 1E6) + " MHz @Port:" + \
                      str(context['Port [#]']) + "; File: " + \
                      str(context['File']) + "; Source: " + \
                      str(context['Source']))

        return legend

    def __get_single_group_stats(self, members, field = 'Gabs', \
                        analysis_range= None, rot_angles = None):
        t_stats = []
        for mem in members:
            t_stats.append(self.get_field_stats( mem, field, analysis_range , rot_angles ))
        t_stats = np.array(t_stats)
        return t_stats

    def load_data(self, input_type, input_file_or_folder):
        '''
        Loads Patterns from various input formats.

        Arguments:
            input_type (str): this parameter indicates the type of the import. Possible values are:
                - json - loads from previously exported JSON file. This type of input requires a\
                    file path.
                - AAU_Legacy - Loads from old AAU chamber CSV file generated by the triggered \
                    Keysight VNA. This type of input requires a file path.
                - AAU_Satimo - loads from AAU's Satimo chamber file exports. This type of input \
                    requires a file path.
                - CST_File - loads from a CST exported pattern. This type of input requires a\
                    file path.
                - CST_Folder - Loads all CST exported files in a folder. This type of input \
                    requires a folder path.
                - CST_Par_Sweep - Loads all files in all folders part of a cached parameter sweep \
                    in CST. This type of input requires a folder path.
            input_file_or_folder (str): full file or folder path depending on ``input_type``.

        Returns:
            bool: returns zero on succesfull completion. All Patterns loaded from any source are\
                appended.

        '''
        includes.data_load_store.check_load_data_input(input_type, input_file_or_folder)
        if input_type == 'json':
            self = includes.data_load_store.load_from_json(self,input_file_or_folder)

        elif input_type == 'AAU_Legacy':
            self = includes.data_load_store.load_from_aau_legacy(self,input_file_or_folder)

        elif input_type == 'AAU_Satimo':
            self = includes.data_load_store.load_from_aau_satimo(self,input_file_or_folder)

        elif input_type == 'CST_File':
            self = includes.data_load_store.load_from_cst_file(self,input_file_or_folder)

        elif input_type == 'CST_Folder':
            self = includes.data_load_store.load_from_cst_folder(self,input_file_or_folder)

        elif input_type == 'CST_Par_Sweep':
            self = includes.data_load_store.load_from_cst_par_sweep(self,input_file_or_folder)

        return 0

    def get_context(self,pat_ind):
        '''
        Get the context of the current pattern index

        Arguments:
            pat_ind (int): the index of the pattern to query. SIngle value only possible. If
                multiple contexts required run a loop and call this function multiple times.

        Returns:
            context (dict): returns an ordered dictionary with pattern context. The output is the\
                 same as the ``Patterns`` structure except it omits the ``ff`` parameter.
        '''
        context = OrderedDict()
        context['Source'] = self.patterns[pat_ind]['source']
        context['File'] = self.patterns[pat_ind]['file']
        context['Frequency [Hz]'] = self.patterns[pat_ind]['frequency']
        context['Port [#]'] = self.patterns[pat_ind]['port']
        context['TH_Step [deg]'] = self.patterns[pat_ind]['th_step']
        context['PH_Step [deg]'] = self.patterns[pat_ind]['ph_step']
        context['Rot. Offset'] = self.patterns[pat_ind]['rot_offset']
        return context

    def fetch_field_with_context(self, pat_ind, field = 'Gabs', field_format = 'dB', \
                                 rot_angles = None):
        '''
        Same behaviour as ``fetch_field`` but with an additional context output.
        '''
        temp_field, temp_phase = self.fetch_field(pat_ind, field, field_format, rot_angles)
        context = self.get_context(pat_ind)
        return temp_field, temp_phase, context

    def fetch_field(self, pat_ind, field = 'Gabs', field_format = 'dB', rot_angles = None):
        '''
        Fetches the ``field`` at an index ``pat_ind`` in the ``field_format`` and ``rotation``
        specified. All fields are stored as E_theta and E_phi complex matrixes and this function
        makes the necessary conversions.

        Standard spherical coordinate system and angular rotations of antenna are defined in [1] and
        [2].

        Arguments:
            pat_ind (int): The index of the pattern requested.

            field (str): the type of field requested. If the requested field is different from the
                default complex E fields the function converts it as necessary. See \
                ``__convert_field`` for list of possible values.

            field_format (str): The format of the output field. Definitions are according to the \
                Touchstone file format. See ``__convert_field_format`` for details on options.

            rot_angles (int,int,int): list of three Euler rotation angles describing the rotation.
                The definitions are according to [2]. The order is --> [yaw, pitch, roll] as defined
                in [2]. Default are set to zero.

        Returns:
            tuple: tuple containing:

                field (list): a two dimensional array containing the theta/phi values of the field \
                    along the columns and rows correspondingly. The number columns/rows corresponds\
                    to the pattern resolution along the theta and phi angles.

                phase (list): a two dimensional array containing the theta/phi values of the field\
                    phase along the columns and rows correspondingly. The number columns/rows\
                    corresponds to the pattern resolution along the theta and phi angles. See field\
                    definitions above for when phase is defined. When phase is NOT defined an empty\
                    list is returned.

        References:

            [1] IEEE Standard for Definitions of Terms for Antennas," in IEEE Std 145-2013 (Revision
            of IEEE Std 145-1993) , vol., no., pp.1-50, 6 March 2014 \
            **doi** : 10.1109/IEEESTD.2014.6758443 \
            **keywords** : {antennas;IEEE standards;antenna term definitions;IEEE Std 145-2013;\
            IEEE Std 145-1993 Revision;IEEE standard;IEEE standards;Antennas;Terminology;antennas;\
            definitions;IEEE 145;terms}, \
            **URL** :\
            http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6758443&isnumber=6758442


            [2] IEEE Standard Test Procedures for Antennas," in ANSI/IEEE Std 149-1979 , vol., no.,
            pp.0_1-, 1979 **doi** : 10.1109/IEEESTD.1979.120310 **keywords** :
            {antennas;electronic equipment testing;measurement standards;IEEE standard;test
            procedures;antenna properties;ANSI/IEEE Std 149-1965;radiation Patterns;antenna
            range;antenna test facilities;instrumentation;Antennas;Electronic equipment
            testing;Measurement standards},
            **URL**: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=19510&isnumber=768

        '''

        temp_pat = self.__get_raw_field_data(pat_ind)

        temp_pat = includes.field_operations.rotate(temp_pat, rot_angles)

        temp_field, temp_phase = \
            includes.field_operations.convert_field(field, field_format, temp_pat)

        return temp_field, temp_phase

    def generate_analytical_pattern(self, input_parameters = None):
        '''
        Creates an analytical antenna pattern.

        Args:
            type (str): 'dipole' - finite length analytical dipole;
                'point source' - ideal isotropic radiator;
                'delta function' - pencil beam is a single direction.
            resolution (int, int): defines the [theta,phi] resolution in degrees - [1,1] as default
            frequency (int): used mostly for the dipole type and the wavelength scaling in Hz.
                Default is 1E9 for 1GHz dipole.
            length (float): finite dipole length as a fraction of wavelength - dimenssionless.
                Default is 0.5 for a half-lambda dipole.
            efficiency (int): once generated the analytical dipole is scaled to certain efficiency
                defined in percent. Default is 100.

        Returns:
            The new pattern is appended to the list of Patterns.
        '''
        self = includes.data_load_store.generate_analytical_pattern(self,input_parameters)

    def get_tot_field_power(self, pat_ind, field, rot_angles = None):
        '''
        This function calculates the total field power by integrating over the entire sphere. The\
        interpretation of the result depends on the field being integrated.
        This operation is NOT defined for AR.

        Arguments:
            pat_ind (int): specifies the index of the patter to be processed. Single value input\
                only possible. If multiple Patterns need be processed run a loop and call this\
                function multiple times.
            field (str): specifies the field to be processed as a string input as defined for\
                ``fetch_field``. Field power is NOT defined for AR.
            rot_angles (int,int,int): rotation angles for the field. Rotation alone should not \
                impact total field power however some numerical inaccuracies can occur.

        Returns:
            float: Returns the 3D integrated total field power in linear scale. If AR is selected\
                returns and empty list.
        '''

        # For efficiency always get the G field
        if field == 'Gabs' or field == 'Eabs':
            eff_field = 'Gabs'
        elif field == 'Gth' or field == 'Eth':
            eff_field = 'Gth'
        elif field == 'Gph' or field == 'Eph':
            eff_field = 'Gph'
        elif field == 'GL' or field == 'EL':
            eff_field = 'GL'
        elif field == 'GR' or field == 'ER':
            eff_field = 'GR'
        elif field == 'AR':
            eff_field = 'AR'
        else:
            sys.exit('Unknown FIELD --> "{}" requested. Options are: Gabs/Eabs, Gth/Eth, Gph/Eph,\
                GL/EL, GR/ER, AR (skips eff. calculation).'.format(field))

        if not field == 'AR':
            pattern, _ = self.fetch_field(pat_ind, eff_field, field_format='MA', \
                                          rot_angles = rot_angles)
            th_step,ph_step = includes.misc.get_angle_steps(pattern, sphere_type='open')
            vth = np.array(range(0, 180 + th_step, th_step))*np.pi/180
            vph = np.array(range(0, 360 + ph_step, ph_step))*np.pi/180
            for i, angle in enumerate(vth):
                pattern[i, :] = pattern[i, :] * np.sin(angle)
            # Close the sphere:
            pattern = includes.misc.close_sphere(pattern)
            tot_field_power = np.trapz(np.trapz(pattern, vth, axis=0), vph)/(4*np.pi)
        else:
            # total field power for Axial Ratio makes no sense...
            tot_field_power = -inf

        return tot_field_power

    def get_field_stats(self, pat_ind, field='Gabs', analysis_range = None, rot_angles=None):
        '''
        This method calculates several statistical metrics of a selected field. Based on pattern\
        index (``pat_ind``) and requested ``field``, the method calculates the minimum and maximum\
        of the field, the average value and the total power. In addition the calcualtion range can\
        be limited to only a portion of the field by specifying ``analysis_range`` as well as some\
        rotation can be performed in advance by specifying ``rot_angles``. The total field power is\
        always calculated for the full 3D sphere.

        Arguments:
            pat_ind (int): pattern index selected for analysis
            field (str): field selected for analysis. The field is selected via the strings defined\
                for the ``fetch_field`` method. The default field is ``Gabs``.
            analysis_range ([int,int],[int,int]): four integers specifying the solid angle defined\
                for the analysis. The first two specify the Theta angle range and the second two\
                specify the Phi angle range. The default is [[0,180],[0,360]] defining a full 3D\
                sphere for analysis.
            rot_angles (int,int.int): defined the rotation Euler angles for the pattern to be \
                rotated before the analysis. ``analysis_range`` refers to the standard antenna \
                coordiante system as defined by IEEE. By default there is no rotation specified.

        Returns:
            tuple: four values with the analysis data in linear scale

                - tot_field_power (flaot): is the total field power as defined in \
                    ``get_tot_field_power``. This is always calculated for the full 3D sphere.
                -  min_field (float): the minimum value of the field after rotation and within\
                    the ``analysis_range`` defined.
                -  max_field (float): the maximum value of the field after rotation and within\
                    the ``analysis_range`` defined.
                -  avg_field (float): the average value of the field after rotation and within\
                    the ``analysis_range`` defined.

        Example:
            Suppose one has a patch antenna radiating along the Z axis and one is interested in the\
            antenna gain properties. One can call to ``get_field_stats`` with the following \
            parameters::

                tot,min,max,avg = get_field_stats(0, analysis_range=[[0, 20], [0, 360]])

            This would return the total efficiency, the min, max and avg gains in the 0 to 20\
            Theta degrees solid angle and full Phi rotation. This is effectively looking at the\
            main beam lobe.

        '''
        tot_field_power = self.get_tot_field_power(pat_ind, field, rot_angles)

        pat, _ = self.fetch_field(pat_ind, field, field_format='MA', rot_angles=rot_angles)
        pat = includes.misc.apply_analysis_range(pat, analysis_range)

        min_field = np.min(pat)
        max_field = np.max(pat)
        avg_field = np.mean(pat)

        return tot_field_power, min_field, max_field, avg_field

    def get_groups(self):
        '''
        This method finds the groups of Patterns. Grouping is based on the source path. Files with\
        same source path belong to the same group. Groups are mostly useful when analyzing CST\
        parametric sweeps or multiple frequencies from same measurment. Groups can be used to\
        analyze multivariate parameter optimizations from parameteric analysis.

        Arguments:
            none

        Returns:
            tuple: returns two lists containing:

                - group_names (list): names of the groups. These are effectively the same as\
                    ``source`` parameter in the context.
                - memberidxs (list): the pattern indexes belonging to each group.
        '''
        memberidxs = []
        sources = [self.patterns[s]['source'] for s in range(0,len(self.patterns))]

        group_names = list(set(sources))

        for g_nam in group_names:
            indices = [i for i, x in enumerate(sources) if x == g_nam]
            memberidxs.append(indices)
        return group_names, memberidxs

    def get_filtered_groups(self,patt_filter):
        '''
        Same as ``get_groups`` but it also applies a filter to the groups and removes any groups
        that are empty after the filter application.
        '''
        group_names, memberidxs = self.get_groups()
        # apply filters
        for idx, gr_members in enumerate(list(memberidxs)):
            memberidxs[idx] = self.filter_patterns(patt_filter, gr_members)

        # Remove empty enties if any
        new_memberidxs = []
        new_gr_members = []
        for idx, mem in enumerate(memberidxs):
            if memberidxs[idx]:
                new_memberidxs.append(mem)
                new_gr_members.append(group_names[idx])
        memberidxs = new_memberidxs
        group_names = new_gr_members

        return group_names, memberidxs

    def filter_patterns(self, patt_filter, pat_inds = None):
        '''
        Applies a filter to the Patterns specified in ``pat_inds`` and returns only the indexes that
        match.
        '''
        if pat_inds is None:
            pat_inds = list(range(self.patterns.__len__()))
        pattern_filter =    {'frequency': []
                            }
        pattern_filter = includes.misc.update_params(pattern_filter, patt_filter)

        for pat in list(pat_inds):
            if not pattern_filter['frequency'][0] <= self.patterns[pat]['frequency'] \
                                                                <= pattern_filter['frequency'][1]:
                pat_inds.remove(pat)

        return pat_inds

    def get_group_stats(self, memberidxs, field = 'Gabs', analysis_range= None, rot_angles = None):
        '''
        This method generates statistics for entire groups. This is useful when analyzing for
        example the AR of a parameter sweep in CST and one is interested which set of parameters
        produces lowest average AR at maximum average gain given some ``analysis_range``.

        For each group the method scans the pattern indexes belonging to the groups and checks if
        the frequency is within the analysis range. Then the pattern is rotated if this is
        specified. The requested field is extracted and statistics are computed within the specified
        angular range using ``get_field_stats``. The results are appended to a group pool. Once all
        Patterns from a group are analyzed the group pool of results is further analyzed by
        computing min, max and average.

        Arguments:
            groupnames (list): names of the groups to be used - output form ``get_groups``.
            memberidxs (list): indexes of the Patterns in the groups - out form ``get_groups``.
            field (str): specified the field to be analyzed as descibed in ``fetch_field``.
            freq_range (list): start and stop frequencies (boundaries included) to search for in \
                the groups. The frequency must be defined in Hz. If a pattern is found within a\
                group that is within the frequency range it will be included in teh statistical\
                analysis.
            analysis_range (int,int,int,int): specifies start and stop theta and phi angles for\
                analysis from the full 3D field.
            rot_angles (int,int,int): three Euler angles defining the rotation of the fields.

        Returns:
            tuple: returns a tuple of four values in linear scale. The results are as below:

                - gr_tot_pwr (float): average total field power for all Patterns in the group. AR\
                    field does NOT have total power defined. The analysis is always done in full 3D\
                    sphere.
                - gr_min (float): minimum field value from all Patterns in the group. The\
                    analysis is done within the ``analysis_range``.
                - gr_max (float): maximum field value from all Patterns in the group. The\
                    analysis is done within the ``analysis_range``.
                - gr_avg (float): average field value from all Patterns in the group. The\
                    analysis is done within the ``analysis_range``.
        '''
        gr_tot_pwr = []
        gr_min = []
        gr_max = []
        gr_avg = []
        for mems in memberidxs:

            t_stats = self.__get_single_group_stats(mems, field, analysis_range, rot_angles)

            if not t_stats.size == 0:
                gr_tot_pwr.append(np.mean(np.array(t_stats[:,0])))
                gr_min.append(np.min(np.array(t_stats[:,1])))
                gr_max.append(np.max(np.array(t_stats[:,2])))
                gr_avg.append(np.mean(np.array(t_stats[:,3])))
            else:
                gr_tot_pwr.append([])
                gr_min.append([])
                gr_max.append([])
                gr_avg.append([])

        return gr_tot_pwr, gr_min, gr_max, gr_avg

    def set_permanent_rotation_offset(self,pat_ind, rot_angles = None):
        '''
        Applies permanent rotation offset to a pattern. This works by storing the rotation values
        for each pattern. Each time a pattern is fetched via ``fetch_field`` first the permanent
        rotation is applied effectively creating a new default orientation. The ``rot_angles``
        parameter of ``fetch_field`` then stacks additionally so that the total rotaions are added
        together.

        The definitions are the same as for ``fetch_field``.

        Arguments:
            pat_ind (int): pattern index rot_angles (int,int,int): three Euler angles of
            rotation.The order is --> [yaw, pitch, roll]. The default is [0,0,0], which means that\
                calling ``set_permanent_rotation_offset`` with only the ``pat_ind`` argument resets\
                any offsets applied earlier.

        Returns:
            bool: returns zero on succesfull execution.
        '''
        if rot_angles is None:
            rot_angles = [0,0,0]

        self.patterns[pat_ind]['rot_offset'] = rot_angles

        return 0

    def prepare_for_plotting(self, pat_inds, field = 'Gabs', rot_angles = None, \
                                interp_resolution = None):
        '''
        Prepares selected far_fields for plotting. First it does interpolation and then creates a
        plotting object inputs that can be directly given to the plotting class contructor.

        Arguments:
            pat_inds (list): a list of integer indexes with the patterns to be processed. Use\
                ``list_patterns`` to identify the patters of interest.

            field (str): a string identifying the field to be used for plotting. See\
                :func:`~includes.field_operations.convert_field`

            rot_angles (:obj:`list` of :obj:`int`, optional): a list of the rotation angles to be\
                used when generating the plotting object. All patterns will be rotated by these\
                values. To align only some patterns by applying some rotation use\
                :meth:`~includes.patterns.Patterns.set_permanent_rotation_offset`. For details on \
                how to define the rotation angles see :func:`~includes.field_operations.rotate`.

            interp_resolution (:obj:`list` of two :obj:`int`, optional): defines the interpolation\
                resolution. If the deault ``None`` is used the resolution will be taken from the\
                smallest pr angle resolution from the selected patterns via ``pat_inds``.

        Returns:
            tuple: returns several variables:

                - fields_to_plot (:obj:`list`): a list of patterns prepated for plotting
                - phase_to_plot (:obj:`list`): a list of phases prepated for plotting where \
                    applicable
                - legend (:obj:`tuple` of :obj:`list`): a tuple of two lists containing ``field``\
                    and legend strings.
        '''
        far_fields = self.__interpolate(pat_inds, interp_resolution)

        fields_to_plot = []
        phase_to_plot = []
        legend = []

        for curr_p in far_fields:
            curr_p = includes.field_operations.rotate(curr_p, rot_angles)
            t_field,t_phase = includes.field_operations.convert_field(field, 'MA', curr_p)
            fields_to_plot.append(t_field)
            phase_to_plot.append(t_phase)

        for curr_p in pat_inds:
            legend.append([field , ' --> ' + self.__create_legends(curr_p)])

        return fields_to_plot,phase_to_plot, legend

    def list_patterns(self):
        '''
        Lists all Patterns legends with their corresponding indexes.

        Returns:
            list: returns a list of pattern legend strings and inxed.
        '''
        pattern_list = []
        for curr_p in range(self.patterns.__len__()):
            pattern_list.append('Index: ' + str(curr_p) + ' --> '+ self.__create_legends(curr_p))
        return pattern_list

    def compute_correlation(self, pat_inds, environment = None, rot_angles = None, \
                                corr_type = 'envelope'):
        '''
        Calculates the correlation coefficient between two radiation Patterns. The Patterns are
        specified as a vector of indexes and the output is a matrix with correlation values for each
        pattern index correlated with all others. This way, the diagomal of the matrix is always 1
        since it corresponds to correlation with self.

        Arguments:
            pat_inds (list): a list of the Patterns to be correlated
            environment (tuple): This is a tuple of two objects - a string and a dict. The \
                environment string for the power distribution function and its parameters. \
                Currently this is NOT used and always defaults to isotropic with XPD 1.
            rot_angles (tuple): tuple of the rotation angles as for all other functions. Based on\
                these the environment will be rotated similar to a radiation pattern and the\
                correlation will be computed afterwards. Since current environment is only \
                isotropic this makes no difference.
            corr_type (str): correlation to be returned. Default is ``envelope`` correlation. Also\
                possible is ``complex``.

        Returns:
            array: an array containing the correlation values - see example.

        Example:
            An example output is given in the table below, where the diagonal is always one. \
            This example is with the ``envelope`` output option.

            +--------+--------+--------+--------+--------+
            |        | pat1   |  pat2  |  pat3  |  pat4  |
            +========+========+========+========+========+
            |  pat1  |  1     |  0.5   |  0.2   |  0.6   |
            +--------+--------+--------+--------+--------+
            |  pat2  |  0.5   |  1     |  0.7   |  0.6   |
            +--------+--------+--------+--------+--------+
            |  pat3  |  0.2   |  0.7   |  1     |  0.8   |
            +--------+--------+--------+--------+--------+
            |  pat4  |  0.6   |  0.6   |  0.8   |  1     |
            +--------+--------+--------+--------+--------+
        '''
        # Make sure to equalize the resolutions first via interpolation
        far_fields = self.__interpolate(pat_inds)

        # Generate the environment power distribution function
        env_pdp, xpd = includes.field_operations.generate_environment(environment, \
                                                 shape = [far_fields[0].shape[1], \
                                                          far_fields[0].shape[2]])
        env_pdp = includes.field_operations.rotate(env_pdp, rot_angles)

        corr_table=np.zeros((far_fields.__len__(),far_fields.__len__()), dtype=complex)
        corr_table[:] = np.nan

        for ind_1 in range(far_fields.__len__()):
            for ind_2 in range(far_fields.__len__()):

                corr_table[ind_1,ind_2] = includes.field_operations.corelation_calculation(\
                                                                        far_fields[ind_1], \
                                                                        far_fields[ind_2], \
                                                                        env_pdp, xpd)

        if corr_type == 'envelope':
            corr_table = np.abs(corr_table)**2

        return corr_table

    def remove_phase(self, pat_ind):
        '''
        Warning:
            This method does a very artificial operation on a radiation pattern. Use with CARE!

        This method takes a pattern, removes all pahse information from teh electric fields (makes
        them all zeros) and appends the new pattern as new.

        Arguments:
            pat_ind (int): the index of the pattern to be copied and altered
        Returns:
            int: appends a new Patterns to the structure and returns the new index
        '''
        new_pat = self.patterns[pat_ind].copy()
        components = includes.field_operations.get_far_field_components(new_pat['ff'])
        components[1] = np.zeros(components[1].shape, dtype=complex)
        components[3] = np.zeros(components[3].shape, dtype=complex)
        new_pat['ff'] = includes.field_operations.combine_far_field_components(components)
        new_pat['file'] = 'PHASE REMOVED --> ' + new_pat['file']
        self.patterns.append(new_pat)

        return len(self.patterns)-1
