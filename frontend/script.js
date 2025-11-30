async function analyzeTasks() {
    let rawInput = document.getElementById("taskInput").value;
    let strategy = document.getElementById("strategy").value;

    try {
        let tasks = JSON.parse(rawInput);

        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tasks: tasks,
                strategy: strategy
            })
        });

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        alert("Invalid JSON or server error!");
        console.log(error);
    }
}


function displayResults(tasks) {
    let container = document.getElementById("results");
    container.innerHTML = "";

    

    tasks.forEach(task => {
        let div = document.createElement("div");
        div.classList.add("task-card");

        // priority coloring
        if (task.score > 100) div.classList.add("high");
        else if (task.score > 70) div.classList.add("medium");
        else div.classList.add("low");

        div.innerHTML = `
            <h3>${task.title}</h3>
            <p><strong>Score:</strong> ${task.score}</p>
            <p><strong>Due Date:</strong> ${task.due_date}</p>
            <p><strong>Importance:</strong> ${task.importance}</p>
            <p><strong>Effort:</strong> ${task.estimated_hours} hrs</p>
        `;

        container.appendChild(div);
    });
}

async function suggestTasks() {
    let rawInput = document.getElementById("taskInput").value;

    try {
        let tasks = JSON.parse(rawInput);

        const response = await fetch("http://127.0.0.1:8000/api/tasks/suggest/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tasks: tasks })
        });

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        alert("Invalid JSON or server error!");
        console.log(error);
    }
}
