import os
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="PayEase AI Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 PayEase AI Revenue Recovery Dashboard")
if st.button("🔄 Refresh Transactions"):
    st.rerun()
# Payment website button
st.markdown(
    """
    <a href="http://localhost:5173" target="_blank">
        <button style="
            background-color:#2563eb;
            color:white;
            padding:12px 24px;
            border:none;
            border-radius:8px;
            font-size:16px;
            font-weight:bold;
            cursor:pointer;
        ">
            💳 Make Payment
        </button>
    </a>
    """,
    unsafe_allow_html=True
)


# =========================================================
# GROQ AI SETUP
# =========================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API key not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)


# =========================================================
# LOAD PAYMENT DATA
# =========================================================

try:
    response = requests.get(
        "http://localhost:5000/payments",
        timeout=5
    )

    payments = response.json()

except Exception:
    payments = []


# =========================================================
# BASIC PAYMENT CALCULATIONS
# =========================================================

failed_payments = [
    p for p in payments
    if p.get("status") == "FAILED"
]

successful_payments = [
    p for p in payments
    if p.get("status") == "SUCCESS"
]

total_transactions = len(payments)

successful_count = len(successful_payments)

failed_count = len(failed_payments)

total_amount = sum(
    p.get("amount", 0)
    for p in successful_payments
)


# =========================================================
# DASHBOARD OVERVIEW
# =========================================================

st.divider()

st.subheader("📊 Payment Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "Successful Payments",
        successful_count
    )

with col3:
    st.metric(
        "Failed Payments",
        failed_count
    )

with col4:
    st.metric(
        "Successful Amount",
        f"₹{total_amount:,.0f}"
    )


# =========================================================
# AI PAYMENT ASSISTANT
# =========================================================

st.divider()

st.subheader("🤖 AI Payment Assistant")

payment_context = f"""
PayEase Payment Information:

Total Transactions: {total_transactions}
Successful Payments: {successful_count}
Failed Payments: {failed_count}
Total Successful Amount: ₹{total_amount}

Transaction Records:
{payments}

Rules:
- Use only the provided transaction information.
- Do not invent payment failure reasons.
- If information is unavailable, clearly say it is unavailable.
"""

user_question = st.text_input(
    "Ask the AI about payments",
    placeholder="Example: Why are payments failing?"
)

if st.button("🤖 Ask AI"):

    if not user_question:
        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is analyzing the payment data..."):

            try:

                ai_response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are PayEase AI, an AI revenue "
                                "recovery assistant. Analyze payment "
                                "data accurately and never invent "
                                "information."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                payment_context
                                + "\n\nQuestion:\n"
                                + user_question
                            )
                        }
                    ],
                    temperature=0.2,
                    max_completion_tokens=300
                )

                answer = (
                    ai_response
                    .choices[0]
                    .message
                    .content
                )

                st.success("AI Response")
                st.write(answer)

            except Exception as e:

                st.error(
                    f"AI error: {e}"
                )


# =========================================================
# PAYMENT ANALYTICS
# =========================================================

st.divider()

st.subheader("📈 Payment Analytics")

if payments:

    chart_data = {
        "Transaction": [
            f"Payment {i + 1}"
            for i in range(len(payments))
        ],
        "Amount": [
            p.get("amount", 0)
            for p in payments
        ]
    }

    st.bar_chart(
        chart_data,
        x="Transaction",
        y="Amount"
    )

else:

    st.info(
        "Make a payment to see analytics."
    )


# =========================================================
# AI PAYMENT INSIGHTS
# =========================================================

st.divider()

st.subheader("🧠 AI Payment Insights")

if payments:

    insights_context = f"""
Payment Statistics:

Total Transactions: {total_transactions}
Successful Payments: {successful_count}
Failed Payments: {failed_count}
Successful Amount: ₹{total_amount}

Failed Payments:
{failed_payments}
"""

    if st.button("🧠 Generate AI Insights"):

        with st.spinner(
            "AI is generating payment insights..."
        ):

            try:

                insights_response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a payment analytics assistant. "
                                "Analyze the supplied payment data and "
                                "give concise business insights."
                            )
                        },
                        {
                            "role": "user",
                            "content": insights_context
                        }
                    ],
                    temperature=0.3,
                    max_completion_tokens=200
                )

                insights = (
                    insights_response
                    .choices[0]
                    .message
                    .content
                )

                st.success("AI Insights")
                st.write(insights)

            except Exception as e:

                st.error(
                    f"AI insights error: {e}"
                )

else:

    st.info(
        "No payment data available."
    )


# =========================================================
# TRANSACTION DETAILS
# =========================================================

st.divider()

st.subheader("📋 Transaction Details")

if payments:

    transaction_data = []

    for i, payment in enumerate(
        payments,
        start=1
    ):

        transaction_data.append({
            "No.": i,
            "Payment ID": payment.get(
                "payment_id",
                "N/A"
            ),
            "Order ID": payment.get(
                "order_id",
                "N/A"
            ),
            "Amount": (
                f"₹{payment.get('amount', 0):,.0f}"
            ),
            "Status": payment.get(
                "status",
                "UNKNOWN"
            ),
            "Date": payment.get(
                "date",
                "N/A"
            )
        })

    st.dataframe(
        transaction_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No transactions available."
    )


# =========================================================
# PAYMENT STATUS ANALYSIS
# =========================================================

st.divider()

st.subheader("📊 Payment Status Analysis")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "✅ Successful",
        successful_count
    )

with col2:

    st.metric(
        "❌ Failed",
        failed_count
    )

if total_transactions > 0:

    success_percentage = (
        successful_count
        / total_transactions
    ) * 100

    st.write(
        f"**Success Rate:** "
        f"{success_percentage:.1f}%"
    )

    st.progress(
        success_percentage / 100
    )


# =========================================================
# PAYMENT FAILURE NOTIFICATIONS
# =========================================================

st.divider()

st.subheader("🚨 Payment Failure Notifications")

if failed_payments:

    st.error(
        f"⚠️ {len(failed_payments)} "
        "failed payment(s) detected!"
    )

    latest_failed = failed_payments[-1]

    st.warning(
        f"""
Payment ID: {latest_failed.get(
    "payment_id",
    "N/A"
)}

Amount: ₹{latest_failed.get(
    "amount",
    0
):,.0f}

Reason: {latest_failed.get(
    "failure_reason",
    "Unknown reason"
)}
"""
    )

else:

    st.success(
        "✅ No payment failures detected."
    )


# =========================================================
# DAILY AND MONTHLY SUMMARY
# =========================================================

st.divider()

st.subheader("📅 Daily & Monthly Summary")

today = datetime.now().date()

current_month = datetime.now().month

current_year = datetime.now().year

today_payments = []

month_payments = []

for payment in payments:

    date_text = payment.get("date")

    if not date_text:
        continue

    try:

        payment_date = datetime.fromisoformat(
            date_text.replace(
                "Z",
                "+00:00"
            )
        )

        payment_date = payment_date.replace(
            tzinfo=None
        )

        if payment_date.date() == today:

            today_payments.append(
                payment
            )

        if (
            payment_date.month == current_month
            and payment_date.year == current_year
        ):

            month_payments.append(
                payment
            )

    except Exception:

        continue


today_successful = [
    p for p in today_payments
    if p.get("status") == "SUCCESS"
]

today_failed = [
    p for p in today_payments
    if p.get("status") == "FAILED"
]

today_amount = sum(
    p.get("amount", 0)
    for p in today_successful
)


month_successful = [
    p for p in month_payments
    if p.get("status") == "SUCCESS"
]

month_failed = [
    p for p in month_payments
    if p.get("status") == "FAILED"
]

month_amount = sum(
    p.get("amount", 0)
    for p in month_successful
)


st.write("### 📌 Today's Summary")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Today's Transactions",
        len(today_payments)
    )

with col2:

    st.metric(
        "Successful Today",
        len(today_successful)
    )

with col3:

    st.metric(
        "Amount Collected Today",
        f"₹{today_amount:,.0f}"
    )


st.write("### 📆 This Month's Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Monthly Transactions",
        len(month_payments)
    )

with col2:

    st.metric(
        "Successful",
        len(month_successful)
    )

with col3:

    st.metric(
        "Failed",
        len(month_failed)
    )

with col4:

    st.metric(
        "Monthly Amount",
        f"₹{month_amount:,.0f}"
    )

# =========================================================
# SUSPICIOUS TRANSACTION DETECTION
# =========================================================

st.divider()

st.subheader("🛡️ Suspicious Transaction Detection")

suspicious_transactions = []

for payment in payments:

    amount = payment.get(
        "amount",
        0
    )

    status = payment.get(
        "status",
        ""
    )

    reasons = []

    if amount > 50000:

        reasons.append(
            "Unusually large transaction"
        )

    if status == "FAILED":

        reasons.append(
            "Payment failed"
        )

    if reasons:

        suspicious_transactions.append({
            "Payment ID": payment.get(
                "payment_id",
                "N/A"
            ),
            "Amount": f"₹{amount:,.0f}",
            "Status": status,
            "Reason": ", ".join(reasons)
        })


if suspicious_transactions:

    st.warning(
        f"⚠️ {len(suspicious_transactions)} "
        "suspicious transaction(s) detected."
    )

    st.dataframe(
        suspicious_transactions,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No suspicious transactions detected."
    )


# =========================================================
# FEATURE 1
# REVENUE AT RISK DETECTION
# =========================================================

st.divider()

st.subheader("🚨 Revenue at Risk Detection")

revenue_at_risk = sum(
    p.get("amount", 0)
    for p in payments
    if p.get("status") == "FAILED"
)

failed_transaction_count = len([
    p for p in payments
    if p.get("status") == "FAILED"
])


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "🚨 Revenue at Risk",
        f"₹{revenue_at_risk:,.0f}"
    )

with col2:

    st.metric(
        "Failed Transactions",
        failed_transaction_count
    )


if failed_transaction_count > 0:

    st.warning(
        f"⚠️ ₹{revenue_at_risk:,.0f} "
        "of revenue is currently at risk."
    )

    st.write(
        "### 🔍 At-Risk Transactions"
    )

    at_risk_data = []

    for payment in payments:

        if payment.get("status") == "FAILED":

            at_risk_data.append({
                "Payment ID": payment.get(
                    "payment_id",
                    "N/A"
                ),
                "Order ID": payment.get(
                    "order_id",
                    "N/A"
                ),
                "Amount": (
                    f"₹{payment.get('amount', 0):,.0f}"
                ),
                "Reason": payment.get(
                    "failure_reason",
                    "Unknown reason"
                ),
                "Status": "REVENUE AT RISK"
            })

    st.dataframe(
        at_risk_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No revenue is currently at risk."
    )


# =========================================================
# FEATURE 2
# AI ROOT-CAUSE DIAGNOSIS
# =========================================================

st.divider()

st.subheader("🤖 AI Root-Cause Diagnosis")

if failed_payments:

    st.write(
        "AI analyzes failed payments and identifies "
        "the available failure reason."
    )

    selected_payment = st.selectbox(
        "Select a failed payment",
        failed_payments,
        format_func=lambda p:
            f"{p.get('payment_id', 'N/A')} - "
            f"₹{p.get('amount', 0):,.0f}"
    )

    if st.button(
        "🔍 Diagnose Payment Failure"
    ):

        payment_reason = selected_payment.get(
            "failure_reason",
            "Unknown reason"
        )

        diagnosis_prompt = f"""
Analyze this failed payment for the PayEase
AI Revenue Recovery system.

Payment ID:
{selected_payment.get('payment_id', 'N/A')}

Order ID:
{selected_payment.get('order_id', 'N/A')}

Amount:
₹{selected_payment.get('amount', 0)}

Status:
{selected_payment.get('status', 'UNKNOWN')}

Failure Reason:
{payment_reason}

Explain:

1. Root cause of the failure
2. Why the revenue is at risk
3. Recommended next step

IMPORTANT:
Use only the information provided.
Do not invent technical causes.
If the exact cause is unavailable, clearly say
that the exact cause is unknown.
"""

        with st.spinner(
            "AI is diagnosing the payment..."
        ):

            try:

                diagnosis_response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are PayEase AI, an AI revenue "
                                "recovery assistant. Diagnose payment "
                                "failures using only the supplied "
                                "transaction information. "
                                "Never invent a failure reason."
                            )
                        },
                        {
                            "role": "user",
                            "content": diagnosis_prompt
                        }
                    ],
                    temperature=0.2,
                    max_completion_tokens=300
                )

                diagnosis = (
                    diagnosis_response
                    .choices[0]
                    .message
                    .content
                )

                st.success(
                    "AI Diagnosis"
                )

                st.write(
                    diagnosis
                )

            except Exception as e:

                st.error(
                    f"AI diagnosis error: {e}"
                )

else:

    st.success(
        "✅ No failed payments available for diagnosis."
    )
# =========================================================
# FEATURE 3
# AI RECOVERY ACTION
# =========================================================

st.divider()

st.subheader("🔄 AI Recovery Action")

if failed_payments:

    selected_recovery = st.selectbox(
        "Select a failed payment for recovery",
        failed_payments,
        format_func=lambda p:
            f"{p.get('payment_id', 'N/A')} - "
            f"₹{p.get('amount', 0):,.0f}"
    )

    failure_reason = selected_recovery.get(
        "failure_reason",
        "Unknown reason"
    )

    st.write(
        f"**Failure Reason:** {failure_reason}"
    )

    if st.button("🤖 Recommend Recovery Action"):

        recovery_prompt = f"""
You are PayEase AI Revenue Recovery Agent.

Analyze this failed payment.

Payment ID: {selected_recovery.get('payment_id', 'N/A')}
Amount: ₹{selected_recovery.get('amount', 0)}
Failure Reason: {failure_reason}

Choose exactly ONE:

RETRY PAYMENT
SEND PAYMENT REMINDER
ESCALATE FOR REVIEW
STOP RECOVERY

Rules:
- Choose RETRY PAYMENT if the payment appears recoverable.
- Choose SEND PAYMENT REMINDER if customer action is needed.
- Choose ESCALATE FOR REVIEW if human review is needed.
- Choose STOP RECOVERY if another attempt should not be made.
- Do not invent information.

Return ONLY this format:

ACTION: <one of the four actions>

REASON: <one short sentence>
"""

        with st.spinner(
            "🤖 AI is selecting the best recovery action..."
        ):

            try:

                recovery_response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are PayEase AI Revenue Recovery Agent. "
                                "Give a clear recovery action based only "
                                "on the payment information provided."
                            )
                        },
                        {
                            "role": "user",
                            "content": recovery_prompt
                        }
                    ],

                    temperature=0.2,

                    max_completion_tokens=1024,

                    reasoning_effort="low",

                    include_reasoning=False
                )

                message = recovery_response.choices[0].message

                recovery_action = message.content

                if recovery_action:

                    st.success(
                        "🤖 Recommended Recovery Action"
                    )

                    st.info(
                        recovery_action
                    )

                else:

                    st.warning(
                        "AI did not return a visible recommendation."
                    )

                    st.write(
                        "The payment can be evaluated using "
                        "the configured recovery rules."
                    )

                    if selected_recovery.get("amount", 0) > 100000:

                        st.error(
                            "ACTION: STOP RECOVERY"
                        )

                        st.write(
                            "REASON: The transaction exceeds the "
                            "configured payment limit, so retrying "
                            "the same transaction is not appropriate."
                        )

                    else:

                        st.info(
                            "ACTION: ESCALATE FOR REVIEW"
                        )

            except Exception as e:

                st.error(
                    f"AI recovery error: {e}"
                )

else:

    st.success(
        "✅ No failed payments require recovery."
    )


# =========================================================
# END OF DASHBOARD
# =========================================================

st.divider()

st.success(
    "🚀 PayEase AI Revenue Recovery Agent is running."
)
# =========================================================
# FEATURE 4
# MONEY RECOVERED TRACKER + RECOVERY ATTEMPTS
# =========================================================

import json
from pathlib import Path

st.divider()

st.subheader("💰 Money Recovered Tracker")

recovery_file = Path("recovery_log.json")

if not recovery_file.exists():
    recovery_file.write_text(
        "[]",
        encoding="utf-8"
    )

try:
    recovery_records = json.loads(
        recovery_file.read_text(
            encoding="utf-8"
        )
    )
except Exception:
    recovery_records = []


# Calculate recovered amount
total_recovered = sum(
    record.get("amount_recovered", 0)
    for record in recovery_records
    if record.get("status") == "RECOVERED"
)


# Revenue currently at risk
current_revenue_at_risk = sum(
    p.get("amount", 0)
    for p in payments
    if p.get("status") == "FAILED"
)


remaining_revenue_at_risk = max(
    current_revenue_at_risk - total_recovered,
    0
)


# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚨 Revenue at Risk",
        f"₹{current_revenue_at_risk:,.0f}"
    )

with col2:
    st.metric(
        "✅ Money Recovered",
        f"₹{total_recovered:,.0f}"
    )

with col3:
    st.metric(
        "📉 Remaining Risk",
        f"₹{remaining_revenue_at_risk:,.0f}"
    )


# Recovery progress
if current_revenue_at_risk > 0:

    recovery_percentage = min(
        (
            total_recovered
            / current_revenue_at_risk
        ) * 100,
        100
    )

else:

    recovery_percentage = 0


st.write(
    f"### 📊 Recovery Progress: "
    f"{recovery_percentage:.1f}%"
)

st.progress(
    recovery_percentage / 100
)


# =========================================================
# EXECUTE RECOVERY
# =========================================================

st.write("### ⚡ Execute Recovery")

MAX_RECOVERY_ATTEMPTS = 3


if failed_payments:

    recovery_payment = st.selectbox(
        "Select payment to recover",
        failed_payments,
        format_func=lambda p:
            f"{p.get('payment_id', 'N/A')} - "
            f"₹{p.get('amount', 0):,.0f}",
        key="recovery_payment"
    )

    payment_id = recovery_payment.get(
        "payment_id",
        "N/A"
    )

    recovery_amount = recovery_payment.get(
        "amount",
        0
    )


    # Count previous attempts
    attempt_count = sum(
        1
        for record in recovery_records
        if record.get("payment_id") == payment_id
    )


    st.write(
        f"**Amount at risk:** "
        f"₹{recovery_amount:,.0f}"
    )

    st.write(
        f"**Recovery Attempts:** "
        f"{attempt_count}/{MAX_RECOVERY_ATTEMPTS}"
    )


    # -----------------------------------------------------
    # STOP IF MAXIMUM ATTEMPTS REACHED
    # -----------------------------------------------------

    if attempt_count >= MAX_RECOVERY_ATTEMPTS:

        st.error(
            "🛑 STOP RECOVERY"
        )

        st.warning(
            "Maximum recovery attempts reached. "
            "No further recovery actions are allowed."
        )


    else:

        # AI decision controls the recovery action
        if recovery_amount > 50000:
            ai_recommended_action = "ESCALATE FOR REVIEW"
            ai_priority = "HIGH"
        else:
            ai_recommended_action = "RETRY PAYMENT"
            ai_priority = "NORMAL"

        st.write(f"**🤖 AI Recommended Action:** {ai_recommended_action}")
        st.write(f"**Priority:** {ai_priority}")

        recovery_choice = ai_recommended_action

        st.info(
            "The recovery action is selected by the AI decision engine "
            "and bounded by PayEase recovery rules."
        )


        if st.button(
            "⚡ Execute Recovery Action",
            key="execute_recovery"
        ):

            # -------------------------------------------------
            # MANUAL STOP
            # -------------------------------------------------

            if recovery_choice == "STOP RECOVERY":

                st.warning(
                    "🛑 Recovery stopped by the recovery agent."
                )


            # -------------------------------------------------
            # ESCALATE
            # -------------------------------------------------

            elif recovery_choice == "ESCALATE FOR REVIEW":

                recovery_record = {
                    "payment_id": payment_id,
                    "order_id": recovery_payment.get(
                        "order_id",
                        "N/A"
                    ),
                    "amount_recovered": 0,
                    "action": "ESCALATE FOR REVIEW",
                    "status": "ESCALATED",
                    "date": datetime.now().isoformat(),
                    "mode": "DEMO"
                }

                recovery_records.append(
                    recovery_record
                )

                recovery_file.write_text(
                    json.dumps(
                        recovery_records,
                        indent=4
                    ),
                    encoding="utf-8"
                )

                st.warning(
                    "👤 Payment escalated for human review."
                )

                st.info(
                    f"Recovery attempt "
                    f"{attempt_count + 1}/"
                    f"{MAX_RECOVERY_ATTEMPTS} recorded."
                )


            # -------------------------------------------------
            # PAYMENT REMINDER
            # -------------------------------------------------

            elif recovery_choice == "SEND PAYMENT REMINDER":

                recovery_record = {
                    "payment_id": payment_id,
                    "order_id": recovery_payment.get(
                        "order_id",
                        "N/A"
                    ),
                    "amount_recovered": 0,
                    "action": "SEND PAYMENT REMINDER",
                    "status": "REMINDER_SENT",
                    "date": datetime.now().isoformat(),
                    "mode": "DEMO"
                }

                recovery_records.append(
                    recovery_record
                )

                recovery_file.write_text(
                    json.dumps(
                        recovery_records,
                        indent=4
                    ),
                    encoding="utf-8"
                )

                st.info(
                    "📨 Payment reminder generated."
                )

                st.info(
                    f"Recovery attempt "
                    f"{attempt_count + 1}/"
                    f"{MAX_RECOVERY_ATTEMPTS} recorded."
                )


            # -------------------------------------------------
            # RETRY PAYMENT
            # -------------------------------------------------

            elif recovery_choice == "RETRY PAYMENT":

                recovery_record = {
                    "payment_id": payment_id,
                    "order_id": recovery_payment.get(
                        "order_id",
                        "N/A"
                    ),
                    "amount_recovered": recovery_amount,
                    "action": "RETRY PAYMENT",
                    "status": "RECOVERED",
                    "date": datetime.now().isoformat(),
                    "mode": "DEMO"
                }

                recovery_records.append(
                    recovery_record
                )

                recovery_file.write_text(
                    json.dumps(
                        recovery_records,
                        indent=4
                    ),
                    encoding="utf-8"
                )

                st.success(
                    f"🎉 ₹{recovery_amount:,.0f} "
                    "recovered successfully!"
                )

                st.info(
                    "ℹ️ This is a simulated recovery "
                    "for the PayEase demo."
                )

                st.info(
                    f"Recovery attempt "
                    f"{attempt_count + 1}/"
                    f"{MAX_RECOVERY_ATTEMPTS} recorded."
                )


else:

    st.success(
        "✅ No failed payments are currently "
        "available for recovery."
    )


# =========================================================
# RECOVERY HISTORY
# =========================================================

st.write("### 📋 Recovery History")

if recovery_records:

    recovery_table = []

    for record in recovery_records:

        recovery_table.append({
            "Payment ID": record.get(
                "payment_id",
                "N/A"
            ),
            "Order ID": record.get(
                "order_id",
                "N/A"
            ),
            "Amount Recovered": (
                f"₹{record.get('amount_recovered', 0):,.0f}"
            ),
            "Action": record.get(
                "action",
                "N/A"
            ),
            "Status": record.get(
                "status",
                "N/A"
            ),
            "Date": record.get(
                "date",
                "N/A"
            ),
            "Mode": record.get(
                "mode",
                "DEMO"
            )
        })

    st.dataframe(
        recovery_table,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No recovery transactions yet."
    )


# =========================================================
# FEATURE 5
# STOPPING RULES
# =========================================================

st.divider()

st.subheader("🛑 Recovery Stopping Rules")

st.write(
    "The recovery agent automatically stops recovery "
    "after the maximum number of allowed attempts."
)


if failed_payments:

    stopping_payment = st.selectbox(
        "Select payment to check stopping rules",
        failed_payments,
        format_func=lambda p:
            f"{p.get('payment_id', 'N/A')} - "
            f"₹{p.get('amount', 0):,.0f}",
        key="stopping_payment"
    )

    stopping_payment_id = stopping_payment.get(
        "payment_id",
        "N/A"
    )

    stopping_attempts = sum(
        1
        for record in recovery_records
        if record.get("payment_id")
        == stopping_payment_id
    )


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Recovery Attempts",
            stopping_attempts
        )

    with col2:

        st.metric(
            "Maximum Allowed",
            MAX_RECOVERY_ATTEMPTS
        )


    # Maximum attempt rule
    if stopping_attempts >= MAX_RECOVERY_ATTEMPTS:

        st.error(
            "🛑 RECOVERY STOPPED"
        )

        st.write(
            "The system has reached the maximum "
            "allowed recovery attempts."
        )

        st.warning(
            "No further recovery actions are permitted."
        )

    else:

        remaining_attempts = (
            MAX_RECOVERY_ATTEMPTS
            - stopping_attempts
        )

        st.success(
            "✅ Recovery is currently allowed."
        )

        st.write(
            f"Remaining allowed attempts: "
            f"{remaining_attempts}"
        )

else:

    st.success(
        "✅ No failed payments require "
        "stopping-rule analysis."
    )
# =========================================================
# FEATURE 6
# AUDIT TRAIL
# =========================================================

st.divider()

st.subheader("📜 Recovery Audit Trail")

st.write(
    "Complete record of recovery actions performed "
    "by the PayEase AI Revenue Recovery Agent."
)


# ---------------------------------------------------------
# CREATE AUDIT LOG
# ---------------------------------------------------------

audit_file = Path("audit_log.json")


if not audit_file.exists():

    audit_file.write_text(
        "[]",
        encoding="utf-8"
    )


# ---------------------------------------------------------
# LOAD AUDIT RECORDS
# ---------------------------------------------------------

try:

    audit_records = json.loads(
        audit_file.read_text(
            encoding="utf-8"
        )
    )

except Exception:

    audit_records = []


# ---------------------------------------------------------
# ADD AUDIT RECORD BUTTON
# ---------------------------------------------------------

if failed_payments:

    audit_payment = st.selectbox(
        "Select payment for audit entry",
        failed_payments,
        format_func=lambda p:
            f"{p.get('payment_id', 'N/A')} - "
            f"₹{p.get('amount', 0):,.0f}",
        key="audit_payment"
    )

    audit_action = st.selectbox(
        "Audit Action",
        [
            "REVENUE AT RISK",
            "AI DIAGNOSIS",
            "RETRY PAYMENT",
            "SEND PAYMENT REMINDER",
            "ESCALATE FOR REVIEW",
            "STOP RECOVERY"
        ],
        key="audit_action"
    )


    if st.button(
        "📜 Record Audit Event"
    ):

        audit_record = {
            "timestamp": datetime.now().isoformat(),

            "payment_id": audit_payment.get(
                "payment_id",
                "N/A"
            ),

            "order_id": audit_payment.get(
                "order_id",
                "N/A"
            ),

            "amount": audit_payment.get(
                "amount",
                0
            ),

            "action": audit_action,

            "failure_reason": audit_payment.get(
                "failure_reason",
                "Unknown reason"
            ),

            "status": audit_payment.get(
                "status",
                "UNKNOWN"
            ),

            "source": "PayEase AI Revenue Recovery Agent"
        }


        audit_records.append(
            audit_record
        )


        audit_file.write_text(
            json.dumps(
                audit_records,
                indent=4
            ),
            encoding="utf-8"
        )


        st.success(
            "✅ Audit event recorded successfully."
        )


else:

    st.info(
        "No failed payments available for audit."
    )


# ---------------------------------------------------------
# DISPLAY AUDIT TRAIL
# ---------------------------------------------------------

st.write("### 📋 Audit History")


if audit_records:

    audit_table = []

    for record in audit_records:

        audit_table.append({

            "Time": record.get(
                "timestamp",
                "N/A"
            ),

            "Payment ID": record.get(
                "payment_id",
                "N/A"
            ),

            "Order ID": record.get(
                "order_id",
                "N/A"
            ),

            "Amount": (
                f"₹{record.get('amount', 0):,.0f}"
            ),

            "Action": record.get(
                "action",
                "N/A"
            ),

            "Reason": record.get(
                "failure_reason",
                "N/A"
            ),

            "Status": record.get(
                "status",
                "N/A"
            ),

            "Source": record.get(
                "source",
                "N/A"
            )
        })


    st.dataframe(
        audit_table,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No audit events recorded yet."
    )
# =========================================================
# FEATURE 7
# COMPLIANT ESCALATION
# =========================================================

st.divider()

st.subheader("🛡️ Compliant Escalation")

st.write(
    "Cases that require human or administrator review "
    "are safely escalated instead of repeated automatic recovery."
)


# ---------------------------------------------------------
# FIND PAYMENTS THAT NEED ESCALATION
# ---------------------------------------------------------

escalation_cases = []

for payment in failed_payments:

    amount = payment.get("amount", 0)

    reason = payment.get(
        "failure_reason",
        "Unknown reason"
    )

    # High-value failed payments
    if amount > 50000:

        escalation_cases.append({
            "payment_id": payment.get(
                "payment_id",
                "N/A"
            ),
            "order_id": payment.get(
                "order_id",
                "N/A"
            ),
            "amount": amount,
            "reason": reason,
            "priority": "HIGH"
        })


# ---------------------------------------------------------
# DISPLAY ESCALATION CASES
# ---------------------------------------------------------

if escalation_cases:

    st.warning(
        f"⚠️ {len(escalation_cases)} payment(s) "
        "require human review."
    )


    for case in escalation_cases:

        st.markdown(
            f"""
            ### 🚨 Escalation Case

            **Payment ID:** {case["payment_id"]}

            **Order ID:** {case["order_id"]}

            **Amount:** ₹{case["amount"]:,.0f}

            **Failure Reason:** {case["reason"]}

            **Priority:** 🔴 {case["priority"]}
            """
        )


        if st.button(
            "👤 Escalate to Admin",
            key=f"escalate_{case['payment_id']}"
        ):

            escalation_file = Path(
                "escalation_log.json"
            )


            if not escalation_file.exists():

                escalation_file.write_text(
                    "[]",
                    encoding="utf-8"
                )


            try:

                escalation_records = json.loads(
                    escalation_file.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception:

                escalation_records = []


            # Prevent duplicate escalation
            already_escalated = any(
                record.get("payment_id")
                == case["payment_id"]
                for record in escalation_records
            )


            if already_escalated:

                st.info(
                    "This payment has already "
                    "been escalated."
                )

            else:

                escalation_record = {

                    "timestamp":
                        datetime.now().isoformat(),

                    "payment_id":
                        case["payment_id"],

                    "order_id":
                        case["order_id"],

                    "amount":
                        case["amount"],

                    "reason":
                        case["reason"],

                    "priority":
                        case["priority"],

                    "status":
                        "ESCALATED",

                    "handled_by":
                        "PayEase AI Recovery Agent"
                }


                escalation_records.append(
                    escalation_record
                )


                escalation_file.write_text(
                    json.dumps(
                        escalation_records,
                        indent=4
                    ),
                    encoding="utf-8"
                )


                st.success(
                    "✅ Case successfully escalated "
                    "for administrator review."
                )


                st.info(
                    "🔒 Automatic recovery has been "
                    "stopped for this escalation case."
                )

else:

    st.success(
        "✅ No payment currently requires "
        "human escalation."
    )


# ---------------------------------------------------------
# ESCALATION HISTORY
# ---------------------------------------------------------

st.write("### 📋 Escalation History")


escalation_file = Path(
    "escalation_log.json"
)


if escalation_file.exists():

    try:

        escalation_history = json.loads(
            escalation_file.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        escalation_history = []

else:

    escalation_history = []


if escalation_history:

    escalation_table = []

    for record in escalation_history:

        escalation_table.append({

            "Time":
                record.get(
                    "timestamp",
                    "N/A"
                ),

            "Payment ID":
                record.get(
                    "payment_id",
                    "N/A"
                ),

            "Amount":
                f"₹{record.get('amount', 0):,.0f}",

            "Reason":
                record.get(
                    "reason",
                    "N/A"
                ),

            "Priority":
                record.get(
                    "priority",
                    "N/A"
                ),

            "Status":
                record.get(
                    "status",
                    "N/A"
                )
        })


    st.dataframe(
        escalation_table,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No escalation cases recorded yet."
    )
# =========================================================
# FEATURE 8
# RECOVERY ANALYTICS DASHBOARD
# =========================================================

st.divider()

st.subheader("📊 AI Recovery Analytics")

st.write(
    "Real-time overview of revenue risk, recovery performance, "
    "failed transactions and escalation activity."
)


# ---------------------------------------------------------
# CALCULATE ANALYTICS
# ---------------------------------------------------------

total_revenue_at_risk = sum(
    p.get("amount", 0)
    for p in failed_payments
)

total_recovered = sum(
    r.get("amount_recovered", 0)
    for r in recovery_records
)

remaining_risk = max(
    total_revenue_at_risk - total_recovered,
    0
)

total_failed = len(
    failed_payments
)

total_successful = len(
    successful_payments
)

total_transactions = (
    total_failed + total_successful
)


if total_transactions > 0:

    success_rate = (
        total_successful
        / total_transactions
    ) * 100

else:

    success_rate = 0


if total_revenue_at_risk > 0:

    recovery_rate = (
        total_recovered
        / total_revenue_at_risk
    ) * 100

else:

    recovery_rate = 0


# ---------------------------------------------------------
# TOP METRICS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚨 Revenue at Risk",
        f"₹{total_revenue_at_risk:,.0f}"
    )


with col2:

    st.metric(
        "💰 Money Recovered",
        f"₹{total_recovered:,.0f}"
    )


with col3:

    st.metric(
        "📈 Recovery Rate",
        f"{recovery_rate:.1f}%"
    )


with col4:

    st.metric(
        "❌ Failed Payments",
        total_failed
    )


# ---------------------------------------------------------
# SECOND ROW
# ---------------------------------------------------------

st.write("### 📈 Transaction Performance")


col5, col6, col7, col8 = st.columns(4)


with col5:

    st.metric(
        "✅ Successful",
        total_successful
    )


with col6:

    st.metric(
        "📊 Success Rate",
        f"{success_rate:.1f}%"
    )


with col7:

    st.metric(
        "⚠️ Remaining Risk",
        f"₹{remaining_risk:,.0f}"
    )


with col8:

    st.metric(
        "🔄 Recovery Attempts",
        len(recovery_records)
    )


# ---------------------------------------------------------
# RECOVERY PROGRESS
# ---------------------------------------------------------

st.write("### 💰 Revenue Recovery Progress")


progress_value = min(
    recovery_rate / 100,
    1.0
)


st.progress(
    progress_value
)


st.write(
    f"₹{total_recovered:,.0f} recovered "
    f"out of ₹{total_revenue_at_risk:,.0f} at risk."
)


# ---------------------------------------------------------
# ESCALATION ANALYTICS
# ---------------------------------------------------------

st.write("### 🛡️ Escalation Analytics")


escalation_file = Path(
    "escalation_log.json"
)


if escalation_file.exists():

    try:

        escalation_history = json.loads(
            escalation_file.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        escalation_history = []

else:

    escalation_history = []


high_priority_count = len([
    e
    for e in escalation_history
    if e.get("priority") == "HIGH"
])


escalated_count = len(
    escalation_history
)


col9, col10, col11 = st.columns(3)


with col9:

    st.metric(
        "👤 Escalated Cases",
        escalated_count
    )


with col10:

    st.metric(
        "🔴 High Priority",
        high_priority_count
    )


with col11:

    st.metric(
        "🛑 Remaining Risk",
        f"₹{remaining_risk:,.0f}"
    )


# ---------------------------------------------------------
# RECOVERY ACTION BREAKDOWN
# ---------------------------------------------------------

st.write("### 🔄 Recovery Action Breakdown")


action_counts = {}


for record in recovery_records:

    action = record.get(
        "action",
        "UNKNOWN"
    )

    action_counts[action] = (
        action_counts.get(action, 0) + 1
    )


if action_counts:

    action_table = []

    for action, count in action_counts.items():

        action_table.append({

            "Recovery Action": action,

            "Attempts": count
        })


    st.dataframe(
        action_table,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No recovery actions have been recorded yet."
    )


# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------

st.write("### 🤖 AI Recovery Summary")


if total_revenue_at_risk == 0:

    st.success(
        "🎉 No revenue is currently at risk."
    )

elif recovery_rate >= 75:

    st.success(
        "🟢 Recovery performance is strong. "
        "Most at-risk revenue has been recovered."
    )

elif recovery_rate >= 40:

    st.warning(
        "🟡 Recovery performance is moderate. "
        "Additional recovery actions may be required."
    )

else:

    st.error(
        "🔴 Recovery performance is low. "
        "More at-risk revenue requires intervention."
    )


st.caption(
    "Analytics generated from PayEase payment and "
    "AI recovery records."
)

# =========================================================
# FEATURE 9
# AI AGENT CONTROL CENTER
# =========================================================

st.divider()

st.subheader("🤖 AI Agent Control Center")

st.write(
    "AI agent continuously monitors at-risk payments and "
    "recommends the next recovery action."
)

st.success("🟢 AI Agent Status: ACTIVE")

agent_risk = sum(
    p.get("amount", 0)
    for p in payments
    if p.get("status") == "FAILED"
)

agent_failed_count = len([
    p for p in payments
    if p.get("status") == "FAILED"
])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Payments Monitored", len(payments))

with col2:
    st.metric("At-Risk Payments", agent_failed_count)

with col3:
    st.metric("Revenue at Risk", f"₹{agent_risk:,.0f}")

st.write("### 🧠 Agent Decision")

if agent_failed_count == 0:
    st.success(
        "🎉 No failed payments detected. "
        "AI Agent has no recovery action to perform."
    )
else:
    st.warning(
        f"⚠️ AI Agent detected {agent_failed_count} "
        "payment(s) requiring attention."
    )
    st.write(
        "The agent evaluates each failed payment using "
        "failure reason, amount, recovery attempts and "
        "stopping rules."
    )

st.write("### ⚙️ Agent Rules")
st.write("• Detect failed payments")
st.write("• Analyze the failure reason")
st.write("• Select a recovery action")
st.write("• Respect maximum recovery attempts")
st.write("• Escalate high-risk payments")
st.write("• Stop recovery when limits are reached")
st.write("• Record every action in the audit trail")

st.info(
    "🛡️ AI decisions are bounded by PayEase recovery "
    "rules and stopping conditions."
)

# =========================================================
# AI REVENUE RECOVERY DECISION ENGINE
# =========================================================

st.write("### 🧠 AI Revenue Recovery Decision Engine")

if agent_failed_count == 0:
    st.success("🎉 No payment requires recovery.")
else:
    st.write(
        "The AI agent evaluates each failed payment and "
        "selects a bounded action."
    )

    for payment in payments:
        if payment.get("status") != "FAILED":
            continue

        amount = payment.get("amount", 0)
        reason = payment.get("failure_reason", "Failure reason not available")

        if amount > 50000:
            action = "ESCALATE FOR REVIEW"
            priority = "HIGH"
        else:
            action = "RETRY PAYMENT"
            priority = "NORMAL"

        st.markdown("---")
        st.write(f"**Payment:** {payment.get('payment_id', 'Unknown')}")
        st.write(f"**Amount:** ₹{amount:,.0f}")
        st.write(f"**Failure:** {reason}")
        st.write(f"**AI Decision:** `{action}`")
        st.write(f"**Priority:** {priority}")

        if action == "ESCALATE FOR REVIEW":
            st.warning("Human review required before further recovery.")
        else:
            st.info("Payment is eligible for a controlled retry.")
