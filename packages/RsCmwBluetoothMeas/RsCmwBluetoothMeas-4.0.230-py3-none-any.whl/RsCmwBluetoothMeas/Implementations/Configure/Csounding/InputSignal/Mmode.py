from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MmodeCls:
	"""Mmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mmode", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.MeasMode:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:MMODe:TYPE \n
		Snippet: value: enums.MeasMode = driver.configure.csounding.inputSignal.mmode.get_type_py() \n
		Specifies the main measurement mode.
			- 1 - round trip time (RTT) measurement
			- 2 - phase-based ranging (PBR) measurement
			- 3 - RTT and PBR measurement \n
			:return: mmode: M1 | M2 | M3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:MMODe:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.MeasMode)

	def set_type_py(self, mmode: enums.MeasMode) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:MMODe:TYPE \n
		Snippet: driver.configure.csounding.inputSignal.mmode.set_type_py(mmode = enums.MeasMode.M1) \n
		Specifies the main measurement mode.
			- 1 - round trip time (RTT) measurement
			- 2 - phase-based ranging (PBR) measurement
			- 3 - RTT and PBR measurement \n
			:param mmode: M1 | M2 | M3
		"""
		param = Conversions.enum_scalar_to_str(mmode, enums.MeasMode)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:MMODe:TYPE {param}')
