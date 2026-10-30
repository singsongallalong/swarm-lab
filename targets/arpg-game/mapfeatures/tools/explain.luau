--!strict
-- Runs one of the game's spec files and, where a check fails, prints what it found and
-- what it expected, not just "expected tables to be deeply equal". Copied into each
-- worktree as .swarm/tools/explain.luau by swarm-lab; run from the worktree root:
--   lune run .swarm/tools/explain <SpecName>        (e.g. OutdoorTilesets)
-- Only the failing checks print. Exits 1 if any failed.
local process = require("@lune/process")

local name = process.args[1]
if not name then
	print("usage: lune run .swarm/tools/explain <SpecName>")
	process.exit(2)
end

local function show(v: any, depth: number?): string
	local d = depth or 0
	if type(v) == "string" then
		return string.format("%q", v)
	elseif type(v) ~= "table" then
		return tostring(v)
	elseif d > 4 then
		return "{...}"
	end
	local parts = {}
	for k, val in v do
		table.insert(parts, (if type(k) == "number" then "" else tostring(k) .. " = ") .. show(val, d + 1))
		if #parts >= 40 then
			table.insert(parts, "...")
			break
		end
	end
	return "{ " .. table.concat(parts, ", ") .. " }"
end

local function deepEqual(a: any, b: any): boolean
	if a == b then
		return true
	end
	if type(a) ~= "table" or type(b) ~= "table" then
		return false
	end
	for k, v in a do
		if not deepEqual(v, b[k]) then
			return false
		end
	end
	for k in b do
		if a[k] == nil then
			return false
		end
	end
	return true
end

local failed = 0
local current = ""
local function expect(actual: any)
	local function fail(what: string)
		failed += 1
		print(`FAIL {current}\n  {what}`)
	end
	return {
		toBe = function(expected: any)
			if actual ~= expected then
				fail(`expected {show(expected)}\n  got      {show(actual)}`)
			end
		end,
		toEqual = function(expected: any)
			if not deepEqual(actual, expected) then
				fail(`expected {show(expected)}\n  got      {show(actual)}`)
			end
		end,
		toBeNear = function(expected: number, epsilon: number?)
			if math.abs(actual - expected) > (epsilon or 1e-6) then
				fail(`expected {expected} (±{epsilon or 1e-6}), got {show(actual)}`)
			end
		end,
		toThrow = function(pattern: string?)
			local ok, err = pcall(actual)
			if ok then
				fail("expected the function to throw")
			elseif pattern and not string.find(tostring(err), pattern) then
				fail(`expected an error matching {show(pattern)}, got {show(tostring(err))}`)
			end
		end,
	}
end

local prefix: { string } = {}
local api = {
	describe = function(n: string, body: () -> ())
		table.insert(prefix, n)
		body()
		table.remove(prefix)
	end,
	it = function(n: string, body: () -> ())
		current = table.concat(prefix, " > ") .. " > " .. n
		local ok, err = pcall(body)
		if not ok then
			failed += 1
			print(`FAIL {current}\n  error: {err}`)
		end
	end,
	expect = expect,
}

local spec = (require :: any)(`../../tests/systems/{name}.spec`)
spec(api)
if failed > 0 then
	process.exit(1)
end
print(`{name}: every check passed`)
