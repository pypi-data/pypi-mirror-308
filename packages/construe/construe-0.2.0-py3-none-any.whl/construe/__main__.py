"""
Primary entry point for construe CLI application
"""

import click
import torch
import platform

from .version import get_version
from .basic import BasicBenchmark
from .exceptions import DeviceError
from .moondream import MoonDreamBenchmark
from .datasets.manifest import generate_manifest
from .datasets.path import get_data_home, FIXTURES


CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(get_version(), message="%(prog)s v%(version)s")
@click.option(
    "-d",
    "--device",
    default=None,
    type=str,
    envvar=["CONSTRUE_DEVICE", "TORCH_DEVICE"],
    help="specify the pytorch device to run on e.g. cpu, mps or cuda",
)
@click.option(
    "-e",
    "--env",
    default=None,
    envvar=["CONSTRUE_ENV", "ENV"],
    help="name of the experimental environment for comparison (default is hostname)",
)
@click.option(
    "-D",
    "--datadir",
    default=None,
    envvar="CONSTRUE_DATA",
    help="specify the location to download datasets to",
)
@click.option(
    "-C",
    "--cleanup/--no-cleanup",
    default=True,
    help="cleanup all downloaded datasets after the benchmark is run",
)
@click.pass_context
def main(ctx, env=None, device=None, datadir=None, cleanup=True):
    if device is not None:
        try:
            torch.set_default_device(device)
        except RuntimeError as e:
            raise DeviceError(e)

        click.echo(f"using torch.device(\"{device}\")")

    if env is None:
        env = platform.node()

    ctx.ensure_object(dict)
    ctx.obj["device"] = device
    ctx.obj["env"] = env
    ctx.obj["data_home"] = get_data_home(datadir)
    ctx.obj["cleanup"] = cleanup


@main.command()
@click.option(
    "-o",
    "--saveto",
    default=None,
    help="path to write the measurements pickle data to",
)
@click.option(
    "-t",
    "--num-threads",
    default=None,
    type=int,
    help="specify number of threads for benchmark (default to maximum)",
)
@click.option(
    "-F",
    "--fuzz/--no-fuzz",
    default=False,
    help="fuzz the tensor sizes of the inputs to the benchmark",
)
@click.option(
    "-S",
    "--seed",
    default=None,
    type=int,
    help="set the random seed for random generation",
)
@click.pass_context
def basic(ctx, **kwargs):
    kwargs["env"] = ctx.obj["env"]
    benchmark = BasicBenchmark(**kwargs)
    benchmark.run()


@main.command()
@click.pass_context
def moondream(ctx, **kwargs):
    kwargs["env"] = ctx.obj["env"]
    benchmark = MoonDreamBenchmark(**kwargs)
    benchmark.run()


@main.command()
@click.option(
    "-f",
    "--fixtures",
    type=str,
    default=FIXTURES,
    help="path to fixtures directory to generate manifest from",
)
@click.option(
    "-o",
    "--out",
    type=str,
    default=None,
    help="path to write the manifest to",
)
def manifest(fixtures=FIXTURES, out=None):
    generate_manifest(fixtures, out)


if __name__ == "__main__":
    main(
        obj={},
        prog_name="construe",
    )
