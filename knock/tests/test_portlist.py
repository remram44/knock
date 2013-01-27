"""Tests for the dat.gui package.

"""


import unittest

from knock.ports import PortList


class TestPortList(unittest.TestCase):
    def test_portlist(self):
        PortList()

    def test_simplelist(self):
        l = PortList()
        self.assertEqual(len(l._ranges), 0)

    def test_list_basic(self):
        l = PortList()

        self.assertTrue(l.add('42-47'))
        self.assertEqual(l.to_arglist(), ['42-47'])
        self.assertEqual(list(iter(l)), list(xrange(42, 48)))

        self.assertTrue(l.add('101-120'))
        self.assertTrue(l.add('200'))
        self.assertEqual(
                list(iter(l)),
                list(xrange(42, 48)) + list(xrange(101, 121)) + [200])
        self.assertEqual(str(l), '42-47,101-120,200')

    def test_list_compact(self):
        l = PortList()
        self.assertTrue(l.add('42-47'))
        self.assertEqual(l._ranges, [(42, 47)])
        self.assertTrue(l.add('101-120'))
        self.assertEqual(l._ranges, [(42, 47), (101, 120)])
        self.assertTrue(l.add('45-52'))
        self.assertEqual(l._ranges, [(42, 52), (101, 120)])
        self.assertTrue(l.add('53-57'))
        self.assertEqual(l._ranges, [(42, 57), (101, 120)])
        self.assertTrue(l.add('30-44'))
        self.assertEqual(l._ranges, [(30, 57), (101, 120)])

    def test_bad_spec(self):
        l = PortList()
        self.assertRaises(ValueError, l.add, '47-42')
        self.assertFalse(l.add('42-45-47'))
