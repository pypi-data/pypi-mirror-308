# pkl-github-action-step-generator

A simple CLI tool to generate a Pkl definition for a given action

## Usage
The tool supports generating Pkl step definitions from two sources, remote or local.

For local, the command is as follows:

```sh
pkl-github-actions-step-generator from-local <path-to-action.yml> <full-reference-to-action> [-o --output <OUTPUT FILE>] [--pkl-github-actions-bindings] [--pkl-github-actions-bindings-version]
```

`full-reference-to-action` should be in the form you would use to reference the action in a workflow (e.g. `actions/checkout@v4`).

The `--pkl-github-actions-bindings` enables the generation of bindings to [pkl-github-actions](https://github.com/emilymclean/pkl-github-actions). The version flag allows you to specify a version (otherwise a default will be used).

If no output is provided, the file content will instead be output to stdout.

Remote has the same options, except it finds the `action.yml` in the remote repository:

```sh
pkl-github-actions-step-generator from-remote <full-reference-to-action> [-o --output <OUTPUT FILE>] [--pkl-github-actions-bindings] [--pkl-github-actions-bindings-version]
```

For example, to generate a file containing the definition for the checkout action, the command would be:
```sh
pkl-github-actions-step-generator from-remote actions/checkout@v4 -o checkout.pkl
```