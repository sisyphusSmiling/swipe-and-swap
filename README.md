# Swipe & Swap Cadence to Typescript

> :warning: This tool is a quick and dirty prototype to address the pain point of importing Cadence into a dependent dApp's source code. If you like the idea, please contribute with issues & PRs!

Just a sorry stand-in for a Cadence package manager. These are some utility Python scripts that will **swipe** `.cdc` files from a GitHub repo, save them to your local directory & **swap** them to TypeScript consts in the same folder structure as the originating repository. These tools can be useful for devs building dApps depending on Cadence source code maintained in another repository.

## `swipe-and-swap.py`

### Swipe

Grab Cadence files from the named repo and save them locally. This does not clone the target repo, it simply copies the files in the repo's `contracts/`, `transactions/`, and `scripts/` directories into your local `cadence/` folder, replacing it if it exists. Note that the script currently expects all Cadence code to exist in the aforementioned directories - any other structure will result in unexpected behavior. This is an oppportunity for future improvements.

### Swap

Translate those local Cadence files (`*.cdc`) in your `cadence/` directory to TypeScript (`*.ts`) files, saving the contents of the Cadence files as:

```ts
const CADENCE_FILENAME = '
    cadence file content
' 

default export FILENAME
```

## Usage

```
usage: swipe-and-swap.py [-h] [--action ACTION] [--repo REPO] [--branch BRANCH] [--swipe-dest SWIPE_DEST] [--swap-dest SWAP_DEST]

Copy contracts, scripts, and transactions from a GitHub repository & swap to TypeScript consts

options:
  -h, --help            show this help message and exit
  --action ACTION       Action to perform - swipe/swap/both (default is both)
  --repo REPO           owner/name of the Cadence repo
  --branch BRANCH       Name of the branch to clone (default is main)
  --swipe-dest SWIPE_DEST
                        Name of the directory to save to
  --swap-dest SWAP_DEST
                        Directory to save your .ts files to (default is src/cadence)
```

## Getting Started

1. Create & activate the virtual environment of your choice
1. Install requirements
    ```sh
    pip install -r requirements
    ```
1. Copy from your desired repo & swap TypeScript consts for use in your dApp!
    ```
    python src/swipe-and-swap.py --action both --repo onflow/flow-nft --branch master --swipe-dest cadence/ --swap-dest src/cadence/
    ```

## Considerations
These tools are a prototype & leverage GitHub's API. Depending on how frequently you use `swipe-cadence.py` and/or how large the repo you're copying is, you may run into rate-limiting. Check out [GitHub docs](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting) for info on their rate limiting policies.

Also note that **swiping will overwrite the target directory**. So if you have a local `cadence/` folder and run the swiper, it will be overwritten by the contents of the source repo. Swapping exhibits safer behavior, leaving your existing TypeScipt folders & directories alone.