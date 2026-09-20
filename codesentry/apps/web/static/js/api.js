/* Тонкие обёртки над fetch к локальному API (тот же localhost:8000). */
const api = {
    async getPrs() {
        const res = await fetch("/api/prs");
        return res.json();
    },
    async getPr(id) {
        const res = await fetch(`/api/prs/${id}`);
        return res.json();
    },
    async getFindings(prId) {
        const res = await fetch(`/api/findings/${prId}`);
        return res.json();
    },
    async getMetrics(lastN = 30) {
        const res = await fetch(`/api/metrics?last_n=${lastN}`);
        return res.json();
    },
    async ask(question, repo = null) {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, repo }),
        });
        return res.json();
    },
};
