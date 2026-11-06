
import { useMemo, useState } from "react";
import "./App.css";

type Priority = "High" | "Medium" | "Low";
type Status = "Pending" | "Completed";

interface Task {
  id: number;
  title: string;
  priority: Priority;
  status: Status;
}

const initialTasks: Task[] = [
  { id: 1, title: "Complete TaskPilot frontend", priority: "High", status: "Pending" },
  { id: 2, title: "Review MCP architecture", priority: "High", status: "Pending" },
  { id: 3, title: "Prepare project documentation", priority: "Medium", status: "Pending" },
  { id: 4, title: "Test LangChain agent", priority: "Medium", status: "Completed" },
  { id: 5, title: "Explore TypeScript", priority: "Low", status: "Completed" },
];

function App() {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");
  const [showForm, setShowForm] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newPriority, setNewPriority] = useState<Priority>("Medium");

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(
    (task) => task.status === "Completed"
  ).length;
  const pendingTasks = totalTasks - completedTasks;

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) => {
      const matchesSearch = task.title
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesFilter =
        filter === "All" || task.status === filter;

      return matchesSearch && matchesFilter;
    });
  }, [tasks, search, filter]);

  function addTask(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!newTitle.trim()) return;

    const task: Task = {
      id: Date.now(),
      title: newTitle.trim(),
      priority: newPriority,
      status: "Pending",
    };

    setTasks((previous) => [task, ...previous]);
    setNewTitle("");
    setNewPriority("Medium");
    setShowForm(false);
  }

  function toggleTask(id: number) {
    setTasks((previous) =>
      previous.map((task) =>
        task.id === id
          ? {
              ...task,
              status:
                task.status === "Pending" ? "Completed" : "Pending",
            }
          : task
      )
    );
  }

  function deleteTask(id: number) {
    setTasks((previous) =>
      previous.filter((task) => task.id !== id)
    );
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✦</div>
          <span>TaskPilot</span>
        </div>

        <div className="nav-section">
          <p className="nav-label">WORKSPACE</p>

          <button className="nav-item active">
            <span>▦</span> Dashboard
          </button>

          <button className="nav-item" onClick={() => setFilter("All")}>
            <span>☷</span> All Tasks
          </button>

          <button className="nav-item" onClick={() => setFilter("Pending")}>
            <span>◷</span> Pending
          </button>

          <button className="nav-item" onClick={() => setFilter("Completed")}>
            <span>✓</span> Completed
          </button>
        </div>

        <div className="sidebar-bottom">
          <div className="ai-status">
            <span className="status-dot" />
            AI Assistant
            <span className="online-label">Ready</span>
          </div>
          <p className="sidebar-footer">TaskPilot v1.0</p>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="breadcrumb">Workspace / Dashboard</p>
            <h1>Dashboard</h1>
          </div>

          <div className="profile">
            <div className="avatar">U</div>
            <div>
              <strong>My Workspace</strong>
              <p>Personal productivity</p>
            </div>
          </div>
        </header>

        <section className="welcome-section">
          <div>
            <p className="eyebrow">YOUR PRODUCTIVITY SPACE</p>
            <h2>Welcome back! 👋</h2>
            <p>Let's make today productive. What would you like to accomplish?</p>
          </div>

          <button
            className="primary-button"
            onClick={() => setShowForm(!showForm)}
          >
            + Add New Task
          </button>
        </section>

        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon purple">▦</div>
            <p>Total Tasks</p>
            <h3>{totalTasks}</h3>
            <span>All your tasks</span>
          </div>

          <div className="stat-card">
            <div className="stat-icon orange">◷</div>
            <p>Pending Tasks</p>
            <h3>{pendingTasks}</h3>
            <span>Waiting to be completed</span>
          </div>

          <div className="stat-card">
            <div className="stat-icon green">✓</div>
            <p>Completed Tasks</p>
            <h3>{completedTasks}</h3>
            <span>Successfully finished</span>
          </div>

          <div className="stat-card">
            <div className="stat-icon blue">↗</div>
            <p>Completion Rate</p>
            <h3>
              {totalTasks === 0
                ? 0
                : Math.round((completedTasks / totalTasks) * 100)}%
            </h3>
            <span>Overall progress</span>
          </div>
        </section>

        {showForm && (
          <section className="form-card">
            <h3>Create a new task</h3>

            <form onSubmit={addTask}>
              <input
                type="text"
                placeholder="Enter task title..."
                value={newTitle}
                onChange={(event) => setNewTitle(event.target.value)}
                autoFocus
              />

              <select
                value={newPriority}
                onChange={(event) =>
                  setNewPriority(event.target.value as Priority)
                }
              >
                <option value="High">High Priority</option>
                <option value="Medium">Medium Priority</option>
                <option value="Low">Low Priority</option>
              </select>

              <button className="primary-button" type="submit">
                Create Task
              </button>

              <button
                className="secondary-button"
                type="button"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </button>
            </form>
          </section>
        )}

        <section className="tasks-section">
          <div className="section-heading">
            <div>
              <h2>My Tasks</h2>
              <p>Manage and track your daily activities.</p>
            </div>
          </div>

          <div className="task-controls">
            <input
              type="search"
              placeholder="Search tasks..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />

            <select
              value={filter}
              onChange={(event) => setFilter(event.target.value)}
            >
              <option value="All">All Tasks</option>
              <option value="Pending">Pending</option>
              <option value="Completed">Completed</option>
            </select>
          </div>

          <div className="task-list">
            {filteredTasks.length === 0 ? (
              <div className="empty-state">
                <span>☷</span>
                <h3>No tasks found</h3>
                <p>Try another search or create a new task.</p>
              </div>
            ) : (
              filteredTasks.map((task) => (
                <div className="task-row" key={task.id}>
                  <button
                    className={`task-check ${
                      task.status === "Completed" ? "checked" : ""
                    }`}
                    onClick={() => toggleTask(task.id)}
                    aria-label={`Toggle ${task.title}`}
                  >
                    {task.status === "Completed" ? "✓" : ""}
                  </button>

                  <div className="task-info">
                    <strong
                      className={
                        task.status === "Completed" ? "completed-title" : ""
                      }
                    >
                      {task.title}
                    </strong>
                    <span>Task #{task.id}</span>
                  </div>

                  <span className={`priority ${task.priority.toLowerCase()}`}>
                    {task.priority}
                  </span>

                  <span
                    className={`task-status ${task.status.toLowerCase()}`}
                  >
                    {task.status}
                  </span>

                  <button
                    className="delete-button"
                    onClick={() => deleteTask(task.id)}
                    aria-label={`Delete ${task.title}`}
                  >
                    ×
                  </button>
                </div>
              ))
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
