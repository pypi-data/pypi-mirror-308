from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsoundingCls:
	"""Csounding commands group definition. 47 total commands, 5 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csounding", core, parent)

	@property
	def comSettings(self):
		"""comSettings commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_comSettings'):
			from .ComSettings import ComSettingsCls
			self._comSettings = ComSettingsCls(self._core, self._cmd_group)
		return self._comSettings

	@property
	def result(self):
		"""result commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	@property
	def scount(self):
		"""scount commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_scount'):
			from .Scount import ScountCls
			self._scount = ScountCls(self._core, self._cmd_group)
		return self._scount

	@property
	def inputSignal(self):
		"""inputSignal commands group. 2 Sub-classes, 18 commands."""
		if not hasattr(self, '_inputSignal'):
			from .InputSignal import InputSignalCls
			self._inputSignal = InputSignalCls(self._core, self._cmd_group)
		return self._inputSignal

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	# noinspection PyTypeChecker
	def get_cprotocol(self) -> enums.CommProtocol:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:CPRotocol \n
		Snippet: value: enums.CommProtocol = driver.configure.csounding.get_cprotocol() \n
		No command help available \n
			:return: comm_protocol: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:CPRotocol?')
		return Conversions.str_to_scalar_enum(response, enums.CommProtocol)

	def set_cprotocol(self, comm_protocol: enums.CommProtocol) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:CPRotocol \n
		Snippet: driver.configure.csounding.set_cprotocol(comm_protocol = enums.CommProtocol.HCI) \n
		No command help available \n
			:param comm_protocol: No help available
		"""
		param = Conversions.enum_scalar_to_str(comm_protocol, enums.CommProtocol)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:CPRotocol {param}')

	# noinspection PyTypeChecker
	def get_hw_interface(self) -> enums.HwInterface:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:HWINterface \n
		Snippet: value: enums.HwInterface = driver.configure.csounding.get_hw_interface() \n
		No command help available \n
			:return: hw_interface: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:HWINterface?')
		return Conversions.str_to_scalar_enum(response, enums.HwInterface)

	def set_hw_interface(self, hw_interface: enums.HwInterface) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:HWINterface \n
		Snippet: driver.configure.csounding.set_hw_interface(hw_interface = enums.HwInterface.NONE) \n
		No command help available \n
			:param hw_interface: No help available
		"""
		param = Conversions.enum_scalar_to_str(hw_interface, enums.HwInterface)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:HWINterface {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:MOEXception \n
		Snippet: value: bool = driver.configure.csounding.get_mo_exception() \n
		Specifies whether measurement results that are identified as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON ON: Results are never rejected. OFF: Faulty results are rejected.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:MOEXception \n
		Snippet: driver.configure.csounding.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that are identified as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON ON: Results are never rejected. OFF: Faulty results are rejected.
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:MOEXception {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.csounding.get_repetition() \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:return: repetition: ALL | SINGle SINGle: Single-shot measurement ALL: Continuous measurement
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:REPetition \n
		Snippet: driver.configure.csounding.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Specifies the repetition mode of the measurement. The repetition mode specifies whether the measurement is stopped after
		a single shot or repeated continuously. Use CONFigure:..:MEAS<i>:...:SCOunt to determine the number of measurement
		intervals per single shot. \n
			:param repetition: ALL | SINGle SINGle: Single-shot measurement ALL: Continuous measurement
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:REPetition {param}')

	def clone(self) -> 'CsoundingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsoundingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
