# Ladybug test, all Porta plane positions (prepared 2 Nov)

Same format **and the same file names** as the Pg Andreu Nin set, so the loader in `test.gh` runs unchanged:
point its folder Panel here. The names say "andreu-nin" only for that reason; the content is all of Porta.

- 832 plane positions: S0 = today's planes; S4 = `S4_s1.00_w0.00_r0.00` from `layouts_tool_v0_sizeexact_trunkTERCERA_20261026.csv`
  (278 Jacaranda, 284 Tipuana, 101 Melia, 66 Styphnolobium, 54 Pyrus, 39 Celtis, 10 Brachychiton)
- 1,119 context trees (non-plane, `flag == ok`, within 60 m of a plane), identical in both runs
- 637 buildings (centroid within 90 m of a plane)
- 21,352 test points: 2 m grid within 8 m of a plane, outside footprints, 1.1 m above ground

About 11x the Andreu Nin points and ~10x the context, so start with `every` = 5 (about 4,270 points).
