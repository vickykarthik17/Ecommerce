import streamlit as st


DATASET_NAMES = {
    "orders": "Orders",
    "customers": "Customers",
    "order_items": "Order Items",
    "payments": "Payments",
    "reviews": "Reviews",
    "products": "Products",
    "sellers": "Sellers",
    "geolocation": "Geolocation",
    "category_translation": "Category Translations",
}


def show_metric_card(name, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{name.upper()}</div>
            <div class="metric-value">{value:,}</div>
            <div class="metric-subtitle">PostgreSQL records</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_dashboard_header():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Data operations / live workspace</div>
            <div class="hero-title">E-Commerce ETL Control Room</div>
            <p class="hero-copy">A clear view of the pipeline, its records, and the PostgreSQL load.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_dataset_overview(counts):
    st.subheader("Dataset Overview")

    items = list(counts.items())

    for start in range(0, len(items), 4):
        row = items[start:start + 4]
        columns = st.columns(4)

        for column, (table, count) in zip(columns, row):
            with column:
                show_metric_card(
                    DATASET_NAMES[table],
                    count
                )


def show_pipeline_result(result):

    if result["success"]:

        st.success(
            f"Pipeline completed successfully in "
            f"{result['runtime']:.2f} seconds."
        )

        st.subheader("Pipeline Stages")

        stages = [
            "Extraction",
            "Transformation",
            "Data Validation",
            "PostgreSQL Loading",
            "Database Validation"
        ]

        for stage in stages:
            st.markdown(
                f'<div class="stage-card">&#10003;&nbsp;&nbsp;{stage}</div>',
                unsafe_allow_html=True,
            )

        st.subheader("Execution Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Status",
                "SUCCESS"
            )

        with col2:
            st.metric(
                "Runtime",
                f"{result['runtime']:.2f} sec"
            )

        st.subheader("Pipeline Logs")

        with st.expander("View Pipeline Logs", expanded=True):
            st.code(
                result["output"],
                language="text"
            )

    else:

        st.error(
            f"Pipeline failed after "
            f"{result['runtime']:.2f} seconds."
        )

        st.subheader("Pipeline Status")

        st.metric(
            "Status",
            "FAILED"
        )

        st.subheader("Error Logs")

        with st.expander("View Pipeline Error", expanded=True):
            st.code(
                result["error"],
                language="text"
            )


def show_live_pipeline(snapshot, status_slot, metrics_slot, log_slot):
    output = snapshot["output"]
    current_stage = "Preparing pipeline"

    for line in reversed(output.splitlines()):
        if "Running:" in line:
            current_stage = line.split("Running:", 1)[1].strip()
            break

    with status_slot.container():
        st.markdown(
            '<div class="live-status"><span class="live-dot"></span> Pipeline running</div>',
            unsafe_allow_html=True,
        )
        st.write(f"Current stage: **{current_stage}**")

    with metrics_slot.container():
        metric_one, metric_two, metric_three = st.columns(3)
        metric_one.metric("Elapsed time", f"{snapshot['runtime']:.1f} sec")
        metric_two.metric("Execution status", "RUNNING")
        metric_three.metric("Output lines", len(output.splitlines()))

    with log_slot.container():
        with st.expander("Live pipeline log", expanded=True):
            st.code(output or "Waiting for pipeline output...", language="text")