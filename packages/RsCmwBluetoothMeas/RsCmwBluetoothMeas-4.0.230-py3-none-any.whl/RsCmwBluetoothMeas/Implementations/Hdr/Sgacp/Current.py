from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Bursts_Out_Of_Tol: float: No parameter help available
			- Nominal_Power: float: No parameter help available
			- Ptx_Ref: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Bursts_Out_Of_Tol'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Ptx_Ref')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Bursts_Out_Of_Tol: float = None
			self.Nominal_Power: float = None
			self.Ptx_Ref: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:HDR:SGACp[:CURRent] \n
		Snippet: value: ResultData = driver.hdr.sgacp.current.read() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:HDR:SGACp:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:HDR:SGACp[:CURRent] \n
		Snippet: value: ResultData = driver.hdr.sgacp.current.fetch() \n
		No command help available \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:HDR:SGACp:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Bursts_Out_Of_Tol: float or bool: No parameter help available
			- Nominal_Power: float or bool: No parameter help available
			- Ptx_Ref: float or bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Bursts_Out_Of_Tol'),
			ArgStruct.scalar_float_ext('Nominal_Power'),
			ArgStruct.scalar_float_ext('Ptx_Ref')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Bursts_Out_Of_Tol: float or bool = None
			self.Nominal_Power: float or bool = None
			self.Ptx_Ref: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:HDR:SGACp[:CURRent] \n
		Snippet: value: CalculateStruct = driver.hdr.sgacp.current.calculate() \n
		No command help available \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:HDR:SGACp:CURRent?', self.__class__.CalculateStruct())
