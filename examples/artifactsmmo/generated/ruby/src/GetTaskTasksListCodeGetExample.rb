require "artifacts_mmo_client"

ArtifactsMMOClient.configure do |config|
    config.access_token = "YOUR_ACCESS_TOKEN";
    # config.username = "YOUR_USERNAME";
    # config.password = "YOUR_PASSWORD";
end

begin
    response = ArtifactsMMOClient::TasksApi.new.get_task_tasks_list_code_get(
        nil, // code
    )

    p response
rescue ArtifactsMMOClient::ApiError => e
    puts "Exception when calling Tasks#get_task_tasks_list_code_get: #{e}"
end
