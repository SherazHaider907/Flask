from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import Task, User
from app.routes.auth import login_required

# Blueprint for all todo-related routes.
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@login_required
def index():
    """Show the main todo page with all tasks for the logged-in user."""
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.id.desc()).all()
    return render_template('tasks.html', tasks=tasks, user=user)


@tasks_bp.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    """Create a new task from the form submission."""
    title = request.form.get('title', '').strip()

    if not title:
        flash('Task title cannot be empty.', 'danger')
        return redirect(url_for('tasks.index'))

    user = db.session.get(User, session['user_id'])
    if user is None:
        abort(404)
    task = Task(title=title, user_id=user.id)
    db.session.add(task)
    db.session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    """Toggle the completed status of a task."""
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    flash('Task updated.', 'info')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task from the list."""
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'warning')
    return redirect(url_for('tasks.index'))
