from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Jacksonian Concept: Routing
@app.route("/")
def home():
    todo_list = Todo.query.all()
    # Jacksonian Concept: Templating
    return render_template("base.html", todo_list=todo_list)

# POST method: allows us to add new todos to the list 
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    # Jacksonian Concept: Session
    db.session.add(new_todo)
    db.session.commit() # Commits the current session
    # Jacksonian Concept: Redirects, allow us to go to a different url
    return redirect(url_for("home"))

# UPDATE method: allows us to update the status of existing todos
@app.route("/update/<int:todo_id>") # Jacksonian Concept: Building Links
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    # If complete, we want to set to incomplete
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# DELETE method: allows us to delete existing todos
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# Driver code 
if __name__ == "__main__":
    # Need to use this wrapper for proper server running
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)
