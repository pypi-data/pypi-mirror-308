from synapse_sdk.clients.base import BaseClient


class CoreClientMixin(BaseClient):
    def get_agent_system(self):
        path = 'agents/system/'
        return self._get(path)

    def get_jobs_progress(self, data):
        path = 'integration/jobs/progress/'
        return self._post(path, data=data, timeout=1)
