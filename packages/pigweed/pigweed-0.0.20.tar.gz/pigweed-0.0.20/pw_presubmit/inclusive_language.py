# Copyright 2021 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Inclusive language presubmit check."""

import dataclasses
from pathlib import Path
import re

from . import presubmit, presubmit_context

# List borrowed from Android:
# https://source.android.com/setup/contribute/respectful-code
# inclusive-language: disable
NON_INCLUSIVE_WORDS = [
    r'master',
    r'slave',
    r'red[-\s]?line',
    r'(white|gr[ae]y|black)[-\s]*(list|hat)',
    r'craz(y|ie)',
    r'insane',
    r'crip+led?',
    r'sanity',
    r'sane',
    r'dummy',
    r'grandfather',
    r's?he',
    r'his',
    r'her',
    r'm[ae]n[-\s]*in[-\s]*the[-\s]*middle',
    r'mitm',
    r'first[-\s]?class[-\s]?citizen',
]
# inclusive-language: enable

# Test: master  # inclusive-language: ignore
# Test: master


def _process_inclusive_language(*words):
    """Turn word list into one big regex with common inflections."""

    if not words:
        words = tuple(NON_INCLUSIVE_WORDS)

    all_words = []
    for entry in words:
        if isinstance(entry, str):
            all_words.append(entry)
        elif isinstance(entry, (list, tuple)):
            all_words.extend(entry)
        all_words.extend(x for x in words)
    all_words = tuple(all_words)

    # Confirm each individual word compiles as a valid regex.
    for word in all_words:
        _ = re.compile(word)

    word_boundary = (
        r'(\b|_|(?<=[a-z])(?=[A-Z])|(?<=[0-9])(?=\w)|(?<=\w)(?=[0-9]))'
    )

    return re.compile(
        r"({b})(?i:{w})(e?[sd]{b}|{b})".format(
            w='|'.join(all_words), b=word_boundary
        ),
    )


NON_INCLUSIVE_WORDS_REGEX = _process_inclusive_language()

# If seen, ignore this line and the next.
IGNORE = 'inclusive-language: ignore'

# Ignore a whole section. Please do not change the order of these lines.
DISABLE = 'inclusive-language: disable'
ENABLE = 'inclusive-language: enable'


@dataclasses.dataclass
class PathMatch:
    word: str

    def __repr__(self):
        return f'Found non-inclusive word "{self.word}" in file path'


@dataclasses.dataclass
class LineMatch:
    line: int
    word: str

    def __repr__(self):
        return f'Found non-inclusive word "{self.word}" on line {self.line}'


def check_file(
    path: Path,
    found_words: dict[Path, list[PathMatch | LineMatch]],
    words_regex: re.Pattern = NON_INCLUSIVE_WORDS_REGEX,
    check_path: bool = True,
    root: Path | None = None,
):
    """Check one file for non-inclusive language.

    Args:
        path: File to check.
        found_words: Output. Data structure where found words are added.
        words_regex: Pattern of non-inclusive terms.
        check_path: Whether to check the path instead of just the contents.
            (Used for testing.)
        root: Path to add as a prefix to path.
    """
    if check_path:
        match = words_regex.search(str(path))
        if match:
            found_words.setdefault(path, [])
            found_words[path].append(PathMatch(match.group(0)))

    if path.is_symlink() or path.is_dir():
        return

    try:
        if root:
            path = root / path

        with open(path, 'r') as ins:
            enabled = True
            prev = ''
            for i, line in enumerate(ins, start=1):
                if DISABLE in line:
                    enabled = False
                if ENABLE in line:
                    enabled = True

                # If we see the ignore line on this or the previous line we
                # ignore any bad words on this line.
                ignored = IGNORE in prev or IGNORE in line

                if enabled and not ignored:
                    match = words_regex.search(line)

                    if match:
                        found_words.setdefault(path, [])
                        found_words[path].append(LineMatch(i, match.group(0)))

                # Not using 'continue' so this line always executes.
                prev = line

    except UnicodeDecodeError:
        # File is not text, like a gif.
        pass


@presubmit.check(name='inclusive_language')
def presubmit_check(
    ctx: presubmit_context.PresubmitContext,
    words_regex=NON_INCLUSIVE_WORDS_REGEX,
):
    """Presubmit check that ensures files do not contain banned words."""

    # No subprocesses are run for inclusive_language so don't perform this check
    # if dry_run is on.
    if ctx.dry_run:
        return

    found_words: dict[Path, list[PathMatch | LineMatch]] = {}

    ctx.paths = presubmit_context.apply_exclusions(ctx)

    for path in ctx.paths:
        check_file(
            path.relative_to(ctx.root),
            found_words,
            words_regex,
            root=ctx.root,
        )

    if found_words:
        with open(ctx.failure_summary_log, 'w') as outs:
            for i, (path, matches) in enumerate(found_words.items()):
                if i:
                    print('=' * 40, file=outs)
                print(path, file=outs)
                for match in matches:
                    print(match, file=outs)

        print(ctx.failure_summary_log.read_text(), end=None)

        print()
        print(
            """
Individual lines can be ignored with "inclusive-language: ignore". Blocks can be
ignored with "inclusive-language: disable" and reenabled with
"inclusive-language: enable".
""".strip()
        )
        # Re-enable just in case: inclusive-language: enable.

        raise presubmit_context.PresubmitFailure


def inclusive_language_checker(*words):
    """Create banned words checker for the given list of banned words."""

    regex = _process_inclusive_language(*words)

    def inclusive_language(  # pylint: disable=redefined-outer-name
        ctx: presubmit_context.PresubmitContext,
    ):
        globals()['inclusive_language'](ctx, regex)

    return inclusive_language
