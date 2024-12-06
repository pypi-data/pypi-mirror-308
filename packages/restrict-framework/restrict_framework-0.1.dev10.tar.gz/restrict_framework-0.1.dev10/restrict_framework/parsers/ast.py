from __future__ import annotations
from collections.abc import Sequence, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from .restrict import RestrictParser  # pragma: no cover


@dataclass
class Modify:
    name: str
    prefix: str
    args: dict[str, Tx | Delete]


@dataclass
class Create:
    name: str
    prefix: str
    args: dict[str, Tx | Delete]


@dataclass
class Delete:
    pass


@dataclass
class Tx:
    pipeline: Sequence[
        Create | Modify | Ref | Boolean | Int | Float | Str | Func | MappedFunc
    ]


@dataclass
class Effects:
    create: Mapping[str, Tx | Delete]
    modify: Mapping[str, Tx | Delete]
    delete: Mapping[str, Tx | Delete]


@dataclass
class Boolean:
    value: bool


@dataclass
class Int:
    value: int


@dataclass
class Float:
    value: float


@dataclass
class Str:
    value: str


@dataclass
class Ref:
    parts: list[str]


@dataclass
class MappedFunc:
    name: str
    prefix: str
    params: list[str]
    body: Tx


@dataclass
class Func:
    name: str
    prefix: str
    args: list[Ref | Int | Float | Boolean | Str]


@dataclass
class Cx:
    init: Ref | Int | Float | Str | Boolean
    funcs: list[Func]


@dataclass
class Field:
    name: str
    type: str
    prefix: str
    collection: str = ""
    constraint: Cx | None = None
    hidden: bool = False
    optional: bool = False
    readonly: bool = False
    unique: bool = False


@dataclass
class Rel:
    name: str
    type: str
    prefix: str
    collection: str
    relation: str
    multiplicity: int | Literal["*"]
    hidden: bool = False
    optional: bool = False
    readonly: bool = False
    unique: bool = False


@dataclass
class Rules:
    list: dict[str, Cx]
    details: dict[str, Cx]
    accstar: dict[str, Cx]
    create: dict[str, Cx]
    modify: dict[str, Cx]
    delete: dict[str, Cx]
    mutstar: dict[str, Cx]
    listentry: bool = False
    detailsentry: bool = False


Fields = list[Field]
Rels = list[Rel]


@dataclass
class Resource:
    archetype: str
    name: str
    prefix: str
    data: Fields
    dnc: Rels
    effects: Effects
    security: Rules


@dataclass
class Include:
    path: Path
    alias: str


@dataclass
class File:
    includes: list[Include]
    declarations: list[Resource]
    parser: Union["RestrictParser", None] = None
