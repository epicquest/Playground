*** Settings ***
Library    RequestsLibrary
Library    Collections

Suite Setup       Setup API Session
Suite Teardown    Delete All Sessions

*** Variables ***
${BASE_URL}    https://playground-rukf.onrender.com/
#${BASE_URL}    http://localhost:8000

*** Keywords ***
Setup API Session
    Create Session    api    ${BASE_URL}

*** Test Cases ***
Health Check Test
    [Documentation]    Test the health check endpoint
    ${response}=    GET On Session    api    /health
    Should Be Equal As Strings    ${response.status_code}    200
    Dictionary Should Contain Key    ${response.json()}    status
    Should Be Equal As Strings    ${response.json()}[status]    healthy

Post Weather Data Test
    [Documentation]    Test posting weather request
    &{payload}=    Create Dictionary    city=London    country_code=UK
    ${response}=    POST On Session    api    /weather    json=${payload}
    Should Be Equal As Strings    ${response.status_code}    200
    Dictionary Should Contain Key    ${response.json()}    city
    Should Be Equal As Strings    ${response.json()}[city]    London

Get Weather By Path Test
    [Documentation]    Test getting weather by path parameter
    ${response}=    GET On Session    api    /weather/Paris
    Should Be Equal As Strings    ${response.status_code}    200
    Dictionary Should Contain Key    ${response.json()}    city
    Should Be Equal As Strings    ${response.json()}[city]    Paris

Invalid Weather Request Test
    [Documentation]    Test invalid weather request
    &{payload}=    Create Dictionary    city=${EMPTY}    country_code=UK
    ${response}=    POST On Session    api    /weather    json=${payload}    expected_status=422
    Should Be Equal As Strings    ${response.status_code}    422

*** Keywords ***
API Should Return Weather Data
    [Arguments]    ${response}
    Dictionary Should Contain Key    ${response.json()}    temperature
    Dictionary Should Contain Key    ${response.json()}    description
    Dictionary Should Contain Key    ${response.json()}    humidity
    Dictionary Should Contain Key    ${response.json()}    timestamp