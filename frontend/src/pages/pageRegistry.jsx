import React from 'react';

const Page = ({ title, description }) => (
  <section>
    <h1>{title}</h1>
    <p>{description}</p>
  </section>
);

export const pages = [
  { path: '/', label: 'Landing', component: <Page title='Landing / Overview' description='Enterprise summary of Zero Trust controls, cloud posture, and insider-risk indicators.' /> },
  { path: '/login', label: 'Login', component: <Page title='Login' description='Username/password authentication with enterprise account style.' /> },
  { path: '/register', label: 'Register', component: <Page title='Register Account' description='Admin-provisioned fake company users with role, department, clearance, and cloud mapping.' /> },
  { path: '/mfa', label: 'MFA', component: <Page title='MFA Step-Up' description='Triggered for risky actions and sensitive resources.' /> },
  { path: '/dashboard', label: 'Dashboard', component: <Page title='User Dashboard' description='Personal access posture, current risk score, and pending approvals.' /> },
  { path: '/cloud-a', label: 'Cloud A', component: <Page title='Cloud A Overview' description='Datasets, model jobs, storage, users, and policy status for Cloud A.' /> },
  { path: '/cloud-b', label: 'Cloud B', component: <Page title='Cloud B Overview' description='Datasets, model jobs, storage, users, and policy status for Cloud B.' /> },
  { path: '/sync', label: 'Sync Mgmt', component: <Page title='Synchronization Management' description='Secure cross-cloud sync workflow with verification and approvals.' /> },
  { path: '/datasets', label: 'Datasets', component: <Page title='Dataset / Logs' description='CERT raw logs, transformed features, and cloud-scoped datasets.' /> },
  { path: '/ml', label: 'ML Training', component: <Page title='ML Training' description='Train Random Forest insider-threat model and review metrics.' /> },
  { path: '/access', label: 'Access Request', component: <Page title='Access Request' description='Submit resource actions for Zero Trust policy evaluation.' /> },
  { path: '/decision', label: 'Decision', component: <Page title='Decision Results' description='ALLOW / STEP-UP / DENY outcomes with reasons and obligations.' /> },
  { path: '/audit', label: 'Audit Logs', component: <Page title='Audit Logs' description='Immutable timeline for authentication, access, policy, and sync actions.' /> },
  { path: '/admin', label: 'Admin', component: <Page title='Admin Console' description='Manage users, permissions, cloud assignments, and sync approvals.' /> },
];
