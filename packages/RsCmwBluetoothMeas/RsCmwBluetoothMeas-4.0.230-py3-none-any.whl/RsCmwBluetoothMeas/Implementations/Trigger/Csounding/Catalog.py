from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	def get_source(self) -> str:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:CATalog:SOURce \n
		Snippet: value: str = driver.trigger.csounding.catalog.get_source() \n
		Lists all trigger source values that can be set using method RsCmwBluetoothMeas.Trigger.Csounding.source. \n
			:return: source: string Comma-separated list of all supported values. Each value is represented as a string.
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:CATalog:SOURce?')
		return trim_str_response(response)
