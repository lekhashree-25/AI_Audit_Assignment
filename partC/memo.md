\# Part C — Engineering Decision Memo



\## Decision



Proceed with the proposed system only with the audit findings and

capacity constraints explicitly accounted for. The tokenizer audit

shows that multilingual inputs can have substantially different

tokenization behavior, so English-only measurements should not be

treated as representative of all languages.



\## Evidence



\### Multilingual tokenizer audit



The evaluation corpus contains English, Hindi, Kannada and Tamil

samples. The audit measures tokenizer fertility using the available

corpus and reports tokenization behavior across languages.



The important observation is that tokenizer efficiency is not uniform

across languages. Therefore, capacity planning based only on English

token counts can underestimate the token and compute requirements for

other languages.



\### Serving benchmark



The benchmark contains measurements across different prompt lengths,

generation lengths and request batch sizes.



The benchmark records reported throughput, time-to-first-token,

inter-token latency, end-to-end latency, preempted sequences and

KV-cache utilization.



The measurements show that increasing concurrent load and sequence

length increases memory pressure and latency. Therefore, peak

capacity should not be estimated from a single benchmark point.



\## Recommendation



Use multilingual measurements rather than an English-only estimate

for capacity planning.



For production deployment:



1\. Include representative multilingual traffic in the benchmark.

2\. Track TTFT and end-to-end latency separately.

3\. Monitor KV-cache utilization and preemptions.

4\. Re-test at the expected peak concurrency.

5\. Keep an operational safety margin rather than targeting maximum

&#x20;  hardware utilization continuously.



\## Limitations



This evaluation uses a small corpus and benchmark measurements from

the provided assignment setup. The results should therefore be treated

as evidence for engineering reasoning rather than a complete

production capacity guarantee.



A larger, representative production corpus and additional load-test

points would be required before making a final production-sizing

decision.



\## Final Position



The evidence supports a cautious deployment decision: multilingual

tokenization and serving capacity must be considered together.

Production sizing should be based on measured worst-case or

high-percentile behavior rather than a single average workload.

