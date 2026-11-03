"""Run the LBT 'utci_comfort_map' recipe (same as the HB UTCI Comfort Map component) on one HBJSON.
Usage: python run_hb_utci.py <model.hbjson> <out_folder>"""
import sys, time, pathlib
from lbt_recipes.recipe import Recipe
from lbt_recipes.settings import RecipeSettings

W = pathlib.Path(r"C:\Users\giofo\Desktop\ARCHIVIO\MASTERS\MACAD\2_MACAD\THESIS_MACAD\1_THESIS_PROJECT\grasshopper\ladybug_andreu_nin_20261102\ladybug")
EPW = W / "ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.2011-2025" / "ESP_CT_Barcelona-El.Prat.AP.081810_TMYx.2011-2025.epw"
DDY = EPW.with_suffix(".ddy")
model, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

r = Recipe("utci_comfort_map")
r.input_value_by_name("model", str(model))
r.input_value_by_name("epw", str(EPW))
r.input_value_by_name("ddy", str(DDY))
r.input_value_by_name("north", 0)
r.input_value_by_name("run-period", "7/15 to 7/15 between 0 and 23 @1")
r.input_value_by_name("cpu-count", 12)
t = time.time()
res = r.run(RecipeSettings(folder=str(out), reload_old=False), radiance_check=True, silent=False)
print("RESULT FOLDER", res, "minutes", round((time.time() - t) / 60, 1), flush=True)
