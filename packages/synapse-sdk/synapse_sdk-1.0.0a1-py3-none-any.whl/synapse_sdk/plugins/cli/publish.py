from pathlib import Path

import click

from synapse_sdk.client import Client
from synapse_sdk.plugins.utils import read_config

from ..upload import archive


@click.command()
@click.option('-h', '--host', required=True)
@click.option('-t', '--token', required=True)
@click.option('-w', '--workspace', required=True)
def publish(host, token, workspace):
    client = Client(host, token, tenant=workspace)
    config = read_config()

    source_path = Path('./')
    archive_path = source_path / 'dist' / 'archive.zip'
    archive(source_path, archive_path)

    data = {'plugin': config['code'], 'file': str(archive_path)}
    client.create_plugin_release(data)
