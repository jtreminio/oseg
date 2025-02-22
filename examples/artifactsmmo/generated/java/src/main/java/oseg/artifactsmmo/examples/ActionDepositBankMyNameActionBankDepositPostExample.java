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

public class ActionDepositBankMyNameActionBankDepositPostExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setAccessToken("YOUR_ACCESS_TOKEN");

        var simpleItemSchema = new SimpleItemSchema();
        simpleItemSchema.code(null);
        simpleItemSchema.quantity(null);

        try
        {
            var response = new MyCharactersApi(config).actionDepositBankMyNameActionBankDepositPost(
                null, // name
                simpleItemSchema
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling MyCharacters#actionDepositBankMyNameActionBankDepositPost");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
