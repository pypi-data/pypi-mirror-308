import click

from synapse_sdk.plugins.utils import get_action


@click.command()
@click.argument('action')
@click.argument('params')
@click.option('--direct/--no-direct', default=False)
@click.pass_context
def run(ctx, action, params, direct):
    debug = ctx.obj['DEBUG']

    action = get_action(action, params, direct=direct, debug=debug)
    result = action.run_action()

    if debug:
        click.echo(result)
