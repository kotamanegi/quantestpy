import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawQubitFinalIdentifierAtEnd(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_draw_qubit_final_identifier
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK
    $
    """

    def test_default(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)

        cd.draw_qubit_final_identifier()
        actual = cd._line_id_to_text
        expect = {0: "0",
                  1: " ",
                  2: "1",
                  3: " ",
                  4: "2"}
        self.assertEqual(actual, expect)

    def test_reg_name(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)
        cd._qubit_id_to_output_reg_name = {
            0: "reg_1",
            1: "",
            2: "reg_aa"
        }

        cd.draw_qubit_final_identifier()
        actual = cd._line_id_to_text
        expect = {0: "reg_1  0",
                  1: "        ",
                  2: "       1",
                  3: "        ",
                  4: "reg_aa 2"}
        self.assertEqual(actual, expect)
