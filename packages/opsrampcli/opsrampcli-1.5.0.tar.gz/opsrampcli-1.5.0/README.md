# OpsRamp Command Line Interface

This is a utility script that allows easy searching and manipulation of various OpsRamp items and configurations.  You can specify connection credentials via command line, or you can [set up an environments file](#credentials) to contain the credentials you need to use, which makes it easier if you need to manage multiple credentials.


# <a id="Available"></a>Available Commands
The available commands are:


| opcli Command                               | Description                                                                                                               |
|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| [getalerts](#getalerts)                     | Search for and take action on alerts                                                                                      |
| [postalerts](#postalerts)                   | Post alerts using the API (using OAuth creds)                                                                             |
| [webhookalerts](#webhookalerts)             | Post alerts to a Webhook integration                                                                                      |
| [getincidents](#getincidents)               | Search and take action on Incidents                                                                                       |
| [getresources](#getresources)               | Search for and take action on resources/devices                                                                           |
| [exportservicemaps](#exportservicemaps)     | Export one or more full Service Map definitions to a file which can be manipulated and re-imported                        |
| [importservicemaps](#importservicemaps)     | Import (and optionally transform while doing so) from a Service Map export file                                           |
| [cloneservicemaps](#cloneservicemaps)       | Copy an existing Service Map, with transformations/replacements (useful when you have a template Service Map to re-use)   |
| [transformsvcmap](#transformsvcmap)         | Apply regex replacements to an exported Service Map and create a new transformed export file with the changes             |
| [getservicemaps](#getservicemaps)           | Get Service Map definitions                                                                                               |
| [getchildsvcgroups](#getchildsvcgroups)     | Get child Service Groups of a parent Service                                                                              |
| [getservicegroup](#getservicegroup)         | Get the full definition of a Service Group                                                                                |
| [exportcustattrfile](#exportcustattrfile)   | Generate an Excel or csv file from existing custom attribute values                                                       |
| [importcustattrfile](#importcustattrfile)   | Import an Excel file containing custom attribute values                                                                   |
| [getcustomattrs](#getcustomattrs)           | Get custom attribute definitions                                                                                          |
| [getdiscoprofile](#getdiscoprofile)         | Get discovery profile definition                                                                                          |
| [getalertesc](#getalertesc)                 | Search and get Escalation Policy definitions                                                                              |
| [migratealertesc](#migratealertesc)         | Migrate/copy Escalation Policies within same tenant or from one tenant to another                                         |
| [clonetemplates](#clonetemplates)           | Clone monitoring templates                                                                                                |

&nbsp;
&nbsp;

For more detailed help on a specific command use the -h option with the command, for example to get help on the cloneservicemaps command:

```shell
% opcli cloneservicemaps -h
usage: opcli cloneservicemaps [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --name NAME --replace REGEX REPLACEWITH [--parentlink] [--clobber]

Command-specific arguments:
  -h, --help            show this help message and exit
  --secure SECURE       Whether or not to verify SSL cert (default: True)
  --name NAME           Name of Service Map to transform and clone (default: None)
  --replace REGEX REPLACEWITH
                        Transforming regex pattern and replacement string (option can be repeated) (default: None)
  --parentlink          If root Service has a link to a parent, link the imported Service Map (default: False)
  --clobber             Overwrite Service Map (i.e. with same name) if it already exists (default: False)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="credentials"></a>Credentials

opcli requires credentials for most operations, either via command line arguments or an *environments.yml* file to be located in the directory where you running it.  Optionally you can specify an explicit environments file path & name using the --envfile option.  The file must follow the following format, where the name is the value you will specify to the --env option to define the URL and credentials you will use:

```yaml
- name: example1
  url:  https://customer2name.api.opsramp.com
  partner: msp_nnnnn
  tenant: client_nnnnn
  client_id: abcdefg1234567
  client_secret: abcdefg1234567

- name: example2
  url:  https://customer2name.api.opsramp.com
  partner: msp_nnnnn
  tenant: client_nnnnn
  client_id: abcdefg1234567
  client_secret: abcdefg1234567
```
If providing credentials directly on the command line, use the following options:

```shell
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
  --vtoken VTOKEN       OpsRamp webhook token (only used for webhookalerts command) (default: None)
```
Note that you only need to provide the attributes needed for the kind of API calls you are making.  Therefore:
* If you are making an API call that does not require a partner id (which is not needed  in most cases) you do not need to provide a *partner* value.
* If you are not doing webhook alert posts, you would not need to specify the *vtoken* value.
* If you are doing only webhook alert posts then you would not need *client_id* and *client_secret*.
* If you are using the environment for a bunch of different scenarios, there is no harm in having the extra values there for the cases where they are not needed.

&nbsp;
&nbsp;
# Commands

## <a id="getalerts"></a>getalerts
Search for and take action on alerts

```shell
usage: opcli getalerts [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --query QUERY [--brief] [--descr] [--count] [--filter FILTER] [--action ACTION] [--heal]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --query QUERY      Query String to filter alerts as per https://develop.opsramp.com/resource-management/tenants-tenantid-resources-search (default: None)
  --brief            Include only key fields in output (default: False)
  --descr            Include the description field in results (runs *much* slower as it requires a separate api call per alert) (default: False)
  --count            Only show the count of matching alerts (default: False)
  --filter FILTER    Post-query filter on alerts. Python expression that will evaluate to True or False such as alert["resource"]["name"].startswith("prod") (default: None)
  --action ACTION    Perform an action on matching alerts (Heal, acknowledge, suppress, close, unsuppress, unAcknowledge) (default: None)
  --heal             Heal the matching alerts (i.e. send a matching Ok) (default: False)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
### Alert search criteria
Alert search --query option uses the syntax documented [here](https://web.archive.org/web/20211024221749/https://docs.opsramp.com/api/alerts/tenants-tenantid-alerts-search/)

*Note: Above link is to an Internet Archive capture of an old doc page, as the latest doc no longer lists query variables* 
### Examples

Search for all alerts with matching resource/device numeric id and metric

    % opcli getalerts --env myenvname --query 'resourceIds:9798408+metrics:testmetric' --brief


Search for all alerts last updated during given time range, and heal & close them

    % opcli getalerts --env myenvname --query 'startDate:2000-01-01T00:00:00 0000+endDate:2020-12-01T00:00:00 0000+alertTimeBase:updated+states:Critical,Warning,Info' --heal --action close

# <a id="postalerts"></a>postalerts
Post alerts directly to the API (using OAuth creds)
```shell
usage: opcli postalerts [-h] [--env ENV] [--envfile ENVFILE] [--url URL] [--client_id KEY] [--client_secret SCRT] [--tenant TENANT] [--partner PARTNER] [--secure SECURE] [--infile INFILE] [--range RANGE] [--subject SUBJECT] [--state {Critical,Warning,Info,Ok}] [--metric METRIC] [--resource RESOURCE] [--source SOURCE] [--comp COMP] [--desc DESC] [--prob PROB] [--client CLIENT]
                        [--custom NAME VALUE]

optional arguments:
  -h, --help            show this help message and exit
  --secure SECURE       Whether or not to verify SSL cert (default: True)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)

Post alerts using alert content from a json file:
  --infile INFILE       File containing a json array of alert payloads (default: None)
  --range RANGE         An integer or range identifying which alert in the file to send (default: None)

Post an alert using alert content from the command line:
  --subject SUBJECT     Alert Subject (default: None)
  --state {Critical,Warning,Info,Ok}
                        Alert Current State (default: None)
  --metric METRIC       Alert metric (default: None)
  --resource RESOURCE   Alert Resource name (default: None)
  --source SOURCE       Alert Source name (default: None)
  --comp COMP           Alert Component name (default: None)
  --desc DESC           Alert Description (default: None)
  --prob PROB           Alert Problem Area (default: None)
  --client CLIENT       Alert Client ID (only required if posting with a partner-level tenant (default: None)
  --custom NAME VALUE   Alert custom attribute name and value (can repeat this option for multiple custom attributes) (default: None)
```
### Example

    % opcli postalerts --env myenv --subject 'test alert' --state Warning --metric testmetric --resource testhost  --comp c1 --desc mydesc --prob p1 --custom attr1 val1 --custom attr2 val2
# <a id="webhookalerts"></a>webhookalerts
Post alerts to a Webhook integration
```shell
usage: opcli webhookalerts [-h] [--url URL] [--vtoken VTOKEN] --infile INFILE [--range RANGE]

Command-specific arguments:
  -h, --help            show this help message and exit
  --infile INFILE       File containing an array of json alert payloads (default: None)
  --range RANGE         An integer or range identifying which alert in the file to send (default: all)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --vtoken VTOKEN       OpsRamp webhook token (default: None)
```
### Example
Post alert #5 from the specified json file (expected to contain an array of alerts), using vtoken authentication

    % opcli webhookalerts --vtoken mytoken --infile myalertsamples.json --range 5

# <a id="getincidents"></a>getincidents
Search and take action on Incidents
```shell
usage: opcli getincidents [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --query QUERY [--brief] [--count] [--filter FILTER] [--resolve]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --query QUERY      Query String to filter incidents (default: None)
  --brief            Include only key fields in output (default: False)
  --count            Only show the count of matching incidents (default: False)
  --filter FILTER    Post-query filter on incidents. Python expression that will evaluate to True or False such as incident["resource"]["name"].startswith("prod") (default: None)
  --resolve          Resolve the matching incidents (default: False)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="getresources"></a>getresources
Search for and take action on resources/devices
```shell
usage: opcli getresources [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] [--query QUERY] [--search SEARCH] [--count] [--delete] [--manage] [--filter FILTER]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --query QUERY      Query String to filter resources as per https://develop.opsramp.com/resource-management/tenants-tenantid-resources-search (default: None)
  --search SEARCH    Search String to filter resources as it would be entered under Resources -> Search (default: None)
  --count            Only show the count of matching resources (default: False)
  --delete           Delete the matching resources (default: False)
  --manage           Manage the matching resources (default: False)
  --filter FILTER    Post-query filter on resources. Python expression that will evaluate to True or False such as alert["resource"]["name"].startswith("prod") (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="exportservicemaps"></a>exportservicemaps    
Export one or more full Service Map definitions to a file which can be manipulated and re-imported
```shell
usage: opcli exportservicemaps [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] [--name NAME] [--outdir OUTDIR] [--clobber] [--timestamp]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --name NAME        Name of the root level Service Map/Group (export all if not specified) (default: None)
  --outdir OUTDIR    Directory path where export will be saved (default: .)
  --clobber          Remove/overwrite prior exports of same maps (default: False)
  --timestamp        Include a timestamp in the Service Map dir name (default: False)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="importservicemaps"></a>importservicemaps    
Import (and optionally transform while doing so) from a Service Map export file
```shell
usage: opcli importservicemaps [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --src SRC [--replace REGEX REPLACEWITH] [--parentlink] [--clobber]

Command-specific arguments:
  -h, --help            show this help message and exit
  --secure SECURE       Whether or not to verify SSL cert (default: True)
  --src SRC             Source: Path to the export file of a Service Map (default: None)
  --replace REGEX REPLACEWITH
                        Transforming regex pattern and replacement string (option can be repeated) (default: None)
  --parentlink          If root Service has a link to a parent, link the imported Service Map (default: False)
  --clobber             Overwrite Service Map (i.e. with same name) if it already exists (default: False)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="cloneservicemaps"></a>cloneservicemaps     
Copy an existing Service Map, with transformations/replacements (useful when you have a template Service Map to re-use)
```shell
usage: opcli cloneservicemaps [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --name NAME --replace REGEX REPLACEWITH [--parentlink] [--clobber]

Command-specific arguments:
  -h, --help            show this help message and exit
  --secure SECURE       Whether or not to verify SSL cert (default: True)
  --name NAME           Name of Service Map to transform and clone (default: None)
  --replace REGEX REPLACEWITH
                        Transforming regex pattern and replacement string (option can be repeated) (default: None)
  --parentlink          If root Service has a link to a parent, link the imported Service Map (default: False)
  --clobber             Overwrite Service Map (i.e. with same name) if it already exists (default: False)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
### Example

```shell
% opcli cloneservicemaps --env myenv --name HUB --replace HUB HUBCOPY --parentlink
```
# <a id="transformsvcmap"></a>transformsvcmap      
Apply regex replacements to an exported Service Map and create a new transformed export file with the changes.  Note that no credentials are required for this command since it is just operating on local export files.
```shell
usage: opcli transformsvcmap [-h] src dest --replace REGEX REPLACEWITH [--clobber]

positional arguments:
  src                   Source: File path where a Service Map was previously exported
  dest                  Destination: File path where the transformed export will be saved

Command-specific arguments:
  -h, --help            show this help message and exit
  --replace REGEX REPLACEWITH
                        Transforming regex pattern and replacement string (option can be repeated) (default: None)
  --clobber             Overwrite dest file if it already exists (default: False)
```
# <a id="getservicemaps"></a>getservicemaps       
Get Service Map definitions
```shell
usage: opcli getservicemaps [-h] --env ENV [--secure SECURE] [--envfile ENVFILE]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="getchildsvcgroups"></a>getchildsvcgroups    
Get child Service Groups of a parent Service
```shell
usage: opcli getchildsvcgroups [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --parent PARENT

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --parent PARENT    ID of the parent Service Map/Group (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="getservicegroup"></a>getservicegroup      
Get the full definition of a Service Group
```shell
usage: opcli getservicegroup [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --id ID

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --id ID            ID of the Service Map/Group (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="exportcustattrfile"></a>exportcustattrfile   
Generate an Excel or csv file from existing custom attribute values
```shell
usage: opcli exportcustattrfile [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] [--query QUERY] [--search SEARCH] [--filter FILTER] [--filename FILENAME]

Command-specific arguments:
  -h, --help           show this help message and exit
  --secure SECURE      Whether or not to verify SSL cert (default: True)
  --query QUERY        Query String to filter resources as per https://develop.opsramp.com/resource-management/tenants-tenantid-resources-search (default: None)
  --search SEARCH      Search String to filter resources as it would be entered under Resources -> Search (default: None)
  --filter FILTER      Post-query filter on resources. Python expression that will evaluate to True or False such as alert["resource"]["name"].startswith("prod") (default: None)
  --filename FILENAME  Name of excel file to generate (.xlsx extension will be added) (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="importcustattrfile"></a>importcustattrfile   
Import an Excel file containing custom attribute values
```shell
usage: opcli importcustattrfile [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] [--commit] [--writeblanks] [--filename FILENAME]

Command-specific arguments:
  -h, --help           show this help message and exit
  --secure SECURE      Whether or not to verify SSL cert (default: True)
  --commit             Make the actual updates on the platform. If not specified, only error checking and import simulation will occur. (default: False)
  --writeblanks        When no value is provided in the spreadsheet for a resource, remove any existing value for that resource on the platform. If not specified then no action is taken for empty values. (default: False)
  --filename FILENAME  Name of excel file to import (.xlsx extension will be added if not specified.) (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="getcustomattrs"></a>getcustomattrs       
Get custom attribute definitions
```shell
usage: opcli getcustomattrs [-h] --env ENV [--secure SECURE] [--envfile ENVFILE]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="getdiscoprofile"></a>getdiscoprofile      
Get discovery profile definition
```shell
usage: opcli getdiscoprofile [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] --id ID --tenantId TENANTID

Command-specific arguments:
  -h, --help           show this help message and exit
  --secure SECURE      Whether or not to verify SSL cert (default: True)
  --id ID              Discovery profile ID (default: None)
  --tenantId TENANTID  Client ID or MSP ID of the tenant (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="getalertesc"></a>getalertesc          
Search and get Escalation Policy definitions
```shell
usage: opcli getalertesc [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] [--query QUERY] [--details] [--count] [--filter FILTER]

Command-specific arguments:
  -h, --help         show this help message and exit
  --secure SECURE    Whether or not to verify SSL cert (default: True)
  --query QUERY      Query String to filter alerts (default: None)
  --details          Get the full details for all matched policies (default: False)
  --count            Only show the count of matching alerts (default: False)
  --filter FILTER    Post-query filter on alerts. Python expression that will evaluate to True or False such as alert["resource"]["name"].startswith("prod") (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="migratealertesc"></a>migratealertesc      
Migrate/copy Escalation Policies within same tenant or from one tenant to another
```shell
usage: opcli migratealertesc [-h] --env ENV [--secure SECURE] [--envfile ENVFILE] [--query QUERY] [--filter FILTER] [--preexec PREEXEC] [--postexec POSTEXEC] --to_env TO_ENV [--test] [--update] [--setactive SETACTIVE]

Command-specific arguments:
  -h, --help            show this help message and exit
  --secure SECURE       Whether or not to verify SSL cert (default: True)
  --query QUERY         Query string to filter policies from source/from instance (default: None)
  --filter FILTER       Filter for which policies to migrate. Python expression that will evaluate to True or False such as alert["resource"]["name"].startswith("prod") (default: None)
  --preexec PREEXEC     Pre-mapped exec command (default: None)
  --postexec POSTEXEC   Post-mapped exec command (default: None)
  --to_env TO_ENV       Target environment to which policy definitions will be migrated. (--env option defines the source/from environment) (default: None)
  --test                Test run only. Will check object mappings for missing items and not actually change the target instance. (default: False)
  --update              Used for bulk updates, will only work if --env and --to_env are the same. Try to update existing policies instead of creating new ones. (default: False)
  --setactive SETACTIVE
                        Specify ON or OFF. Will force all policies created on the target to be ON or OFF. Otherwise will be set the same as the source. (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
```
# <a id="clonetemplates"></a>clonetemplates
Clone monitoring templates
```shell
 usage: opcli clonetemplates [-h] [--env ENV] [--envfile ENVFILE] [--url URL] [--client_id KEY] [--client_secret SCRT] [--tenant TENANT] [--partner PARTNER] [--secure SECURE] (--name NAME | --infile INFILE)
                            (--prefix PREFIX | --copyname COPYNAME)

Command-specific arguments:
  -h, --help            show this help message and exit
  --secure SECURE       Whether or not to verify SSL cert (default: True)
  --name NAME           Name of the Monitoring Template to clone (default: None)
  --infile INFILE       File containing list of templates to clone (requires use of --prefix option) (default: None)
  --prefix PREFIX       New template name will be same as original name but with this text prepended (default: None)
  --copyname COPYNAME   New template will have this as its name (default: None)

Specify credentials via YAML file:
  --env ENV             Name of environment to use, as defined in your environments.yml file (default: None)
  --envfile ENVFILE     Location of environments YAML file (default: environments.yml)

Specify credentials via command line:
  --url URL             OpsRamp API URL (default: None)
  --client_id KEY       OpsRamp API Key (default: None)
  --client_secret SCRT  OpsRamp API Secret (default: None)
  --tenant TENANT       OpsRamp tenant ID (default: None)
  --partner PARTNER     OpsRamp partner ID (usually unnecessary - only needed for partner-level API calls) (default: None)
  ```


