# azure-devops-release-governance-toolkit

## Architecture Overview

```mermaid
flowchart TD
    A[Git Push / PR] --> B[CI: Lint & Unit Tests]
    B --> C[Step Template: SAST Scan]
    C --> D[Artifact / Image Registry]
    D --> E[CD: Staging Deployment]
    E --> F[Step Template: Automated Smoke Tests]
    F --> G{Manual Approval Gate}
    G -- Approved --> H[CD: Production Rolling / Blue-Green]
    H --> I[Canary Health Check]
    I --> J[Release Notes Generation]
---
