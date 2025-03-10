# ML-Git commands #

<details markdown="1">
<summary><code> ml-git --help </code></summary>
<br>

```
Usage: ml-git [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.

Commands:
  clone       Clone an ml-git repository ML_GIT_REPOSITORY_URL
  datasets    Management of datasets within this ml-git repository.
  labels      Management of labels sets within this ml-git repository.
  models      Management of models within this ml-git repository.
  repository  Management of this ml-git repository.
```

Example:
```
ml-git --help
```

</details>

<details markdown="1">
<summary><code> ml-git --version </code></summary>

Displays the installed version of ML-Git.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; add </code></summary>
<br>

```
Usage: ml-git datasets add [OPTIONS] ML_ENTITY_NAME [FILE_PATH]...

  Add datasets change set ML_ENTITY_NAME to the local ml-git staging area.

Options:
  --bumpversion                   Increment the version number when adding
                                  more files.
  --fsck                          Run fsck after command execution.
  --metric <TEXT FLOAT>...        Metric key and value.
  --metrics-file                  Metrics file path.
  --wizard                        Enable the wizard to request information
                                  when needed.
  --verbose                       Debug mode
```

Dataset example:
```
ml-git datasets add dataset-ex --bumpversion
```

ml-git expects datasets to be managed under _dataset_ directory.
\<ml-entity-name\> is also expected to be a repository under the tree structure and ml-git will search for it in the tree.
Under that repository, it is also expected to have a \<ml-entity-name\>.spec file, defining the ML entity to be added.
Optionally, one can add a README.md which will describe the dataset and be what will be shown in the github repository for that specific dataset.

Internally, the _ml-git add_ will add all the files under the \<ml-entity\> directory into the ml-git index / staging area.

Model example:
```
ml-git models add model-ex --metrics-file='/path/to/your/file.csv'
```

ml-git allows you to enter a metrics file or the metrics themselves on the command line when adding a model.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; branch </code></summary>
<br>

```
Usage: ml-git datasets branch [OPTIONS] ML_ENTITY_NAME

  This command allows to check which tag is checked out in the ml-git
  workspace.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets branch imagenet8
```
Output:
```
('vision-computing__images__imagenet8__1', '48ba1e994a1e39e1b508bff4a3302a5c1bb9063e')
```

That information is equal to the HEAD reference from a git concept. ml-git keeps that information on a per \<ml-entity-name\> basis. which enables independent checkout of each of these \<ml-entity-name\>.

The output is a tuple:
1) the tag auto-generated by ml-git based on the \<ml-entity-name\>.spec (composite with categories, \<ml-entity-name\>, version)
2) the sha of the git commit of that \<ml-entity\> version
Both are the same representation. One is human-readable and is also used internally by ml-git to find out the path to the referenced \<ml-entity-name\>.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; checkout </code></summary>
<br>

```
Usage: ml-git models checkout [OPTIONS] ML_ENTITY_TAG|ML_ENTITY

  Checkout the ML_ENTITY_TAG|ML_ENTITY of a model set into user workspace.

Options:
  -l, --with-labels           The checkout associated labels  in user
                              workspace as well.
  -d, --with-dataset          The checkout associated dataset in user
                              workspace as well.
  --retry INTEGER RANGE       Number of retries to download the files from the
                              storage. This number must be in the range 
                              0-999999999 [default: 2].
  --force                     Force checkout command to delete
                              untracked/uncommitted files from local
                              repository.
  --bare                      Ability to add/commit/push without having the
                              ml-entity checked out.
  --version INTEGER RANGE     Number of artifact version to be downloaded.
                              This number must be in the range 0-999999999 
                              [default: latest].
  --fail-limit INTEGER RANGE  Number of failures before aborting the command.
                              This number must be in the range 0-999999999
                              [default: no limit].
  --full                      Show all contents for each directory when
                              there are files to be discarded at checkout.
  --wizard                    Enable the wizard to request information when
                              needed.
  --verbose                   Debug mode
```

Examples:
```
ml-git datasets checkout computer-vision__images__faces__fddb__1
```
or you can use the name of the entity directly and download the latest available tag
```
ml-git datasets checkout fddb
```


Note:

```--d:``` It can only be used in checkout of labels and models to get the entities that are associated with the entity.

```--l:``` It can only be used in checkout of models to get the label entity that are associated with the entity.

```--sample-type, --sampling, --seed:``` These options are available only for dataset. If you use this option ml-git will not allow you to make changes to the entity and create a new tag.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; commit </code></summary>
<br>

```
Usage: ml-git models commit [OPTIONS] ML_ENTITY_NAME

  Commit model change set of ML_ENTITY_NAME locally to this ml-git
  repository.

Options:
  --dataset NOT EMPTY STRING  Link a dataset entity name to this model set
                              version
  --labels NOT EMPTY STRING   Link a labels entity name to this model set
                              version
  --version INTEGER RANGE     Set the version number of the artifact. This
                              number must be in the range 0-999999999.
  -m, --message TEXT          Use the provided <msg> as the commit message.
  --fsck                      Run fsck after command execution.
  --wizard                    Enable the wizard to request information when
                              needed.
  --verbose                   Debug mode
```

Example:
```
ml-git models commit model-ex --dataset=dataset-ex
```

This command commits the index / staging area to the local repository. It is a 2-step operation in which 1) the actual data (blobs) is copied to the local repository, 2) committing the metadata to the git repository managing the metadata.
Internally, ml-git keeps track of files that have been added to the data storage and is storing that information to the metadata management layer to be able to restore any version of each \<ml-entity-name\>.

Another important feature of ml-git is the ability to keep track of the relationship between the ML entities. So when committing a label set, one can (should) provide the option ```--dataset=<dataset-name>```.
Internally, ml-git will inspect the HEAD / ref of the specified \<dataset-name\> checked out in the ml-git repository and will add that information to the specificatino file that is committed to the metadata repository.
With that relationship kept into the metadata repository, it is now possible for anyone to checkout exactly the same versions of labels and dataset.

Same for ML model, one can specify which dataset and label set that have been used to generate that model through ```--dataset=<dataset-name>``` and ```--labels=<labels-name>```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; create </code></summary>
<br>

```
Usage: ml-git datasets create [OPTIONS] ARTIFACT_NAME

  This command will create the workspace structure with data and spec file
  for an entity and set the git and storage configurations. [This command 
  has a wizard that will request the necessary information if it is not 
  informed]

Options:
  --categories TEXT               Artifact's categories names. The categories
                                  names must be separated by comma. 
                                  E.g: "category1,category2,category3". [required]
  --mutability [strict|flexible|mutable]
                                  Mutability type.  [required]
  --storage-type [s3h|azureblobh|gdriveh|sftph]
                                  Storage type (s3h, azureblobh, gdriveh,
                                  sftph) [default: s3h]
  --version INTEGER RANGE         Set the version number of the artifact. This
                                  number must be in the range 0-999999999.
  --import NOT EMPTY STRING       Path to be imported to the project. NOTE:
                                  Mutually exclusive with argument:
                                  credentials_path, import_url.
  --wizard-config                 If specified, ask interactive questions at
                                  console for git & storage configurations.
                                  [DEPRECATED: This option should no longer be
                                  used.]
  --bucket-name NOT EMPTY STRING  Bucket name
  --import-url NOT EMPTY STRING   Import data from a google drive url. NOTE:
                                  Mutually exclusive with argument: import.
  --credentials-path NOT EMPTY STRING
                                  Directory of credentials.json. NOTE: This
                                  option is required if --import-url is used.
  --unzip                         Unzip imported zipped files. Only available
                                  if --import-url is used.
  --entity-dir NOT EMPTY STRING   The relative path where the entity will be
                                  created inside the ml entity directory.
  --wizard                        Enable the wizard to request information
                                  when needed.
  --verbose                       Debug mode
```

Examples:
 - To create an entity with s3 as storage and importing files from a path of your computer:
```
ml-git datasets create imagenet8 --storage-type=s3h --categories="computer-vision, images" --version=0 --import='/path/to/dataset' --mutability=strict
```

- To create an entity with s3 as storage and importing files from a google drive URL:
```
ml-git datasets create imagenet8 --storage-type=s3h --categories=computer-vision,images --import-url='gdrive.url' --credentials-path='/path/to/gdrive/credentials' --mutability=strict --unzip
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; diff </code></summary>
<br>

```
Usage: ml-git datasets diff [OPTIONS] ML_ENTITY_NAME FIRST_TAG SECOND_TAG
                            
  Print the difference between two entity tag versions. The command will
  show added, updated and deleted files.

Options:
  --full     Show all contents for each directory.
  --verbose  Debug mode
```

Examples:
 - To check the difference between entity tag versions:
```
ml-git datasets diff dataset-ex computer-vision__images__dataset-ex__1 computer-vision__images__dataset-ex__4
```
Output:
```
Added files:
    data/   ->      4 FILES
    tabular.csv
Updated files:
    data/dataset_test.csv
Deleted files:
    data/dataset_old.csv
```

- To check the difference between entity tag versions showing all contents for each directory:
```
ml-git datasets diff --full dataset-ex computer-vision__images__dataset-ex__1 computer-vision__images__dataset-ex__4
```
Output:
```
Added files:
    data/dataset_1.csv
    data/dataset_2.csv
    data/dataset_3.csv
    data/dataset_4.csv
    tabular.csv
Updated files:
    data/dataset_test.csv
Deleted files:
    data/dataset_old.csv
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; export </code></summary>
<br>

```
Usage: ml-git datasets export [OPTIONS] ML_ENTITY_TAG BUCKET_NAME

  This command allows you to export files from one storage (S3|MinIO) to
  another (S3|MinIO).

Options:
  --credentials TEXT     Profile of AWS credentials [default: default].
  --endpoint TEXT        Storage endpoint url.
  --region TEXT          AWS region name [default: us-east-1].
  --retry INTEGER RANGE  Number of retries to download the files from the
                         storage. This number must be in the range
                         0-999999999 [default: 2].
  --verbose              Debug mode
```

Example:
```
ml-git datasets export computer-vision__images__faces__fddb__1 minio
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; fetch </code></summary>
<br>

```
Usage: ml-git datasets fetch [OPTIONS] ML_ENTITY_TAG

  Allows you to download just the metadata files of an entity.

Options:
  --sample-type [group|range|random]
  --sampling TEXT                 The group: <amount>:<group> The group sample
                                  option consists of amount and group used to
                                  download a sample.
                                  range: <start:stop:step>
                                  The range sample option consists of start,
                                  stop and step used to download a sample. The
                                  start parameter can be equal or greater than
                                  zero.The stop parameter can be 'all', -1 or
                                  any integer above zero.
                                  random:
                                  <amount:frequency> The random sample option
                                  consists of amount and frequency used to
                                  download a sample.
  --seed TEXT                     Seed to be used in random-based samplers.
  --retry INTEGER RANGE           Number of retries to download the files from
                                  the storage. This number must be in the
                                  range 0-999999999 [default: 2].
  --verbose                       Debug mode
```

Example:
```
ml-git datasets fetch computer-vision__images__faces__fddb__1
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; fsck </code></summary>
<br>

```
Usage: ml-git datasets fsck [OPTIONS]

Options:
  --fix-workspace  Use this option to repair files identified as corrupted in
                   the entity workspace.
  --full           Show the list of corrupted files.
  --verbose        Debug mode
```

Example:
```
ml-git datasets fsck
```

This command will walk through the internal ml-git directories (index & local repository) and check the presence and integrity of all file blobs under its management.

This command will basically try to:

* Detect any chunk/blob that is corrupted or missing in the internal ml-git directory (.ml-git/{entity-type}/objects)
* Fetch files detected as corrupted or missing from storage
* Check the integrity of files mounted in the entities workspace
*  In fix-workspace mode, repair corrupted files found in the entities workspace. A file in the entities workspace is considered 'corrupted' based on the business rule defined by the mutability of the entity.
If you want to know more about each type of mutability and how it works, please take a look at [Mutability documentation](mutability_helper.md).

It will return the list of blobs that are corrupted/missing if the user passes the --full option.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; import </code></summary>
<br>

```
Usage: ml-git datasets import [OPTIONS] BUCKET_NAME ENTITY_DIR

  This command allows you to download a file or directory from the S3 or
  Gdrive to ENTITY_DIR.

Options:
  --credentials TEXT          Input your profile to an s3 storage or your
                              credentials path to a gdrive storage.(eg,
                              --credentials=path/to/.credentials
  --region TEXT               AWS region name [default: us-east-1].
  --retry INTEGER RANGE       Number of retries to download the files from the
                              storage. This number must be in the range 
                              0-999999999 [default: 2].
  --path TEXT                 Storage folder path.
  --object TEXT               Filename in storage.
  --storage-type [s3|gdrive]  Storage type (s3, gdrive) [default: s3]
  --endpoint-url TEXT         Storage endpoint url.
  --verbose                   Debug mode

```

Example:
```
ml-git datasets import bucket-name dataset/computer-vision/imagenet8/data
```
For google drive storage:
```
ml-git datasets import gdrive-folder --storage-type=gdrive --object=file_to_download --credentials=credentials-path dataset/
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; init </code></summary>
<br>

```
Usage: ml-git datasets init [OPTIONS]

  Init a ml-git datasets repository.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets init
```

This command is mandatory to be executed just after the addition of a remote metadata repository (_ml-git \<ml-entity\> remote add_).
It initializes the metadata by pulling all metadata to the local repository.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; metrics </code></summary>
<br>

```
Usage: ml-git models metrics [OPTIONS] ML_ENTITY_NAME

  Shows metrics information for each tag of the entity.

Options:
  --export-path TEXT        Set the path to export metrics to a file. NOTE:
                            This option is required if --export-type is used.
  --export-type [csv|json]  Choose the format of the file that will be
                            generated with the metrics [default: json].
  --verbose                 Debug mode
```

Example:
```
ml-git models metrics model-ex
```

Note:
```
This command is only available for model entities.
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; list </code></summary>
<br>

```
Usage: ml-git datasets list [OPTIONS]

  List datasets managed under this ml-git repository.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets list
```
Output:
```
ML dataset
|-- computer-vision
|   |-- images
|   |   |-- dataset-ex-minio
|   |   |-- imagenet8
|   |   |-- dataset-ex
```

</details>


<details markdown="1">
<summary><code>ml-git &lt;ml-entity&gt; log </code></summary>
<br>

```
Usage: ml-git datasets log [OPTIONS] ML_ENTITY_NAME

  This command shows ml-entity-name's commit information like author, date,
  commit message.

Options:
  --stat      Show amount of files and size of an ml-entity.
  --fullstat  Show added and deleted files.
  --verbose   Debug mode
```

Example:
```
ml-git datasets log dataset-ex
```

</details>



<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; push </code></summary>
<br>

```
Usage: ml-git datasets push [OPTIONS] ML_ENTITY_NAME

  Push local commits from ML_ENTITY_NAME to remote ml-git repository &
  storage.

Options:
  --retry INTEGER RANGE       Number of retries to download the files from the
                              storage. This number must be in the range 
                              0-999999999 [default: 2].
  --clearonfail               Remove the files from the storage in case of
                              failure during the push operation.
  --fail-limit INTEGER RANGE  Number of failures before aborting the command.
                              This number must be in the range 0-999999999 
                              [default: no limit].
  --verbose                   Debug mode
```

Example:
```
ml-git datasets push dataset-ex
```

This command will perform a 2-step operations:
1. push all blobs to the configured data storage.
2. push all metadata related to the commits to the remote metadata repository.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; remote-fsck </code></summary>
<br>

```
Usage: ml-git datasets remote-fsck [OPTIONS] ML_ENTITY_NAME
  This command will check and repair the remote, by default it will 
  only repair by uploading lacking chunks/blobs. Options bring more 
  specialized repairs.

Options:
  --thorough             Try to download the IPLD if it is not present in the
                         local repository to verify the existence of all
                         contained IPLD links associated.
  --paranoid             Adds an additional step that will download all IPLD
                         and its associated IPLD links to verify the content
                         by computing the multihash of all these.
  --retry INTEGER RANGE  Number of retries to download the files from the
                         storage. This number must be in the range 0-999999999 
                         [default: 2].
  --full                 Show the list of fixed and unfixed blobs and IPLDs.
  --wizard               Enable the wizard to request information when needed.
  --verbose              Debug mode
```

Example:
```
ml-git datasets remote-fsck dataset-ex
```

This ml-git command will basically try to:

* Detects any chunk/blob lacking in a remote storage for a specific ML artefact version
* Repair - if possible - by uploading lacking chunks/blobs
* In paranoid mode, verifies the content of all the blobs

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; reset </code></summary>
<br>

```
Usage: ml-git datasets reset [OPTIONS] ML_ENTITY_NAME

  Reset ml-git state(s) of an ML_ENTITY_NAME

Options:
  --hard                     Remove untracked files from workspace, files to
                             be committed from staging area as well as
                             committed files upto <reference>.
  --mixed                    Revert the committed files and the staged files
                             to 'Untracked Files'. This is the default action.
  --soft                     Revert the committed files to 'Changes to be
                             committed'.
  --reference [head|head~1]  head:Will keep the metadata in the current
                             commit.
                             head~1:Will move the metadata to the last
                             commit.
  --verbose                  Debug mode
```

Examples:

```
ml-git datasets reset dataset-ex --hard
```

* Undo the committed changes.
* Undo the added/tracked files.
* Reset the workspace to fit with the current HEAD state.

```
ml-git datasets reset dataset-ex --mixed
```
if HEAD:
* nothing happens.
else:
* Undo the committed changes.
* Undo the added/tracked files.

```
ml-git datasets reset dataset-ex --soft
```
if HEAD:
* nothing happens.
else:
* Undo the committed changes.

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; show </code></summary>
<br>

```
Usage: ml-git datasets show [OPTIONS] ML_ENTITY_NAME

  Print the specification file of the entity.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets show dataset-ex
```
Output:
```
-- dataset : imagenet8 --
categories:
- vision-computing
- images
manifest:
  files: MANIFEST.yaml
  storage: s3h://mlgit-datasets
name: imagenet8
version: 1
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; status </code></summary>
<br>

```
Usage: ml-git datasets status [OPTIONS] ML_ENTITY_NAME [STATUS_DIRECTORY]

  Print the files that are tracked or not and the ones that are in the
  index/staging area.

Options:
  --full     Show all contents for each directory.
  --verbose  Debug mode
```

Example:
```
ml-git datasets status dataset-ex
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; tag add</code></summary>
<br>

```
Usage: ml-git datasets tag add [OPTIONS] ML_ENTITY_NAME TAG

  Use this command to associate a tag to a commit.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets tag add dataset-ex my_tag
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; tag list </code></summary>
<br>

```
Usage: ml-git datasets tag list [OPTIONS] ML_ENTITY_NAME

  List tags of ML_ENTITY_NAME from this ml-git repository.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets tag list dataset-ex
```

</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; update </code></summary>
<br>

```
Usage: ml-git datasets update [OPTIONS]

  This command will update the metadata repository.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets update
```

This command enables one to have the visibility of what has been shared since the last update (new ML entity, new versions).
</details>

<details markdown="1">
<summary><code> ml-git &lt;ml-entity&gt; unlock </code></summary>
<br>

```
Usage: ml-git datasets unlock [OPTIONS] ML_ENTITY_NAME FILE

  This command add read and write permissions to file or directory. Note:
  You should only use this command for the flexible mutability option.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git datasets unlock dataset-ex data/file1.txt
```

Note:

```
You should only use this command for the flexible mutability option.
```
 
</details>


<details markdown="1">
<summary><code> ml-git clone &lt;repository-url&gt; </code></summary>
<br>

```
Usage: ml-git clone [OPTIONS] REPOSITORY_URL [DIRECTORY]

  Clone an ml-git repository ML_GIT_REPOSITORY_URL

Options:
  --untracked  Does not preserve git repository tracking.
  --verbose    Debug mode
```

Example:
```
ml-git clone https://git@github.com/mlgit-repository
```

</details>

<details markdown="1">
<summary><code> ml-git login </code></summary>
<br>

```
Usage: ml-git login [OPTIONS]

  login command generates new Aws credential.

Options:
  --credentials TEXT  profile name for store credentials [default: default].
  --insecure          use this option when operating in a insecure location.
                      This option prevents storage of a cookie in the folder.
                      Never execute this program without --insecure option in
                      a compute device you do not trust.
  --rolearn TEXT      directly STS to this AWS Role ARN instead of the
                      selecting the option during runtime.
  --help              Show this message and exit.

```

Example:
```
ml-git login
```

</details>

<details markdown="1">
<summary><code> ml-git repository config </code></summary>
<br>

```
Usage: ml-git repository config [OPTIONS] COMMAND [ARGS]...

  Management of the ML-Git config file.

Options:
  --set-wizard [enabled|disabled] Enable or disable the wizard for all
                                  supported commands.
  --help                          Show this message and exit.

Commands:
  push  Create a new version of the ML-Git configuration file.
  show  Configuration of this ML-Git repository

```

Example:
```
ml-git repository config --set-wizard=enabled
```

</details>

<details markdown="1">
<summary><code> ml-git repository config push</code></summary>
<br>

```
Usage: ml-git repository config push [OPTIONS]

  Create a new version of the ML-Git configuration file. This command
  internally runs git's add, commit and push commands.

Options:
  -m, --message TEXT  Use the provided <msg> as the commit message.
  --verbose           Debug mode
```

Example:
```
ml-git repository config push -m "My commit message"
```

</details>

<details markdown="1">
<summary><code> ml-git repository config show</code></summary>
<br>

```
Usage: ml-git repository config show [OPTIONS]

  Configuration of this ml-git repository

Options:
  -l, --local   Local configurations
  -g, --global  Global configurations
  --verbose     Debug mode
```

Example:
```
ml-git repository config show
```
Output:
```
config:
{'datasets': {'git': 'git@github.com:example/your-mlgit-datasets'},
 'storages': {'s3': {'mlgit-datasets': {'aws-credentials': {'profile': 'mlgit'},
                                     'region': 'us-east-1'}}},
 'verbose': 'info'}
```

Use this command if you want to check what configuration ml-git is running with. It is highly likely one will need to 
change the default configuration to adapt for her needs.

</details>

<details markdown="1">
<summary><code> ml-git repository gc </code></summary>
<br>

```
Usage: ml-git repository gc [OPTIONS]

  Cleanup unnecessary files and optimize the use of the disk space.

Options:
  --verbose  Debug mode
```

This command will remove unnecessary files contained in the cache and objects directories of the ml-git metadata (.ml-git).

</details>


<details markdown="1">
<summary><code> ml-git repository graph </code></summary>
<br>

```
Usage: ml-git repository graph [OPTIONS]

  Creates a graph of all entity relations as an HTML file and automatically
  displays it in the default system application.

Options:
  --verbose           Debug mode
  --dot               Instead of creating an HTML file, it displays the graph
                      on the command line as a DOT language.
  --export-path TEXT  Set the directory path to export the generated graph file.
```

Example:
```
ml-git repository graph
```
Output:
```
digraph "Entities Graph" {
"models-ex (1)" [color="#d63638"];
"dataset-ex (1)" [color="#2271b1"];
"models-ex (1)" -> "dataset-ex (1)";
"models-ex (1)" [color="#d63638"];
"labels-ex (1)" [color="#996800"];
"models-ex (1)" -> "labels-ex (1)";
}
```

This command will iterate through the tags of all ML-Git entities and create the relationships between them.

Note: 

```
To successfully execute the command it is necessary that it is in an ML-Git project initialized, and with the URLs of the remote repositories properly configured.
```

</details>

<details markdown="1">
<summary><code> ml-git repository init </code></summary>
<br>

```
Usage: ml-git repository init [OPTIONS]

  Initialization of this ML-Git repository

Options:
  --help  Show this message and exit.
```

Example:
```
ml-git repository init
```

This is the first command you need to run to initialize a ml-git project. It will bascially create a default .ml-git/config.yaml

</details>

<details markdown="1">
<summary><code> ml-git repository remote &lt;ml-entity&gt; add </code></summary>
<br>

```
Usage: ml-git repository remote datasets add [OPTIONS] REMOTE_URL

  Add remote dataset metadata REMOTE_URL to this ml-git repository.

Options:
  -g, --global  Use this option to set configuration at global level
  --verbose     Debug mode
```

Example:
```
ml-git repository remote datasets add https://git@github.com/mlgit-datasets
```

</details>

<details markdown="1">
<summary><code> ml-git repository remote &lt;ml-entity&gt; del </code></summary>
<br>

```
Usage: ml-git repository remote datasets del [OPTIONS]

  Remove the REMOTE_URL datasets' metadata from this ml-git repository

Options:
  -g, --global  Use this option to set configuration at global level
  --verbose     Debug mode
```

Example:
```
ml-git repository remote datasets del
```

</details>

<details markdown="1">
<summary><code> ml-git repository remote config add </code></summary>
<br>

```
Usage: ml-git repository remote config add [OPTIONS] REMOTE_URL

  Starts a git at the root of the project and configure the remote.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git repository remote config add https://git@github.com/mlgit-config
```

</details>

<details markdown="1">
<summary><code> ml-git repository storage add </code></summary>
<br>

```
Usage: ml-git repository storage add [OPTIONS] BUCKET_NAME

  Add a storage BUCKET_NAME to ml-git [This command has a wizard that 
  will request the necessary information if it is not informed]

Options:
  --credentials TEXT              Profile name for storage credentials
  --type [s3h|azureblobh|gdriveh|sftph]
                                  Storage type (s3h, azureblobh, gdriveh,
                                  sftph) [default: s3h]
  --region TEXT                   AWS region name for S3 bucket
  --endpoint-url TEXT             Storage endpoint url.
  --username TEXT                 The username for the sftp login.
  --private-key TEXT              Full path for the private key file.
  --port INTEGER                  SFTP port [default: 22].
  -g, --global                    Use this option to set configuration at
                                  global level
  --wizard                        Enable the wizard to request information
                                  when needed.
  --verbose                       Debug mode
```

Example:
```
ml-git repository storage add minio --endpoint-url=<minio-endpoint-url>
```

Use this command to add a data storage to a ml-git project.

</details>

<details markdown="1">
<summary><code> ml-git repository storage del </code></summary>
<br>

```
Usage: ml-git repository storage del [OPTIONS] BUCKET_NAME

  Delete a storage BUCKET_NAME from ml-git

Options:
  --type [s3h|azureblobh|gdriveh|sftph]
                                  Storage type (s3h, azureblobh, gdriveh,
                                  sftph) [default: s3h]
  -g, --global                    Use this option to set configuration at
                                  global level
  --wizard                        Enable the wizard to request information 
                                  when needed.
  --verbose                       Debug mode
```

Example:
```
ml-git repository storage del minio
```

</details>

<details markdown="1">
<summary><code> ml-git repository update </code></summary>
<br>

```
Usage: ml-git repository update [OPTIONS]

  This command will update all ml-entities' metadata repository.

Options:
  --verbose  Debug mode
```

Example:
```
ml-git repository update
```

</details>

