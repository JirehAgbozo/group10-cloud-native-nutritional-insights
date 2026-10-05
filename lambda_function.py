import io
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient


AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONTAINER_NAME = "datasets"
BLOB_NAME = "All_Diets.csv"
OUTPUT_FILE = "nutritional_averages.json"


def calculate_averages(dataframe):
    averages = (
        dataframe.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]]
        .mean()
        .round(2)
        .reset_index()
    )

    return averages.to_dict(orient="records")


def lambda_handler(event=None, context=None):
    print("Connecting to Azurite Blob Storage...")

    blob_service_client = BlobServiceClient.from_connection_string(
        AZURITE_CONNECTION_STRING,
        api_version="2019-07-07"
    )

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=BLOB_NAME
    )

    print(f"Downloading {BLOB_NAME} from Azurite...")

    blob_data = blob_client.download_blob().readall()

    dataframe = pd.read_csv(io.BytesIO(blob_data))

    print(f"Successfully loaded {len(dataframe)} rows.")

    results = calculate_averages(dataframe)

    with open(OUTPUT_FILE, "w") as output_file:
        json.dump(results, output_file, indent=4)

    print("\nAverage nutritional values by diet type:")

    for result in results:
        print(
            f"{result['Diet_type']}: "
            f"Protein={result['Protein(g)']}, "
            f"Carbs={result['Carbs(g)']}, "
            f"Fat={result['Fat(g)']}"
        )

    print(f"\nResults saved to {OUTPUT_FILE}")

    return results


if __name__ == "__main__":
    lambda_handler()
