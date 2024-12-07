# Knowledge Base CLI

There simple concepts you always forget? Do you have a lot of notes and you can't find the one you need?
This is a simple fuzzy finder CLI tool that allows you to interact with a knowledge base saved as notes.

## Installation

Just run pip or uv to install the package:

```bash
# using uvx
uv tool install git+https://github.com/joseph-pq/kb-cli.git
# using pipx
pipx install git+https://github.com/joseph-pq/kb-cli.git
```

## Usage

Create some yaml file with your notes.
For example, `~/Documents/metrics.yaml` file with some statistics concepts:

```yaml
precision: |
  Precision is the fraction of relevant instances among the retrieved instances.
  formula: TP / (TP + FP)
recall: |
  Recall is the fraction of relevant instances that have been retrieved over the total amount of relevant instances.
  formula: TP / (TP + FN)
f1_score: |
  The F1 score is the harmonic mean of precision and recall.
  formula: 2 * (precision * recall) / (precision + recall)
```

Then you can use kb to add this file to your knowledge base:

```bash
kb add ~/Documents/metrics.yaml
```

Finally, you can search for a concept:

```bash
kb search
```

You can also run `kb --help` to see all available commands.
