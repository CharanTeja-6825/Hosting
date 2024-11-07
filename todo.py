from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=True)  # New description field
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form.get('description')  # Get description input
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        priority = request.form['priority']

        new_task = Todo(subject=subject, description=description, deadline=deadline, priority=priority)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))

    tasks = Todo.query.order_by(Todo.deadline).all()
    return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

