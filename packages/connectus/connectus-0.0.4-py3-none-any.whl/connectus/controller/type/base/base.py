from .configuration import Configuration
from abc import ABC, abstractmethod
import asyncio

class BaseController(ABC, Configuration):
    def __init__(self):
        Configuration.__init__(self)

    async def start(self):
        await self.initialize()
        await self.run()
    
    @abstractmethod
    async def initialize(self):
        await asyncio.sleep(3)

    async def run(self):
        try:
            while self.is_running:
                data = self.acquisition.run()
                self.data_processing.process(data)
                output = self.model.run()
                output_data = self.data_processing.process(output)
                self.dispatch.run(output_data)
                await self.check_stop()
                await asyncio.sleep(self.sample_time)
        except Exception as e:
            print(f"An error occurred while running the controller: {e}")

