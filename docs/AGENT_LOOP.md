# Optional bounded agent loop

Aikya can execute one explicitly authorized ODD or SDD task through the optional
Claude Agent SDK. Aikya controls scope, dependencies, iterations, checks and task
closure; Claude Code owns model/tool execution, conversation storage and context.
The SDK is not installed automatically. The existing 27 slash commands remain.

## Prepare and authorize

Use /aikya-feature, /aikya-bugfix or /aikya-implement with an explicit request to use
the agent loop. First initialize an ODD worklist or approve the active SDD
specification, plan and tasks. Every task dependency must be complete. Small ODD
work can continue through the ordinary inline workflow without creating a dossier.
/aikya-init and /aikya-analyze never start this loop automatically.

Install the optional runtime in a separate Python environment when you choose to
use it. The tested SDK is 0.2.173, with Python 3.10 or later:

```bash
python3 -m venv .venv-aikya-loop
.venv-aikya-loop/bin/python -m pip install -r /path/to/aikya/requirements-agent-loop.txt
.venv-aikya-loop/bin/python /path/to/aikya/agent_runtime.py check
```

Authenticate Claude in that environment using your organization's supported
method. Do not put credentials in the reviewed JSON, task files or audit records.
The SDK's API estimate is not a subscription quota or authoritative bill.

Review a configuration like this, adapting the files and checks to your project:

```json
{
  "schema": 1,
  "command": "aikya-feature",
  "work_id": "value",
  "task_id": "TASK-001",
  "files": ["src/value.py"],
  "context_files": ["tests/test_value.py"],
  "max_iterations": 3,
  "max_turns": 8,
  "timeout_seconds": 120,
  "max_cost_usd": 0.25,
  "memory_budget_chars": 4000,
  "hooks_approved": false,
  "checks": [
    {
      "name": "value-tests",
      "phase": "validate",
      "argv": ["python3", "-m", "unittest", "discover", "-s", "tests"],
      "timeout_seconds": 30
    },
    {
      "name": "project-security",
      "phase": "security",
      "argv": ["python3", "scripts/check_security.py"],
      "timeout_seconds": 30
    }
  ]
}
```

Checks must actually exist and be appropriate to the change. Their exact argv are
part of the authorization: they run locally with the selected environment and can
have side effects. Aikya does not certify arbitrary check scripts as safe or turn
them into a sandbox. Validation and scoped Security checks are both required.

The model can only Read approved files/context and Edit/Write approved task files.
Bash, Skill, subagents, network/MCP tools and writes to Aikya controls are not
available as child tools. In SDD, use work_id=SPEC-NNN; the loop checks the real
stage approvals before execution and never creates them. The SDK loads user,
project and local settings, preserving deny/ask rules. Configured hooks execute
under those settings and need separate review with hooks_approved=true; their
settings hashes are bound to the invocation. This is an application policy layer,
not protection against a hostile OS user concurrently replacing filesystem paths.

## Execute, observe and stop

Use the Python environment containing the optional SDK and the resolved Aikya CLI
(project runtime first, otherwise the registered global runtime):

```bash
python /path/to/aikya_cli.py feature --target . --agent-loop --loop-input reviewed-loop.json --approved
```

The JSON command must match the requested feature, bugfix or implement command.
Explore, Plan, Implement, Validate, Security and Review remain English; status is
separate. The local process observer and the durable summary record outcomes.
Review uses a separate read-only model invocation. A model's claim of success
cannot replace process checks or approve SDD stages.

The loop handles one task per invocation and reports its outcome; select a new
task explicitly instead of silently expanding the approved files/checks. It runs
at most three implementation iterations, stops after two unchanged candidates
with no accepted outcome, and applies the reviewed runtime turn/time limits.
The same time/cost ledger survives resume. max_turns applies to each SDK query;
iteration, elapsed-time and cumulative estimate limits bound the enclosing loop.
Estimated-cost limits can overshoot by an in-flight provider request; they are not
hard billing guarantees. Missing cost data blocks further execution. Missing token
counts stay unknown, and provider weekly limits are never inferred from them.

## Audit and recovery

The loop creates only substantive records:

```text
aikya/docs/loops/<run-id>/
  state.json
  summary.md
  evidence.json    # only after checks and review accept the current candidate
```

summary.md follows the configured en/es documentation language and has the exact
Aikya footer; indice.md includes it. JSON holds control metadata, not conversation
prompts, credentials or raw tool output. Evidence contains check exit codes,
command hashes, candidate fingerprints and the review invocation reference.
Writes use temporary files, fsync and atomic replacement; files are separate
checkpoints, not a multi-file ACID transaction or a tamper-proof signed receipt.
Custom summaries, changed approvals/context, symlinks and another checkout require
review instead of being silently overwritten. Do not manually edit state to reset
budgets or mark outcomes complete.

```bash
python /path/to/agent_loop.py status --root . --run-id RUN_ID
python /path/to/aikya_cli.py feature --target . --agent-loop --loop-input reviewed-loop.json --loop-run-id RUN_ID --approved
```

An effect intent is durably acknowledged before the child writes. If a process
stops before its matching result arrives, automatic resume refuses to replay it.
Inspect the files and checkpoints, then explicitly reconcile when appropriate:

```bash
python /path/to/agent_loop.py reconcile --root . --run-id RUN_ID --approved
```

Reconciliation does not replay tools or erase history. An unfinished model query
has unknown usage and blocks further model calls; it does not become a free retry.
Exhausted limits remain exhausted. A separately reviewed new run is a new budget
and authorization decision. Successful closure updates the ODD task or SDD task;
it does not perform requirement-level SDD verification or certify an application
as secure. External installation, publication and deployment retain their own
permissions.

## Selective project memory

Reviewed notes are optional references under aikya/docs/memory/. Each note has a
type (user, feedback, project or reference), source fingerprint, creation time and
TTL. Existing custom notes are preserved; stale sources and expired notes are
excluded. MEMORY.md is a generated index. Only this project's notes are searched,
with at most five selected notes and a total character budget; this is lexical
retrieval, not embeddings. Private/team stores and automatic extraction are not
part of this implementation.

```bash
python /path/to/agent_memory.py add --root . --input reviewed-memory.json --approved
python /path/to/agent_memory.py recall --root . --query "value lookup" --budget-chars 4000
```

The input has exactly kind, text, source and ttl_days (1–365). The source must be a
current regular project file. Memory never grants permissions, completes tasks or
replaces actual files/evidence. The controller labels recovered notes as untrusted
reference material.

## Verify in another environment

Local tests exercise process behavior, installation and failure boundaries without
calling a model. The optional SDK contract check constructs real SDK options and
runs its callbacks without authentication:

```bash
python tests/sdk_agent_loop_contract.py
python -m unittest discover -s tests -p 'test_agent_loop*.py'
python -m unittest discover -s tests -p 'test_agent_memory.py'
```

For the controlled live smoke, use scripts/ci/agent_loop_smoke.py with --live,
--approved and an explicit --max-cost-usd. It creates an isolated synthetic project,
allows only its value file, executes real validation/Security checks and requires
read-only model review. It never deploys or installs SDKs. A successful fixture
suite alone is not a successful live SDK run.

Official references: [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview),
[permissions](https://code.claude.com/docs/en/agent-sdk/permissions),
[usage estimates](https://code.claude.com/docs/en/agent-sdk/cost-tracking).

GENERATED BY AIKYA HARNESS
