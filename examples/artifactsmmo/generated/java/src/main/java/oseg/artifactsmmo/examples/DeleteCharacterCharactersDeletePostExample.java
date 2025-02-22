package oseg.artifacts_mmo.examples;

import com.artifacts_mmo.client.ApiException;
import com.artifacts_mmo.client.Configuration;
import com.artifacts_mmo.client.api.*;
import com.artifacts_mmo.client.auth.*;
import com.artifacts_mmo.client.model.*;

import java.io.File;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class DeleteCharacterCharactersDeletePostExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setAccessToken("YOUR_ACCESS_TOKEN");

        var deleteCharacterSchema = new DeleteCharacterSchema();
        deleteCharacterSchema.name(null);

        try
        {
            var response = new CharactersApi(config).deleteCharacterCharactersDeletePost(
                deleteCharacterSchema
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Characters#deleteCharacterCharactersDeletePost");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
