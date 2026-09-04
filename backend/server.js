const express = require("express");
const cors = require("cors");
const fs = require("fs");
const crypto = require("crypto");
const Razorpay = require("razorpay");
require("dotenv").config();

const app = express();

app.use(cors());
app.use(express.json());

const paymentsFile = "./payments.json";

// Create payments.json if it doesn't exist
if (!fs.existsSync(paymentsFile)) {
    fs.writeFileSync(paymentsFile, "[]");
}

// Razorpay Test Mode
const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID,
    key_secret: process.env.RAZORPAY_KEY_SECRET
});
console.log(
    "Razorpay Key ID loaded:",
    process.env.RAZORPAY_KEY_ID ? "YES" : "NO"
);

console.log(
    "Razorpay Secret loaded:",
    process.env.RAZORPAY_KEY_SECRET ? "YES" : "NO"
);

app.get("/", (req, res) => {
    res.send("PayEase Razorpay payment backend is running!");
});

// ---------------------------------------------------------
// CREATE RAZORPAY ORDER
// ---------------------------------------------------------

app.post("/create-order", async (req, res) => {
    try {
        const { amount } = req.body;

        if (!amount || Number(amount) <= 0) {
            return res.status(400).json({
                success: false,
                message: "Invalid amount"
            });
        }

        const options = {
            amount: Math.round(Number(amount) * 100),
            currency: "INR",
            receipt: "receipt_" + Date.now()
        };

        const order = await razorpay.orders.create(options);

        res.json({
            success: true,
            order: order,
            key_id: process.env.RAZORPAY_KEY_ID
        });

    } catch (error) {
        console.error("Order creation error:", error);

        res.status(500).json({
            success: false,
            message: "Unable to create Razorpay order."
        });
    }
});

// ---------------------------------------------------------
// VERIFY RAZORPAY PAYMENT
// ---------------------------------------------------------

app.post("/verify-payment", (req, res) => {
    try {
        const {
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        } = req.body;

        if (
            !razorpay_order_id ||
            !razorpay_payment_id ||
            !razorpay_signature
        ) {
            return res.status(400).json({
                success: false,
                message: "Missing payment verification details."
            });
        }

        const generatedSignature =
            crypto
                .createHmac("sha256", process.env.RAZORPAY_KEY_SECRET)
                .update(
                    razorpay_order_id +
                    "|" +
                    razorpay_payment_id
                )
                .digest("hex");

        if (generatedSignature !== razorpay_signature) {
            return res.status(400).json({
                success: false,
                message: "Payment signature verification failed."
            });
        }

        // Payment is verified
        const payment = {
            payment_id: razorpay_payment_id,
            order_id: razorpay_order_id,
            amount: Number(req.body.amount),
            status: "SUCCESS",
            failure_reason: null,
            date: new Date().toISOString()
        };

        const payments = JSON.parse(
            fs.readFileSync(paymentsFile, "utf8")
        );

        payments.push(payment);

        fs.writeFileSync(
            paymentsFile,
            JSON.stringify(payments, null, 2)
        );

        res.json({
            success: true,
            payment: payment,
            message: "Payment verified successfully!"
        });

    } catch (error) {
        console.error("Payment verification error:", error);

        res.status(500).json({
            success: false,
            message: "Payment verification failed."
        });
    }
});
app.post("/verify-payment", (req, res) => {
    // your existing verification code
});


// ADD THE NEW CODE HERE
app.post("/record-failed-payment", (req, res) => {
    try {
        const {
            razorpay_payment_id,
            razorpay_order_id,
            amount,
            error_code,
            error_description,
            error_reason
        } = req.body;

        const payment = {
            payment_id: razorpay_payment_id || "N/A",
            order_id: razorpay_order_id || "N/A",
            amount: Number(amount) || 0,
            status: "FAILED",
            failure_reason:
                error_description ||
                error_reason ||
                error_code ||
                "Payment failed",
            date: new Date().toISOString()
        };

        const payments = JSON.parse(
            fs.readFileSync(paymentsFile, "utf8")
        );

        payments.push(payment);

        fs.writeFileSync(
            paymentsFile,
            JSON.stringify(payments, null, 2)
        );

        console.log("Failed payment recorded:", payment);

        res.json({
            success: true,
            payment: payment,
            message: "Failed payment recorded successfully."
        });

    } catch (error) {
        console.error("Failed payment recording error:", error);

        res.status(500).json({
            success: false,
            message: "Unable to record failed payment."
        });
    }
});

// ---------------------------------------------------------
// GET ALL PAYMENTS
// ---------------------------------------------------------

app.get("/payments", (req, res) => {
    try {
        const payments = JSON.parse(
            fs.readFileSync(paymentsFile, "utf8")
        );

        res.json(payments);

    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Unable to read payment history."
        });
    }
});

const PORT = 5000;

app.listen(PORT, () => {
    console.log(
        `PayEase Razorpay backend running on http://localhost:${PORT}`
    );
});