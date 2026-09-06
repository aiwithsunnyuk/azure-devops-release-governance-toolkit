# Azure DevOps Release Governance Toolkit

[![CI & Governance Quality Gate](https://github.com/aiwithsunnyuk/azure-devops-release-governance-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/aiwithsunnyuk/azure-devops-release-governance-toolkit/actions)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Framework](https://img.shields.io/badge/framework-Streamlit%20%7C%20Pydantic-red.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Compliance](https://img.shields.io/badge/governance-SOC2%20%7C%20ISO27001%20%7C%20SLSA-success.svg)

An enterprise deployment quality gate and release orchestration control plane for **Azure Pipelines**. It bridges release automation, security compliance, and change management into an automated, auditable gatekeeper preventing risky code from reaching production.

---

## The Problem It Solves

Modern CI/CD pipelines move fast, but enterprise deployments require strict guardrails. Development, DevOps, and Security teams often face:
* **Manual Change Advisory Board (CAB) bottlenecks:** Hours wasted chasing approvals and audit evidence across disconnected tools.
* **Late-stage CVE discoveries:** High-severity vulnerabilities slipping through CI steps into staging and production clusters.
* **Lack of unified visibility:** No central pane where engineering leads, compliance auditors, and release managers can inspect build artifacts, coverage metrics, and SBOM provenance simultaneously.

This toolkit provides a **programmable, shift-left governance layer** that acts as an automated gatekeeper. If pre-configured baselines (coverage, CVE thresholds, SonarQube quality gates, branch protections) pass, releases progress automatically; if policies fail, clear audit paths and break-glass override protocols are enforced.

---

## Architectural Workflow

```mermaid
flowchart TD
    Build[Azure Pipelines CI / Build Stage] --> Package[Artifact Packaging & Container Registry]
    Package --> Evaluator[Governance & Quality Gate Engine]

    subgraph Automated Policy Evaluations
        Evaluator --> Cov[Code Coverage Baseline >= 80%]
        Evaluator --> Sonar[SonarQube Quality Gate == PASS]
        Evaluator --> Sec[Vulnerability Scan: 0 Critical / 0 High CVEs]
        Evaluator --> SBOM[CycloneDX SBOM Provenance Check]
    end

    Cov --> Decision{All Baselines Satisfied?}
    Sonar --> Decision
    Sec --> Decision
    SBOM --> Decision

    Decision -->|PASS| AutoDeploy[Automated Release Dispatch to Target Stage]
    Decision -->|FAIL| Blocked[Deployment Blocked]

    Blocked --> CAB[Manual CAB Review / Audited Break-Glass Override]
    CAB -->|Approved & Justified| AutoDeploy
    CAB -->|Rejected| Terminate[Pipeline Terminated]
