import importlib
import re
import sys
import click
import yaml

from infracalc.region import REGION_SHORTS

CONTEXT_SETTINGS = dict(auto_envvar_prefix='infracalc', help_option_names=['-h', '--help'])


def my_import(name):
    cls = importlib.import_module(name)
    return cls


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class Context(object):

    def __init__(self):
        self.verbose = False
        self.config = {}

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def elog(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.secho(msg, fg="red")

    def wlog(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.secho(msg, fg="yellow")

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('-f', '--file', help='File to read.', type=click.File('r'))
@click.command(context_settings=CONTEXT_SETTINGS, name="infracalc")
@pass_context
def cli(ctx, verbose, file):
    ctx.verbose = verbose
    pricing_info = []
    infra = yaml.load(file, Loader=yaml.FullLoader)
    region = REGION_SHORTS[infra["region"]]
    classCache = {}
    pricing_api = infra["type"]
    if infra["type"].lower() == "aws":
        for service_infra in infra["services"]:
            service_type = service_infra["service"]
            if service_type not in classCache:
                module = my_import("infracalc.{}.{}".format(pricing_api, camel_to_snake(service_type)))
                klass = getattr(module, service_type)
                classCache[service_type] = klass(region)
            service_instance = classCache[service_type]
            pricing_info.append(service_instance.price_info(service_infra))
    if "export" in infra:
        exporter = infra["export"]["exporter"]
        params = infra["export"]["params"]
        export_module = my_import("infracalc.{}.{}".format("exporters", camel_to_snake(exporter)))
        exporter_klass = getattr(export_module, exporter)
        exporter_klass(pricing_info, params).export()


if __name__ == '__main__':
    cli()
