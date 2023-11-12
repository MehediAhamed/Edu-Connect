// app.js
document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayTasks();
});

function fetchAndDisplayTasks() {
    const sortOption = document.getElementById('sortOption').value;
    const category = document.getElementById('categoryFilter').value;
    const status = document.getElementById('statusFilter').value;
    const search = document.getElementById('searchInput').value;

    fetch(`/tasks?sortBy=${sortOption}&category=${category}&status=${status}&search=${search}`)
        .then(response => response.json())
        .then(tasks => displayTasks(tasks))
        .catch(error => console.error(error));
}

function displayTasks(tasks) {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(task => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${task.title}</td>
            <td>${task.description}</td>
            <td>${task.dueDate}</td>
            <td>${task.priority}</td>
            <td>${task.category}</td>
            <td>${task.status}</td>
            <td>
                <button onclick="showTaskDetails('${task._id}')">Details</button>
                <button onclick="editTask('${task._id}')">Edit</button>
                <button onclick="markTaskCompleted('${task._id}')">Complete</button>
                <button onclick="deleteTask('${task._id}')">Delete</button>
            </td>
        `;
        taskList.appendChild(row);
    });
}

function showTaskDetails(taskId) {
    fetch(`/tasks/${taskId}`)
        .then(response => response.json())
        .then(task => {
            const taskDetailsContent = document.getElementById('taskDetailsContent');
            taskDetailsContent.innerHTML = `
                <p><strong>Title:</strong> ${task.title}</p>
                <p><strong>Description:</strong> ${task.description}</p>
                <p><strong>Due Date:</strong> ${task.dueDate}</p>
                <p><strong>Priority:</strong> ${task.priority}</p>
                <p><strong>Category:</strong> ${task.category}</p>
                <p><strong>Status:</strong> ${task.status}</p>
                <button onclick="editTask('${task._id}')">Edit</button>
                <button onclick="markTaskCompleted('${task._id}')">Complete</button>
                <button onclick="deleteTask('${task._id}')">Delete</button>
            `;
            openTaskDetailsModal();
        })
        .catch(error => console.error(error));
}

function openTaskDetailsModal() {
    const taskDetailsModal = document.getElementById('taskDetailsModal');
    taskDetailsModal.style.display = 'block';
}

function closeTaskDetailsModal() {
    const taskDetailsModal = document.getElementById('taskDetailsModal');
    taskDetailsModal.style.display = 'none';
}

function markTaskCompleted(taskId) {
    fetch(`/tasks/${taskId}/complete`, { method: 'PUT' })
        .then(response => {
            if (response.ok) {
                // Task marked as completed successfully
                fetchAndDisplayTasks();
            } else {
                console.error('Failed to mark task as completed');
            }
        })
        .catch(error => console.error(error));
}

function deleteTask(taskId) {
    fetch(`/tasks/${taskId}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                // Task deleted successfully
                fetchAndDisplayTasks();
                closeTaskDetailsModal();
            } else {
                console.error('Failed to delete task');
            }
        })
        .catch(error => console.error(error));
}

let currentTaskId; // Declare a global variable to store the taskId

function editTask(taskId) {
    fetch(`/tasks/${taskId}`)
        .then(response => response.json())
        .then(task => {
            currentTaskId = taskId; // Store the taskId in the global variable
            document.getElementById('editTitle').value = task.title;
            document.getElementById('editDescription').value = task.description;
            document.getElementById('editDueDate').value = task.dueDate;
            document.getElementById('editPriority').value = task.priority;
            document.getElementById('editCategory').value = task.category;

            openEditModal();
        })
        .catch(error => console.error(error));
}


function openEditModal() {
    const editModal = document.getElementById('editModal');
    editModal.style.display = 'block';
}

function closeEditModal() {
    const editModal = document.getElementById('editModal');
    editModal.style.display = 'none';
}

function submitEditForm() {
    const title = document.getElementById('editTitle').value;
const description = document.getElementById('editDescription').value;
const dueDate = document.getElementById('editDueDate').value;
const priority = document.getElementById('editPriority').value;
const category = document.getElementById('editCategory').value;


    console.log(title, description, dueDate, priority, category);

    fetch(`/tasks/${currentTaskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            description: description,
            dueDate: dueDate,
            priority: priority,
            category: category,
        }),
    })
    
        .then(response => {
            if (response.ok) {
                console.log("test :" + description);
                return response.json();
            } else {
                throw new Error('Failed to update task');
            }
        })
        .then(updatedTask => {
            console.log('Task updated successfully:', updatedTask);
            fetchAndDisplayTasks();
            closeEditModal();
        })
        .catch(error => console.error(error));
}


