---

## Directory Structure

```text
.
├── .azuredevops
│   └── pull_request_template.md
├── pipelines
│   ├── templates
│   │   ├── steps
│   │   │   ├── sast-scan.yml
│   │   │   └── automated-smoke-test.yml
│   │   └── jobs
│   ├── ci-pipeline.yml
│   └── cd-release-pipeline.yml
├── scripts
│   └── bash
│       └── generate-release-notes.sh
└── terraform
    └── environments
