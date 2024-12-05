from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PlengthCls:
	"""Plength commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("plength", core, parent)

	# noinspection PyTypeChecker
	def get_fixed(self) -> enums.PayloadLengthCs:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:FIXed \n
		Snippet: value: enums.PayloadLengthCs = driver.configure.csounding.inputSignal.plength.get_fixed() \n
		Specifies the payload length in bytes for a fixed pattern. The setting is relevant for main mode 1 and 3. \n
			:return: fixed: B4 | B8 | B12 | B16
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:FIXed?')
		return Conversions.str_to_scalar_enum(response, enums.PayloadLengthCs)

	def set_fixed(self, fixed: enums.PayloadLengthCs) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:FIXed \n
		Snippet: driver.configure.csounding.inputSignal.plength.set_fixed(fixed = enums.PayloadLengthCs.B12) \n
		Specifies the payload length in bytes for a fixed pattern. The setting is relevant for main mode 1 and 3. \n
			:param fixed: B4 | B8 | B12 | B16
		"""
		param = Conversions.enum_scalar_to_str(fixed, enums.PayloadLengthCs)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:FIXed {param}')

	# noinspection PyTypeChecker
	def get_random(self) -> enums.PayloadLengthCs:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:RANDom \n
		Snippet: value: enums.PayloadLengthCs = driver.configure.csounding.inputSignal.plength.get_random() \n
		Specifies the payload length in bytes for a random pattern. The setting is relevant for main mode 1 and 3. \n
			:return: random: B4 | B8 | B12 | B16
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:RANDom?')
		return Conversions.str_to_scalar_enum(response, enums.PayloadLengthCs)

	def set_random(self, random: enums.PayloadLengthCs) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:RANDom \n
		Snippet: driver.configure.csounding.inputSignal.plength.set_random(random = enums.PayloadLengthCs.B12) \n
		Specifies the payload length in bytes for a random pattern. The setting is relevant for main mode 1 and 3. \n
			:param random: B4 | B8 | B12 | B16
		"""
		param = Conversions.enum_scalar_to_str(random, enums.PayloadLengthCs)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:RANDom {param}')

	# noinspection PyTypeChecker
	def get_sounding(self) -> enums.Sounding:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:SOUNding \n
		Snippet: value: enums.Sounding = driver.configure.csounding.inputSignal.plength.get_sounding() \n
		Specifies the payload length in bytes for a sounding pattern. The setting is relevant for main mode 1 and 3. \n
			:return: sounding: B4 | B12
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:SOUNding?')
		return Conversions.str_to_scalar_enum(response, enums.Sounding)

	def set_sounding(self, sounding: enums.Sounding) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:SOUNding \n
		Snippet: driver.configure.csounding.inputSignal.plength.set_sounding(sounding = enums.Sounding.B12) \n
		Specifies the payload length in bytes for a sounding pattern. The setting is relevant for main mode 1 and 3. \n
			:param sounding: B4 | B12
		"""
		param = Conversions.enum_scalar_to_str(sounding, enums.Sounding)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth:SOUNding {param}')

	def set(self, plength_sounding: List[int], plength_random: List[int], plength_fixed: List[int]) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth \n
		Snippet: driver.configure.csounding.inputSignal.plength.set(plength_sounding = [1, 2, 3], plength_random = [1, 2, 3], plength_fixed = [1, 2, 3]) \n
		Specifies the payload length in bytes for different types of pattern. \n
			:param plength_sounding: numeric
			:param plength_random: numeric
			:param plength_fixed: numeric
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('plength_sounding', plength_sounding, DataType.IntegerList, None, False, False, 3), ArgSingle('plength_random', plength_random, DataType.IntegerList, None, False, False, 3), ArgSingle('plength_fixed', plength_fixed, DataType.IntegerList, None, False, False, 3))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth {param}'.rstrip())

	# noinspection PyTypeChecker
	class PlengthStruct(StructBase):
		"""Response structure. Fields: \n
			- Plength_Sounding: List[int]: numeric
			- Plength_Random: List[int]: numeric
			- Plength_Fixed: List[int]: numeric"""
		__meta_args_list = [
			ArgStruct('Plength_Sounding', DataType.IntegerList, None, False, False, 3),
			ArgStruct('Plength_Random', DataType.IntegerList, None, False, False, 3),
			ArgStruct('Plength_Fixed', DataType.IntegerList, None, False, False, 3)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Plength_Sounding: List[int] = None
			self.Plength_Random: List[int] = None
			self.Plength_Fixed: List[int] = None

	def get(self) -> PlengthStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth \n
		Snippet: value: PlengthStruct = driver.configure.csounding.inputSignal.plength.get() \n
		Specifies the payload length in bytes for different types of pattern. \n
			:return: structure: for return value, see the help for PlengthStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PLENgth?', self.__class__.PlengthStruct())
