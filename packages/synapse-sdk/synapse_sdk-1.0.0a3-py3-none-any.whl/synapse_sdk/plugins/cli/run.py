import os

import click

from synapse_sdk.clients.agent import AgentClient
from synapse_sdk.clients.backend import BackendClient
from synapse_sdk.plugins.utils import get_action, read_config


@click.command()
@click.argument('action')
@click.argument('params')
@click.option('--job-id')
@click.option('--direct/--no-direct', default=False)
@click.option('--run-by', type=click.Choice(['script', 'agent', 'backend']), default='script')
@click.option('--agent-host')
@click.option('--agent-token')
@click.option('--host')
@click.option('--agent')
@click.option('--user-token')
@click.option('--tenant')
@click.pass_context
def run(ctx, action, params, job_id, direct, run_by, agent_host, agent_token, host, agent, user_token, tenant):
    debug = ctx.obj['DEBUG']

    if run_by == 'script':
        run_by_script(action, params, job_id, direct, debug)
    elif run_by == 'agent':
        run_by_agent(action, params, job_id, agent_host, agent_token, user_token, tenant, debug)
    elif run_by == 'backend':
        run_by_backend(action, params, agent, host, user_token, tenant)


def run_by_script(action, params, job_id, direct, debug):
    action = get_action(action, params, job_id=job_id, direct=direct, debug=debug)
    result = action.run_action()

    if debug:
        click.echo(result)


def run_by_agent(action, params, job_id, agent_host, agent_token, user_token, tenant, debug):
    client = AgentClient(agent_host, agent_token, user_token, tenant)
    data = {'action': action, 'params': params, 'job_id': job_id}
    if debug:
        data.update({
            'plugin_path': os.getcwd(),
            'modules': os.getenv('SYNAPSE_DEBUG_MODULES', '').split(','),
        })
        result = client.run_debug_plugin_release(data=data)
    else:
        config = read_config()
        result = client.run_plugin_release(code=f'{config["code"]}@{config["version"]}', data=data)

    click.echo(result)


def run_by_backend(action, params, agent, host, user_token, tenant):
    client = BackendClient(host, user_token, tenant=tenant)
    config = read_config()
    data = {'agent': agent, 'version': config['version'], 'action': action, 'params': params}
    result = client.run_plugin(config['code'], data=data)

    click.echo(result)
