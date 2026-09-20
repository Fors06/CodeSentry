/* Отрисовка графика тренда технического долга через Chart.js. */

async function renderTechDebtChart() {
    const metrics = await api.getMetrics(30);
    const ctx = document.getElementById("techDebtChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: metrics.map((m) => m.date),
            datasets: [
                {
                    label: "Индекс техдолга",
                    data: metrics.map((m) => m.tech_debt_index),
                    borderColor: "#ff6b6b",
                    tension: 0.3,
                },
                {
                    label: "Средняя сложность",
                    data: metrics.map((m) => m.avg_complexity),
                    borderColor: "#6ea8fe",
                    tension: 0.3,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: "#e6e6e6" } } },
            scales: {
                x: { ticks: { color: "#8a8f9c" } },
                y: { ticks: { color: "#8a8f9c" } },
            },
        },
    });
}

renderTechDebtChart();
