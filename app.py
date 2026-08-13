from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Todo table
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=False)


# Home page
@app.route('/')
def index():
    todo_list = Todo.query.all()

    return render_template(
        "index.html",
        todos=todo_list
    )


# Add Todo
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("task_name")

    if name:
        new_task = Todo(
            task_name=name,
            status=False
        )

        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for("index"))


# Update Todo status
@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)

    if todo:
        todo.status = not todo.status
        db.session.commit()

    return redirect(url_for("index"))


# Delete Todo
@app.route('/dele/<int:todo_id>')
def dele(todo_id):
    todo = Todo.query.get(todo_id)

    if todo:
        db.session.delete(todo)
        db.session.commit()

    return redirect(url_for("index"))


# Run application
if __name__ == '__main__':


    app.run(debug=True)