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

public class GetAccountAchievementsAccountsAccountAchievementsGetExample
{
    public static void main(String[] args)
    {
        var config = Configuration.getDefaultApiClient();
        config.setAccessToken("YOUR_ACCESS_TOKEN");
        // config.setUsername("YOUR_USERNAME");
        // config.setPassword("YOUR_PASSWORD");

        try
        {
            var response = new AccountsApi(config).getAccountAchievementsAccountsAccountAchievementsGet(
                null, // account
                null, // type
                null, // completed
                1, // page
                50 // size
            );

            System.out.println(response);
        } catch (ApiException e) {
            System.err.println("Exception when calling Accounts#getAccountAchievementsAccountsAccountAchievementsGet");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
