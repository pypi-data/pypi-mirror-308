class IntegrationClientMixin:
    def get_plugin(self, pk):
        path = f'plugins/{pk}/'
        return self._get(path)

    def create_plugin(self, data):
        path = 'plugins/'
        return self._post(path, payload=data)

    def update_plugin(self, pk, data):
        path = f'plugins/{pk}/'
        return self._put(path, payload=data)

    def get_plugin_release(self, pk, params=None):
        path = f'plugin_releases/{pk}/'
        return self._get(path, payload=params)

    def create_plugin_release(self, data):
        path = 'plugin_releases/'
        files = {'file': data.pop('file')}
        return self._post(path, payload=data, files=files)

    def create_logs(self, data):
        path = 'logs/'
        return self._post(path, payload=data)

    def create_task(self, data):
        path = 'agent_tasks/'
        return self._post(path, payload=data)
