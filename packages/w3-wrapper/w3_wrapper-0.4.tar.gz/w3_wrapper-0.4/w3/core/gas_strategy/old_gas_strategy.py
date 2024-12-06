from ..gas_strategy.gas_strategy import GasStrategy


class OldGasStrategy(GasStrategy):
    async def calculate_gas(self, gas_multiplier) -> dict:
        return {
            'gasPrice': int(await self._w3.async_w3.eth.gas_price * gas_multiplier)
        }
