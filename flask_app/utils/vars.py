VERSION_REGEX_PATTERN = "^[0-9]+\.[0-9]+\.[0-9]+[+0-9A-Za-z-]*$"

required_params = ["env", "name", "version"]

expected_create_body = "Expected minimal body : \n {\"env\": \"dev\", \"name\":\"app_name\", \"version\" : \"0.0.1\"}"
