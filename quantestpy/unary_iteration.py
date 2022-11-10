import copy
import unittest

import numpy as np

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError

ut_test_case = unittest.TestCase()


def _get_qubit_idx_to_ctrl_val_for_given_val_in_select_reg(
        val_in_select_reg: str,
        ftc: FastTestCircuit,
        select_reg: list,
        ancilla_reg: list) -> dict:

    # init ancilla reg to 0
    ftc.set_qubit_value(ancilla_reg, [0] * len(ancilla_reg))
    # init select reg to val_in_select_reg
    ftc.set_qubit_value(select_reg, [int(i) for i in val_in_select_reg])

    # get ctrl vals for all ops on syst reg
    qubit_idx_to_ctrl_val = {idx: [] for idx in select_reg + ancilla_reg}
    for i, gate in enumerate(ftc._gates):

        ctrl_qubit_idx_for_one_op = gate["control_qubit"]
        ctrl_qubit_val_for_one_op = \
            ftc._qubit_value[ctrl_qubit_idx_for_one_op].tolist()

        for j, ctrl_qubit_idx in enumerate(ctrl_qubit_idx_for_one_op):
            if ctrl_qubit_idx in qubit_idx_to_ctrl_val.keys():
                qubit_idx_to_ctrl_val[ctrl_qubit_idx].append(
                    ctrl_qubit_val_for_one_op[j])

        ftc._execute_i_th_gate(i)

    return qubit_idx_to_ctrl_val


def assert_get_ctrl_val(
        circuit: FastTestCircuit,
        select_reg: list,
        ancilla_reg: list = [],
        assert_is_ancilla_uncomputated: bool = False,
        verbose: bool = True) -> dict:

    # check inputs
    FastTestCircuit._assert_is_fast_test_circuit(circuit, "Input circuit")
    ftc = copy.deepcopy(circuit)
    ftc._assert_is_correct_reg(select_reg, "select_reg")
    ftc._assert_is_correct_reg(ancilla_reg, "ancilla_reg")
    if not isinstance(assert_is_ancilla_uncomputated, bool):
        raise QuantestPyError(
            "assert_is_ancilla_uncomputated must be bool type."
        )
    if not isinstance(verbose, bool):
        raise QuantestPyError(
            "verbose must be bool type."
        )

    len_select_reg = len(select_reg)
    qubit_idx_to_val_in_select_reg_to_ctrl_val = \
        {idx: dict() for idx in select_reg + ancilla_reg}

    for dec_val_in_select_reg in range(2**len_select_reg):

        bin_val_in_select_reg = \
            ("0" * len_select_reg + bin(dec_val_in_select_reg)[2:])[
                -len_select_reg:]

        qubit_idx_to_ctrl_val = \
            _get_qubit_idx_to_ctrl_val_for_given_val_in_select_reg(
                bin_val_in_select_reg,
                ftc,
                select_reg,
                ancilla_reg
            )

        if assert_is_ancilla_uncomputated:
            if not np.all(ftc._qubit_value[ancilla_reg] == 0):
                err_msg = "ancilla reg is not uncomputated to 0 " \
                    + f"when val in select reg is {bin_val_in_select_reg}."
                raise QuantestPyAssertionError(err_msg)

        if verbose:
            print(f"val in select reg: {bin_val_in_select_reg},",
                  f"qubit idx to ctrl val: {qubit_idx_to_ctrl_val}")

        for qubit_idx, ctrl_val in qubit_idx_to_ctrl_val.items():
            tmp_dict = qubit_idx_to_val_in_select_reg_to_ctrl_val[qubit_idx]
            tmp_dict[bin_val_in_select_reg] = ctrl_val
            qubit_idx_to_val_in_select_reg_to_ctrl_val[qubit_idx] = tmp_dict

    return qubit_idx_to_val_in_select_reg_to_ctrl_val
