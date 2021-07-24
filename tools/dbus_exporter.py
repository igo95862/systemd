#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run, PIPE


def extract_interfaces_xml(output_dir: Path, executables: Path) -> None:
    output_dir.mkdir(mode=0o755, exist_ok=True)

    list_interfaces_process = run(
        args=[
            executables.absolute(),
            '--bus-introspect', 'list',
        ],
        stdout=PIPE,
    )
    list_interfaces_process.check_returncode()

    interfaces_lines = list_interfaces_process.stdout.decode().splitlines()

    interface_names = [x.split('\t')[1] for x in interfaces_lines]

    for interface_name in interface_names:
        interface_introspection_run = run(
            args=[
                executables.absolute(),
                '--bus-introspect', interface_name,
            ],
            stdout=PIPE,
        )

        interface_introspection_run.check_returncode()

        with open(output_dir / (interface_name + '.xml'), mode='wb') as f:
            f.write(interface_introspection_run.stdout)


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument(
        '--output',
        type=Path,
        required=True,
    )

    parser.add_argument(
        '--executables',
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    extract_interfaces_xml(args.output, args.executables)


if __name__ == '__main__':
    main()
