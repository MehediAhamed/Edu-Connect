const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

mongoose
    .connect("mongodb+srv://radibbk:weblabparina@cluster0.bvqap2y.mongodb.net/?retryWrites=true&w=majority")
    .then(() => { console.log('Connection successful'); })
    .catch((err) => console.log(err));

const taskSchema = new mongoose.Schema({
    title: String,
    description: String,
    dueDate: Date,
    priority: String,
    category: String,
    status: { type: String, default: 'pending' }, // default status
});

const Task = mongoose.model('Task', taskSchema);

app.post('/tasks/create', async (req, res) => {
    try {
        const newTask = new Task({
            title: req.body.title,
            description: req.body.description,
            dueDate: req.body.dueDate,
            priority: req.body.priority,
            category: req.body.category,
        });

        await newTask.save();
        console.log("Data inserted successfully");
        res.redirect('/');
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/tasks', async (req, res) => {
    try {
        let sortQuery = {};

        if (req.query.sortBy) {
            if (req.query.sortBy === 'priority') {
                sortQuery.priority = 1;
            } else if (req.query.sortBy === 'dueDate') {
                sortQuery.dueDate = 1;
            }
        }

        let filterQuery = {};

        if (req.query.category) {
            filterQuery.category = req.query.category;
        }

        if (req.query.status) {
            filterQuery.status = req.query.status;
        }

        if (req.query.search) {
            filterQuery.$or = [
                { title: { $regex: new RegExp(req.query.search, 'i') } },
                { description: { $regex: new RegExp(req.query.search, 'i') } },
            ];
        }

        const tasks = await Task.find(filterQuery).sort(sortQuery);

        console.log("Tasks are retrieved from the database");
        res.json(tasks);
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/tasks/:taskId', async (req, res) => {
    try {
        const taskId = req.params.taskId;
        const task = await Task.findById(taskId);

        if (!task) {
            return res.status(404).send('Task not found');
        }

        res.json(task);
        console.log("item retrieved");
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.put('/tasks/:taskId', async (req, res) => {
    try {
        const taskId = req.params.taskId;
        const updatedTask = {
            title: req.body.title,
            description: req.body.description,
            dueDate: req.body.dueDate,
            priority: req.body.priority,
            category: req.body.category,
        };

        console.log('Updating task with ID:', taskId);
        console.log('Updated task data:', updatedTask);

        const task = await Task.findByIdAndUpdate(taskId, updatedTask, { new: true });

        if (!task) {
            console.log('Task not found');
            return res.status(404).send('Task not found');
        }

        console.log('Task updated successfully');
        res.json(task);
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});


app.put('/tasks/:taskId/complete', async (req, res) => {
    try {
        const taskId = req.params.taskId;

        const task = await Task.findByIdAndUpdate(taskId, { status: 'completed' }, { new: true });

        if (!task) {
            return res.status(404).send('Task not found');
        }

        res.json(task);
        console.log("item completed");
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});

app.delete('/tasks/:taskId', async (req, res) => {
    try {
        const taskId = req.params.taskId;
        const deletedTask = await Task.findByIdAndDelete(taskId);

        if (!deletedTask) {
            // If the task with the specified ID is not found
            return res.status(404).json({ error: 'Task not found' });
        }

        console.log("Task deleted successfully");
        res.json({ message: 'Task deleted successfully' });
    } catch (err) {
        console.error(err);
        res.status(500).send('Internal Server Error');
    }
});


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/tasklist', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'tasklist.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
