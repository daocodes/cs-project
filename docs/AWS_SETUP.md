# AWS Setup

Account and access setup for Phase 0 (issue #3). Covers AWS account structure, IAM access for local dev, Bedrock model access, and billing guardrails.

---

## Account

- **Account ID:** `451664151866`
- **Region:** `us-east-1` (N. Virginia) — required for Bedrock Claude model availability and CloudWatch billing metrics
- Root user owns only account-level actions (billing, IAM). Root MFA is enabled. **Root is never used for day-to-day work.**

## IAM access for local dev

Each partner has their own IAM user (no shared root login, no shared credentials):

- Both users belong to the `developers` IAM group
- Group policies: `ReadOnlyAccess` (console navigation) + `AmazonBedrockFullAccess` (Bedrock invoke + console access)
- Each user has console access (own password + MFA) and an access key for CLI/local dev use only

### Local CLI setup

Install the AWS CLI and configure a named profile — do **not** put raw keys in `.env` or any committed file:

```bash
brew install awscli
aws configure --profile internbase-dev
```

You'll be prompted for your personal access key ID, secret access key, region (`us-east-1`), and output format (`json`).

Verify it works:

```bash
aws sts get-caller-identity --profile internbase-dev
aws bedrock list-foundation-models --region us-east-1 --profile internbase-dev
```

The first confirms your IAM identity; the second confirms Bedrock model access from the CLI.

## Bedrock model access

AWS's standalone "Model access" console page is retired — models now auto-enable per-account on first invoke. Anthropic models require a one-time "Submit use case details for Anthropic" form before first invocation.

Access was confirmed working via:
- Bedrock Playground (Chat) — test invocation succeeded
- AWS CLI — `aws bedrock list-foundation-models` returns Claude models

## Billing guardrails

- **CloudWatch billing alarms:** $30 and $50 thresholds on the `EstimatedCharges` metric (namespace `Billing`), notifying via SNS topic `billing-alarms` (email subscription confirmed)
- **AWS Budget:** $10 monthly budget with an alert at $5
- Treat these as tripwires, not a spending plan — the goal is to stay within free credits. Review Cost Explorer whenever an alarm or budget alert fires.

## Credentials policy

- AWS access keys are local-only, stored via named CLI profiles (`internbase-dev`), never committed
- No `.env` file in this repo should ever contain `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — use `.env.example` as the template and keep real values out of version control
