from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDevCls:
	"""StandardDev commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#Modulation CMDLINKRESOLVED]) exceeding the specified limits, see 'Modulation limits (LE) '. Range: 0 % to 100 %
			- Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 us
			- Freq_Offset: float: float Range: -0.99999 MHz to 0.99999 MHz , Unit: Hz
			- Init_Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Offset'),
			ArgStruct.scalar_float('Init_Freq_Drift')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Offset: float = None
			self.Init_Freq_Drift: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:CTE:LENergy:LE2M:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.modulation.cte.lowEnergy.le2M.standardDev.fetch() \n
		Returns current, average, standard deviation, absolute min (xmin) , absolute max (xmax) , and max CTE modulation results
		for LE uncoded PHY (LE 1M PHY, LE 2M PHY) . The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:CTE:LENergy:LE2M:SDEViation?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float or bool: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#Modulation CMDLINKRESOLVED]) exceeding the specified limits, see 'Modulation limits (LE) '. Range: 0 % to 100 %
			- Freq_Drift: float or bool: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift: float or bool: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 us
			- Freq_Offset: float or bool: float Range: -0.99999 MHz to 0.99999 MHz , Unit: Hz
			- Init_Freq_Drift: float or bool: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Out_Of_Tol'),
			ArgStruct.scalar_float_ext('Freq_Drift'),
			ArgStruct.scalar_float_ext('Max_Drift'),
			ArgStruct.scalar_float_ext('Freq_Offset'),
			ArgStruct.scalar_float_ext('Init_Freq_Drift')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float or bool = None
			self.Freq_Drift: float or bool = None
			self.Max_Drift: float or bool = None
			self.Freq_Offset: float or bool = None
			self.Init_Freq_Drift: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:CTE:LENergy:LE2M:SDEViation \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.cte.lowEnergy.le2M.standardDev.calculate() \n
		Returns current, average, standard deviation, absolute min (xmin) , absolute max (xmax) , and max CTE modulation results
		for LE uncoded PHY (LE 1M PHY, LE 2M PHY) . The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:CTE:LENergy:LE2M:SDEViation?', self.__class__.CalculateStruct())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:CTE:LENergy:LE2M:SDEViation \n
		Snippet: value: ResultData = driver.multiEval.modulation.cte.lowEnergy.le2M.standardDev.read() \n
		Returns current, average, standard deviation, absolute min (xmin) , absolute max (xmax) , and max CTE modulation results
		for LE uncoded PHY (LE 1M PHY, LE 2M PHY) . The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:CTE:LENergy:LE2M:SDEViation?', self.__class__.ResultData())
