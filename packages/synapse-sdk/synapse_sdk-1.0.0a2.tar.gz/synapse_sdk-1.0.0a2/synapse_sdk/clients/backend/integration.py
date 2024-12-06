from synapse_sdk.clients.base import BaseClient


class IntegrationClientMixin(BaseClient):
    def get_plugin(self, pk):
        path = f'plugins/{pk}/'
        return self._get(path)

    def create_plugin(self, data):
        path = 'plugins/'
        return self._post(path, data=data)

    def update_plugin(self, pk, data):
        path = f'plugins/{pk}/'
        return self._put(path, data=data)

    def run_plugin(self, pk, data):
        path = f'plugins/{pk}/run/'
        return self._post(path, data=data)

    def get_plugin_release(self, pk, params=None):
        path = f'plugin_releases/{pk}/'
        return self._get(path, params=params)

    def create_plugin_release(self, data):
        path = 'plugin_releases/'
        files = {'file': data.pop('file')}
        return self._post(path, data=data, files=files)

    def create_logs(self, data):
        path = 'logs/'
        return self._post(path, data=data)

    def create_task(self, data):
        path = 'agent_tasks/'
        return self._post(path, data=data)
