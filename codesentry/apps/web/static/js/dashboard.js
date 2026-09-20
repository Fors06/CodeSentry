/* Логика главной страницы дашборда. */

async function loadPrsTable() {
    const prs = await api.getPrs();
    const tbody = document.querySelector("#prsTable tbody");
    tbody.innerHTML = prs
        .map(
            (pr) => `<tr onclick="window.location.href='/pr_detail.html?id=${pr.id}'">
                <td>${pr.title}</td>
                <td>${pr.author}</td>
                <td>${pr.repo}</td>
                <td>${pr.status}</td>
            </tr>`
        )
        .join("");
}

document.getElementById("askForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = document.getElementById("questionInput").value.trim();
    if (!question) return;

    const answerBox = document.getElementById("askAnswer");
    answerBox.textContent = "Думаю...";

    const response = await api.ask(question);
    answerBox.textContent = response.answer;
});

loadPrsTable();
