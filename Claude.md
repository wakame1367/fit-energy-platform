# 🚀 Project Overview
This repository implements a lightweight solar FIT-pipeline:
- Download monthly FIT Excel → parse to CSV → geocode → convert to GeoParquet.
- Data stored in S3; DuckDB used for querying and dashboard.
- Apps: frontend (Next.js + Mapbox + DuckDB‑WASM), API (Lambda), data pipeline (Lambda ETL).
- Infra managed with Terraform modules (`lambda`, `s3`, `eventbridge`, etc.).

# 🔧 Common Commands
- `make infra-dev apply` / `make infra-prod apply` – Deploy Terraform in respective envs.
- `make run-local-pipeline` – Run Excel-to-GeoParquet flow locally.
- `make test` – Run tests across packages.
- `make lint` – Code formatting and linting.

# 🧰 Code Style & Structure
- Terraform modules under `modules/terraform/*`.
- Apps under `apps/{frontend, api, data_pipeline}`.
- Use snake_case for filenames/scripts, PascalCase for components.
- Use Prettier / ESLint / black for formatting.

# 🧵 Workflow
1. Read and understand context: don't edit before planning.
2. Use agentic cycle: **think → plan → code → test → commit**.
3. Tests (DuckDB queries or Lambda integration) must pass before commit.
4. Frequent small PRs; request ≥2 reviews before merge.
5. Clear commit messages (e.g. `feat: add geocode lambda`).

# ☁️ Tool Permissions
- Allow: `bash:*, git commit:*`, `claude code`.
- Disallow elevated ops (e.g. infrastructure apply) unless explicitly approved.

# 🧪 Pipeline Modules
- `lambda_excel_download`: Polls FIT portal via EventBridge.
- `lambda_csv_to_geoparquet`: Parses and geocodes addresses → GeoParquet.
- Frontend: Next.js + DuckDB‑WASM + Mapbox.
- API: Lambda + API Gateway to query GeoParquet files via DuckDB.
- Infra: Terraform modules with env-differentiated config.

# ⚠️ Special Instructions
- Geocoder API keys are stored securely in SSM Parameter Store.
- S3 bucket naming: prefixed by `solar-pipeline-{env}`.
- DuckDB HTTPFS and spatial extensions are installed in API layer.
- For local, set `AWS_PROFILE` and run `install_duckdb_exts.sh`.

# 🔄 Reinforcement & Updates
- Keep this file up-to-date as modules evolve.
- Use `claude code` to assist in updating sections dynamically:
  > “Update CLAUDE.md to reflect new Lambda for weather ingestion.”

# 🤖 Agentic & Prompt Practices
- Be **explicit**: specify files, funcs, tests.
- Provide motivation/context for each task.
- Use `think`, `think hard` modes for design-level requests.
- Validate parsing/integration via DuckDB queries.

# 📘 References
- CLAUDE.md is auto-loaded by Claude Code to avoid token overhead :contentReference[oaicite:1]{index=1}.
- Use top-level and module-level `CLAUDE.md` for shared and specific settings :contentReference[oaicite:2]{index=2}.
