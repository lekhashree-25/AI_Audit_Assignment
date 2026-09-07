\# AI Audit Report



\## 1. Executive Summary



The supplied v0 report contains several conclusions that are not fully supported by the measured evidence.



The tokenizer audit shows that GPT-2 has substantially higher Hindi fertility than English, but comparison with XLM-R demonstrates that tokenizer choice has a major effect. Therefore, the high Hindi fertility observed with GPT-2 should not be attributed solely to the script or generalized to all tokenizers.



The serving benchmark also contradicts the assumption of linear throughput scaling. Long-prompt throughput peaks at batch 24 with 1607.4 tok/s and declines at larger batches. Batch 48 achieves only 1298.5 tok/s, rather than the approximately 3200 tok/s predicted in the v0 report. Larger batches also show increased KV-cache utilization, preemptions, and latency.



\## 2. Tokenizer Fertility Audit



\### 2.1 Whitespace Handling



The original implementation used:



&#x20;   words = line.split(" ")



This can count empty strings when multiple spaces occur in a line.



The corrected implementation uses:



&#x20;   words = line.split()



This treats consecutive whitespace as a separator and avoids counting empty strings as words.



Using the corrected implementation, the GPT-2 results are:



| Language | Fertility (tok/word) | Tok/char |

|---|---:|---:|

| English | 1.28 | 0.226 |

| Hindi | 7.60 | 1.579 |



Therefore, the whitespace correction changes the fertility measurement and should be included in the audit.



\### 2.2 Tokenizer Comparison



The audit was also performed using XLM-R:



| Language | GPT-2 | XLM-R |

|---|---:|---:|

| English | 1.28 | 1.30 |

| Hindi | 7.60 | 1.45 |



XLM-R substantially reduces Hindi fertility compared with GPT-2.



Therefore, the original conclusion that Hindi tokenization difficulty is primarily a property of the script is not supported by these measurements. Tokenizer design has a major impact on the observed fertility.



The original recommendation to budget approximately 6x serving cost for Hindi should therefore not be applied universally. The appropriate tokenizer/model should be evaluated before making a serving-cost assumption.



\### 2.3 Case Normalization



The audit checked token counts before and after lowercasing.



| Language | Original tokens | Lowercase tokens |

|---|---:|---:|

| English | 96 | 99 |

| Hindi | 459 | 459 |



Lowercasing changes the English token count in the sample, so casing is not completely neutral for GPT-2 tokenization. The effect should therefore be documented rather than assumed to be irrelevant.



\## 3. Tokenizer Findings



\### 3.1 GPT-2



With the original whitespace implementation, the supplied GPT-2 benchmark reported:



| Language | Fertility (tok/word) | Tok/char |

|---|---:|---:|

| English | 1.27 | 0.226 |

| Hindi | 7.45 | 1.579 |



The corrected whitespace implementation produced approximately:



| Language | Fertility (tok/word) | Tok/char |

|---|---:|---:|

| English | 1.28 | 0.226 |

| Hindi | 7.60 | 1.579 |



The Hindi-to-English fertility ratio is therefore approximately 5.9x.



However, this result applies to the GPT-2 tokenizer and should not be generalized to all tokenizers.



\### 3.2 XLM-R



The XLM-R benchmark reported:



| Language | Fertility (tok/word) | Tok/char |

|---|---:|---:|

| English | 1.30 | 0.228 |

| Hindi | 1.45 | 0.303 |



The Hindi fertility difference is therefore much smaller with XLM-R than with GPT-2.



This demonstrates that tokenizer selection materially affects multilingual token efficiency.



\## 4. Serving Throughput Audit



\### 4.1 Long-Prompt Benchmark



For prompt length 3584 and generation length 512, the measured throughput was:



| Batch | Throughput (tok/s) |

|---:|---:|

| 4 | 565.4 |

| 8 | 902.6 |

| 16 | 1311.4 |

| 24 | 1607.4 |

| 32 | 1384.0 |

| 48 | 1298.5 |



Throughput increases from batch 4 through batch 24.



The highest observed throughput is at batch 24:



&#x20;   1607.4 tok/s



After batch 24, throughput decreases:



&#x20;   Batch 32 = 1384.0 tok/s

&#x20;   Batch 48 = 1298.5 tok/s



Therefore, the benchmark does not support a linear relationship between batch size and throughput.



\### 4.2 Comparison With the Original Report



The original v0 report stated that:



&#x20;   Batch 16 = 1311 tok/s



and suggested that throughput could scale approximately linearly to:



&#x20;   Batch 48 ≈ 3200 tok/s



The measured batch-48 throughput is instead:



&#x20;   1298.5 tok/s



Therefore, the predicted 3200 tok/s at batch 48 is not supported by the benchmark.



The measured data show a throughput peak followed by degradation at higher batch sizes.



\### 4.3 KV-Cache Utilization



The benchmark shows increasing KV-cache utilization at larger batch sizes.



Relevant measurements include:



| Batch | KV-cache utilization | Preempted sequences |

|---:|---:|---:|

| 16 | 0.62 | 0 |

| 24 | 0.93 | 0 |

| 32 | 0.97 | 7 |

| 48 | 0.97 | 23 |



At batch 24, utilization reaches 0.93 without observed preemptions.



At batch 32, utilization reaches 0.97 and 7 sequences are preempted.



At batch 48, utilization remains at 0.97 and 23 sequences are preempted.



This indicates increasing memory pressure and scheduler preemption at larger batch sizes.



\### 4.4 Latency



For long prompts, the measured latency also increases with larger batch sizes.



| Batch | TTFT p50 (ms) | ITL p50 (ms) | E2E p95 (ms) |

|---:|---:|---:|---:|

| 4 | 483.2 | 51.33 | 32673.3 |

| 8 | 519.0 | 62.26 | 39982.9 |

| 16 | 498.3 | 77.20 | 54602.1 |

| 24 | 500.5 | 96.07 | 69221.3 |

| 32 | 636.9 | 101.79 | 97465.7 |

| 48 | 955.4 | 100.00 | 105427.5 |



The batch-48 configuration has substantially higher TTFT and p95 end-to-end latency than the lower-batch configurations.



Therefore, the highest possible batch size should not automatically be treated as the best serving configuration.



\## 5. Short-Prompt vs Long-Prompt Throughput



For batch 16:



\- Short prompt throughput = 883.2 tok/s

\- Long prompt throughput = 1311.4 tok/s



The long-prompt benchmark therefore achieves higher measured throughput at batch 16.



However, the longer prompt also has substantially higher latency:



\- Long-prompt TTFT p50 = 498.3 ms

\- Long-prompt E2E p95 = 54602.1 ms



Therefore, the observation that long prompts achieve higher throughput does not by itself justify encouraging clients to add more context.



Throughput and latency must be considered together.



\## 6. Audit of Original Conclusions



\### 6.1 Claim: Hindi fertility is 5.89x worse than English



The GPT-2 measurement supports an approximately 5.9x fertility ratio.



However, this conclusion is specific to GPT-2. XLM-R produces Hindi fertility of 1.45 tok/word compared with English fertility of 1.30 tok/word.



Therefore, the result should not be generalized to all tokenizers.



\### 6.2 Claim: Hindi will cost approximately 6x more per request



The fertility measurements alone do not establish a universal 6x serving-cost multiplier.



Serving cost also depends on the tokenizer, model, prompt length, generation length, batching, hardware utilization, and serving configuration.



Therefore, a fixed 6x Hindi cost assumption is not justified from the supplied measurements alone.



\### 6.3 Claim: Tok/char confirms the per-word result



The tok/char values show a substantial difference between English and Hindi under GPT-2:



&#x20;   English = 0.226 tok/char

&#x20;   Hindi = 1.579 tok/char



However, the tok/char ratio and fertility ratio measure different quantities.



Therefore, tok/char provides additional evidence of tokenization differences but does not by itself confirm the proposed causal explanation.



&#x20;6.4 Claim: Hindi difficulty is a property of the script, not the tokenizer



This conclusion is not supported by the tokenizer comparison.



GPT-2:



&#x20;   Hindi = 7.60 tok/word



XLM-R:



&#x20;   Hindi = 1.45 tok/word



The large difference demonstrates that tokenizer choice has a major effect.



\### 6.5 Claim: Longer prompts clearly give better GPU utilization



The benchmark shows higher throughput for the tested long prompts at batch 16.



However, longer prompts also produce higher TTFT and end-to-end latency.



Therefore, higher throughput alone does not establish that clients should be encouraged to send longer prompts.



\### 6.6 Claim: Throughput scales linearly with batch size



The benchmark directly contradicts this assumption.



Throughput:



&#x20;   Batch 16 = 1311.4 tok/s

&#x20;   Batch 24 = 1607.4 tok/s

&#x20;   Batch 32 = 1384.0 tok/s

&#x20;   Batch 48 = 1298.5 tok/s



Throughput peaks at batch 24 and decreases afterward.



Therefore, linear scaling should not be assumed.



\### 6.7 Claim: Batch 48 should achieve approximately 3200 tok/s



The measured batch-48 throughput is only:



&#x20;   1298.5 tok/s



This is substantially below the predicted 3200 tok/s.



The prediction is therefore not supported by the supplied benchmark.



7\. Revised Recommendations



1\. Do not assume a universal 6x Hindi serving-cost multiplier based only on GPT-2 fertility.



2\. Evaluate tokenizer choice separately for each target language.



3\. Use whitespace-aware word counting with:



&#x20;      words = line.split()



&#x20;  rather than:



&#x20;      words = line.split(" ")



4\. Treat tokenizer fertility and tokens-per-character as separate metrics.



5\. Do not attribute multilingual tokenization efficiency solely to the writing system.



6\. Do not assume throughput scales linearly with batch size.



7\. For the supplied long-prompt benchmark, batch 24 provides the highest observed throughput of 1607.4 tok/s.



8\. Consider KV-cache utilization and scheduler preemption when increasing batch size.



9\. Consider TTFT, inter-token latency, and p95 end-to-end latency together with throughput.



10\. Do not encourage clients to add context solely because long prompts showed higher throughput in this benchmark.



11\. For capacity planning, use measured operating points rather than extrapolating linearly beyond the observed benchmark.



8\. Final Conclusion



The audit identifies two major issues in the supplied v0 report.



First, the tokenizer conclusion is too broad. GPT-2 shows very high Hindi fertility, but XLM-R produces substantially better Hindi fertility. This demonstrates that tokenizer choice is an important factor and that the observed GPT-2 result should not be treated as a universal property of Hindi.



Second, the serving recommendation incorrectly assumes linear throughput scaling. The benchmark reaches its highest throughput at batch 24 and then degrades at larger batches. KV-cache utilization, preemptions, and latency also increase at high batch sizes.



The revised analysis should therefore use measured tokenizer-specific results and measured serving operating points rather than broad assumptions about language cost or linear batch scaling.

