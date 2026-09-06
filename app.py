import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Azure DevOps Release Governance",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Azure DevOps Release Governance & Deployment Gate")
st.markdown("Automated pre-deployment quality gates, security audits, and compliance validation for Azure Pipelines.")

# Sidebar Configuration
with st.sidebar:
    st.header("Pipeline Environment")
    target_env = st.selectbox("Target Stage:", ["Production", "Staging / UAT", "Integration / QA"])
    release_tag = st.text_input("Release Candidate Tag:", value="release-v2.4.0-rc1")
    
    st.divider()
    st.header("Governance Thresholds")
    min_coverage = st.slider("Minimum Code Coverage (%)", min_value=60, max_value=95, value=80)
    allow_high_cve = st.checkbox("Allow High Severity CVE (Waiver Required)", value=False)
    require_cab_approval = st.checkbox("Require CAB / Dual Approval", value=True)

# Simulated Pipeline Data
pipeline_metrics = {
    "Unit Test Pass Rate": "100% (142/142)",
    "Code Coverage": 84.5,
    "Critical CVEs": 0,
    "High CVEs": 1,
    "Medium CVEs": 3,
    "SonarQube Quality Gate": "PASSED",
    "Branch Protection": "Enforced (main)",
    "SBOM Artifact": "Generated (CycloneDX)",
}

tab1, tab2, tab3 = st.tabs(["🚀 Release Gate Assessment", "📋 Policy Checks & Audit Trail", "📦 Artifact Provenance"])

with tab1:
    st.subheader(f"Deployment Assessment for: `{target_env}`")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Code Coverage", f"{pipeline_metrics['Code Coverage']}%", delta=f"{pipeline_metrics['Code Coverage'] - min_coverage:.1f}% vs threshold")
    col2.metric("Critical Security CVEs", pipeline_metrics["Critical CVEs"], delta="0 Allowed", delta_color="normal")
    col3.metric("High CVEs", pipeline_metrics["High CVEs"], delta="Requires Waiver" if not allow_high_cve else "Waiver Active", delta_color="inverse" if not allow_high_cve else "off")
    col4.metric("SonarQube Gate", pipeline_metrics["SonarQube Quality Gate"])

    # Governance Decision Engine
    failures = []
    if pipeline_metrics["Code Coverage"] < min_coverage:
        failures.append(f"Code coverage {pipeline_metrics['Code Coverage']}% is below target {min_coverage}%.")
    if pipeline_metrics["Critical CVEs"] > 0:
        failures.append(f"Found {pipeline_metrics['Critical CVEs']} critical CVEs.")
    if pipeline_metrics["High CVEs"] > 0 and not allow_high_cve:
        failures.append(f"Found {pipeline_metrics['High CVEs']} high severity CVEs with no active waiver.")

    st.divider()
    if not failures:
        st.success("✅ **GOVERNANCE GATE PASSED:** All enterprise compliance baselines satisfied. Release approved for automated pipeline execution.")
        st.button("🚀 Trigger Azure DevOps Release Pipeline", type="primary", width="stretch")
    else:
        st.error("⛔ **DEPLOYMENT BLOCKED (Gate Failed):**")
        for f in failures:
            st.write(f"- {f}")
        if target_env == "Production":
            st.warning("⚠️ Manual CAB override required to bypass quality gate failures.")
            override_reason = st.text_area("Emergency Bypass Justification (Audited to Azure DevOps Logs):")
            st.button("Authorize Emergency Break-Glass Release", disabled=(len(override_reason) < 15))

with tab2:
    st.subheader("Automated Compliance Policy Audit")
    checks = [
        {"Policy Name": "Branch Protection Rule", "Requirement": "Must originate from protected main branch", "Status": "PASS", "Severity": "High"},
        {"Policy Name": "Static Code Analysis", "Requirement": "SonarQube gate status == PASSED", "Status": "PASS", "Severity": "Critical"},
        {"Policy Name": "Test Coverage Baseline", "Requirement": f"Coverage >= {min_coverage}%", "Status": "PASS" if pipeline_metrics["Code Coverage"] >= min_coverage else "FAIL", "Severity": "Medium"},
        {"Policy Name": "Container Vulnerability Scan", "Requirement": "Zero Critical / High CVEs", "Status": "FAIL" if (pipeline_metrics["High CVEs"] > 0 and not allow_high_cve) else "PASS", "Severity": "Critical"},
        {"Policy Name": "Software Bill of Materials (SBOM)", "Requirement": "CycloneDX or SPDX compliant schema", "Status": "PASS", "Severity": "Low"},
    ]
    df_checks = pd.DataFrame(checks)
    st.dataframe(df_checks, width="stretch")

with tab3:
    st.subheader("Release Package & Artifact Metadata")
    st.json({
        "pipelineId": "ADO-BUILD-94821",
        "repository": "azure-devops-release-governance-toolkit",
        "commitHash": "8f3a11c8b209e82103fca3",
        "evaluatedAt": datetime.utcnow().isoformat() + "Z",
        "artifacts": [
            {"name": "production-service-image", "digest": "sha256:7b1e4...", "registry": "myacr.azurecr.io"},
            {"name": "helm-chart-deployment", "version": "1.2.0"}
        ]
    })
