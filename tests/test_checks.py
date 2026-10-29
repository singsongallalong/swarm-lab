"""Unit checks for the filter's code and file rules, with no game or model needed.

    python3 tests/test_checks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from swarm import config  # noqa: E402
from swarm.check import check_code, check_rows  # noqa: E402

PURITY = config.job(config.target("arpg-game"), "kinds").data["purity"]
GOOD = '''--!strict
-- A comment may mention game, task.wait or Instance freely.
local AreaLayout = require("../AreaLayout")
local DraftedTypes = require("../../DraftedTypes")
local M = {}
M.about = "Says task.wait in a string, which is fine."
function M.count(look: any): number
	return look.n
end
return M
'''


def expect(label: str, got, want) -> None:
    ok = (want is None and got is None) or (want is not None and got is not None and want in got)
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {got}")
    if not ok:
        raise SystemExit(f"expected {want!r}")


def main() -> None:
    f = "src/shared/systems/drafted/ColdSnapX.luau"
    expect("a pure module passes", check_code(f, GOOD, PURITY), None)
    expect("must start --!strict", check_code(f, GOOD.replace("--!strict\n", ""), PURITY), "doesn't start with --!strict")
    expect("no task", check_code(f, GOOD.replace("return look.n", "task.wait()\n\treturn look.n"), PURITY), "task.")
    expect("no game", check_code(f, GOOD.replace("return look.n", "return game.Workspace"), PURITY), "game")
    expect("no Instance", check_code(f, GOOD.replace("return look.n", "return Instance.new('Part')"), PURITY), "Instance")
    expect("no while true", check_code(f, GOOD.replace("return look.n", "while true do end"), PURITY), "while")
    expect("no loadstring", check_code(f, GOOD.replace("return look.n", "return loadstring('')"), PURITY), "loadstring")
    expect("only listed requires", check_code(f, GOOD.replace('"../AreaLayout"', '"../../net/Remotes"'), PURITY), "isn't on the job's list")
    expect("no computed requires", check_code(f, GOOD.replace('local AreaLayout = require("../AreaLayout")', 'local where = "../../net/Remotes"\nlocal AreaLayout = require(where)'), PURITY), "other than a plain path")
    expect("size cap", check_code(f, GOOD + "\n" * 400, PURITY), "lines, over 300")

    expect("a new module is new", check_rows(f, "new_file", None, GOOD, "ColdSnap"), None)
    expect("can't overwrite an existing file", check_rows(f, "new_file", "old", GOOD, "ColdSnap"), "already existed")
    expect("row modes need an existing file", check_rows("x.luau", "add_rows", None, "", "ColdSnap"), "new file")

    pattern = config.job(config.target("arpg-game"), "kinds").files["src/shared/systems/DraftedKinds.luau"]["pattern"]
    reg = 'local K = {\n\tShardBloom = require("./drafted/ShardBloom"),\n}\n'
    added = reg.replace("),\n}", '),\n\tColdSnapSpiral = require("./drafted/ColdSnapSpiral"),\n}')
    expect("registry: one entry for the skill", check_rows("r", "add_lines", reg, added, "ColdSnap", pattern), None)
    expect("registry: another skill's entry", check_rows("r", "add_lines", reg, added.replace("ColdSnapSpiral", "SleetSpiral"), "ColdSnap", pattern), "isn't a ColdSnap entry")
    expect("registry: entry pointing at another module", check_rows("r", "add_lines", reg, added.replace('"./drafted/ColdSnapSpiral"', '"./drafted/ShardBloom"'), "ColdSnap", pattern), "isn't a ColdSnap entry")
    expect("registry: existing line changed", check_rows("r", "add_lines", reg, added.replace("ShardBloom = ", "Shard = "), "ColdSnap", pattern), "changed or removed")
    expect("registry: existing line removed", check_rows("r", "add_lines", reg, 'local K = {\n\tColdSnapSpiral = require("./drafted/ColdSnapSpiral"),\n}\n', "ColdSnap", pattern), "changed or removed")

    # Snake_case data: a rule's prefix with {skill_lower} names rows moonwell_...
    sc = "local S = {\n\tash_stump = {\n\t\tkind = \"tree\",\n\t},\n}\n"
    sc2 = sc.replace("\n}\n", "\n\tmoonwell_arch = {\n\t\tkind = \"arch\",\n\t},\n}\n")
    expect("prefixed row with the lowercase name", check_rows("s", "add_rows", sc, sc2, "Moonwell", None, "{skill_lower}_"), None)
    expect("row without the prefix", check_rows("s", "add_rows", sc, sc2.replace("moonwell_arch", "arch"), "Moonwell", None, "{skill_lower}_"), "doesn't start with moonwell_")
    expect("lowercase pattern in add_lines", check_rows("r", "add_lines", "x\n", "x\nmoonwell = Moonwell,\n", "Moonwell", r"{skill_lower} = {skill},"), None)

    j = config.job(config.target("arpg-game"), "kinds")
    expect("glob rule matches the skill's module", j.rule(f, "ColdSnap") and "matched", "matched")
    expect("glob rule refuses another skill's module", j.rule("src/shared/systems/drafted/SleetX.luau", "ColdSnap"), None)
    expect("glob rule refuses other folders", j.rule("src/shared/systems/ColdSnapX.luau", "ColdSnap"), None)
    print("\nchecks: all passed")


if __name__ == "__main__":
    main()
