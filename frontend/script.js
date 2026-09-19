/* =========================================================
   NETSENSE AI
   FRONTEND JAVASCRIPT
   ========================================================= */


/* =========================================================
   CONFIGURATION
   ========================================================= */

const API_URL = "http://127.0.0.1:8000";


/* =========================================================
   ELEMENTS
   ========================================================= */

const apiKeyInput = document.getElementById("apiKey");
const toggleKey = document.getElementById("toggleKey");
const analyzeBtn = document.getElementById("analyzeBtn");

const inputError = document.getElementById("inputError");

const loadingBox = document.getElementById("loadingBox");
const results = document.getElementById("results");

const useOptions = document.querySelectorAll(".use-option");


/* =========================================================
   SELECTED USE CASE
   ========================================================= */

let selectedUseCase = "Gaming";


useOptions.forEach(option => {

    option.addEventListener("click", () => {

        useOptions.forEach(item => {
            item.classList.remove("selected");
        });

        option.classList.add("selected");

        selectedUseCase = option.dataset.use;

    });

});


/* =========================================================
   SHOW / HIDE API KEY
   ========================================================= */

toggleKey.addEventListener("click", () => {

    if (apiKeyInput.type === "password") {

        apiKeyInput.type = "text";

        toggleKey.textContent = "HIDE";

    } else {

        apiKeyInput.type = "password";

        toggleKey.textContent = "SHOW";

    }

});


/* =========================================================
   API KEY INPUT
   ========================================================= */

apiKeyInput.addEventListener("input", () => {

    inputError.textContent = "";

});


/* =========================================================
   ANALYZE BUTTON
   ========================================================= */

analyzeBtn.addEventListener("click", analyzeConnection);


/* =========================================================
   MAIN ANALYSIS FUNCTION
   ========================================================= */

async function analyzeConnection() {

    const apiKey = apiKeyInput.value.trim();


    /* Clear old error */

    inputError.textContent = "";


    /* Validate API key */

    if (!apiKey) {

        inputError.textContent =
            "Please enter your Gemini API key.";

        apiKeyInput.focus();

        return;

    }


    /* Hide previous results */

    results.classList.add("hidden");


    /* Show loading */

    loadingBox.classList.remove("hidden");


    /* Disable button */

    analyzeBtn.disabled = true;

    analyzeBtn.style.opacity = "0.65";

    analyzeBtn.innerHTML = `
        <span class="button-icon">⟳</span>
        ANALYZING...
    `;


    try {

        const response = await fetch(`${API_URL}/analyze`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                api_key: apiKey,

                use_case: selectedUseCase

            })

        });


        /* Check HTTP error */

        if (!response.ok) {

            throw new Error(
                `Backend returned ${response.status}`
            );

        }


        const data = await response.json();


        /* Display results */

        displayResults(data);


    } catch (error) {

        console.error("Analysis Error:", error);

        inputError.textContent =
            "Unable to connect to the backend. Make sure FastAPI is running on port 8000.";

    } finally {

        /* Hide loading */

        loadingBox.classList.add("hidden");


        /* Enable button */

        analyzeBtn.disabled = false;

        analyzeBtn.style.opacity = "1";

        analyzeBtn.innerHTML = `
            <span class="button-icon">✦</span>
            ANALYZE MY CONNECTION
            <span class="button-arrow">→</span>
        `;

    }

}


/* =========================================================
   DISPLAY RESULTS
   ========================================================= */

function displayResults(data) {

    console.log("API Response:", data);


    if (!data) {

        throw new Error("Empty API response.");

    }


    /* =====================================================
       NETWORK DATA
       ===================================================== */

    const network = data.network || {};

    const fuzzy = data.fuzzy || {};


    const latency =
        network.latency ?? "--";

    const jitter =
        network.jitter ?? "--";

    const packetLoss =
        network.packet_loss ?? "--";

    const score =
        fuzzy.score ?? "--";

    const category =
        fuzzy.category ?? "Unknown";


    /* =====================================================
       METRICS
       ===================================================== */

    document.getElementById("latencyValue").textContent =
        latency;

    document.getElementById("jitterValue").textContent =
        jitter;

    document.getElementById("packetValue").textContent =
        packetLoss;

    document.getElementById("scoreValue").textContent =
        score;


    document.getElementById("overallScore").textContent =
        score;

    document.getElementById("overallCategory").textContent =
        category;


    /* =====================================================
       QUALITY PILL
       ===================================================== */

    const qualityPill =
        document.getElementById("qualityPill");

    qualityPill.textContent =
        category.toUpperCase();


    qualityPill.style.background =
        getCategoryBackground(category);

    qualityPill.style.color =
        getCategoryColor(category);


    /* =====================================================
       FUZZY MEMBERSHIP
       ===================================================== */

    const membership =
        fuzzy.membership || {};


    const latencyMembership =
        membership.latency || {};

    const jitterMembership =
        membership.jitter || {};

    const packetMembership =
        membership.packet_loss || {};


    document.getElementById("latLow").textContent =
        formatMembership(latencyMembership.low);

    document.getElementById("latMedium").textContent =
        formatMembership(latencyMembership.medium);

    document.getElementById("latHigh").textContent =
        formatMembership(latencyMembership.high);


    document.getElementById("jitLow").textContent =
        formatMembership(jitterMembership.low);

    document.getElementById("jitMedium").textContent =
        formatMembership(jitterMembership.medium);

    document.getElementById("jitHigh").textContent =
        formatMembership(jitterMembership.high);


    document.getElementById("packetLow").textContent =
        formatMembership(packetMembership.low);

    document.getElementById("packetMedium").textContent =
        formatMembership(packetMembership.medium);

    document.getElementById("packetHigh").textContent =
        formatMembership(packetMembership.high);


    /* =====================================================
       CHART
       ===================================================== */

    createMembershipChart(
        latencyMembership,
        jitterMembership,
        packetMembership
    );


    /* =====================================================
       AI ANALYSIS
       ===================================================== */

    const ai =
        data.ai || {};

    if (ai.success) {

        displayAIAnalysis(ai.analysis);

    } else {

        displayAIError(
            ai.message || "AI analysis unavailable."
        );

    }


    /* =====================================================
       SHOW RESULTS
       ===================================================== */

    results.classList.remove("hidden");


    /* Scroll to results */

    setTimeout(() => {

        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }, 150);

}


/* =========================================================
   MEMBERSHIP FORMAT
   ========================================================= */

function formatMembership(value) {

    if (value === undefined || value === null) {
        return "--";
    }

    return Number(value).toFixed(2);

}


/* =========================================================
   CATEGORY COLORS
   ========================================================= */

function getCategoryBackground(category) {

    const value =
        String(category).toLowerCase();


    if (value === "poor") {
        return "#fff0f2";
    }

    if (value === "average") {
        return "#fff8e8";
    }

    return "#eafff5";

}


function getCategoryColor(category) {

    const value =
        String(category).toLowerCase();


    if (value === "poor") {
        return "#d94b61";
    }

    if (value === "average") {
        return "#bd7a15";
    }

    return "#179367";

}


/* =========================================================
   CHART
   ========================================================= */

let membershipChart = null;


function createMembershipChart(
    latency,
    jitter,
    packet
) {

    const canvas =
        document.getElementById("membershipChart");


    if (!canvas) {
        return;
    }


    /* Destroy previous chart */

    if (membershipChart) {

        membershipChart.destroy();

    }


    membershipChart = new Chart(
        canvas,
        {

            type: "bar",

            data: {

                labels: [
                    "Latency",
                    "Jitter",
                    "Packet Loss"
                ],

                datasets: [

                    {
                        label: "Low",

                        data: [
                            latency.low ?? 0,
                            jitter.low ?? 0,
                            packet.low ?? 0
                        ]
                    },

                    {
                        label: "Medium",

                        data: [
                            latency.medium ?? 0,
                            jitter.medium ?? 0,
                            packet.medium ?? 0
                        ]
                    },

                    {
                        label: "High",

                        data: [
                            latency.high ?? 0,
                            jitter.high ?? 0,
                            packet.high ?? 0
                        ]
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false
                },

                plugins: {

                    legend: {
                        position: "top",

                        labels: {
                            font: {
                                family: "Inter",
                                size: 11
                            }
                        }
                    },

                    tooltip: {

                        callbacks: {

                            label: function(context) {

                                return (
                                    context.dataset.label +
                                    ": " +
                                    Number(context.raw).toFixed(2)
                                );

                            }

                        }

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        max: 1,

                        ticks: {
                            stepSize: 0.2,

                            font: {
                                family: "Inter",
                                size: 10
                            }
                        },

                        title: {
                            display: true,
                            text: "Membership Value"
                        }

                    },

                    x: {

                        ticks: {
                            font: {
                                family: "Inter",
                                size: 10
                            }
                        }

                    }

                }

            }

        }
    );

}


/* =========================================================
   AI ANALYSIS PARSER
   ========================================================= */

function displayAIAnalysis(text) {

    if (!text) {

        displayAIError(
            "Gemini returned an empty response."
        );

        return;

    }


    const sections =
        parseAISections(text);


    document.getElementById("aiSummary").textContent =
        sections.summary ||
        "No summary was generated.";


    document.getElementById("aiPerformance").textContent =
        sections.performance ||
        "No performance analysis was generated.";


    document.getElementById("aiUseCase").textContent =
        sections.useCase ||
        "No use-case analysis was generated.";


    const recommendationList =
        document.getElementById("recommendationList");


    recommendationList.innerHTML = "";


    if (
        sections.recommendations &&
        sections.recommendations.length > 0
    ) {

        sections.recommendations.forEach(
            (recommendation, index) => {

                const item =
                    document.createElement("div");

                item.className =
                    "recommendation-item";


                item.innerHTML = `

                    <span>
                        ${String(index + 1).padStart(2, "0")}
                    </span>

                    <p>
                        ${escapeHTML(recommendation)}
                    </p>

                `;


                recommendationList.appendChild(item);

            }
        );

    } else {

        recommendationList.innerHTML = `

            <div class="recommendation-item">

                <span>01</span>

                <p>
                    No recommendations were generated.
                </p>

            </div>

        `;

    }

}


/* =========================================================
   AI ERROR
   ========================================================= */

function displayAIError(message) {

    document.getElementById("aiSummary").textContent =
        "AI analysis unavailable.";

    document.getElementById("aiPerformance").textContent =
        message;

    document.getElementById("aiUseCase").textContent =
        "Please verify your Gemini API key and model configuration.";

    document.getElementById("recommendationList").innerHTML = `

        <div class="recommendation-item">

            <span>!</span>

            <p>
                ${escapeHTML(message)}
            </p>

        </div>

    `;

}


/* =========================================================
   PARSE GEMINI RESPONSE
   ========================================================= */

function parseAISections(text) {

    const result = {

        summary: "",
        performance: "",
        useCase: "",
        recommendations: []

    };


    /* Normalize text */

    const normalized =
        text.replace(/\r/g, "").trim();


    /* =====================================================
       SUMMARY
       ===================================================== */

    const summaryMatch =
        normalized.match(
            /SUMMARY:\s*([\s\S]*?)(?=\n\s*PERFORMANCE:|\n\s*USE CASE:|\n\s*RECOMMENDATIONS:|$)/i
        );


    if (summaryMatch) {

        result.summary =
            cleanAIText(summaryMatch[1]);

    }


    /* =====================================================
       PERFORMANCE
       ===================================================== */

    const performanceMatch =
        normalized.match(
            /PERFORMANCE:\s*([\s\S]*?)(?=\n\s*USE CASE:|\n\s*RECOMMENDATIONS:|$)/i
        );


    if (performanceMatch) {

        result.performance =
            cleanAIText(performanceMatch[1]);

    }


    /* =====================================================
       USE CASE
       ===================================================== */

    const useCaseMatch =
        normalized.match(
            /USE CASE:\s*([\s\S]*?)(?=\n\s*RECOMMENDATIONS:|$)/i
        );


    if (useCaseMatch) {

        result.useCase =
            cleanAIText(useCaseMatch[1]);

    }


    /* =====================================================
       RECOMMENDATIONS
       ===================================================== */

    const recommendationMatch =
        normalized.match(
            /RECOMMENDATIONS:\s*([\s\S]*)$/i
        );


    if (recommendationMatch) {

        const recommendationText =
            recommendationMatch[1];


        result.recommendations =
            recommendationText
                .split(/\n+/)
                .map(item =>
                    item
                        .replace(
                            /^\s*(?:[-•*]|\d+[.)])\s*/,
                            ""
                        )
                        .trim()
                )
                .filter(item => item.length > 0);

    }


    return result;

}


/* =========================================================
   CLEAN AI TEXT
   ========================================================= */

function cleanAIText(text) {

    return text
        .replace(/\*\*/g, "")
        .replace(/\*/g, "")
        .replace(/^[-•]\s*/gm, "")
        .trim();

}


/* =========================================================
   BASIC HTML ESCAPING
   ========================================================= */

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


/* =========================================================
   NAVIGATION ACTIVE STATE
   ========================================================= */

const navLinks =
    document.querySelectorAll(".nav-link");


navLinks.forEach(link => {

    link.addEventListener("click", () => {

        navLinks.forEach(item => {
            item.classList.remove("active");
        });

        link.classList.add("active");

    });

});