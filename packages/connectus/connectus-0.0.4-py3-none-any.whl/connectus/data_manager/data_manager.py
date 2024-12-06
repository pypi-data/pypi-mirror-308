import asyncio

class DataManager:
    def __init__(self, stop_event: asyncio.Event):
        self.nodes = []
        self.stop_event = stop_event

    def add(self, node):
        try:
            item = {}
            item['name'] = node.name
            item['type'] = node.type
            item['instance'] = node
            self.nodes.append(item)
        except Exception as e:
            print('An error occurred adding a node: ', e)

    async def start(self):
        start_bundle = []
        for node in self.nodes:
            await node['instance'].connect()
            if node['type'] == 'communication':
                start_task = asyncio.create_task(node['instance'].start())
                start_bundle.append(start_task)
        if start_bundle:
            await asyncio.gather(*start_bundle)
        print("Data Manager is running")

    async def save(self, data: dict[str, any]): ## only database ??
        for node in self.nodes:
            if node['type'] == 'database':
                await node['instance'].write(data)

    async def stop(self):
        for node in self.nodes:
            await node['instance'].stop()