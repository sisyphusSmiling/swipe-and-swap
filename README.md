# Swipe & Swap Cadence to Typescript

> :warning: This tool is a quick and dirty prototype to address the pain point of importing Cadence into a dependent dApp's source code. If you like the idea, please contribute with issues & PRs!

Just a sorry stand-in for a Cadence package manager. These are some utility Python scripts that will **swipe** `.cdc` files from a GitHub repo, save them to your local directory & **swap** them to TypeScript consts in the same folder structure as the originating repository. These tools can be useful for devs building dApps depending on Cadence source code maintained in another repository.

## `swipe-cadence.py`
Grab Cadence files from the named repo and save them locally. This does not clone the target repo, it simply copies the files in the repo's `contracts/`, `transactions/`, and `scripts/` directories into your local `cadence/` folder, replacing it if it exists.

### Usage

```
Swap contracts, scripts, and transactions from a GitHub repository to your local machine (without cloning)

options:
  -h, --help       show this help message and exit
  --repo REPO      owner/name of the Cadence repo
  --branch BRANCH  Name of the branch to clone (default is main)
```

## `swap-cadence.py`
Translate those local Cadence files (`*.cdc`) in your `cadence/` directory to TypeScript (`*.ts`) files, saving the contents of the Cadence files as:

```ts
const CADENCE_FILENAME = '
    cadence file content
' 

default export FILENAME
```

### Usage

```
usage: swap-cadence.py [-h] [--source-dir SOURCE_DIR] [--dest DEST]

Swap contracts, scripts, and transactions from your local directory to TypeScript constants

options:
  -h, --help            show this help message and exit
  --source-dir SOURCE_DIR
                        Directory holding your .cdc files (default is cadence/)
  --dest DEST           Directory to save your .ts files to (default is src/cadence)
```

## Using these scripts

1. Create & activate the virtual environment of your choice
1. Install requirements
    ```sh
    pip install -r requirements
    ```
1. Copy from your desired repo
    ```
    python swipe-cadence.py --repo onflow/flow --branch main
    ```
1. Swap from Cadence to TypeScript
    ```sh
    python swap-cadence.py --source-dir cadence/ --dest src/cadence/
    ```

## Considerations
These tools are a prototype & leverage GitHub's API. Depending on how frequently you use `swipe-cadence.py` and/or how large the repo you're copying is, you may run into rate-limiting. Check out [GitHub docs](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting) for info on their rate limiting policies.

Also note that swipe-cadence.py will overwrite target directories. So if you have a local `cadence/` folder and run the swiper, it will be overwritten by the contents of the source repo. Swapping exhibits safer behavior, leaving your existing TypeScipt folders & directories alone.