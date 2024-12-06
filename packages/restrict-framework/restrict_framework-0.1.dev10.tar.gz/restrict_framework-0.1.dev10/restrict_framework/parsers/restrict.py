import functools
from itertools import permutations
from typing import Literal

from ..lexers.restrict import RestrictLexer
from ..ply.yacc import LRParser, yacc
from .ast import (
    Boolean,
    Create,
    Cx,
    Delete,
    Effects,
    Field,
    Fields,
    File,
    Float,
    Func,
    Include,
    Int,
    MappedFunc,
    Modify,
    Ref,
    Rel,
    Rels,
    Resource,
    Rules,
    Str,
    Tx,
)

FieldName = str
FieldPrefix = str
FieldCollectionType = str


def RULE(*args):
    def set_doc(func):
        @functools.wraps(func)
        def wrapper(self, p):
            return func(self, p)

        wrapper.__doc__ = "\n".join(args)
        return wrapper

    return set_doc


class RestrictParser:
    _parser: LRParser | None = None
    _lexer: RestrictLexer | None = None
    _debug: bool = False

    start = "file"

    @property
    def tokens(self) -> list[str]:
        if self._lexer is None:
            return []
        print("TOKENS", self._lexer.tokens)
        return self._lexer.tokens

    def build(self, debug=False) -> "RestrictParser":
        self._debug = debug
        self._lexer = RestrictLexer().build(debug=debug)
        self._parser = yacc(module=self, debug=debug)
        return self

    def parse(self, input: str) -> File:
        if len(input.strip()) == 0:
            return File([], [])
        if self._parser is None:
            raise NameError("You must build the parser first")
        return self._parser.parse(input, lexer=self._lexer)

    def p_error(self, p):
        if self._debug:
            raise SyntaxError(p)
        print("Syntax error in input", p)

    @RULE(
        "file : use_stmt opt_use_stmts",
        "     | use_stmt opt_use_stmts resource opt_resources",
        "     | resource opt_resources",
    )
    def p_file(self, p) -> File:
        if isinstance(p[1][0], Include):
            uses = p[1] + p[2]
            resources = [] if len(p) == 3 else p[3] + p[4]
        else:
            uses = []
            resources = p[1] + p[2]
        p[0] = File(uses, resources)
        return p[0]

    @RULE("resource : RESTYPE RESNAME '{' sections '}'")
    def p_resource(self, p) -> list[Resource]:
        p[0] = [Resource(p[1], p[2], "", *p[4])]
        return p[0]

    @RULE(
        "opt_resources : resource opt_resources",
        "              | empty",
    )
    def p_opt_resources(self, p) -> list[Resource]:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE(
        "sections : "
        + "\n         | ".join(
            " ".join(y)
            for x in [
                list(permutations(["data", "dnc", "effects", "security"], n))
                for n in range(1, 5)
            ]
            for y in x
        )
    )
    def p_sections(self, p) -> tuple[Fields, Rels, Effects, Rules]:
        sections = [
            [],
            [],
            Effects({}, {}, {}),
            Rules({}, {}, {}, {}, {}, {}, {}),
        ]
        for section in p[1:]:
            match section[0]:
                case "data":
                    sections[0] = section[1]
                case "dnc":
                    sections[1] = section[1]
                case "effects":
                    sections[2] = section[1]
                case "security":
                    sections[3] = section[1]
        p[0] = tuple(sections)
        return p[0]

    @RULE(
        "security : SECURITY '{' mutators '}'",
        "         | SECURITY '{' accessors '}'",
        "         | SECURITY '{' mutators accessors '}'",
        "         | SECURITY '{' accessors mutators '}'",
    )
    def p_security(self, p) -> tuple[str, Rules]:
        if len(p) == 5:
            directives = p[3]
        else:
            directives = p[3] | p[4]
        for key, field in Rules.__dataclass_fields__.items():
            if key not in directives:
                directives[key] = False if field.type == "bool" else {}
        p[0] = ("security", Rules(**directives))
        return p[0]

    @RULE(
        "mutators : MUTATORS '{' "
        + " '}' \n         | MUTATORS '{' ".join(
            " ".join(y)
            for x in [
                list(permutations(["mutcreate", "mutmodify", "mutdelete"], n))
                for n in range(1, 4)
            ]
            for y in x
        )
        + " '}'\n| MUTATORS '{' "
        + " secstar '}'\n          | MUTATORS '{' ".join(
            " ".join(y)
            for x in [
                list(permutations(["mutcreate", "mutmodify", "mutdelete"], n))
                for n in range(1, 3)
            ]
            for y in x
        )
        + " secstar '}'"
    )
    def p_mutators(self, p) -> dict[str, Cx]:
        d = {}
        for s in p[3:-1]:
            name = "mutstar" if s[0] == "*" else s[0]
            cx = s[1]
            d[name] = cx
        p[0] = d
        return p[0]

    @RULE("mutcreate : CREATE secdef")
    def p_mutcreate(self, p) -> tuple[Literal["create"], dict[str, Cx]]:
        p[0] = ("create", p[2])
        return p[0]

    @RULE("mutmodify : MODIFY secdef")
    def p_mutmodify(self, p) -> tuple[Literal["modify"], dict[str, Cx]]:
        p[0] = ("modify", p[2])
        return p[0]

    @RULE("mutdelete : DELETE secdef")
    def p_mutdelete(self, p) -> tuple[Literal["delete"], dict[str, Cx]]:
        p[0] = ("delete", p[2])
        return p[0]

    @RULE(
        "accessors : ACCESSORS '{' acclist '}'",
        "          | ACCESSORS '{' acclist secstar '}'",
        "          | ACCESSORS '{' accdets '}'",
        "          | ACCESSORS '{' accdets secstar '}'",
        "          | ACCESSORS '{' accdets acclist '}'",
        "          | ACCESSORS '{' acclist accdets '}'",
    )
    def p_accessors(self, p) -> dict[str, Cx]:
        d = {}
        for section in p[3:-1]:
            name = "accstar" if section[0] == "*" else section[0]
            cx = section[-1]
            d[name] = cx
            if section[0] == "list" and section[1] is True:
                d["listentry"] = True
            elif section[0] == "details" and section[1] is True:
                d["detailsentry"] = True
        p[0] = d
        return p[0]

    @RULE("accdets : opt_entrypoint DETAILS secdef")
    def p_accdets(self, p) -> tuple[Literal["details"], bool, dict[str, Cx]]:
        p[0] = ("details", p[1], p[3])
        return p[0]

    @RULE("acclist : opt_entrypoint LIST secdef")
    def p_acclist(self, p) -> tuple[Literal["list"], bool, dict[str, Cx]]:
        p[0] = ("list", p[1], p[3])
        return p[0]

    @RULE("secstar : '*' secdef")
    def p_secstar(self, p) -> tuple[Literal["*"], dict[str, Cx]]:
        p[0] = ("*", p[2])
        return p[0]

    @RULE(
        "secdef : '{' secfield opt_secfields '}'",
        "       | ':' arg opt_bfuncbinds",
    )
    def p_secdef(self, p) -> dict[str, Cx]:
        p[0] = {"*": Cx(p[2], p[3])} if len(p) == 4 else p[2] | p[3]
        return p[0]

    @RULE("secfield : valid_sec_id ':' arg opt_bfuncbinds")
    def p_secfield(self, p) -> dict[str, Cx]:
        p[0] = {p[1]: Cx(p[3], p[4])}
        return p[0]

    @RULE(
        "opt_secfields : secfield opt_secfields",
        "              | empty",
    )
    def p_opt_secfields(self, p) -> dict[str, Cx]:
        p[0] = {} if len(p) == 2 else p[1] | p[2]
        return p[0]

    @RULE(
        "valid_sec_id : valid_id",
        "             | '*'",
    )
    def p_valid_sec_id(self, p) -> str:
        p[0] = p[1]
        return p[0]

    @RULE(
        "opt_entrypoint : '<' ENTRYPOINT '>'",
        "               | empty",
    )
    def p_opt_entrypoint(self, p) -> bool:
        p[0] = len(p) > 2
        return p[0]

    @RULE("effects : EFFECTS '{' effectsecs '}'")
    def p_effects(self, p) -> tuple[str, Effects]:
        p[0] = ("effects", Effects(**p[3]))
        return p[0]

    @RULE(
        "effectsecs : "
        + "\n          | ".join(
            " ".join(y)
            for x in [
                list(permutations(["create", "modify", "delete"], n))
                for n in range(1, 4)
            ]
            for y in x
        )
    )
    def p_effectsecs(self, p) -> tuple[dict[str, dict[str, Tx | Delete]]]:
        sections = {}
        for section in p[1:]:
            sections[section[0]] = section[1]
        p[0] = sections
        return p[0]

    @RULE("create : CREATE '{' effect opt_effects '}'")
    def p_create(self, p) -> tuple[str, dict[str, Tx | Delete]]:
        p[0] = ("create", p[3] | p[4])
        return p[0]

    @RULE("modify : MODIFY '{' effect opt_effects '}'")
    def p_modify(self, p) -> tuple[str, dict[str, Tx | Delete]]:
        p[0] = ("modify", p[3] | p[4])
        return p[0]

    @RULE("delete : DELETE '{' effect opt_effects '}'")
    def p_delete(self, p) -> tuple[str, dict[str, Tx | Delete]]:
        p[0] = ("delete", p[3] | p[4])
        return p[0]

    @RULE("effect : valid_id ':' tx")
    def p_effect(self, p) -> dict[str, Tx | Delete]:
        p[0] = {p[1]: p[3]}
        return p[0]

    @RULE(
        "tx : scalar_arg",
        "   | DELETE",
        "   | tfunc",
        "   | ref opt_tfuncbinds",
    )
    def p_tx(self, p) -> Delete | Tx:
        if p[1] == "delete":
            p[0] = Delete()
        else:
            if len(p) == 2:
                txl = [p[1]]
            else:
                txl = [p[1]] + p[2]
            p[0] = Tx(txl)
        return p[0]

    @RULE(
        "opt_tfuncbinds : tfuncbind opt_tfuncbinds",
        "               | empty",
    )
    def p_opt_tfuncbinds(self, p) -> list[Func | MappedFunc | Create | Modify]:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE(
        "tfuncbind : PIPEOP tfunc",
    )
    def p_tfuncbind(self, p) -> list[Func | MappedFunc | Create | Modify]:
        p[0] = [p[2]]
        return p[0]

    @RULE(
        "tfunc : ID '(' ')'",
        "      | ID '(' arg opt_args ')'",
        "      | ID '[' id_list ']' '(' tfunc opt_tfuncbinds ')'",
        "      | CREATE no_coll_field_type '{' effect opt_effects '}'",
        "      | MODIFY no_coll_field_type '{' effect opt_effects '}'",
    )
    def p_tfunc(self, p) -> Func | MappedFunc | Create | Modify:
        if len(p) == 4:
            p[0] = Func(p[1], "", [])
        elif len(p) == 6:
            p[0] = Func(p[1], "", [p[3]] + p[4])
        elif len(p) == 9:
            p[0] = MappedFunc(p[1], "", p[3], Tx([p[6]] + p[7]))
        elif p[1] == "create":
            name, prefix = p[2]
            p[0] = Create(name, prefix, p[4] | p[5])
        elif p[1] == "modify":
            name, prefix = p[2]
            p[0] = Modify(name, prefix, p[4] | p[5])
        return p[0]

    @RULE("id_list : ID opt_id_list")
    def p_id_list(self, p) -> list[str]:
        p[0] = [p[1]] + p[2]
        return p[0]

    @RULE(
        "opt_id_list : ',' ID opt_id_list",
        "            | empty",
    )
    def p_opt_id_list(self, p) -> list[str]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "opt_effects : effect opt_effects",
        "            | empty",
    )
    def p_opt_effects(self, p) -> dict[str, Tx | Delete]:
        p[0] = {} if len(p) == 2 else p[1] | p[2]
        return p[0]

    @RULE("dnc : DNC '{' rel opt_rels '}'")
    def p_dnc(self, p) -> tuple[str, Rels]:
        p[0] = ("dnc", p[3] + p[4])
        return p[0]

    @RULE(
        "rel : '<' DESCTYPE '>' valid_id ':' opt_field_mods field_type",
        "    | '<' DNCDIR ':' mult '>' valid_id ':' opt_field_mods field_type",
        "    | '<' RESTYPE ':' mult '>' valid_id ':' opt_field_mods field_type",
    )
    def p_rel(self, p) -> Rels:
        type_name, prefix, collection_type = p[len(p) - 1]
        name = p[len(p) - 4]
        mult = 1 if len(p) == 8 else p[4]
        field_mods = p[len(p) - 2]
        p[0] = [
            Rel(
                name,
                type_name,
                prefix,
                collection_type,
                p[2],
                mult,
                *field_mods,
            )
        ]
        return p[0]

    @RULE(
        "valid_id : ID",
        "         | RESTYPE",
        "         | DATA",
        "         | DNC",
        "         | DNCDIR",
    )
    def p_valid_id(self, p) -> str:
        p[0] = p[1]
        return p[0]

    @RULE(
        "mult : INT",
        "     | '*'",
    )
    def p_mult(self, p) -> Int | Literal["*"]:
        p[0] = p[1]
        return p[0]

    @RULE(
        "opt_rels : rel opt_rels",
        "         | empty",
    )
    def p_opt_rels(self, p) -> Rels:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE("data : DATA '{' field opt_fields '}'")
    def p_data(self, p) -> tuple[str, Fields]:
        p[0] = ("data", p[3] + p[4])
        return p[0]

    @RULE(
        "field : valid_id ':' opt_field_mods field_type opt_constraint",
    )
    def p_field(self, p) -> Fields:
        name, prefix, collection_type = p[4]
        p[0] = [Field(p[1], name, prefix, collection_type, p[5], *p[3])]
        return p[0]

    @RULE(
        "opt_field_mods : field_mod opt_field_mods",
        "               | empty",
    )
    def p_opt_field_mods(self, p) -> tuple[bool, bool, bool, bool]:
        p[0] = [False, False, False, False]
        if len(p) == 3:
            p[0] = list(p[2])
            p[0][p[1]] = True
        return tuple(p[0])

    @RULE(
        "field_mod : HIDDEN",
        "          | OPTIONAL",
        "          | READONLY",
        "          | UNIQUE",
    )
    def p_field_mod(self, p) -> int:
        p[0] = ["hidden", "optional", "readonly", "unique"].index(p[1])
        return p[0]

    @RULE(
        "opt_constraint : ':' ref bfuncbind opt_bfuncbinds",
        "               | empty",
    )
    def p_opt_constraint(self, p) -> Cx | None:
        p[0] = None
        if len(p) == 5:
            p[0] = Cx(p[2], p[3] + p[4])
        return p[0]

    @RULE(
        "bfuncbind : PIPEOP ID '(' ')'",
        "         | PIPEOP ID '(' arg opt_args ')'",
    )
    def p_bfuncbind(self, p) -> list[Func]:
        if len(p) == 5:
            p[0] = [Func(p[2], "", [])]
        else:
            p[0] = [Func(p[2], "", [p[4]] + p[5])]
        return p[0]

    @RULE(
        "scalar_arg : INT",
        "           | INT '.' INT",
        "           | STR",
        "           | BOOLEAN",
    )
    def p_scalar_arg(self, p) -> Int | Float | Str | Boolean:
        if len(p) == 4:
            p[0] = Float(float("".join([str(x) for x in p[1:]])))
        elif isinstance(p[1], bool):
            p[0] = Boolean(p[1])
        elif isinstance(p[1], int):
            p[0] = Int(p[1])
        elif isinstance(p[1], str):
            p[0] = Str(p[1])
        return p[0]

    @RULE(
        "arg : scalar_arg",
        "    | ref",
    )
    def p_arg(self, p) -> Ref | Int | Float | Str:
        p[0] = p[1]
        return p[0]

    @RULE(
        "opt_args : ',' arg opt_args",
        "         | empty",
    )
    def p_opt_args(self, p) -> list[Ref | Int | Float | Str]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "opt_bfuncbinds : bfuncbind opt_bfuncbinds",
        "              | empty",
    )
    def p_opt_bfuncbinds(self, p) -> list[Func]:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE(
        "ref : ID opt_dot_names",
        "    | SELF opt_dot_names",
    )
    def p_ref(self, p) -> Ref:
        p[0] = Ref([p[1]] + p[2])
        return p[0]

    @RULE(
        "opt_dot_names : '.' ID opt_dot_names",
        "              | empty",
    )
    def p_opt_dot_names(self, p) -> list[str]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "field_type : LIST ID '.' RESNAME",
        "           | LIST RESTYPE '.' RESNAME",
        "           | LIST ID '.' ID",
        "           | LIST RESTYPE '.' ID",
        "           | LIST RESNAME",
        "           | LIST ID",
        "           | SET ID '.' RESNAME",
        "           | SET RESTYPE '.' RESNAME",
        "           | SET ID '.' ID",
        "           | SET RESTYPE '.' ID",
        "           | SET RESNAME",
        "           | SET ID",
        "           | no_coll_field_type",
    )
    def p_field_type(
        self, p
    ) -> tuple[FieldName, FieldPrefix, FieldCollectionType]:
        collection_type = ""
        name = ""
        prefix = ""

        if len(p) == 2:
            name, prefix = p[1]
        else:
            collection_type = p[1]
            if len(p) == 3:
                name = p[2]
            else:
                name = p[4]
                prefix = p[2]

        p[0] = (name, prefix, collection_type)
        return p[0]

    @RULE(
        "no_coll_field_type : ID '.' RESNAME",
        "                   | RESTYPE '.' RESNAME",
        "                   | ID '.' ID",
        "                   | RESTYPE '.' ID",
        "                   | RESNAME",
        "                   | ID",
    )
    def p_no_coll_field_type(self, p) -> tuple[FieldName, FieldPrefix]:
        if len(p) == 4:
            name = p[3]
            prefix = p[1]
        else:
            name = p[1]
            prefix = ""
        p[0] = (name, prefix)
        return p[0]

    @RULE(
        "opt_fields : field opt_fields",
        "           | empty",
    )
    def p_opt_fields(self, p) -> Fields:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE("use_stmt : USE PATH")
    def p_use_stmt(self, p) -> list[Include]:
        p[0] = [Include(p[2], "")]
        return p[0]

    @RULE(
        "opt_use_stmts : use_stmt opt_use_stmts",
        "              | empty",
    )
    def p_opt_use_stmts(self, p) -> list[Include]:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE("empty :")
    def p_empty(self, _):
        pass
