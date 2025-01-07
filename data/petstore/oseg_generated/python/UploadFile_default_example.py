from pprint import pprint

from openapi_client import ApiClient, ApiException, Configuration, api, models

configuration = Configuration()

with ApiClient(configuration) as api_client:
    try:
        api_caller = api.PetApi(api_client)

        response = api_caller.upload_file(
            pet_id=12345,
            additional_metadata=None,
            file=open("/path/to/file", "rb").read(),
        )

        pprint(response)
    except ApiException as e:
        print("Exception when calling Pet#upload_file: %s\n" % e)
