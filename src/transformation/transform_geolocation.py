from pathlib import Path
import pandas as pd

project_root=Path(__file__).resolve().parents[2]
raw_data_path=project_root/"data"/"raw"
processed_data_path=project_root/"data"/"processed"

input_file=raw_data_path/"olist_geolocation_dataset.csv"
output_file=processed_data_path/"geolocation_clean.csv"

data=pd.read_csv(input_file)

data["geolocation_city"]=data["geolocation_city"].str.strip().str.lower()

data["geolocation_state"]=data["geolocation_state"].str.strip().str.upper()

data=data.drop_duplicates()
data.to_csv(output_file,index=False)

print(f"Geolocation transformed:  {len(data)} rows ")
print(f"Saved to: {output_file} ")
