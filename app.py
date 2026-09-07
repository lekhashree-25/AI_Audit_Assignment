import streamlit as st
from pathlib import Path
import pandas as pd
import re

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="AI Audit — Results Demo",
    page_icon="🔎",
    layout="wide"
)

ROOT = Path(__file__).parent

st.title("🔎 AI Audit — Results Demo")
st.caption("Multilingual Tokenizer Audit • Benchmark Evidence • Decision")

# =========================================================
# SIDEBAR
# =========================================================

page = st.sidebar.radio(
    "Demo Navigation",
    [
        "🏠 Overview",
        "📊 Part A — Audit Results",
        "⚡ Part B — Benchmark Results",
        "📝 Part C — Decision"
    ]
)

# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.header("AI Audit Assignment")

    st.write(
        "Interactive demonstration of the audit evidence, "
        "measured results and engineering decision."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Part A", "Tokenizer Audit")

    with c2:
        st.metric("Part B", "Benchmarks")

    with c3:
        st.metric("Part C", "Decision")

    st.success("Demo is running successfully.")

    st.info(
        "Use the sidebar to open Part A and view the actual "
        "audit results from audit_report.md."
    )


# =========================================================
# PART A — RESULTS
# =========================================================

elif page == "📊 Part A — Audit Results":

    st.header("📊 Part A — Multilingual Audit Results")

    report_file = ROOT / "partA" / "audit_report.md"

    if not report_file.exists():
        st.error("partA/audit_report.md was not found.")
        st.stop()

    report = report_file.read_text(encoding="utf-8")

    # -----------------------------------------------------
    # SHOW NUMERICAL RESULTS FOUND IN THE REPORT
    # -----------------------------------------------------

    st.subheader("🔢 Audit Results")

    # Find markdown table rows
    table_rows = []

    for line in report.splitlines():

        line = line.strip()

        if (
            line.startswith("|")
            and line.endswith("|")
            and "---" not in line
        ):
            cells = [
                x.strip()
                for x in line.strip("|").split("|")
            ]

            if len(cells) >= 2:
                table_rows.append(cells)

    # Display markdown tables found in the report
    if table_rows:

        header = table_rows[0]

        data_rows = table_rows[1:]

        # Remove accidental header/separator rows
        data_rows = [
            row for row in data_rows
            if not all(
                re.fullmatch(r"[-: ]+", cell or "")
                for cell in row
            )
        ]

        if data_rows:

            # Make equal length
            width = len(header)

            cleaned_rows = []

            for row in data_rows:

                if len(row) < width:
                    row = row + [""] * (width - len(row))

                cleaned_rows.append(row[:width])

            result_df = pd.DataFrame(
                cleaned_rows,
                columns=header
            )

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No markdown results table was detected in "
            "partA/audit_report.md."
        )

    st.divider()

    # -----------------------------------------------------
    # DISPLAY THE ACTUAL REPORT
    # -----------------------------------------------------

    st.subheader("📄 Audit Evidence")

    with st.expander(
        "Open complete audit report",
        expanded=True
    ):
        st.markdown(report)

    st.divider()

    # -----------------------------------------------------
    # CORPUS
    # -----------------------------------------------------

    st.subheader("🌐 Evaluation Corpus")

    corpus_dir = ROOT / "partA" / "corpus"

    if corpus_dir.exists():

        files = sorted(
            corpus_dir.glob("*.txt")
        )

        for file in files:

            with st.expander(
                f"📄 {file.name}"
            ):

                text = file.read_text(
                    encoding="utf-8"
                )

                st.text(text)

    else:

        st.error(
            "partA/corpus directory was not found."
        )

    st.divider()

    # -----------------------------------------------------
    # FERTILITY SCRIPT
    # -----------------------------------------------------

    fertility_file = ROOT / "partA" / "fertility.py"

    if fertility_file.exists():

        with st.expander(
            "View fertility.py"
        ):

            st.code(
                fertility_file.read_text(
                    encoding="utf-8"
                ),
                language="python"
            )


# =========================================================
# PART B — BENCHMARK RESULTS
# =========================================================

elif page == "⚡ Part B — Benchmark Results":

    st.header("⚡ Part B — Capacity Benchmark Results")

    model_file = ROOT / "partB" / "model_spec.md"
    bench_file = ROOT / "partB" / "bench_log.csv"

    # -----------------------------------------------------
    # MODEL
    # -----------------------------------------------------

    if model_file.exists():

        st.subheader("Model Specification")

        st.markdown(
            model_file.read_text(
                encoding="utf-8"
            )
        )

    st.divider()

    # -----------------------------------------------------
    # BENCHMARK CSV
    # -----------------------------------------------------

    if not bench_file.exists():

        st.error(
            "partB/bench_log.csv was not found."
        )

    else:

        df = pd.read_csv(bench_file)

        st.subheader("📈 Measured Benchmark Data")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"{len(df)} benchmark measurements loaded."
        )

        st.divider()

        # -------------------------------------------------
        # NUMERICAL SUMMARY
        # -------------------------------------------------

        st.subheader("🔢 Numerical Benchmark Summary")

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_columns:

            metric = st.selectbox(
                "Select measured metric",
                numeric_columns
            )

            minimum = df[metric].min()
            average = df[metric].mean()
            maximum = df[metric].max()

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Minimum",
                    f"{minimum:.2f}"
                )

            with c2:
                st.metric(
                    "Average",
                    f"{average:.2f}"
                )

            with c3:
                st.metric(
                    "Maximum",
                    f"{maximum:.2f}"
                )

            st.subheader(
                f"📊 {metric}"
            )

            st.line_chart(
                df[metric]
            )

        else:

            st.warning(
                "No numerical columns were detected."
            )



 # =========================================================
# PART C — DECISION DEMO
# =========================================================

elif page == "📝 Part C — Decision":

    st.header("📝 Part C — Engineering Decision")

    st.write(
        "Decision demo for making multilingual assistant responses "
        "more casual and conversational."
    )

    st.divider()

    st.subheader("🎯 Decision")

    st.success(
        "RECOMMENDATION: Choose Path (a) — SFT on synthetic "
        "casualized response pairs."
    )

    st.write(
        "Reason: the launch review is only 3 weeks away, the team has "
        "one A100-80GB for two weeks, and prompt-only changes are the "
        "least controllable way to change response style across six languages."
    )

    st.divider()

    st.subheader("🔢 Final Numbers")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Languages",
            "6"
        )

    with c2:
        st.metric(
            "Reviewer Hours",
            "30 h"
        )

    with c3:
        st.metric(
            "Reviewed Pairs",
            "360"
        )

    with c4:
        st.metric(
            "Success Threshold",
            "≥ 90%"
        )

    st.divider()

    st.subheader("📐 Back-of-the-Envelope Arithmetic")

    st.markdown(
        """
### Reviewer capacity

- Reviewer availability = **10 h/week**
- Evaluation period = **3 weeks**
- Total reviewer capacity = **10 × 3 = 30 hours**

Assumption:

- Review speed = **12 response pairs/hour**
- Therefore reviewed pairs = **30 × 12 = 360 pairs**

### Synthetic training data

Planning assumption:

- **6,000 synthetic casualized response pairs**
- **1,000 pairs/language × 6 languages = 6,000 pairs**

The synthetic set is generated first, then a smaller reviewer-reviewed
subset is used for quality control because the single reviewer only
supports Hindi + Kannada.

### GPU budget

- Available GPU = **1 × A100 80GB**
- Available training window = **14 days**
- GPU budget = **1 × 14 = 14 GPU-days**

The demo treats this as the maximum available training budget, not as
a measured training time.
"""
    )

    st.divider()

    st.subheader("📊 Success Criterion")

    st.metric(
        "Target casual-style preference",
        "≥ 90%"
    )

    st.write(
        "On a blinded human evaluation set, at least 90% of evaluated "
        "responses should be judged more casual/conversational than "
        "the current baseline."
    )

    st.divider()

    st.subheader("🛑 Kill Criterion")

    st.error(
        "Kill the SFT approach if the Day-10 evaluation remains below "
        "80% casual-style preference, or if quality regressions appear "
        "in factual correctness/safety during review."
    )

    st.divider()

    st.subheader("🧪 Day-1 Experiment")

    st.info(
        "Create a small pilot of 300 synthetic pairs: "
        "50 examples × 6 languages. Run the current model and the "
        "casualized target through the same evaluation prompts, then "
        "manually review the Hindi and Kannada subset before committing "
        "the full training budget."
    )

    st.divider()

    st.subheader("⚖️ Why not the other options?")

    comparison = pd.DataFrame({
        "Path": [
            "(a) SFT",
            "(b) ≤1B rewriter",
            "(c) Prompt engineering"
        ],
        "Assessment": [
            "Recommended",
            "Fallback",
            "Baseline / experiment"
        ],
        "Main reason": [
            "Directly changes response style",
            "Adds serving latency and another model",
            "Fast but less reliable for consistent style"
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------------------------------
    # FINAL RESULT BUTTON
    # -----------------------------------------------------

    if st.button(
        "🚀 SHOW FINAL DECISION",
        type="primary",
        use_container_width=True
    ):

        st.balloons()

        st.success(
            "FINAL RESULT: Proceed with Path (a) — SFT, "
            "subject to the Day-10 kill criterion."
        )

        st.subheader("🏆 Final Decision Summary")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "Training Data",
                "6,000 pairs"
            )

        with r2:
            st.metric(
                "Human Review Capacity",
                "360 pairs"
            )

        with r3:
            st.metric(
                "Required Success",
                "≥ 90%"
            )

        st.write(
            "The first production decision should be made only after "
            "the Day-1 pilot and subsequent quality evaluation. "
            "All numerical values above are planning assumptions for "
            "the decision memo, not measured benchmark results."
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Audit Assignment — Evidence-driven interactive demonstration"
)