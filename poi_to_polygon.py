import pathlib

import geopandas as gpd
import pandas as pd
import typer


def main(
    input_xlsx: pathlib.Path = pathlib.Path("input.xlsx"),
    output_kml: pathlib.Path = pathlib.Path("output.kml"),
    radius_m: int = 1000,
):
    df_pois = pd.read_excel(input_xlsx.expanduser(), engine="openpyxl")
    gdf = gpd.GeoDataFrame(
        df_pois,
        geometry=gpd.points_from_xy(df_pois["longitude"], df_pois["latitude"], crs="EPSG:4326"),
    )
    gdf = gdf.to_crs(3043)
    gdf["geometry"] = gdf["geometry"].buffer(radius_m)
    gdf = gdf.to_crs(4326)
    gdf.to_file(str(output_kml.expanduser()), driver="KML")


if __name__ == "__main__":
    typer.run(main)
