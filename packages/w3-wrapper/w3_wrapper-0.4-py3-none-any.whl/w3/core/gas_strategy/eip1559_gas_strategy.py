import statistics
from ..gas_strategy.gas_strategy import GasStrategy

class EIP1559GasStrategy(GasStrategy):
    async def calculate_gas(self, gas_multiplier) -> dict:
        block = await self._w3.async_w3.eth.get_block('latest', full_transactions=True)
        transactions = block['transactions']

        max_fee_per_gas_list = []
        max_priority_fee_per_gas_list = []

        for tx in transactions:
            if 'maxPriorityFeePerGas' in tx and tx['maxPriorityFeePerGas'] is not None:
                max_priority_fee_per_gas_list.append(tx['maxPriorityFeePerGas'])
            if 'maxFeePerGas' in tx and tx['maxFeePerGas'] is not None:
                max_fee_per_gas_list.append(tx['maxFeePerGas'])

        if not max_priority_fee_per_gas_list and not max_fee_per_gas_list:
            max_priority_fee = await self._w3.async_w3.eth.max_priority_fee
            return {
                'maxFeePerGas': int(max_priority_fee * gas_multiplier),
                'maxPriorityFeePerGas': int((max_priority_fee / 10) * gas_multiplier)
            }
        else:
            median_max_fee = int(statistics.median(max_fee_per_gas_list)) if max_fee_per_gas_list else 0
            median_max_priority_fee = int(statistics.median(max_priority_fee_per_gas_list)) if max_priority_fee_per_gas_list else 0
            return {
                'maxFeePerGas': int(median_max_fee * gas_multiplier),
                'maxPriorityFeePerGas': int(median_max_priority_fee * gas_multiplier)
            }
