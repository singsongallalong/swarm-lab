#!/usr/bin/env bash
# Mutation score for a Hash spec: each mutant breaks systems/Hash one way; a good spec
# fails on it ("killed"). Prints "<killed> passed, <survived> failed" for swarm's held-out scorer.
set -u
F=src/shared/systems/Hash.luau
cp "$F" /tmp/Hash.orig.$$
killed=0; survived=0
mutate() {  # $1: python expression rewriting s
  cp /tmp/Hash.orig.$$ "$F"
  python3 - "$F" "$1" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read(); exec(sys.argv[2]); open(p,'w').write(s)
PY
  if lune run tests Hash.spec >/dev/null 2>&1; then survived=$((survived+1)); echo "survived: $2"; else killed=$((killed+1)); fi
}
mutate 's=s.replace("return x - math.floor(x)","return x")' "unit not wrapped into [0,1)"
mutate 's=s.replace("a * 12.9898 + b * 78.233 + c * 37.719","a * 12.9898 + c * 37.719")' "unit ignores b"
mutate 's=s.replace("x = mix((x + math.floor(c)) % TWO32)","x = x")' "draw ignores c"
mutate 's=s.replace("x = bit32.bxor(x, bit32.rshift(x, 16))\n\tx = mul(x, 0x7feb352d)","x = mul(x, 0x7feb352d)")' "mix loses its first xorshift"
mutate 's=s.replace("return x / TWO32","return x / TWO32 * 0.5")' "draw only covers [0, 0.5)"
cp /tmp/Hash.orig.$$ "$F"; rm -f /tmp/Hash.orig.$$
echo "$killed passed, $survived failed"
