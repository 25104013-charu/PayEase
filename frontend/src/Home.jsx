import "./Home.css";

function Home({ onMakePayment }) {
    return (
        <div className="home">

            {/* NAVBAR */}
            <nav className="home-nav">

                <div className="home-logo">
                    <div className="logo-mark">P</div>
                    <span>PayEase</span>
                </div>

                <div className="nav-links">
                    <a href="#home">Home</a>
                    <a href="#features">Features</a>
                    <a href="#workflow">How It Works</a>
                    <a
                        href="https://payease-ai-dashboard.streamlit.app"
                        target="_blank"
                        rel="noreferrer"
                    >
                        AI Dashboard
                    </a>
                </div>

                <button
                    className="nav-payment-btn"
                    onClick={onMakePayment}
                >
                    Make Payment
                </button>

            </nav>


            {/* HERO */}
            <section className="hero" id="home">

                <div className="hero-content">

                    <div className="hero-badge">
                        <span>✦</span>
                        AI-Powered Revenue Recovery
                    </div>

                    <h1>
                        Smart Payments.
                        <br />
                        <span>Intelligent Recovery.</span>
                    </h1>

                    <p>
                        PayEase combines secure digital payments
                        with AI-powered revenue recovery to detect
                        failed transactions, understand why they
                        failed, and recover lost revenue intelligently.
                    </p>

                    <div className="hero-buttons">

                        <button
                            className="primary-btn"
                            onClick={onMakePayment}
                        >
                            💳 Make a Payment
                        </button>

                        <a
                            className="secondary-btn"
                            href="https://payease-ai-recovery.streamlit.app/"
                            target="_blank"
                            rel="noreferrer"
                        >
                            🤖 Open AI Dashboard
                        </a>

                    </div>

                    <div className="trust-row">

                        <span>✓ Secure Payments</span>
                        <span>✓ AI-Powered Recovery</span>
                        <span>✓ Real-Time Analytics</span>

                    </div>

                </div>


                {/* DASHBOARD PREVIEW */}
                <div className="dashboard-preview">

                    <div className="preview-header">

                        <div>
                            <small>PayEase</small>
                            <h3>Revenue Recovery</h3>
                        </div>

                        <div className="live-badge">
                            ● LIVE
                        </div>

                    </div>


                    <div className="revenue-card">

                        <div>
                            <span>Total Revenue</span>
                            <strong>₹8.64L</strong>
                        </div>

                        <div className="revenue-icon">
                            ₹
                        </div>

                    </div>


                    <div className="preview-grid">

                        <div className="mini-card">

                            <span className="mini-icon green">
                                ✓
                            </span>

                            <div>
                                <small>Successful</small>
                                <strong>7</strong>
                            </div>

                        </div>

                        <div className="mini-card">

                            <span className="mini-icon red">
                                !
                            </span>

                            <div>
                                <small>Failed</small>
                                <strong>4</strong>
                            </div>

                        </div>

                    </div>


                    <div className="risk-card">

                        <div className="risk-top">
                            <span>Revenue at Risk</span>
                            <span className="risk-tag">
                                AI DETECTED
                            </span>
                        </div>

                        <strong>₹56,490</strong>

                        <div className="risk-bar">
                            <div></div>
                        </div>

                        <p>
                            AI identified failed transactions
                            requiring recovery.
                        </p>

                    </div>


                    <div className="ai-action">

                        <div className="ai-symbol">
                            ✦
                        </div>

                        <div>
                            <small>AI Recommended Action</small>
                            <strong>
                                Retry Payment
                            </strong>
                        </div>

                        <span className="arrow">
                            →
                        </span>

                    </div>

                </div>

            </section>


            {/* FEATURES */}
            <section className="features-section" id="features">

                <div className="section-heading">

                    <span>POWERFUL FEATURES</span>

                    <h2>
                        Everything you need to
                        <br />
                        recover lost revenue.
                    </h2>

                    <p>
                        PayEase brings payments, AI diagnosis,
                        recovery decisions and analytics together
                        in one platform.
                    </p>

                </div>


                <div className="features-grid">

                    <div className="feature-card">

                        <div className="feature-icon blue">
                            💳
                        </div>

                        <h3>
                            Secure Payments
                        </h3>

                        <p>
                            Process college and digital payments
                            securely through Razorpay.
                        </p>

                    </div>


                    <div className="feature-card">

                        <div className="feature-icon purple">
                            🎯
                        </div>

                        <h3>
                            Revenue-at-Risk Detection
                        </h3>

                        <p>
                            Automatically identify failed
                            transactions that represent lost revenue.
                        </p>

                    </div>


                    <div className="feature-card">

                        <div className="feature-icon orange">
                            🧠
                        </div>

                        <h3>
                            AI Diagnosis
                        </h3>

                        <p>
                            Understand the possible reason behind
                            every failed payment.
                        </p>

                    </div>


                    <div className="feature-card">

                        <div className="feature-icon green">
                            ⚡
                        </div>

                        <h3>
                            Smart Recovery
                        </h3>

                        <p>
                            AI recommends the appropriate recovery
                            action based on transaction conditions.
                        </p>

                    </div>


                    <div className="feature-card">

                        <div className="feature-icon cyan">
                            📊
                        </div>

                        <h3>
                            Recovery Analytics
                        </h3>

                        <p>
                            Track failed payments, recovered money,
                            escalation and recovery performance.
                        </p>

                    </div>


                    <div className="feature-card">

                        <div className="feature-icon red">
                            🛡️
                        </div>

                        <h3>
                            Controlled Recovery
                        </h3>

                        <p>
                            Stopping rules and escalation controls
                            prevent unlimited recovery attempts.
                        </p>

                    </div>

                </div>

            </section>


            {/* WORKFLOW */}
            <section
                className="workflow-section"
                id="workflow"
            >

                <div className="section-heading">

                    <span>HOW IT WORKS</span>

                    <h2>
                        From failed payment
                        <br />
                        to revenue recovery.
                    </h2>

                </div>


                <div className="workflow">

                    <div className="workflow-step">

                        <div className="step-number">
                            01
                        </div>

                        <div className="step-icon">
                            🔎
                        </div>

                        <h3>Detect</h3>

                        <p>
                            PayEase detects failed transactions
                            and identifies revenue at risk.
                        </p>

                    </div>


                    <div className="workflow-line"></div>


                    <div className="workflow-step">

                        <div className="step-number">
                            02
                        </div>

                        <div className="step-icon">
                            🧠
                        </div>

                        <h3>Diagnose</h3>

                        <p>
                            AI analyses the transaction and
                            identifies the likely failure cause.
                        </p>

                    </div>


                    <div className="workflow-line"></div>


                    <div className="workflow-step">

                        <div className="step-number">
                            03
                        </div>

                        <div className="step-icon">
                            ⚡
                        </div>

                        <h3>Decide</h3>

                        <p>
                            The AI decision engine selects a
                            suitable recovery action.
                        </p>

                    </div>


                    <div className="workflow-line"></div>


                    <div className="workflow-step">

                        <div className="step-number">
                            04
                        </div>

                        <div className="step-icon">
                            💰
                        </div>

                        <h3>Recover</h3>

                        <p>
                            The bounded recovery workflow attempts
                            to recover eligible revenue.
                        </p>

                    </div>

                </div>

            </section>


            {/* AI SECTION */}
            <section className="ai-section">

                <div className="ai-content">

                    <div className="hero-badge">
                        <span>✦</span>
                        Intelligent Decision Engine
                    </div>

                    <h2>
                        Payments are only
                        <br />
                        the beginning.
                    </h2>

                    <p>
                        PayEase doesn't stop when a transaction
                        fails. Its AI-powered recovery system
                        identifies revenue at risk, recommends
                        recovery actions, tracks outcomes and
                        escalates important cases when required.
                    </p>

                    <div className="ai-points">

                        <div>
                            <span>✓</span>
                            Detect revenue at risk
                        </div>

                        <div>
                            <span>✓</span>
                            Diagnose transaction failures
                        </div>

                        <div>
                            <span>✓</span>
                            Recommend recovery actions
                        </div>

                        <div>
                            <span>✓</span>
                            Measure recovered revenue
                        </div>

                    </div>

                    <a
                        className="ai-dashboard-btn"
                        href="http://localhost:8501"
                        target="_blank"
                        rel="noreferrer"
                    >
                        Explore AI Dashboard →
                    </a>

                </div>


                <div className="ai-visual">

                    <div className="ai-glow"></div>

                    <div className="ai-main-card">

                        <div className="ai-card-top">

                            <div className="ai-big-icon">
                                ✦
                            </div>

                            <div>
                                <small>
                                    PayEase AI
                                </small>

                                <h3>
                                    Recovery Engine
                                </h3>
                            </div>

                        </div>


                        <div className="decision">

                            <span>
                                Transaction
                            </span>

                            <strong>
                                ₹56,490
                            </strong>

                        </div>


                        <div className="decision">

                            <span>
                                Status
                            </span>

                            <strong className="failed">
                                FAILED
                            </strong>

                        </div>


                        <div className="decision">

                            <span>
                                AI Decision
                            </span>

                            <strong className="retry">
                                RETRY PAYMENT
                            </strong>

                        </div>


                        <div className="decision-footer">
                            ✓ Decision bounded by recovery rules
                        </div>

                    </div>

                </div>

            </section>


            {/* CTA */}
            <section className="cta-section">

                <div>

                    <span className="cta-label">
                        READY TO GET STARTED?
                    </span>

                    <h2>
                        Make payments smarter.
                    </h2>

                    <p>
                        Experience secure payments with
                        intelligent revenue recovery.
                    </p>

                </div>

                <button
                    className="cta-button"
                    onClick={onMakePayment}
                >
                    💳 Make a Payment
                </button>

            </section>


            {/* FOOTER */}
            <footer className="home-footer">

                <div className="footer-brand">

                    <div className="home-logo">

                        <div className="logo-mark">
                            P
                        </div>

                        <span>
                            PayEase
                        </span>

                    </div>

                    <p>
                        Smart payments. Intelligent recovery.
                    </p>

                </div>

                <div className="footer-right">
                    © 2026 PayEase • Built for Razorpay Buildathon
                </div>

            </footer>

        </div>
    );
}

export default Home;