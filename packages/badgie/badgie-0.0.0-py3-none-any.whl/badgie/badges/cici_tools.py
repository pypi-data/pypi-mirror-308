# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: MIT

from .. import tokens as to
from ..models import Badge
from ._base import register_badges

register_badges(
    {
        to.CICI_TOOLS: Badge(
            name="cici-tools",
            description="This project uses [cici-tools](https://gitlab.com/buildgarden/tools/cici-tools).",
            example="https://img.shields.io/badge/%E2%9A%A1_cici--tools-enabled-c0ff33",
            title="cici-tools enabled",
            link="https://gitlab.com/buildgarden/tools/cici-tools",
            image="https://img.shields.io/badge/%E2%9A%A1_cici--tools-enabled-c0ff33",
            weight=20,
        ),
    }
)
