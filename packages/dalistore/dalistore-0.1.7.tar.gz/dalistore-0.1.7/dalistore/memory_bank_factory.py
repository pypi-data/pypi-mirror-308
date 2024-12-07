from dalistore.memory_bank import MemoryBank
from dalistore.text_memory_bank import TextMemoryBank
from dalistore.multimodal_memory_bank import MultimodalMemoryBank


class MemoryBankFactory:
    def get_memory_bank(self, multimodal: bool = False) -> MemoryBank:
        """
        Returns the appropriate MemoryBank instance based on the input data.

        Parameters:
        - multimodal: A boolean indicating whether to use the MultimodalMemoryBank. Defaults to False.

        Returns:
        - An instance of TextMemoryBank or MultimodalMemoryBank.
        """
        if multimodal:
            return MultimodalMemoryBank()
        else:
            return TextMemoryBank()
