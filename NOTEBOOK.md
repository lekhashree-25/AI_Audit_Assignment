\# AI Audit Assignment — Lab Notebook



\## Day 1 — Repository and Corpus Setup



\- Organized the assignment into Part A, Part B and Part C.

\- Prepared a focused multilingual corpus containing English, Hindi, Kannada and Tamil samples.

\- Documented the corpus files under `partA/corpus/`.

\- The corpus is treated as an evaluation sample and not as a population-representative dataset.

\- Created the initial audit and fertility-analysis files.



\## Day 2 — Metric and Audit Work



\- Reviewed the tokenization/fertility metric used in the analysis.

\- Examined how the metric is calculated from the corpus.

\- Checked the relationship between the metric definition, numerator, denominator and interpretation.

\- Documented the audit findings in `partA/audit\_report.md`.



\## Day 3 — Corrected Analysis



\- Reproduced the relevant analysis using the available corpus and scripts.

\- Compared the reported interpretation with the underlying evidence.

\- Focused on denominator and aggregation reasoning rather than accepting a numerical result without checking its definition.

\- Recorded the resulting interpretation and limitations in the audit report.



\## Day 4 — Capacity and Benchmark Analysis



\- Documented the FLM-4B-Instruct model and serving configuration in `partB/model\_spec.md`.

\- Reviewed the NVIDIA L4 hardware assumptions.

\- Examined benchmark measurements in `partB/bench\_log.csv`.

\- Compared theoretical hardware specifications with measured serving behavior.

\- Considered workload shape, sequence length, batching, latency and KV-cache utilization when reasoning about capacity.



\## Day 5 — Decision and Submission Preparation



\- Organized the final repository structure.

\- Prepared the Part C decision memo.

\- Added this chronological notebook to document the work process.

\- Added `AI\_USAGE.md` to document AI assistance transparently.

\- Reviewed the repository structure and prepared the work for the live defense.



\## Key Lessons



1\. A plausible metric value is not sufficient evidence by itself.

2\. The denominator and aggregation method can materially affect interpretation.

3\. A focused corpus should not automatically be treated as representative of an entire language.

4\. Peak GPU specifications are not equivalent to real inference serving capacity.

5\. Benchmark measurements should be interpreted together with model, hardware and workload assumptions.

6\. Conclusions should clearly state their limitations.



\## Final Workflow



Corpus → Metric Audit → Corrected Analysis → Benchmark Evidence → Capacity Reconciliation → Decision

