import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm


st.set_page_config(
    page_title="Normal Distribution Calculator",
    page_icon="📊",
    layout="wide",
)


# ---------- helpers ----------
def validate_sigma(sigma: float) -> None:
    if sigma <= 0:
        raise ValueError("Standard deviation must be greater than 0.")


def validate_probability(p: float) -> None:
    if not (0 < p < 1):
        raise ValueError("Probability must be between 0 and 1.")


def calculate_probability(mu: float, sigma: float, option: str, input1: float, input2: float | None = None):
    dist = norm(loc=mu, scale=sigma)

    if option == "X ≤ q":
        p = dist.cdf(input1)
        return f"Probability = {p:.4f}", {"mode": "left", "q": input1}

    if option == "X > q":
        p = 1 - dist.cdf(input1)
        return f"Probability = {p:.4f}", {"mode": "right", "q": input1}

    if input2 is None:
        raise ValueError("Second input is required for this option.")

    q1, q2 = sorted([input1, input2])

    if option == "q1 < X ≤ q2":
        p = dist.cdf(q2) - dist.cdf(q1)
        return f"Probability = {p:.4f}", {"mode": "between", "q1": q1, "q2": q2}

    p = dist.cdf(q1) + (1 - dist.cdf(q2))
    return f"Probability = {p:.4f}", {"mode": "outside", "q1": q1, "q2": q2}


def calculate_values(mu: float, sigma: float, option: str, input1: float, input2: float | None = None):
    dist = norm(loc=mu, scale=sigma)

    if option == "X ≤ q":
        validate_probability(input1)
        q = dist.ppf(input1)
        return f"Value = {q:.4f}", {"mode": "left", "q": q}

    if option == "X > q":
        validate_probability(input1)
        q = dist.ppf(1 - input1)
        return f"Value = {q:.4f}", {"mode": "right", "q": q}

    if input2 is None:
        raise ValueError("Second input is required for this option.")

    validate_probability(input1)
    validate_probability(input2)

    if option == "q1 < X ≤ q2":
        q1 = dist.ppf(input1)
        q2 = dist.ppf(input2)
        q_low, q_high = sorted([q1, q2])
        area = dist.cdf(q_high) - dist.cdf(q_low)
        return (
            f"Values = ({q_low:.4f}, {q_high:.4f}) | Area = {area:.4f}",
            {"mode": "between", "q1": q_low, "q2": q_high},
        )

    q1 = dist.ppf(input1)
    q2 = dist.ppf(1 - input2)
    q_low, q_high = sorted([q1, q2])
    area = dist.cdf(q_low) + (1 - dist.cdf(q_high))
    return (
        f"Values = ({q_low:.4f}, {q_high:.4f}) | Area = {area:.4f}",
        {"mode": "outside", "q1": q_low, "q2": q_high},
    )


def plot_distribution(mu: float, sigma: float, shade_data: dict | None = None):
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    y = norm.pdf(x, mu, sigma)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, linewidth=2)

    if shade_data:
        mode = shade_data.get("mode")

        if mode in {"left", "right"}:
            q = shade_data["q"]
            if mode == "left":
                xs = x[x <= q]
            else:
                xs = x[x >= q]
            ys = norm.pdf(xs, mu, sigma)
            ax.fill_between(xs, ys, alpha=0.8)
            ax.axvline(q, linestyle="--", linewidth=1.2)

        elif mode in {"between", "outside"}:
            q1 = shade_data["q1"]
            q2 = shade_data["q2"]

            if mode == "between":
                xs = x[(x >= q1) & (x <= q2)]
                ys = norm.pdf(xs, mu, sigma)
                ax.fill_between(xs, ys, alpha=0.8)
            else:
                xs_left = x[x <= q1]
                ys_left = norm.pdf(xs_left, mu, sigma)
                xs_right = x[x >= q2]
                ys_right = norm.pdf(xs_right, mu, sigma)
                ax.fill_between(xs_left, ys_left, alpha=0.8)
                ax.fill_between(xs_right, ys_right, alpha=0.8)

            ax.axvline(q1, linestyle="--", linewidth=1.2)
            ax.axvline(q2, linestyle="--", linewidth=1.2)

    ax.set_title("Normal Distribution")
    ax.set_xlabel("X")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.25)
    return fig


# ---------- UI ----------
st.title("📊 Normal Distribution Calculator")
st.caption("Interactive probability and quantile calculator for the normal distribution")

with st.sidebar:
    st.subheader("Distribution Characteristics")
    distribution = st.selectbox("Distribution", ["Normal"], index=0)
    mu = st.number_input("Mean (μ)", value=0.0, step=0.1)
    sigma = st.number_input("Std. Dev. (σ)", value=1.0, step=0.1, min_value=0.0000001)

    st.subheader("Type of Calculation")
    calculation_type = st.radio(
        "Choose mode",
        [
            "Input values and calculate probability",
            "Input probability and calculate values",
        ],
        label_visibility="collapsed",
    )

st.markdown("---")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Calculations")

    option = st.radio(
        "Probability Options",
        ["X ≤ q", "X > q", "q1 < X ≤ q2", "X ≤ q1 OR X > q2"],
    )

    two_inputs = option in {"q1 < X ≤ q2", "X ≤ q1 OR X > q2"}
    prob_mode = calculation_type == "Input probability and calculate values"

    if prob_mode:
        input1_label = "Probability" if not two_inputs else "Probability 1"
        input2_label = "Probability 2"
        default1 = 0.8413
        default2 = 0.9772
    else:
        input1_label = "Value" if not two_inputs else "Value 1"
        input2_label = "Value 2"
        default1 = 1.0
        default2 = 2.0

    input1 = st.number_input(input1_label, value=float(default1), format="%.6f")
    input2 = None
    if two_inputs:
        input2 = st.number_input(input2_label, value=float(default2), format="%.6f")

    try:
        validate_sigma(sigma)
        if prob_mode:
            result_text, shade_data = calculate_values(mu, sigma, option, input1, input2)
        else:
            result_text, shade_data = calculate_probability(mu, sigma, option, input1, input2)

        st.success(result_text)
    except Exception as e:
        shade_data = None
        st.error(str(e))

with right_col:
    st.subheader("Visualization")
    fig = plot_distribution(mu, sigma, shade_data)
    st.pyplot(fig, use_container_width=True)

st.markdown("---")
st.markdown(
    """
    **How to run locally**

    ```bash
    streamlit run normal_distribution_calculator_streamlit.py
    ```
    """
)
