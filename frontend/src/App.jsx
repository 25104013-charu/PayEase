import { useState } from "react";
import { jsPDF } from "jspdf";
import "./App.css";
import Home from "./Home";

function App() {
    const [amount, setAmount] = useState(500);
    const [loading, setLoading] = useState(false);
    const [payment, setPayment] = useState(null);
    const [showHome, setShowHome] = useState(true);

    const [history, setHistory] = useState(
        JSON.parse(localStorage.getItem("paymentHistory")) || []
    );

    const [error, setError] = useState("");

    // ----------------------------
    // DOWNLOAD PAYMENT RECEIPT
    // ----------------------------
    const downloadReceipt = () => {
        if (!payment || payment === "history") return;

        const doc = new jsPDF();

        doc.setFontSize(24);
        doc.text("PayEase", 85, 25);

        doc.setFontSize(16);
        doc.text("PAYMENT RECEIPT", 70, 42);

        doc.setFontSize(12);

        doc.text(
            `Amount: Rs. ${payment.amount}`,
            30,
            70
        );

        doc.text(
            `Payment ID: ${payment.paymentId}`,
            30,
            85
        );

        doc.text(
            `Order ID: ${payment.orderId}`,
            30,
            100
        );

        doc.text(
            "Status: SUCCESS",
            30,
            115
        );

        doc.text(
            `Date: ${payment.date}`,
            30,
            130
        );

        doc.text(
            "Thank you for your payment!",
            30,
            155
        );

        doc.save("PayEase-Receipt.pdf");
    };

    // ----------------------------
    // MAKE RAZORPAY PAYMENT
    // ----------------------------
    const payNow = async () => {
        if (!amount || Number(amount) <= 0) {
            setError("Please enter a valid amount.");
            return;
        }

        setLoading(true);
        setError("");

        try {
            // 1. Create Razorpay order
            const orderResponse = await fetch(
                "http://localhost:5000/create-order",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        amount: Number(amount)
                    })
                }
            );

            const orderData =
                await orderResponse.json();

            if (!orderData.success) {
                setError(
                    orderData.message ||
                    "Unable to create Razorpay order."
                );

                setLoading(false);
                return;
            }

            // 2. Razorpay Checkout options
            const options = {
                key: orderData.key_id,

                amount:
                    orderData.order.amount,

                currency:
                    orderData.order.currency,

                name: "PayEase",

                description:
                    "College Registration Payment",

                order_id:
                    orderData.order.id,

                handler: async function (response) {
                    try {
                        // 3. Verify payment
                        const verifyResponse =
                            await fetch(
                                "http://localhost:5000/verify-payment",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({
                                        razorpay_order_id:
                                            response.razorpay_order_id,

                                        razorpay_payment_id:
                                            response.razorpay_payment_id,

                                        razorpay_signature:
                                            response.razorpay_signature,

                                        amount:
                                            Number(amount)
                                    })
                                }
                            );

                        const verifyData =
                            await verifyResponse.json();

                        if (verifyData.success) {

                            const newPayment = {
                                paymentId:
                                    response.razorpay_payment_id,

                                orderId:
                                    response.razorpay_order_id,

                                amount:
                                    Number(amount),

                                date:
                                    new Date().toLocaleString(),

                                status: "SUCCESS"
                            };

                            // Update local history
                            const updatedHistory = [
                                newPayment,
                                ...history
                            ];

                            setHistory(
                                updatedHistory
                            );

                            localStorage.setItem(
                                "paymentHistory",
                                JSON.stringify(
                                    updatedHistory
                                )
                            );

                            setPayment(
                                newPayment
                            );

                        } else {

                            setError(
                                verifyData.message ||
                                "Payment verification failed."
                            );
                        }

                    } catch (error) {

                        console.error(
                            "Verification error:",
                            error
                        );

                        setError(
                            "Payment verification failed."
                        );
                    }

                    setLoading(false);
                },

                // ----------------------------
                // PAYMENT FAILED
                // ----------------------------
                modal: {
                    ondismiss: function () {
                        setLoading(false);

                        setError(
                            "Payment cancelled."
                        );
                    }
                },

                theme: {
                    color: "#2563eb"
                }
            };

            // Check Razorpay Checkout
            if (!window.Razorpay) {

                setError(
                    "Razorpay Checkout failed to load."
                );

                setLoading(false);
                return;
            }

            const razorpay =
                new window.Razorpay(options);

            // ----------------------------
            // RECORD FAILED PAYMENT
            // ----------------------------
            razorpay.on(
                "payment.failed",
                async function (response) {

                    console.log(
                        "Payment failed:",
                        response
                    );

                    try {

                        await fetch(
                            "http://localhost:5000/record-failed-payment",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    razorpay_payment_id:
                                        response.error.metadata
                                            ?.payment_id ||
                                        "N/A",

                                    razorpay_order_id:
                                        response.error.metadata
                                            ?.order_id ||
                                        orderData.order.id,

                                    amount:
                                        Number(amount),

                                    error_code:
                                        response.error.code ||
                                        "UNKNOWN",

                                    error_description:
                                        response.error.description ||
                                        "Payment failed",

                                    error_reason:
                                        response.error.reason ||
                                        "Unknown reason"
                                })
                            }
                        );

                        setError(
                            "❌ Payment failed. The transaction has been recorded in the dashboard."
                        );

                    } catch (error) {

                        console.error(
                            "Failed payment recording error:",
                            error
                        );

                        setError(
                            "Payment failed, but the transaction could not be recorded."
                        );
                    }

                    setLoading(false);
                }
            );

            // Open Razorpay
            razorpay.open();

        } catch (error) {

            console.error(
                "Payment error:",
                error
            );

            setError(
                "Cannot connect to payment server."
            );

            setLoading(false);
        }
    };

    // =====================================================
    // HOME PAGE
    // =====================================================
    if (showHome && !payment) {

        return (
            <Home
                onMakePayment={() => {
                    setShowHome(false);
                    setError("");
                }}
            />
        );
    }

    // =====================================================
    // PAYMENT HISTORY
    // =====================================================
    if (payment === "history") {

        return (
            <div className="page">

                <div className="success-card">

                    <div className="header">

                        <div className="logo">
                            PayEase
                        </div>

                        <div className="secure">
                            🔒 Secure Payment
                        </div>

                    </div>

                    <div className="content">

                        <h1>
                            📋 Payment History
                        </h1>

                        <p className="success-text">
                            Your previous transactions
                        </p>

                        {history.length === 0 ? (

                            <p className="success-text">
                                No payments yet.
                            </p>

                        ) : (

                            history.map(
                                (item, index) => (

                                    <div
                                        className="details"
                                        key={index}
                                    >

                                        <div className="detail-row">

                                            <span>
                                                Amount
                                            </span>

                                            <strong>
                                                ₹{item.amount}
                                            </strong>

                                        </div>

                                        <div className="detail-row">

                                            <span>
                                                Payment ID
                                            </span>

                                            <strong>
                                                {item.paymentId}
                                            </strong>

                                        </div>

                                        <div className="detail-row">

                                            <span>
                                                Order ID
                                            </span>

                                            <strong>
                                                {item.orderId}
                                            </strong>

                                        </div>

                                        <div className="detail-row">

                                            <span>
                                                Date
                                            </span>

                                            <strong>
                                                {item.date}
                                            </strong>

                                        </div>

                                        <div className="detail-row">

                                            <span>
                                                Status
                                            </span>

                                            <strong className="status">
                                                ✓ {item.status}
                                            </strong>

                                        </div>

                                    </div>
                                )
                            )
                        )}

                        <button
                            className="pay-button"
                            onClick={() => {
                                setPayment(null);
                                setShowHome(false);
                            }}
                        >
                            ← Back to Payment
                        </button>

                        <button
                            className="history-button"
                            onClick={() =>
                                setShowHome(true)
                            }
                        >
                            🏠 Home
                        </button>

                    </div>

                </div>

            </div>
        );
    }

    // =====================================================
    // PAYMENT SUCCESS
    // =====================================================
    if (payment) {

        return (
            <div className="page">

                <div className="success-card">

                    <div className="success-icon">
                        ✓
                    </div>

                    <h1>
                        Payment Successful!
                    </h1>

                    <p className="success-text">
                        Your payment has been
                        completed successfully.
                    </p>

                    <div className="paid-amount">
                        ₹{payment.amount}
                    </div>

                    <div className="details">

                        <div className="detail-row">

                            <span>
                                Payment ID
                            </span>

                            <strong>
                                {payment.paymentId}
                            </strong>

                        </div>

                        <div className="detail-row">

                            <span>
                                Order ID
                            </span>

                            <strong>
                                {payment.orderId}
                            </strong>

                        </div>

                        <div className="detail-row">

                            <span>
                                Status
                            </span>

                            <strong className="status">
                                SUCCESS ✓
                            </strong>

                        </div>

                    </div>

                    <button
                        className="pay-button"
                        onClick={() => {
                            setPayment(null);
                            setShowHome(false);
                        }}
                    >
                        Make Another Payment
                    </button>

                    <button
                        className="history-button"
                        onClick={downloadReceipt}
                    >
                        📄 Download Receipt
                    </button>

                    <button
                        className="history-button"
                        onClick={() =>
                            setPayment("history")
                        }
                    >
                        📋 Payment History
                    </button>

                    <button
                        className="history-button"
                        onClick={() =>
                            setShowHome(true)
                        }
                    >
                        🏠 Back to Home
                    </button>

                    <p className="secure-text">
                        🔒 Payment processed securely
                    </p>

                </div>

            </div>
        );
    }

    // =====================================================
    // PAYMENT PAGE
    // =====================================================
    return (
        <div className="page">

            <div className="payment-card">

                <div className="header">

                    <div className="logo">
                        PayEase
                    </div>

                    <div className="secure">
                        🔒 Secure Payment
                    </div>

                </div>

                <div className="content">

                    <h1>
                        Complete Your Payment
                    </h1>

                    <p className="subtitle">
                        Fast, simple and secure payment
                    </p>

                    <div className="order-box">

                        <h3>
                            Order Summary
                        </h3>

                        <div className="row">

                            <span>
                                Product
                            </span>

                            <span>
                                College Registration
                            </span>

                        </div>

                        <div className="row">

                            <span>
                                Amount
                            </span>

                            <span>
                                ₹{amount || 0}
                            </span>

                        </div>

                    </div>

                    <label>
                        Payment Amount
                    </label>

                    <div className="amount-input">

                        <span>
                            ₹
                        </span>

                        <input
                            type="number"
                            min="1"
                            value={amount}
                            onChange={(e) =>
                                setAmount(
                                    e.target.value
                                )
                            }
                        />

                    </div>

                    <button
                        className="pay-button"
                        onClick={payNow}
                        disabled={loading}
                    >
                        {loading
                            ? "Processing Payment..."
                            : "🔒 Pay Securely"}
                    </button>

                    <button
                        className="history-button"
                        onClick={() =>
                            setPayment("history")
                        }
                    >
                        📋 Payment History
                    </button>

                    <button
                        className="history-button"
                        onClick={() => {
                            window.location.href =
                                "http://localhost:8501";
                        }}
                    >
                        📊 Go to Dashboard
                    </button>

                    <button
                        className="history-button"
                        onClick={() =>
                            setShowHome(true)
                        }
                    >
                        🏠 Back to Home
                    </button>

                    {error && (
                        <div className="error">
                            ⚠️ {error}
                        </div>
                    )}

                    <div className="security">
                        🛡️ Your payment information
                        is securely processed
                    </div>

                </div>

                <div className="footer">
                    © 2026 PayEase • Payment Demo
                </div>

            </div>

        </div>
    );
}

export default App;