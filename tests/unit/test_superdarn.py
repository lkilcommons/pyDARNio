# Copyright (C) 2019 SuperDARN Canada, University of Saskatchewan
# Author: Marina Schmidt, Angeline Burrell
"""
This test suite is to test the implementation for the following classes:
    SDarnRead
    DarnUtilities
    SDarnWrite
Support for the following SuperDARN file types:
    iqdat
    rawacf
    fitacf
    grid
    map
"""

import copy
import collections
import logging
import numpy as np
import os
import unittest

import pyDARNio
from pyDARNio import superdarn_exceptions as sdarn_exp

import map_data_sets
import grid_data_sets
import fitacf_data_sets
import iqdat_data_sets
import rawacf_data_sets
import tfile_utils

pydarnio_logger = logging.getLogger('pydarnio')


class TestSDarnRead(tfile_utils.TestRead):
    """
    Testing class for SDarnRead class
    """
    def setUp(self):
        self.test_file = "somefile.rawacf"
        self.test_dir = os.path.join("..", "testfiles")
        self.data = None
        self.rec = None
        self.read_func = pyDARNio.SDarnRead
        self.file_types = ["rawacf", "fitacf", "iqdat", "grid", "map"]
        self.corrupt_read_type = "rawacf"

    def tearDown(self):
        del self.test_file, self.test_dir, self.data, self.rec
        del self.read_func, self.file_types, self.corrupt_read_type

    def test_read_iqdat(self):
        """
        Test reading records from iqdat.

        Checks:
            - returns correct data structures
            - returns expected values
        """
        if not os.path.isdir(self.test_dir):
            self.skipTest('test directory is not included with pyDARNio')

        # Load the data and read in the first record
        test_file_dict = tfile_utils.get_test_files("good",
                                                    test_dir=self.test_dir)
        self.test_file = test_file_dict['iqdat']
        self.load_file_record(file_type='iqdat')

        # Test the first record
        self.assertIsInstance(self.rec, collections.deque)
        self.assertIsInstance(self.rec[0], collections.OrderedDict)
        self.assertIsInstance(self.rec[0]['rxrise'], pyDARNio.DmapScalar)
        self.assertIsInstance(self.rec[3]['tsc'], pyDARNio.DmapArray)
        self.assertIsInstance(self.rec[5]['mppul'].value, int)
        self.assertIsInstance(self.rec[6]['tnoise'].value, np.ndarray)
        self.assertEqual(self.rec[7]['channel'].value, 0)
        self.assertEqual(self.rec[10]['data'].dimension, 1)

    def test_read_rawacf(self):
        """
        Test reading records from rawacf.

        Checks:
            - returns correct data structures
            - returns expected values
        """
        if not os.path.isdir(self.test_dir):
            self.skipTest('test directory is not included with pyDARNio')

        # Load the data and read in the first record
        test_file_dict = tfile_utils.get_test_files("good",
                                                    test_dir=self.test_dir)
        self.test_file = test_file_dict['rawacf']
        self.load_file_record(file_type='rawacf')

        # Test the first record
        self.assertIsInstance(self.rec, collections.deque)
        self.assertIsInstance(self.rec[0], collections.OrderedDict)
        self.assertIsInstance(self.rec[4]['channel'], pyDARNio.DmapScalar)
        self.assertIsInstance(self.rec[1]['ptab'], pyDARNio.DmapArray)
        self.assertIsInstance(self.rec[7]['channel'].value, int)
        self.assertIsInstance(self.rec[2]['xcfd'].value, np.ndarray)
        self.assertEqual(self.rec[0]['xcfd'].dimension, 3)

    def test_read_fitacf(self):
        """
        Test reading records from fitacf.

        Checks:
            - returns correct data structures
            - returns expected values
        """
        if not os.path.isdir(self.test_dir):
            self.skipTest('test directory is not included with pyDARNio')

        # Load the data and read in the first record
        test_file_dict = tfile_utils.get_test_files("good",
                                                    test_dir=self.test_dir)
        self.test_file = test_file_dict['fitacf']
        self.load_file_record(file_type='fitacf')

        # Test the first record
        self.assertIsInstance(self.rec, collections.deque)
        self.assertIsInstance(self.rec[0], collections.OrderedDict)
        self.assertIsInstance(self.rec[4]['bmnum'], pyDARNio.DmapScalar)
        self.assertIsInstance(self.rec[1]['ptab'], pyDARNio.DmapArray)
        self.assertIsInstance(self.rec[7]['channel'].value, int)
        self.assertIsInstance(self.rec[2]['ltab'].value, np.ndarray)
        self.assertEqual(self.rec[0]['ptab'].dimension, 1)

    def test_read_grid(self):
        """
        Test reading records from grid file.

        Checks:
            - returns correct data structures
            - returns expected values
        """
        if not os.path.isdir(self.test_dir):
            self.skipTest('test directory is not included with pyDARNio')

        # Load the data and read in the first record
        test_file_dict = tfile_utils.get_test_files("good",
                                                    test_dir=self.test_dir)
        self.test_file = test_file_dict['grid']
        self.load_file_record(file_type='grid')

        # Test the first record
        self.assertIsInstance(self.rec, collections.deque)
        self.assertIsInstance(self.rec[0], collections.OrderedDict)
        self.assertIsInstance(self.rec[4]['start.year'], pyDARNio.DmapScalar)
        self.assertIsInstance(self.rec[1]['v.max'], pyDARNio.DmapArray)
        self.assertIsInstance(self.rec[7]['end.day'].value, int)
        self.assertIsInstance(self.rec[2]['stid'].value, np.ndarray)
        self.assertEqual(self.rec[0]['nvec'].dimension, 1)

    def test_read_map(self):
        """
        Test reading records from map file.

        Checks:
            - returns correct data structures
            - returns expected values
        """
        if not os.path.isdir(self.test_dir):
            self.skipTest('test directory is not included with pyDARNio')

        # Load the data and read in the first record
        test_file_dict = tfile_utils.get_test_files("good",
                                                    test_dir=self.test_dir)
        self.test_file = test_file_dict['map']
        self.load_file_record(file_type='map')

        # Test the first record
        self.assertIsInstance(self.rec, collections.deque)
        self.assertIsInstance(self.rec[0], collections.OrderedDict)
        self.assertIsInstance(self.rec[2]['IMF.flag'],
                              pyDARNio.io.datastructures.DmapScalar)
        self.assertIsInstance(self.rec[3]['stid'], pyDARNio.DmapArray)
        self.assertIsInstance(self.rec[8]['IMF.flag'].value, int)
        self.assertIsInstance(self.rec[10]['stid'].value, np.ndarray)
        self.assertEqual(self.rec[3]['stid'].dimension, 1)
        # this will be file dependent... future working test project.
        self.assertEqual(self.rec[0]['stid'].shape[0], 14)


class TestSDarnUtilities(unittest.TestCase):
    """
    Testing DarnUtilities class.

    Notes
    -----
    All methods in this class are static so there is no constructor testing
    """
    def setUp(self):
        self.tdicts = [{'a': 's', 'c': 'i', 'd': 'f'},
                       {'rst': '4.1', 'stid': 3, 'vel': [2.3, 4.5]},
                       {'fitacf': 'f', 'rawacf': 's', 'map': 'm'}]

    def tearDown(self):
        del self.tdicts

    def test_dict_key_diff(self):
        """
        Test the difference in keys between two dictionaries, order dependent
        """
        self.tdicts[1] = {'1': 'a', 'c': 2, 'z': 'fun', 'd': 'dog'}

        for val in [(self.tdicts[0], self.tdicts[1], {'a'}),
                    (self.tdicts[1], self.tdicts[0], {'1', 'z'})]:
            with self.subTest(val=val):
                out = pyDARNio.SDarnUtilities.dict_key_diff(val[0], val[1])
                self.assertEqual(val[2], out)

    def test_dict_list2set(self):
        """
        Test conversion of lists of dictionaries into concatenated full sets

        Expected behaviour
        ------------------
        Returns only a single set the comprises of the dictionary keys
        given in the list
        """
        dict_keys = {'a', 'c', 'd', 'rst', 'stid', 'vel', 'fitacf', 'rawacf',
                     'map'}
        out = pyDARNio.SDarnUtilities.dict_list2set(self.tdicts)
        self.assertEqual(dict_keys, out)

    def test_extra_field_check_pass(self):
        """
        Test extra_field_check success

        Method - this method checks if there are differences in the key sets of
        dictionaries that when passed a record and field names it will indicate
        if there is an extra field in the record key set

        Expected behaviour
        ------------------
        Silent success - if there are no differences in the key set then
        nothing is returned or raised
        """
        out = {'a': 3, 'c': 3, 'd': 3, 'rst': 1, 'vel': 'd'}
        pyDARNio.SDarnUtilities.extra_field_check(self.tdicts, out, 1)

    def test_extra_field_check_fail(self):
        """
        Test extra_field_check failur raises SuperDARNExtraFieldError

        Method - this method checks if there are  differences in the key sets
        of dictionaries that when passed a record and field names it will
        indicate if there is an extra field in the record key set

        Expected behaviour
        -----------------
        Raises SuperDARNExtraFieldError because there are differences between
        the two dictionary sets
        """
        out = {'a': 3, 'b': 3, 'c': 2, 'd': 3, 'rst': 1, 'vel': 'd'}
        with self.assertRaises(sdarn_exp.SuperDARNExtraFieldError) as err:
            pyDARNio.SDarnUtilities.extra_field_check(self.tdicts, out, 1)

        self.assertEqual(err.exception.fields, {'b'})

    def test_missing_field_check_pass(self):
        """
        Testing missing_field_check - Reverse idea of the extra_field_check,
        should find missing fields in a record when compared to a key set of
        SuperDARN field names

        Expected behaviour
        ------------------
        Nothing - if there is not differences then nothing happens
        """
        in_list = [dict(self.tdicts[0]),
                   {'a': 3, 'c': 2, 'd': 2, 'stid': 's', 'rst': 1, 'vel': 'd'},
                   dict(self.tdicts[1])]
        in_list[0].update(self.tdicts[-1])
        in_list[2].update(self.tdicts[2])
        for val in in_list:
            with self.subTest(val=val):
                pyDARNio.SDarnUtilities.missing_field_check(self.tdicts,
                                                            val, 1)

    def test_missing_field_check_fail(self):
        """
        Test raises SuperDARNFieldMissingError with appropriate fields missing

        Method - Reverse idea of the extra_field_check, should find missing
        fields in a record when compared to a key set of SuperDARN field names

        Expected behaviour
        ------------------
        Raise SuperDARNFieldMissingError - raised when there is a difference
        between dictionary key sets
        """
        in_list = [({'a': 3, 'b': 3, 'd': 2, 'stid': 's', 'vel': 'd'},
                    {'c', 'rst'}),
                   ({'a': 3, 'b': 3, 'd': 2, 'stid': 's', 'rst': 1,
                     'vel': 'd', 'fitacf': 3, 'map': 4}, {'c', 'rawacf'})]

        for val in in_list:
            with self.subTest(val=val):
                with self.assertRaises(
                        sdarn_exp.SuperDARNFieldMissingError) as err:
                    pyDARNio.SDarnUtilities.missing_field_check(self.tdicts,
                                                                val[0], 1)

                # Items in tdicts, but not in rdict
                self.assertEqual(err.exception.fields, val[1])

    def test_incorrect_types_check_pass(self):
        """
        Test incorrect_types_check - this method checks if the field data
        format type is not correct to specified SuperDARN field type.

        Note
        ----
        This method only works on pyDARNio DMAP record data structure

        Expected Behaviour
        ------------------
        Nothing - should not return or raise anything if the fields
        are the correct data format type
        """
        rdict = {'a': pyDARNio.DmapScalar('a', 1, 1, self.tdicts[0]['a']),
                 'c': pyDARNio.DmapScalar('a', 1, 1, self.tdicts[0]['c']),
                 'd': pyDARNio.DmapArray('a', np.array([2.4, 2.4]), 1,
                                         self.tdicts[0]['d'], 1, [3]),
                 'fitacf': pyDARNio.DmapScalar('a', 1, 1,
                                               self.tdicts[-1]['fitacf']),
                 'rawacf': pyDARNio.DmapScalar('a', 1, 1,
                                               self.tdicts[-1]['rawacf']),
                 'map': pyDARNio.DmapScalar('a', 1, 1,
                                            self.tdicts[-1]['map'])}

        pyDARNio.SDarnUtilities.incorrect_types_check([self.tdicts[0],
                                                       self.tdicts[-1]],
                                                      rdict, 1)

    def test_incorrect_types_check_fail(self):
        """
        Test incorrect_types_check - this method checks if the field data
        format type is not correct to specified SuperDARN field type.

        Note
        ----
        This method only works on pyDARNio DMAP record data structure

        Expected Behaviour
        ------------------
        Raises SuperDARNDataFormatTypeError - because the field format types
        should not be the same.
        """
        rdict = {'a': pyDARNio.DmapScalar('a', 1, 1, self.tdicts[0]['a']),
                 'c': pyDARNio.DmapScalar('a', 1, 1, self.tdicts[0]['c']),
                 'd': pyDARNio.DmapArray('a', np.array([2.4, 2.4]), 1,
                                         self.tdicts[0]['d'], 1, [3]),
                 'fitacf': pyDARNio.DmapScalar('a', 1, 1,
                                               self.tdicts[-1]['rawacf']),
                 'rawacf': pyDARNio.DmapScalar('a', 1, 1,
                                               self.tdicts[-1]['rawacf']),
                 'map': pyDARNio.DmapScalar('a', 1, 1,
                                            self.tdicts[-1]['map'])}

        with self.assertRaises(sdarn_exp.SuperDARNDataFormatTypeError) as err:
            pyDARNio.SDarnUtilities.incorrect_types_check([self.tdicts[0],
                                                           self.tdicts[-1]],
                                                          rdict, 1)

        self.assertEqual(err.exception.incorrect_params, {'fitacf': 'f'})


class TestSDarnWrite(unittest.TestCase):
    """
    Tests SDarnWrite class
    """
    def setUp(self):
        """ Runs before every test to create the test environment
        """
        self.write_func = None
        self.data_type = None
        self.data = None
        self.temp_file = "not_a_file.acf"

    def tearDown(self):
        """ Runs after every test to clean up the test environment
        """
        self.remove_temp_file()
        del self.temp_file, self.data, self.data_type, self.write_func

    def load_data_w_filename(self):
        """ Utility for loading data and constructing a temporary filename
        """
        if self.data_type == "rawacf":
            self.data = copy.deepcopy(rawacf_data_sets.rawacf_data)
        elif self.data_type == "fitacf":
            self.data = copy.deepcopy(fitacf_data_sets.fitacf_data)
        elif self.data_type == "iqdat":
            self.data = copy.deepcopy(iqdat_data_sets.iqdat_data)
        elif self.data_type == "grid":
            self.data = copy.deepcopy(grid_data_sets.grid_data)
        elif self.data_type == "map":
            self.data = copy.deepcopy(map_data_sets.map_data)

        self.temp_file = "{:s}_test.{:s}".format(self.data_type,
                                                 self.data_type)

    def remove_temp_file(self):
        """ Utility for removing temporary files
        """
        if os.path.isfile(self.temp_file):
            os.remove(self.temp_file)
            return True
        else:
            return False

    def set_write_func(self):
        """ Utility to retrieve the writing function
        """
        darn = pyDARNio.SDarnWrite(self.data)
        self.write_func = getattr(darn, "write_{:s}".format(self.data_type))

    def test_darn_write_constructor(self):
        """
        Tests SDarnWrite constructor for different file types

        Expected behaviour
        ------------------
        Contains file name of the data if given to it.
        """
        test_file_dict = tfile_utils.get_test_files("good")
        for val in test_file_dict.keys():
            with self.subTest(val=val):
                self.data_type = val
                self.load_data_w_filename()
                darn = pyDARNio.SDarnWrite(self.data, self.temp_file)
                self.assertEqual(darn.filename, self.temp_file)
                self.assertFalse(self.remove_temp_file())

    def test_empty_record(self):
        """
        Test raises DmapDataError if an empty record is given

        TODO: Change this for real-time implementation
        """
        with self.assertRaises(pyDARNio.dmap_exceptions.DmapDataError):
            pyDARNio.SDarnWrite([], self.temp_file)

    def test_incorrect_filename_input_using_write_methods(self):
        """
        Test raises FilenameRequiredError when no filename is given to write
        """
        test_file_dict = tfile_utils.get_test_files("good")
        for val in test_file_dict.keys():
            with self.subTest(val=val):
                self.data_type = val
                self.load_data_w_filename()

                # Attempt to write data without a filename
                self.set_write_func()
                with self.assertRaises(
                        pyDARNio.dmap_exceptions.FilenameRequiredError):
                    self.write_func()

    def test_writing_success(self):
        """
        Test successful file writing and removal of temporary file
        """
        test_file_dict = tfile_utils.get_test_files("good")
        for val in test_file_dict.keys():
            with self.subTest(val=val):
                self.data_type = val
                self.load_data_w_filename()
                self.set_write_func()

                # Only testing the file is created since it should only be
                # created at the last step after all checks have passed.
                # Testing the integrity of the insides of the file will be part
                # of integration testing since we need SDarnRead for that.
                self.write_func(self.temp_file)
                self.assertTrue(self.remove_temp_file())

    def test_SDarnWrite_missing_field(self):
        """
        Test raises SuperDARNFieldMissingError when required data is missing
        """
        missing_fields = {"rawacf": "nave", "fitacf": "stid",
                          "iqdat": "chnnum", "map": "IMF.Kp",
                          "grid": "start.year"}
        rnum = 0

        for val in missing_fields.keys():
            with self.subTest(val=val):
                # Set up the data, removing a required value
                self.data_type = val
                self.load_data_w_filename()
                del self.data[rnum][missing_fields[val]]

                # Attempt to write the data
                self.set_write_func()
                with self.assertRaises(
                        sdarn_exp.SuperDARNFieldMissingError) as err:
                    self.write_func(self.temp_file)

                # Evaluate the error message
                self.assertEqual(err.exception.fields, {missing_fields[val]})
                self.assertEqual(err.exception.record_number, rnum)

    def test_extra_field(self):
        """
        Raises SuperDARNExtraFieldErrorSuperDARNExtraFieldError with extra data
        """
        rnum = 0
        extra_name = "dummy"
        extra_field = pyDARNio.DmapArray(extra_name, np.array([1, 2]), chr(1),
                                         'c', 1, [2])
        test_file_dict = tfile_utils.get_test_files("good")

        for val in test_file_dict.keys():
            with self.subTest(val=val):
                # Set up the data, adding and extra data field
                self.data_type = val
                self.load_data_w_filename()
                self.data[rnum][extra_name] = extra_field

                # Attempt to write the data
                self.set_write_func()
                with self.assertRaises(
                        sdarn_exp.SuperDARNExtraFieldError) as err:
                    self.write_func(self.temp_file)

                # Evaluate the error message
                self.assertEqual(err.exception.fields, {extra_name})
                self.assertEqual(err.exception.record_number, rnum)

    def test_incorrect_data_format(self):
        """
        Test raises SuperDARNDataFormatTypeError for writing with bad format
        """
        rnum = 0
        incorrect_param = {"rawacf": "scan", "fitacf": "ltab",
                           "iqdat": "lagfr", "map": "IMF.Bx", "grid": "v.min"}
        incorrect_type = {"rawacf": "c", "fitacf": "s", "iqdat": "d",
                          "map": "i", "grid": "d"}

        for val in incorrect_type.keys():
            with self.subTest(val=val):
                # Set up the data, adding and extra data field
                self.data_type = val
                self.load_data_w_filename()
                self.data[rnum][incorrect_param[val]] = \
                    self.data[rnum][incorrect_param[val]]._replace(
                        data_type_fmt=incorrect_type[val])

                # Attempt to write the data
                self.set_write_func()
                with self.assertRaises(
                        sdarn_exp.SuperDARNDataFormatTypeError) as err:
                    self.write_func(self.temp_file)

                # Evaluate the error message
                self.assertEqual(err.exception.incorrect_params.keys(),
                                 {incorrect_param[val]})
                self.assertEqual(err.exception.record_number, rnum)
