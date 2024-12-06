# README

`tea-utils` is a set of libraries that simplify Python developers' lives by providing Atlassian-related capabilities:
* It enables services to seamlessly read or write Socrates data by easily implementing an Extract-Transform-Load (ETL) flow.
* It allows browsing AWS IAM role actions.
* It allows connecting to the official [OpenAI SDK](https://platform.openai.com/docs/quickstart?language-preference=python) through the approved Atlassian AI Gateway mechanisms.
* It provides a simple Splunk query interface.

`tea-utils` can be used both in the local development environment and within Bitbucket pipelines.

If you are creating a Python service that interacts with Socrates, you can save yourself time and effort by using this library.

## Installation

`tea-utils` is available from Atlassian's internal pypi repository.
To use `tea-utils`, add the following lines to your `Pipfile`.

```toml
[[source]]
url = "https://${ARTIFACTORY_USERNAME}:${ARTIFACTORY_PASSWORD}@packages.atlassian.com/pypi/pypi/simple"
verify_ssl = true
name = "atlassian-pypi"

[packages]
atlassian-tea-utils = {version="~=1.1.1", index="atlassian-pypi"}
```

If you want to use the ai code then add

```
[packages]
atlassian-tea-utils = {version="~=1.1.1", index="atlassian-pypi", extras=["ai"]}
```


## Bitbucket pipelines integration

`tea-utils` can be used from Bitbucket pipelines to read and write data
to Socrates tables. To configure Socrates access to your pipeline,
follow the following instructions.

#### 1. Find out your repository’s ID in Bitbucket

You can do this by browsing to your repo’s administration page
(e.g. https://bitbucket.org/asecurityteam/YOUR_REPO/admin),
clicking “Advanced”, and then reading the UUID at the bottom.

#### 2. Register your Pipeline to be able to write to the appropriate Socrates zone

Browse to https://data-portal.internal.atlassian.com/access/zone_security_stg or https://data-portal.internal.atlassian.com/access/zone_security_prod (or whichever Data Portal zone you want to write to).

If you’re a Delegate on the zone, you can do this part yourself.
Otherwise, ask one of the Delegates (right-hand column)
to register your Pipeline’s details as follows:

```
Build Principal: pipelinesBuild:<YOUR_REPO'S_UUID>
Contact: Your LDAP
Repository: The URL of your repository
```

**Note**: to request W/R access to `zone_security_*`, you can
[go/letmein](https://go/letmein).

#### 3. Register your Pipeline to be able to contact Socrates via Gateway

Edit [socrates-config: configs/socrates-gateway-consumers/config.yml](https://bitbucket.org/atlassian/socrates-config/src/fa58d848077d73ffeffadc1f84901c66d1a8c7b5/configs/socrates-gateway-consumers/config.yml#lines-183)
and add your Pipeline’s details under build.
[Here’s an example PR doing this.](https://bitbucket.org/atlassian/socrates-config/pull-requests/207)

## Usage

### Querying socrates

The module [`sql.socrates`](atlassian_tea_utils/sql/socrates.py)
exposes the `sql()` function
to run arbitrary queries against socrates
and retrieve the results.

#### Example

```python
from atlassian_tea_utils.sql import socrates

results = socrates.sql("SELECT * from atlas.staff LIMIT 10;")
print(results)
```

### Uploading data

The module [`batchupload.uploader`](atlassian_tea_utils/batchupload/uploader.py)
exposes the `upload_file()` and `send_to_socrates()` functions
to upload JSON-formatted data to socrates using the data portal's [batch upload service](https://data-portal.internal.atlassian.com/batchupload).

#### Example

```python
auth_header_value = uploader.get_auth_value_for_data_portal(
    # Data Portal is only available in prod, even though we may be
    # uploading to a staging table.
    "prod")
session = uploader.get_data_portal_session(auth_header_value)

zone = "scratch"
table = "scratch_table"
zone_and_table = zone + "." + table

# Flow: https://data-portal.internal.atlassian.com/batchupload/flows/06b4b9e0-bb08-43d5-88a2-f847f83aa5b7
flow_id = "06b4b9e0-bb08-43d5-88a2-f847f83aa5b7"

json_items = ["{'test': 'test'}"]
uploader.send_to_socrates(json_items, flow_id, zone, table, session)
```
