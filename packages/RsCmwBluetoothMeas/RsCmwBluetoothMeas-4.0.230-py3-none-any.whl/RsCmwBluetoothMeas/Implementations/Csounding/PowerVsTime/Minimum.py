from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MinimumCls:
	"""Minimum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("minimum", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Steps_Out_Of_Tol: float: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.Csounding.Scount#Power CMDLINKRESOLVED]) exceeding the specified limits ([CMDLINKRESOLVED Configure.Csounding.Limit#Power CMDLINKRESOLVED]) . Range: 1 Steps to 1000 Steps
			- Average_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm
			- Power_Cssync: float: float Range: -99.99 dBm to 99.99 dBm
			- Power_Tpm: float: float Range: -99.99 dBm to 99.99 dBm
			- Power_Leakage: float: float Range: -99.99 dBm to 99.99 dBm
			- Ramp_Up: float: float Range: 0 us to 9.99 us
			- Ramp_Down: float: float Range: 0 us to 9.99 us"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Steps_Out_Of_Tol'),
			ArgStruct.scalar_float('Average_Power'),
			ArgStruct.scalar_float('Power_Cssync'),
			ArgStruct.scalar_float('Power_Tpm'),
			ArgStruct.scalar_float('Power_Leakage'),
			ArgStruct.scalar_float('Ramp_Up'),
			ArgStruct.scalar_float('Ramp_Down')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Steps_Out_Of_Tol: float = None
			self.Average_Power: float = None
			self.Power_Cssync: float = None
			self.Power_Tpm: float = None
			self.Power_Leakage: float = None
			self.Ramp_Up: float = None
			self.Ramp_Down: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:PVTime:MINimum \n
		Snippet: value: ResultData = driver.csounding.powerVsTime.minimum.read() \n
		Returns the power vs time scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:PVTime:MINimum?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:PVTime:MINimum \n
		Snippet: value: ResultData = driver.csounding.powerVsTime.minimum.fetch() \n
		Returns the power vs time scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:PVTime:MINimum?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Steps_Out_Of_Tol: float or bool: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.Csounding.Scount#Power CMDLINKRESOLVED]) exceeding the specified limits ([CMDLINKRESOLVED Configure.Csounding.Limit#Power CMDLINKRESOLVED]) . Range: 1 Steps to 1000 Steps
			- Average_Power: float or bool: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm
			- Power_Cssync: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Power_Tpm: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Power_Leakage: float or bool: float Range: -99.99 dBm to 99.99 dBm
			- Ramp_Up: float or bool: float Range: 0 us to 9.99 us
			- Ramp_Down: float or bool: float Range: 0 us to 9.99 us"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Steps_Out_Of_Tol'),
			ArgStruct.scalar_float_ext('Average_Power'),
			ArgStruct.scalar_float_ext('Power_Cssync'),
			ArgStruct.scalar_float_ext('Power_Tpm'),
			ArgStruct.scalar_float_ext('Power_Leakage'),
			ArgStruct.scalar_float_ext('Ramp_Up'),
			ArgStruct.scalar_float_ext('Ramp_Down')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Steps_Out_Of_Tol: float or bool = None
			self.Average_Power: float or bool = None
			self.Power_Cssync: float or bool = None
			self.Power_Tpm: float or bool = None
			self.Power_Leakage: float or bool = None
			self.Ramp_Up: float or bool = None
			self.Ramp_Down: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:PVTime:MINimum \n
		Snippet: value: CalculateStruct = driver.csounding.powerVsTime.minimum.calculate() \n
		Returns the power vs time scalar results. The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:PVTime:MINimum?', self.__class__.CalculateStruct())
