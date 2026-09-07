document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("task-form");
    const taskTitle = document.getElementById("task-title");
    const taskPriority = document.getElementById("task-priority");
    const taskDueDate = document.getElementById("task-due-date");
    const taskList = document.getElementById("task-list");
    const taskCount = document.getElementById("task-count");

    let tasks = JSON.parse(localStorage.getItem("taskflow_tasks")) || [];

    function saveAndRender() {
        localStorage.setItem("taskflow_tasks", JSON.stringify(tasks));
        renderTasks();
    }

    function renderTasks() {
        taskList.innerHTML = "";
        taskCount.textContent = `${tasks.length} task${tasks.length === 1 ? '' : 's'}`;

        if (tasks.length === 0) {
            taskList.innerHTML = `<li style="text-align:center; color:var(--text-muted); padding:1rem;">No tasks found. Add one above!</li>`;
            return;
        }

        tasks.forEach((task) => {
            const li = document.createElement("li");
            li.className = `task-item ${task.completed ? 'completed' : ''}`;

            li.innerHTML = `
                <div class="task-left">
                    <input type="checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}" class="toggle-check">
                    <div class="task-info">
                        <span class="task-title-text">${escapeHtml(task.title)}</span>
                        <div class="task-meta">
                            <span class="priority-tag priority-${task.priority}">${task.priority}</span>
                            ${task.dueDate ? `<span>Due: ${task.dueDate}</span>` : ''}
                        </div>
                    </div>
                </div>
                <button class="btn-delete" data-id="${task.id}">&times;</button>
            `;

            taskList.appendChild(li);
        });
    }

    taskForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const title = taskTitle.value.trim();
        if (!title) return;

        const newTask = {
            id: Date.now(),
            title: title,
            priority: taskPriority.value,
            dueDate: taskDueDate.value,
            completed: false
        };

        tasks.push(newTask);
        saveAndRender();

        taskTitle.value = "";
        taskDueDate.value = "";
        taskPriority.value = "medium";
    });

    taskList.addEventListener("click", (e) => {
        if (e.target.classList.contains("toggle-check")) {
            const id = Number(e.target.dataset.id);
            const task = tasks.find(t => t.id === id);
            if (task) {
                task.completed = e.target.checked;
                saveAndRender();
            }
        }

        if (e.target.classList.contains("btn-delete")) {
            const id = Number(e.target.dataset.id);
            tasks = tasks.filter(t => t.id !== id);
            saveAndRender();
        }
    });

    function escapeHtml(str) {
        return str.replace(/[&<>"']/g, (m) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
        })[m]);
    }

    renderTasks();
});
