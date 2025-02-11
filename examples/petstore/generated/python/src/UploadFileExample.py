from datetime import date, datetime
from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration(
    access_token="YOUR_ACCESS_TOKEN",
)

with ApiClient(configuration) as api_client:
    try:
        response = api.PetApi(api_client).upload_file(
            pet_id=12345,
            additional_metadata="Additional data to pass to server",
            file=open("/path/to/file", "rb").read(),
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#upload_file: %s\n" % e)
