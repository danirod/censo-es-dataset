---
version: "0.1.2"
level: copilot
processes:
  design: copilot
  implementation: none
  testing: copilot
  documentation: none
components:
  docs/llm_analysis: copilot
---

This format is based on [AI-DECLARATION.md](https://ai-declaration.md/en/0.1.2).

## Notes

Anything that has to do with understanding the upstream data files format as
well as large scale analysis and validation of the datasets was outsourced to
an AI model.

The AI model might have access to a separate memory vault to store notes about
the parsed dataset, and to dump one off scripts to efficiently analyze and test
the dataset.
