
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"

db = SQLAlchemy(app)


# Job Application table
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    status = db.Column(db.String(30))


# Home page
@app.route("/")
def home():
    jobs = Job.query.all()
    return render_template("index.html", jobs=jobs)


# Add a job
@app.route("/add", methods=["POST"])
def add_job():

    company = request.form["company"]
    position = request.form["position"]
    status = request.form["status"]

    new_job = Job(
        company=company,
        position=position,
        status=status
    )

    db.session.add(new_job)
    db.session.commit()

    return redirect("/")


# Delete a job
@app.route("/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):

    job = db.session.get(Job, job_id)

    if job:
        db.session.delete(job)
        db.session.commit()

    return redirect("/")


# Create database
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
