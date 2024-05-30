# Get the absolute path of the .ps1 script directory
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Get the absolute path of the project directory (the root)
$projectDirectory = Resolve-Path "$scriptDirectory\..\.."

# Define the full path to the .env file
$envFilePath = Join-Path -Path $projectDirectory -ChildPath '.env'

# Read the contents of the .env file
$envFileContent = Get-Content -Path $envFilePath

# Define a dictionary to store the variables
$envVariables = @{}

# Parse the variables from the .env file and add them to the dictionary
foreach ($line in $envFileContent) {
    $key, $value = $line -split '=', 2
    if ($key -ne $null -and $value -ne $null) {
        $envVariables[$key.Trim()] = $value.Trim()
    }
}

# Access the necessary variables (treating all values as strings)
$dbName = $envVariables["DB_NAME"]
$dbUser = $envVariables["DB_USERNAME"]
$dbPassword = $envVariables["DB_PASSWORD"]
$dbUrl = $envVariables["DB_URL"]
$dbManager = $envVariables["DB_MANAGER"]

# Use the variables in your script
Remove-Item -Recurse -Force "$projectDirectory\migrations\versions" -ErrorAction SilentlyContinue
pipenv run init
try {
    if ($dbManager -eq "postgresql") {
        psql -U $dbUser -c "DROP DATABASE IF EXISTS $dbName";
        if ($LASTEXITCODE -ne 0) { throw "Failed to drop database" }
        psql -U $dbUser -c "CREATE DATABASE $dbName";
        if ($LASTEXITCODE -ne 0) { throw "Failed to create database" }
        psql -U $dbUser -c "CREATE EXTENSION unaccent" -d $dbName;
        if ($LASTEXITCODE -ne 0) { throw "Failed to create extension in database" }
    } else {
        mysql -h $dbUrl -u $dbUser -p -e "DROP DATABASE IF EXISTS $dbName"; if ($?) { Write-Output "DROP DATABASE" }
        if ($LASTEXITCODE -ne 0) { throw "Failed to drop database" }
        mysql -h $dbUrl -u $dbUser -p -e "CREATE DATABASE $dbName"; if ($?) { Write-Output "CREATE DATABASE" }
        if ($LASTEXITCODE -ne 0) { throw "Failed to create database" }
    }
    pipenv run migrate
    if ($LASTEXITCODE -ne 0) { throw "Failed to run migrations" }
    
    pipenv run upgrade
    if ($LASTEXITCODE -ne 0) { throw "Failed to upgrade database" }
} catch {
    Write-Error "An error occurred: $_"
    exit 1
}