const API_BASE = "";

const sections = ["overview", "inbox", "spam"];

/* =========================================================
   PAGINATION STATE
========================================================= */

const paginationState = {
    inbox: {
        page: 1,
        pageSize: 10,
        emails: []
    },

    spam: {
        page: 1,
        pageSize: 10,
        emails: []
    }
};

const expandedEmails = {
    inbox: null,
    spam: null
};


/* =========================================================
   LOAD OVERVIEW
========================================================= */

async function loadOverview() {

    const response =
        await fetch(`${API_BASE}/overview`);

    if (!response.ok) {
        throw new Error("Failed to load overview");
    }

    const data =
        await response.json();

    document.getElementById(
        "emails-scanned"
    ).textContent =
        data.emails_scanned;

    document.getElementById(
        "emails-delivered"
    ).textContent =
        data.delivered;

    document.getElementById(
        "emails-quarantined"
    ).textContent =
        data.quarantined;

    document.getElementById(
        "spam-rate"
    ).textContent =
        `${data.spam_rate}%`;
}


/* =========================================================
   LOAD INBOX
========================================================= */

async function loadInbox() {

    const response =
        await fetch(`${API_BASE}/inbox`);

    if (!response.ok) {
        throw new Error("Failed to load inbox");
    }

    const data =
        await response.json();

    document.getElementById(
        "inbox-count"
    ).textContent =
        data.count;

    /*
     * Store the complete dataset locally.
     * Only the current page is rendered.
     */

    paginationState.inbox.emails =
        sortNewestFirst(data.emails);

    const totalPages =
        getTotalPages("inbox");

    if (
        paginationState.inbox.page >
        totalPages &&
        totalPages > 0
    ) {
        paginationState.inbox.page =
            totalPages;
    }

    renderInbox();
}


/* =========================================================
   RENDER INBOX
========================================================= */

function renderInbox() {

    const state =
        paginationState.inbox;

    const table =
        document.getElementById(
            "inbox-table"
        );

    if (!state.emails.length) {

        table.innerHTML = `
            <tr>
                <td colspan="3" class="empty-state">
                    No emails in inbox.
                </td>
            </tr>
        `;

        renderPagination("inbox");

        return;
    }

    const pageEmails =
        getCurrentPageEmails("inbox");

    table.innerHTML =
        pageEmails.map(email => {

            const emailId =
                String(email.id);

            const isExpanded =
                expandedEmails.inbox ===
                emailId;

            return `
                <tr
                    class="email-row ${isExpanded ? "expanded" : ""}"
                    onclick="toggleEmailDetails('inbox', '${escapeJsString(emailId)}')"
                >

                    <td>
                        <div class="email-subject">
                            ${escapeHtml(
                                email.subject ||
                                "(No subject)"
                            )}
                        </div>
                    </td>

                    <td>
                        <span class="status ${
                            email.status === "released"
                                ? "released"
                                : "delivered"
                        }">
                            ${escapeHtml(
                                email.status ||
                                "delivered"
                            )}
                        </span>
                    </td>

                    <td>
                        ${escapeHtml(
                            email.timestamp ||
                            "-"
                        )}
                    </td>

                </tr>

                ${
                    isExpanded
                        ? renderEmailDetails(
                            email,
                            3
                        )
                        : ""
                }
            `;
        }).join("");

    renderPagination("inbox");
}


/* =========================================================
   LOAD QUARANTINE
========================================================= */

async function loadQuarantine() {

    const response =
        await fetch(`${API_BASE}/quarantine`);

    if (!response.ok) {
        throw new Error(
            "Failed to load quarantine"
        );
    }

    const data =
        await response.json();

    document.getElementById(
        "spam-count"
    ).textContent =
        data.count;

    paginationState.spam.emails =
        sortNewestFirst(data.emails);

    const totalPages =
        getTotalPages("spam");

    if (
        paginationState.spam.page >
        totalPages &&
        totalPages > 0
    ) {
        paginationState.spam.page =
            totalPages;
    }

    renderQuarantine();
}


/* =========================================================
   RENDER QUARANTINE
========================================================= */

function renderQuarantine() {

    const state =
        paginationState.spam;

    const table =
        document.getElementById(
            "spam-table"
        );

    if (!state.emails.length) {

        table.innerHTML = `
            <tr>
                <td colspan="4" class="empty-state">
                    No quarantined emails.
                </td>
            </tr>
        `;

        renderPagination("spam");

        return;
    }

    const pageEmails =
        getCurrentPageEmails("spam");

    table.innerHTML =
        pageEmails.map(email => {

            const emailId =
                String(email.id);

            const isExpanded =
                expandedEmails.spam ===
                emailId;

            return `
                <tr
                    class="email-row ${isExpanded ? "expanded" : ""}"
                    onclick="toggleEmailDetails('spam', '${escapeJsString(emailId)}')"
                >

                    <td>
                        <div class="email-subject">
                            ${escapeHtml(
                                email.subject ||
                                "(No subject)"
                            )}
                        </div>
                    </td>

                    <td>
                        <span class="status quarantined">
                            ${escapeHtml(
                                email.status ||
                                "quarantined"
                            )}
                        </span>
                    </td>

                    <td>
                        ${escapeHtml(
                            email.timestamp ||
                            "-"
                        )}
                    </td>

                    <td>
                        <button
                            class="release-button"
                            type="button"
                            onclick="
                                event.stopPropagation();
                                releaseEmail('${escapeJsString(emailId)}')
                            "
                        >
                            Release
                        </button>
                    </td>

                </tr>

                ${
                    isExpanded
                        ? renderEmailDetails(
                            email,
                            4
                        )
                        : ""
                }
            `;
        }).join("");

    renderPagination("spam");
}


/* =========================================================
   EMAIL DETAILS
========================================================= */

function renderEmailDetails(
    email,
    columnCount
) {

    return `
        <tr class="email-details-row">

            <td colspan="${columnCount}">

                <div class="email-details">

                    <div class="email-details-header">
                        <span>Email content</span>
                        <span class="details-hint">
                            Click row to collapse
                        </span>
                    </div>

                    <div class="email-details-subject">
                        <strong>Subject:</strong>
                        ${escapeHtml(
                            email.subject ||
                            "(No subject)"
                        )}
                    </div>

                    <div class="email-details-body">
                        ${escapeHtml(
                            email.body ||
                            "(No email body)"
                        )}
                    </div>

                </div>

            </td>

        </tr>
    `;
}


/* =========================================================
   TOGGLE EMAIL DETAILS
========================================================= */

function toggleEmailDetails(
    type,
    emailId
) {

    if (
        expandedEmails[type] ===
        String(emailId)
    ) {

        expandedEmails[type] = null;

    } else {

        expandedEmails[type] =
            String(emailId);
    }

    if (type === "inbox") {
        renderInbox();
    } else {
        renderQuarantine();
    }
}


/* =========================================================
   PAGINATION
========================================================= */

function getTotalPages(type) {

    const state =
        paginationState[type];

    return Math.max(
        1,
        Math.ceil(
            state.emails.length /
            state.pageSize
        )
    );
}


function getCurrentPageEmails(type) {

    const state =
        paginationState[type];

    const start =
        (state.page - 1) *
        state.pageSize;

    const end =
        start +
        state.pageSize;

    return state.emails.slice(
        start,
        end
    );
}


function changePage(
    type,
    page
) {

    const state =
        paginationState[type];

    const totalPages =
        getTotalPages(type);

    if (
        page < 1 ||
        page > totalPages
    ) {
        return;
    }

    state.page = page;

    expandedEmails[type] = null;

    if (type === "inbox") {
        renderInbox();
    } else {
        renderQuarantine();
    }

    scrollToSection(
        type === "inbox"
            ? "inbox"
            : "spam"
    );
}


function renderPagination(type) {

    const state =
        paginationState[type];

    const container =
        document.getElementById(
            `${type}-pagination`
        );

    if (!container) {
        return;
    }

    const total =
        state.emails.length;

    const totalPages =
        getTotalPages(type);

    if (total <= state.pageSize) {

        container.innerHTML = "";

        return;
    }

    const start =
        ((state.page - 1) *
        state.pageSize) + 1;

    const end =
        Math.min(
            state.page *
            state.pageSize,
            total
        );

    container.innerHTML = `

        <div class="pagination-info">
            Showing ${start}-${end}
            of ${total}
        </div>

        <div class="pagination-controls">

            <button
                type="button"
                class="pagination-button"
                ${state.page === 1 ? "disabled" : ""}
                onclick="changePage('${type}', ${state.page - 1})"
            >
                ← Previous
            </button>

            <span class="pagination-page">
                Page ${state.page} of ${totalPages}
            </span>

            <button
                type="button"
                class="pagination-button"
                ${
                    state.page === totalPages
                        ? "disabled"
                        : ""
                }
                onclick="changePage('${type}', ${state.page + 1})"
            >
                Next →
            </button>

        </div>
    `;
}


/* =========================================================
   SORT NEWEST FIRST
========================================================= */

function sortNewestFirst(
    emails
) {

    return [...emails].sort(
        (a, b) => {

            const dateA =
                new Date(
                    a.timestamp || 0
                ).getTime();

            const dateB =
                new Date(
                    b.timestamp || 0
                ).getTime();

            return dateB - dateA;
        }
    );
}


/* =========================================================
   REFRESH DASHBOARD
========================================================= */

async function refreshDashboard(
    options = {}
) {

    const refreshButton =
        document.getElementById(
            "refresh-button"
        );

    if (refreshButton) {

        refreshButton.classList.add(
            "loading"
        );

        refreshButton.disabled =
            true;
    }

    try {

        await Promise.all([
            loadOverview(),
            loadInbox(),
            loadQuarantine()
        ]);

        if (options.target) {

            scrollToSection(
                options.target
            );
        }

    } catch (error) {

        console.error(
            "Dashboard refresh error:",
            error
        );

        showFormStatus(
            "Some dashboard data could not be refreshed. Please try again.",
            "error"
        );

    } finally {

        if (refreshButton) {

            refreshButton.classList.remove(
                "loading"
            );

            refreshButton.disabled =
                false;
        }
    }
}


/* =========================================================
   RELEASE QUARANTINED EMAIL
========================================================= */

async function releaseEmail(
    emailId
) {

    try {

        const response =
            await fetch(
                `/quarantine/${encodeURIComponent(emailId)}/release`,
                {
                    method: "POST"
                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to release email."
            );
        }

        showFormStatus(
            "Email released and delivered to Inbox.",
            "success"
        );

        await refreshDashboard({
            target: "inbox"
        });

    } catch (error) {

        console.error(
            "Release error:",
            error
        );

        showFormStatus(
            error.message ||
            "Unable to release email.",
            "error"
        );
    }
}


/* =========================================================
   CLASSIFY JSON EMAIL
========================================================= */

document
    .getElementById("email-form")
    .addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const subject =
                document
                    .getElementById("subject")
                    .value
                    .trim();

            const body =
                document
                    .getElementById("body")
                    .value
                    .trim();

            if (!body) {

                showFormStatus(
                    "Email body is required.",
                    "error"
                );

                return;
            }

            setClassifyLoading(true);

            showFormStatus(
                "Analyzing email...",
                ""
            );

            try {

                const response =
                    await fetch(
                        "/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                subject,
                                body
                            })
                        }
                    );

                const data =
                    await response.json();

                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Prediction failed"
                    );
                }

                const prediction =
                    String(
                        data.prediction
                    ).toLowerCase();

                showClassificationResult(
                    prediction
                );

                const target =
                    prediction === "spam"
                        ? "spam"
                        : "inbox";

                showFormStatus(

                    prediction === "spam"
                        ? "Email classified and moved to Spam / Quarantine."
                        : "Email classified and delivered to Inbox.",

                    "success"
                );

                await refreshDashboard({
                    target
                });

            } catch (error) {

                console.error(
                    "Prediction error:",
                    error
                );

                showFormStatus(
                    error.message ||
                    "Unable to classify email.",
                    "error"
                );

            } finally {

                setClassifyLoading(false);
            }
        }
    );


/* =========================================================
   UPLOAD EML
========================================================= */

document
    .getElementById("email-file")
    .addEventListener(
        "change",
        async function() {

            const file =
                this.files[0];

            if (!file) {
                return;
            }

            const formData =
                new FormData();

            formData.append(
                "file",
                file
            );

            showFormStatus(
                `Analyzing ${file.name}...`,
                ""
            );

            try {

                const response =
                    await fetch(
                        "/predict-file",
                        {
                            method: "POST",
                            body: formData
                        }
                    );

                const data =
                    await response.json();

                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "File prediction failed"
                    );
                }

                const prediction =
                    String(
                        data.prediction
                    ).toLowerCase();

                showClassificationResult(
                    prediction
                );

                const target =
                    prediction === "spam"
                        ? "spam"
                        : "inbox";

                showFormStatus(

                    prediction === "spam"
                        ? "Email classified and moved to Spam / Quarantine."
                        : "Email classified and delivered to Inbox.",

                    "success"
                );

                await refreshDashboard({
                    target
                });

            } catch (error) {

                console.error(
                    "File prediction error:",
                    error
                );

                showFormStatus(
                    error.message ||
                    "Unable to classify file.",
                    "error"
                );

            } finally {

                this.value = "";
            }
        }
    );


/* =========================================================
   SHOW CLASSIFICATION RESULT
========================================================= */

function showClassificationResult(
    prediction
) {

    const resultCard =
        document.getElementById(
            "classification-result"
        );

    const resultIcon =
        document.getElementById(
            "result-icon"
        );

    const resultLabel =
        document.getElementById(
            "result-label"
        );

    const resultMessage =
        document.getElementById(
            "result-message"
        );

    const targetButton =
        document.getElementById(
            "result-target-button"
        );

    resultCard.classList.remove(
        "hidden",
        "ham",
        "spam"
    );

    targetButton.classList.remove(
        "hidden"
    );

    if (prediction === "spam") {

        resultCard.classList.add(
            "spam"
        );

        resultIcon.textContent =
            "🚨";

        resultLabel.textContent =
            "SPAM DETECTED";

        resultMessage.textContent =
            "This email has been classified as spam and moved to quarantine.";

        targetButton.textContent =
            "View Spam →";

        targetButton.onclick =
            () => scrollToSection(
                "spam"
            );

    } else {

        resultCard.classList.add(
            "ham"
        );

        resultIcon.textContent =
            "✓";

        resultLabel.textContent =
            "HAM — SAFE";

        resultMessage.textContent =
            "This email has been classified as legitimate and delivered to the inbox.";

        targetButton.textContent =
            "View Inbox →";

        targetButton.onclick =
            () => scrollToSection(
                "inbox"
            );
    }
}


/* =========================================================
   CLEAR CLASSIFIER
========================================================= */

document
    .getElementById("clear-button")
    .addEventListener(
        "click",
        clearClassifier
    );


function clearClassifier() {

    document
        .getElementById("subject")
        .value = "";

    document
        .getElementById("body")
        .value = "";

    document
        .getElementById("email-file")
        .value = "";

    const resultCard =
        document.getElementById(
            "classification-result"
        );

    resultCard.classList.add(
        "hidden"
    );

    resultCard.classList.remove(
        "ham",
        "spam"
    );

    document
        .getElementById(
            "result-target-button"
        )
        .classList.add(
            "hidden"
        );

    showFormStatus(
        "Ready for a new email.",
        ""
    );

    document
        .getElementById("subject")
        .focus();
}


/* =========================================================
   NAVIGATION
========================================================= */

const navLinks =
    document.querySelectorAll(
        ".nav-link"
    );


navLinks.forEach(
    link => {

        link.addEventListener(
            "click",
            function(event) {

                event.preventDefault();

                const target =
                    document.getElementById(
                        this.dataset.section
                    );

                if (target) {

                    setActiveNav(
                        this.dataset.section
                    );

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }
            }
        );
    }
);


/* =========================================================
   SCROLL SPY
========================================================= */

const sectionElements =
    sections
        .map(
            id =>
                document.getElementById(id)
        )
        .filter(Boolean);


function updateActiveSection() {

    const scrollPosition =
        window.scrollY +
        150;

    let activeSection =
        "overview";

    sectionElements.forEach(
        section => {

            if (
                section.offsetTop <=
                scrollPosition
            ) {
                activeSection =
                    section.id;
            }
        }
    );

    setActiveNav(
        activeSection
    );
}


window.addEventListener(
    "scroll",
    updateActiveSection,
    {
        passive: true
    }
);


window.addEventListener(
    "resize",
    updateActiveSection
);


function setActiveNav(
    sectionId
) {

    navLinks.forEach(
        link => {

            link.classList.toggle(
                "active",
                link.dataset.section ===
                sectionId
            );
        }
    );
}


function scrollToSection(
    sectionId
) {

    const section =
        document.getElementById(
            sectionId
        );

    if (!section) {
        return;
    }

    setActiveNav(
        sectionId
    );

    section.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


/* =========================================================
   MANUAL REFRESH
========================================================= */

document
    .getElementById("refresh-button")
    .addEventListener(
        "click",
        async () => {

            await refreshDashboard();

        }
    );


/* =========================================================
   FORM HELPERS
========================================================= */

function setClassifyLoading(
    isLoading
) {

    const button =
        document.getElementById(
            "classify-button"
        );

    button.disabled =
        isLoading;

    button
        .querySelector("span")
        .textContent =
            isLoading
                ? "Analyzing..."
                : "Classify Email";
}


function showFormStatus(
    message,
    type = ""
) {

    const status =
        document.getElementById(
            "form-status"
        );

    status.textContent =
        message;

    status.classList.remove(
        "hidden",
        "error",
        "success"
    );

    if (type) {

        status.classList.add(
            type
        );
    }
}


/* =========================================================
   HTML / JS ESCAPING
========================================================= */

function escapeHtml(
    value
) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


function escapeJsString(
    value
) {

    return String(value)
        .replace(
            /\\/g,
            "\\\\"
        )
        .replace(
            /'/g,
            "\\'"
        )
        .replace(
            /\r/g,
            "\\r"
        )
        .replace(
            /\n/g,
            "\\n"
        );
}


/* =========================================================
   INITIAL LOAD
========================================================= */

refreshDashboard();

setTimeout(
    updateActiveSection,
    100
);