import streamlit as st


def apply_styles():

    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --ink: #18313b;
            --muted: #6d7d83;
            --paper: #fffaf5;
            --surface: #ffffff;
            --line: #f0e4d8;
            --coral: #f26b5e;
            --teal: #087f8c;
            --yellow: #f7c948;
        }

        .main {
            background: linear-gradient(135deg, #fffaf5 0%, #fffefc 58%, #effaf8 100%);
            color: var(--ink);
        }

        .stApp {
            background: var(--paper);
            font-family: 'DM Sans', sans-serif;
        }

        h1, h2, h3 {
            color: var(--ink) !important;
            font-family: 'Space Grotesk', sans-serif;
            letter-spacing: 0;
        }

        h1 {
            font-size: clamp(2rem, 4vw, 3.4rem) !important;
            line-height: 1.05 !important;
        }

        h2 {
            margin-top: 2rem !important;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 3.5rem;
            padding-bottom: 4rem;
        }

        .hero {
            background: linear-gradient(120deg, #fff0dc 0%, #fff8ef 62%, #dff5f1 100%);
            border: 1px solid #f5dfc9;
            border-radius: 20px;
            padding: 2rem 2.25rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 14px 32px rgba(28, 72, 80, 0.08);
        }

        .hero-kicker {
            color: var(--coral);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .hero-title {
            color: var(--ink);
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(2rem, 4vw, 3.4rem);
            font-weight: 700;
            line-height: 1.05;
            margin: 0.4rem 0;
        }

        .hero-copy {
            color: #52656b;
            font-size: 1rem;
            margin: 0;
        }

        .metric-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 14px;
            min-height: 130px;
            margin-bottom: 15px;
            padding: 20px;
            box-shadow: 0 8px 20px rgba(28, 72, 80, 0.06);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        .metric-card:hover {
            box-shadow: 0 12px 26px rgba(28, 72, 80, 0.11);
            transform: translateY(-2px);
        }

        .metric-title {
            color: var(--teal);
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--ink);
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            margin-top: 8px;
        }

        .metric-subtitle {
            color: var(--muted);
            font-size: 0.75rem;
            margin-top: 5px;
        }

        .status-pill {
            background: #e5f6ed;
            border: 1px solid #b8e8cc;
            border-radius: 999px;
            color: #147a45;
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.45rem 0.8rem;
        }

        .live-status {
            background: #fff4d6;
            border: 1px solid #f1d27a;
            border-radius: 12px;
            color: #805b00;
            font-weight: 700;
            padding: 0.8rem 1rem;
        }

        .live-dot {
            background: var(--coral);
            border-radius: 50%;
            display: inline-block;
            height: 0.65rem;
            margin-right: 0.45rem;
            width: 0.65rem;
        }

        .stage-card {
            background: var(--surface);
            border-left: 4px solid var(--teal);
            border-radius: 10px;
            box-shadow: 0 6px 16px rgba(28, 72, 80, 0.05);
            color: var(--ink);
            margin: 0.45rem 0;
            padding: 0.8rem 1rem;
        }

        .stButton > button {
            background: var(--coral);
            border: 0;
            border-radius: 10px;
            color: white;
            font-weight: 700;
            min-height: 2.75rem;
            padding: 0.65rem 1.25rem;
        }

        .stButton > button:hover {
            background: #d9574c;
            border: 0;
            color: white;
        }

        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 0.8rem 1rem;
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div {
            color: var(--ink) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricDelta"] {
            color: var(--muted) !important;
        }

        .live-status + div p,
        [data-testid="stMarkdownContainer"] p {
            color: var(--ink);
        }

        [data-testid="stAlert"] {
            border-radius: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )