import argparse
import base64
import hashlib
from collections.abc import Callable
from io import BufferedReader, TextIOWrapper
from pathlib import Path
from typing import Sequence

from .__version__ import __version__
from .algorithm import Algorithm
from .drunken_bishop import DrunkenBishop

_algorithms: dict[str, type[Algorithm]] = {'drunken_bishop': DrunkenBishop}
_digest_choices: dict[str, Callable[[bytes], str]] = {
    'base64': lambda b: base64.standard_b64encode(b).decode(),
    'hex': lambda b: b.hex(),
}


def cli(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        prog='hashime',
        description='hash visualization tool',
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
    )

    parser.add_argument(
        '-l',
        '--list',
        nargs=0,
        action=PrintAndExitAction,
        const=f"""\
Algorithms:\n    {', '.join(_algorithms.keys())}
Hash Functions:\n    {', '.join(sorted(hashlib.algorithms_available))}
Digest Forms:\n    {', '.join(_digest_choices.keys())}""",
        help='show visualization algorithms, hashing functions, '
        'digest forms and exit',
    )

    parser.add_argument(
        '-a',
        '--algorithm',
        choices=_algorithms.keys(),
        default='drunken_bishop',
        metavar='ALGO',
        help='visualization algorithm (defaults to drunken_bishop)',
    )

    parser.add_argument(
        '-H',
        '--hash-function',
        choices=hashlib.algorithms_available,
        default='sha256',
        metavar='HASH',
        help='hashing function (defaults to sha256)',
    )

    frame_group = parser.add_mutually_exclusive_group()

    frame_group.add_argument(
        '--frame',
        default='-,|,-,|,+,+,+,+,[,]',
        help="""
        comma-separated frame characters in order of
        (top_line, right_line, bottom_line, left_line,
        top_left_corner, top_right_corner, bottom_right_corner,
        bottom_left_corner, left_bracket, right_bracket)
        """,
    )

    frame_group.add_argument(
        '--no-frame',
        action='store_true',
        help='output visualization without a frame',
    )

    parser.add_argument(
        '--top-text',
        help='text on the top frame line',
    )

    parser.add_argument(
        '--bottom-text',
        help='text on the bottom frame line',
    )

    parser.add_argument(
        '-d',
        '--digest',
        nargs='?',
        metavar='DIGEST_FORM',
        default=None,
        const='base64',
        choices=_digest_choices.keys(),
        help='show digest (defaults to base64)',
    )

    parser.add_argument(
        '-f',
        '--file',
        type=argparse.FileType('br'),
        default='-',
        help='input file (defaults to stdin)',
    )

    parser.add_argument(
        '-o',
        '--output',
        type=argparse.FileType('w'),
        default='-',
        metavar='OUT',
        help='output file (defaults to stdout)',
    )

    args = parser.parse_args(argv)

    algorithm = _algorithms[args.algorithm]
    hash_function: str = args.hash_function
    should_be_framed: bool = not args.no_frame
    digest_form: str | None = args.digest
    out: TextIOWrapper = args.output
    file: BufferedReader = args.file

    digest = hashlib.file_digest(file, hash_function).digest()

    frame_kwargs = {}
    if not args.no_frame:
        val = args.frame.split(',')
        if len(val) != 10:
            raise ValueError(
                f'number of frame characters is not 10: {len(val)}'
            )
        frame_kwargs['lines'] = val[:4]
        frame_kwargs['corners'] = val[4:8]
        frame_kwargs['brackets'] = val[8:]

    top_text = args.top_text
    bottom_text = args.bottom_text

    if top_text is None:
        top_text = Path(file.name).name
    if bottom_text is None:
        bottom_text = hash_function.upper()

    algo = algorithm(data=digest)
    art = algo.to_art(
        should_be_framed,
        top_text=top_text or None,
        bottom_text=bottom_text or None,
        **frame_kwargs,
    )

    out.write(art)
    out.write('\n')
    if digest_form:
        encoded = _digest_choices[digest_form](digest)
        out.write(f'{hash_function}: {encoded}\n')


class PrintAndExitAction(argparse.Action):
    def __call__(self, parser, *_):
        print(self.const)
        parser.exit()


if __name__ == '__main__':
    cli()
