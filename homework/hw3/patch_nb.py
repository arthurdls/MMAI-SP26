import nbformat, sys
from pathlib import Path

NB_PATH = Path("/home/arthurdls/Documents/SP26/6.S985/adls_mmai_HW3.ipynb")

NEW_SOURCE = r"""import json
import sys
import os
from pathlib import Path
from sklearn.model_selection import train_test_split

# Make api_card_renderer importable (adjust path if running on Colab with Drive mount)
_REPO_ROOT = Path("/home/arthurdls/Documents/SP26/6.S985")  # local
# On Colab: _REPO_ROOT = Path("/content/drive/MyDrive")
sys.path.insert(0, str(_REPO_ROOT))
from api_card_renderer import render_one_example, truncate_text

MMAI_ROOT = Path("/content/mmai-data")  # Colab target; change for local runs
MMAI_ROOT.mkdir(parents=True, exist_ok=True)
(MMAI_ROOT / "images").mkdir(exist_ok=True)

N_TRAIN = 800
N_TEST  = 200
RANDOM_STATE = 42

df_sub = df.sample(n=min(N_TRAIN + N_TEST, len(df)), random_state=RANDOM_STATE)
train_df, test_df = train_test_split(df_sub, test_size=N_TEST, random_state=RANDOM_STATE)


def build_jsonl(split_df, split_name):
    records = []
    for idx, (_, row) in enumerate(split_df.iterrows()):
        img_name = f"{split_name}_{idx:05d}.jpg"
        img_path = MMAI_ROOT / "images" / img_name
        render_one_example(row, out_path=img_path)

        # Vision input  = API list image (rendered above)
        # Language input = NL instruction (injected into question)
        # Language output = function calls used (the label)
        question = (
            f"Instruction: {row['instruction']}\n\n"
            "Given the available APIs shown in the image, which function calls should be made?"
        )
        answer = truncate_text(row["function_calls_used"], 300)
        records.append({
            "image":    f"images/{img_name}",
            "question": question,
            "answer":   answer,
        })
    return records


train_records = build_jsonl(train_df, "train")
test_records  = build_jsonl(test_df,  "test")

with open(MMAI_ROOT / "data.jsonl", "w") as f:
    for r in train_records + test_records:
        f.write(json.dumps(r) + "\n")

print(f"Saved {len(train_records)} train + {len(test_records)} test records.")
print(f"Example train record:\n{json.dumps(train_records[0], indent=2)[:400]}")
"""

nb = nbformat.read(NB_PATH, as_version=4)
# Find cell containing build_jsonl and render_one_example
target = None
for i, cell in enumerate(nb.cells):
    if cell.cell_type == "code" and "build_jsonl" in cell.source and "render_one_example" in cell.source:
        target = i
        break
if target is None:
    # Fallback: cell index 9
    target = 9
    print(f"Warning: marker not found, patching cell index {target}")
else:
    print(f"Found build_jsonl cell at notebook cell index {target}")

nb.cells[target].source = NEW_SOURCE
nbformat.write(nb, NB_PATH)
print(f"Patched {NB_PATH}")
