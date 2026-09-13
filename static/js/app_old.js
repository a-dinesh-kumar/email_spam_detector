const API_BASE = "";


/* =========================================================
   LOAD OVERVIEW
========================================================= */

async function loadOverview() {

    try {

        const response = await fetch(
            `${API_BASE}/overview`
        );

        if (!response.ok) {
            throw new Error("Failed to load overview");
        }

        const data = await response.json();

        document.getElementById("emails-scanned").textContent =
            data.emails_scanned;

        document.getElementById("emails-delivered").textContent =
            data.delivered;

        document.getElementById("emails-quarantined").textContent =
            data.quarantined;

        document.getElementById("spam-rate").textContent =
            `${data.spam_rate}%`;

    } catch (error) {

        console.error("Overview error:", error);

    }
}


/* =========================================================
   LOAD INBOX
========================================================= */

async function loadInbox() {

    try {

        const response = await fetch(
            `${API_BASE}/inbox`
        );

        if (!response.ok) {
            throw new Error("Failed to load inbox");
        }

        const data = await response.json();

        const table = document.getElementById("inbox-table");

        document.getElementById("inbox-count").textContent =
            data.count;

        if (data.emails.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="3" class="empty-state">
                        No emails in inbox.
                    </td>
                </tr>
            `;

            return;
        }

        table.innerHTML = data.emails.map(email => {

            return `
                <tr>

                    <td>
                        ${escapeHtml(email.subject || "(No subject)")}
                    </td>

                    <td>
                        <span class="status delivered">
                            ${escapeHtml(email.status || "delivered")}
                        </span>
                    </td>

                    <td>
                        ${escapeHtml(email.timestamp || "-")}
                    </td>

                </tr>
            `;

        }).join("");

    } catch (error) {

        console.error("Inbox error:", error);

    }
}


/* =========================================================
   LOAD QUARANTINE
========================================================= */

async function loadQuarantine() {

    try {

        const response = await fetch(
            `${API_BASE}/quarantine`
        );

        if (!response.ok) {
            throw new Error("Failed to load quarantine");
        }

        const data = await response.json();

        const table = document.getElementById("spam-table");

        document.getElementById("spam-count").textContent =
            data.count;

        if (data.emails.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-state">
                        No quarantined emails.
                    </td>
                </tr>
            `;

            return;
        }

        table.innerHTML = data.emails.map(email => {

            return `
                <tr>

                    <td>
                        ${escapeHtml(email.subject || "(No subject)")}
                    </td>

                    <td>
                        <span class="status quarantined">
                            ${escapeHtml(email.status)}
                        </span>
                    </td>

                    <td>
                        ${escapeHtml(email.timestamp || "-")}
                    </td>

                    <td>
                        <button
                            class="release-button"
                            onclick="releaseEmail('${escapeHtml(email.id)}')"
                        >
                            Release
                        </button>
                    </td>

                </tr>
            `;

        }).join("");

    } catch (error) {

        console.error("Quarantine error:", error);

    }
}


/* =========================================================
   RELEASE QUARANTINED EMAIL
========================================================= */

async function releaseEmail(emailId) {

    try {

        const response = await fetch(
            `/quarantine/${encodeURIComponent(emailId)}/release`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!response.ok) {

            alert(
                data.detail || "Failed to release email."
            );

            return;
        }

        alert("Email released successfully.");

        await refreshDashboard();

    } catch (error) {

        console.error("Release error:", error);

        alert("Unable to release email.");

    }
}


/* =========================================================
   CLASSIFY JSON EMAIL
========================================================= */

document
    .getElementById("email-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const subject =
            document.getElementById("subject").value;

        const body =
            document.getElementById("body").value;

        const resultCard =
            document.getElementById("classification-result");

        try {

            const response = await fetch(
                "/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        subject: subject,
                        body: body
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Prediction failed"
                );
            }

            showClassificationResult(
                data.prediction
            );

        } catch (error) {

            console.error("Prediction error:", error);

            alert(error.message);

        }

    });


/* =========================================================
   UPLOAD EML
========================================================= */

document
    .getElementById("email-file")
    .addEventListener("change", async function() {

        const file = this.files[0];

        if (!file) {
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        try {

            const response = await fetch(
                "/predict-file",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail || "File prediction failed"
                );

            }

            showClassificationResult(
                data.prediction
            );

        } catch (error) {

            console.error("File prediction error:", error);

            alert(error.message);

        }

        this.value = "";

    });


/* =========================================================
   SHOW CLASSIFICATION RESULT
========================================================= */

function showClassificationResult(prediction) {

    const resultCard =
        document.getElementById("classification-result");

    const resultIcon =
        document.getElementById("result-icon");

    const resultLabel =
        document.getElementById("result-label");

    const resultMessage =
        document.getElementById("result-message");

    resultCard.classList.remove(
        "hidden",
        "ham",
        "spam"
    );

    if (prediction === "spam") {

        resultCard.classList.add("spam");

        resultIcon.textContent = "🚨";

        resultLabel.textContent =
            "SPAM DETECTED";

        resultMessage.textContent =
            "This email has been classified as spam.";

    } else {

        resultCard.classList.add("ham");

        resultIcon.textContent = "✅";

        resultLabel.textContent =
            "HAM — SAFE";

        resultMessage.textContent =
            "This email has been classified as legitimate.";

    }

}


/* =========================================================
   REFRESH DASHBOARD
========================================================= */

async function refreshDashboard() {

    await Promise.all([
        loadOverview(),
        loadInbox(),
        loadQuarantine()
    ]);

}


/* =========================================================
   HTML ESCAPING
========================================================= */

function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


/* =========================================================
   INITIAL LOAD
========================================================= */

refreshDashboard();