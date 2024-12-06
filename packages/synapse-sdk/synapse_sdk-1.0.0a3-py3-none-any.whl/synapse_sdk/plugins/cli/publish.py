import json
from pathlib import Path

import click

from synapse_sdk.clients.backend import BackendClient
from synapse_sdk.plugins.upload import archive
from synapse_sdk.plugins.utils import read_config


@click.command()
@click.option('--host', required=True)
@click.option('--user_token', required=True)
@click.option('--tenant', required=True)
@click.option('--debug_modules', default='', envvar='SYNAPSE_DEBUG_MODULES')
@click.pass_context
def publish(ctx, host, user_token, tenant, debug_modules):
    debug = ctx.obj['DEBUG']

    config = read_config()

    source_path = Path('./')
    archive_path = source_path / 'dist' / 'archive.zip'
    archive(source_path, archive_path)

    data = {'plugin': config['code'], 'file': str(archive_path), 'debug': debug}
    if debug:
        data['debug_meta'] = json.dumps({'modules': debug_modules.split(',')})

    client = BackendClient(host, user_token, tenant=tenant)
    client.create_plugin_release(data)
    click.secho(
        f'Successfully published "{config["name"]}" ({config["code"]}@{config["version"]}) to synapse backend!',
        fg='green',
        bold=True,
    )
