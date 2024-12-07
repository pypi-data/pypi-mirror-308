from __future__ import annotations

import shlex
from typing import Tuple

import click
from click import option, argument, command
from utz import process

from qmdx.cli import shell_exec_opt, no_shell_opt, verbose_opt, exec_cmd_opt
from qmdx.diff_x import color_opt, unified_opt, ignore_whitespace_opt
from qmdx.utils import join_pipelines


@command('git-diff-x', short_help='Diff a Git-tracked file at two commits (or one commit vs. current worktree), optionally passing both through another command first')
@color_opt
@option('-r', '--refspec', default='HEAD', help='<commit 1>..<commit 2> (compare two commits) or <commit> (compare <commit> to the worktree)')
@shell_exec_opt
@no_shell_opt
@unified_opt
@verbose_opt
@ignore_whitespace_opt
@exec_cmd_opt
@argument('args', metavar='[exec_cmd...] <path>', nargs=-1)
def main(
    color: bool,
    refspec: str | None,
    shell_executable: str | None,
    no_shell: bool,
    unified: int | None,
    verbose: bool,
    ignore_whitespace: bool,
    exec_cmds: Tuple[str, ...],
    args: Tuple[str, ...],
):
    """Diff a file at two commits (or one commit vs. current worktree), optionally passing both through `cmd` first

    Examples:

    dvc-utils diff -r HEAD^..HEAD wc -l foo.dvc  # Compare the number of lines (`wc -l`) in `foo` (the file referenced by `foo.dvc`) at the previous vs. current commit (`HEAD^..HEAD`).

    dvc-utils diff md5sum foo  # Diff the `md5sum` of `foo` (".dvc" extension is optional) at HEAD (last committed value) vs. the current worktree content.
    """
    if not args:
        raise click.UsageError('Must specify [cmd...] <path>')

    shell = not no_shell
    *cmds, path = args
    cmds = list(exec_cmds) + cmds

    pcs = refspec.split('..', 1)
    if len(pcs) == 1:
        ref1 = pcs[0]
        ref2 = None
    elif len(pcs) == 2:
        ref1, ref2 = pcs
    else:
        raise ValueError(f"Invalid refspec: {refspec}")

    diff_args = [
        *(['-w'] if ignore_whitespace else []),
        *(['-U', str(unified)] if unified is not None else []),
        *(['--color=always'] if color else []),
    ]
    if cmds:
        cmds1 = [ f'git show {ref1}:{path}', *cmds ]
        if ref2:
            cmds2 = [ f'git show {ref2}:{path}', *cmds ]
        else:
            cmd, *sub_cmds = cmds
            cmds2 = [ f'{cmd} {path}', *sub_cmds ]
        if not shell:
            cmds1 = [ shlex.split(c) for c in cmds1 ]
            cmds2 = [ shlex.split(c) for c in cmds2 ]

        join_pipelines(
            base_cmd=['diff', *diff_args],
            cmds1=cmds1,
            cmds2=cmds2,
            verbose=verbose,
            shell=not no_shell,
            shell_executable=shell_executable,
        )
    else:
        process.run(['git', 'diff', *diff_args, refspec, '--', path])
