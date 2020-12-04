import unittest
from intcomputer import IntComputer


class TestIntComputer(unittest.TestCase):
    def test_some(self):
        # Test cases from scul repo
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
        IntComputer(program, [7]).run()
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i == 8))

        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i < 8))

        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i == 8))

        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i < 8))

        for i in [0, 1, -2]:
            program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(), (i != 0))

            program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
            computer = IntComputer(program, [i])
            computer.run()
            self.assertEqual(computer.pop_output(),  (i != 0))

        program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125,
                   20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        a = {7: 999, 8: 1000, 9: 1001}
        for i in [7, 8, 9]:
            computer = IntComputer(program, [i])
            computer.run()
            assert computer.pop_output() == a[i]

    # Test cases from Day 9

    def test_day9_test1(self):
        program = [109, 1, 204, -1, 1001, 100, 1,
                   100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        computer = IntComputer(program, [1])
        computer.run()
        self.assertTrue(computer.output_buffer == [
                        109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])

    def test_day9_test2(self):
        program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        computer = IntComputer(program, [1])
        computer.run()
        self.assertTrue(len(str(computer.pop_output())) == 16)

    def test_day9_test3(self):
        program = [104, 1125899906842624, 99]
        computer = IntComputer(program, [1])
        computer.run()
        self.assertTrue(computer.output_buffer == [1125899906842624])
