from abc import ABC, abstractmethod

class BaseDispatch(ABC):
    def __init__(self):
        pass

    def run(self, request: list[dict[str, any]]):
        if request:
            self.controller.device_manager.set(request)