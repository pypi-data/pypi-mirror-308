from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MinimumCls:
	"""Minimum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("minimum", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float or bool: float | ON | OFF Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#PowerVsTime CMDLINKRESOLVED]) exceeding the specified limits, see [CMDLINKRESOLVED Configure.MultiEval.Limit.LowEnergy.Le1M.PowerVsTime#set CMDLINKRESOLVED]. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float or bool: float Average power during the carrier-on state Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Peak_Power: float or bool: float Peak power Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Leakage_Power: float or bool: float Leakage power Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Peak_Min_Avg_Pow: float or bool: float Difference between the peak power and the average power in the burst Range: -128.0 dBm to 30.0 dBm , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Out_Of_Tol'),
			ArgStruct.scalar_float_ext('Nominal_Power'),
			ArgStruct.scalar_float_ext('Peak_Power'),
			ArgStruct.scalar_float_ext('Leakage_Power'),
			ArgStruct.scalar_float_ext('Peak_Min_Avg_Pow')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float or bool = None
			self.Nominal_Power: float or bool = None
			self.Peak_Power: float or bool = None
			self.Leakage_Power: float or bool = None
			self.Peak_Min_Avg_Pow: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:NMODe:LENergy[:LE1M]:MINimum \n
		Snippet: value: CalculateStruct = driver.multiEval.powerVsTime.nmode.lowEnergy.le1M.minimum.calculate() \n
		Returns the current, average, min, and max power results for LE normal mode. Commands for uncoded LE 1M PHY (..:LE1M..) ,
		LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. The values described below are returned by FETCh
		and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:NMODe:LENergy:LE1M:MINimum?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ReadStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float or bool: float | ON | OFF Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#PowerVsTime CMDLINKRESOLVED]) exceeding the specified limits, see [CMDLINKRESOLVED Configure.MultiEval.Limit.LowEnergy.Le1M.PowerVsTime#set CMDLINKRESOLVED]. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Peak_Power: float: float Peak power Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Leakage_Power: float: float Leakage power Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Peak_Min_Avg_Pow: float: float Difference between the peak power and the average power in the burst Range: -128.0 dBm to 30.0 dBm , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Leakage_Power'),
			ArgStruct.scalar_float('Peak_Min_Avg_Pow')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float or bool = None
			self.Nominal_Power: float = None
			self.Peak_Power: float = None
			self.Leakage_Power: float = None
			self.Peak_Min_Avg_Pow: float = None

	def read(self) -> ReadStruct:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:NMODe:LENergy[:LE1M]:MINimum \n
		Snippet: value: ReadStruct = driver.multiEval.powerVsTime.nmode.lowEnergy.le1M.minimum.read() \n
		Returns the current, average, min, and max power results for LE normal mode. Commands for uncoded LE 1M PHY (..:LE1M..) ,
		LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. The values described below are returned by FETCh
		and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ReadStruct structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:NMODe:LENergy:LE1M:MINimum?', self.__class__.ReadStruct())

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float: float | ON | OFF Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#PowerVsTime CMDLINKRESOLVED]) exceeding the specified limits, see [CMDLINKRESOLVED Configure.MultiEval.Limit.LowEnergy.Le1M.PowerVsTime#set CMDLINKRESOLVED]. Range: 0 % to 100 %, Unit: %
			- Nominal_Power: float: float Average power during the carrier-on state Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Peak_Power: float: float Peak power Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Leakage_Power: float: float Leakage power Range: -128.0 dBm to 30.0 dBm , Unit: dBm
			- Peak_Min_Avg_Pow: float: float Difference between the peak power and the average power in the burst Range: -128.0 dBm to 30.0 dBm , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Peak_Power'),
			ArgStruct.scalar_float('Leakage_Power'),
			ArgStruct.scalar_float('Peak_Min_Avg_Pow')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Peak_Power: float = None
			self.Leakage_Power: float = None
			self.Peak_Min_Avg_Pow: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:NMODe:LENergy[:LE1M]:MINimum \n
		Snippet: value: FetchStruct = driver.multiEval.powerVsTime.nmode.lowEnergy.le1M.minimum.fetch() \n
		Returns the current, average, min, and max power results for LE normal mode. Commands for uncoded LE 1M PHY (..:LE1M..) ,
		LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. The values described below are returned by FETCh
		and READ commands. CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:PVTime:NMODe:LENergy:LE1M:MINimum?', self.__class__.FetchStruct())
