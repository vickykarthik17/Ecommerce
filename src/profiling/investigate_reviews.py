'''from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]
data_path = project_root / "data" / "raw" / "olist_order_reviews_dataset.csv"

reviews = pd.read_csv(data_path)

duplicate_review_ids = reviews[reviews["review_id"].duplicated(keep=False)]
duplicate_order_ids = reviews[reviews["order_id"].duplicated(keep=False)]

print("Duplicate review IDs: ")
print(duplicate_review_ids[["review_id", "order_id", "review_score"]].head(20))

print("\nDuplicate order IDs:")
print(duplicate_order_ids[["review_id", "order_id", "review_score"]].head(20))'''


from pathlib import Path
from analyse_keys import check_key
import pandas as pd


project_root = Path(__file__).resolve().parents[2]
data_path = project_root / "data" / "raw" / "olist_order_reviews_dataset.csv"

reviews = pd.read_csv(data_path)

duplicate_review_ids = reviews[
    reviews["review_id"].duplicated(keep=False)
]

print(duplicate_review_ids.sort_values("review_id").head(20))
print("Reviews")
check_key(reviews, ["review_id"])
check_key(reviews, ["order_id"])
check_key(reviews, ["review_id", "order_id"])