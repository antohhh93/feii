## Fix error ilm index in Elasticsearch

## Usage

```
Usage: feii [OPTIONS] COMMAND [ARGS]...

  Feii - utility for ilm indexes in Elasticsearch that allows you to:
    * fix errors in indexes
    * delete empty indexes
    * rollover big indexes
    * adding alias in indexes
    * applying parameters
    * fix write in indices

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  alias     Fix indexes without an alias.
  delete    Deletion of empty indexes.
  error     Fix ILM error.
  rollover  Rollover the big indexes.
  test      In the development.
  update    Update index settings.
  write     Fix of writing in indices.

  Run 'feii COMMAND --help' for more information on a command.
```
