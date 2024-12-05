from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1MCls:
	"""Le1M commands group definition. 6 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le1M", core, parent)

	@property
	def sacp(self):
		"""sacp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sacp'):
			from .Sacp import SacpCls
			self._sacp = SacpCls(self._core, self._cmd_group)
		return self._sacp

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .PowerVsTime import PowerVsTimeCls
			self._powerVsTime = PowerVsTimeCls(self._core, self._cmd_group)
		return self._powerVsTime

	@property
	def faccuracy(self):
		"""faccuracy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_faccuracy'):
			from .Faccuracy import FaccuracyCls
			self._faccuracy = FaccuracyCls(self._core, self._cmd_group)
		return self._faccuracy

	@property
	def foffset(self):
		"""foffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_foffset'):
			from .Foffset import FoffsetCls
			self._foffset = FoffsetCls(self._core, self._cmd_group)
		return self._foffset

	@property
	def mratio(self):
		"""mratio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mratio'):
			from .Mratio import MratioCls
			self._mratio = MratioCls(self._core, self._cmd_group)
		return self._mratio

	# noinspection PyTypeChecker
	class FdriftStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Fields: \n
			- Frequency_Drift: float: numeric Range: 0 Hz to 250 kHz, Unit: Hz
			- Max_Drift_Rate: float: numeric Range: 0 Hz to 250 kHz, Unit: Hz/50 us (LE coded PHY: Hz/48 us)
			- Initl_Freq_Drift: float: numeric Range: 0 Hz to 250 kHz, Unit: Hz
			- Freq_Drift_Enable: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values) .
			- Max_Drift_Rate_Enb: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values) .
			- Init_Freq_Drift_En: List[bool]: OFF | ON Disable or enable limit checking for current, average, and maximum results (3 values) ."""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency_Drift'),
			ArgStruct.scalar_float('Max_Drift_Rate'),
			ArgStruct.scalar_float('Initl_Freq_Drift'),
			ArgStruct('Freq_Drift_Enable', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Max_Drift_Rate_Enb', DataType.BooleanList, None, False, False, 3),
			ArgStruct('Init_Freq_Drift_En', DataType.BooleanList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency_Drift: float = None
			self.Max_Drift_Rate: float = None
			self.Initl_Freq_Drift: float = None
			self.Freq_Drift_Enable: List[bool] = None
			self.Max_Drift_Rate_Enb: List[bool] = None
			self.Init_Freq_Drift_En: List[bool] = None

	def get_fdrift(self) -> FdriftStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FDRift \n
		Snippet: value: FdriftStruct = driver.configure.multiEval.limit.lowEnergy.le1M.get_fdrift() \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: structure: for return value, see the help for FdriftStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FDRift?', self.__class__.FdriftStruct())

	def set_fdrift(self, value: FdriftStruct) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy[:LE1M]:FDRift \n
		Snippet with structure: \n
		structure = driver.configure.multiEval.limit.lowEnergy.le1M.FdriftStruct() \n
		structure.Frequency_Drift: float = 1.0 \n
		structure.Max_Drift_Rate: float = 1.0 \n
		structure.Initl_Freq_Drift: float = 1.0 \n
		structure.Freq_Drift_Enable: List[bool] = [True, False, True] \n
		structure.Max_Drift_Rate_Enb: List[bool] = [True, False, True] \n
		structure.Init_Freq_Drift_En: List[bool] = [True, False, True] \n
		driver.configure.multiEval.limit.lowEnergy.le1M.set_fdrift(value = structure) \n
		Sets and enables limits for frequency drift, maximum drift rate and initial frequency drift. Commands for uncoded LE 1M
		PHY (..:LE1M..) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param value: see the help for FdriftStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LE1M:FDRift', value)

	def clone(self) -> 'Le1MCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Le1MCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
