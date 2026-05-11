from sqlite3 import IntegrityError

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db_connection, init_db
from logic import calculate_average_rating, count_items_by_status, count_items_by_type
from logic import validate_rating, validate_year

app = Flask(__name__)
app.secret_key = "temporary-secret-key"

TYPE_OPTIONS = ["Movie", "Book"]
STATUS_OPTIONS = ["Plan to Start", "In Progress", "Completed"]


def login_required(route_function):
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("signin"))
        return route_function(*args, **kwargs)

    wrapper.__name__ = route_function.__name__
    return wrapper


@app.route("/")
@login_required
def home():
    selected_type = request.args.get("type", "")
    selected_status = request.args.get("status", "")

    query = "SELECT * FROM collection_items WHERE user_id = ?"
    parameters = [session["user_id"]]

    if selected_type != "":
        query += " AND item_type = ?"
        parameters.append(selected_type)

    if selected_status != "":
        query += " AND status = ?"
        parameters.append(selected_status)

    query += " ORDER BY id DESC"

    connection = get_db_connection()
    items = connection.execute(query, parameters).fetchall()
    all_items = connection.execute(
        "SELECT * FROM collection_items WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    connection.close()

    movie_count = count_items_by_type(all_items, "Movie")
    book_count = count_items_by_type(all_items, "Book")
    completed_count = count_items_by_status(all_items, "Completed")
    average_rating = calculate_average_rating(all_items)

    return render_template(
        "dashboard.html",
        items=items,
        type_options=TYPE_OPTIONS,
        status_options=STATUS_OPTIONS,
        selected_type=selected_type,
        selected_status=selected_status,
        total_count=len(all_items),
        movie_count=movie_count,
        book_count=book_count,
        completed_count=completed_count,
        average_rating=average_rating
    )


@app.route("/init-db")
def initialize_database():
    init_db()
    return "Database initialized successfully."


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if username == "" or password == "":
            return render_template("signup.html", error="Username and password are required.")

        password_hash = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            connection.commit()
        except IntegrityError:
            connection.close()
            return render_template("signup.html", error="This username is already taken.")

        connection.close()

        return redirect(url_for("signin"))

    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        connection = get_db_connection()
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        connection.close()

        if user is None:
            return render_template("signin.html", error="Invalid username or password.")

        if not check_password_hash(user["password_hash"], password):
            return render_template("signin.html", error="Invalid username or password.")

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("home"))

    return render_template("signin.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("signin"))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        title = request.form["title"].strip()
        item_type = request.form["item_type"]
        creator = request.form["creator"].strip()
        genre = request.form["genre"].strip()
        status = request.form["status"]
        rating = request.form["rating"]
        notes = request.form["notes"].strip()
        release_year = request.form["release_year"]

        error = validate_item_form(title, item_type, status, rating, release_year)
        if error is not None:
            return render_template(
                "add_item.html",
                error=error,
                type_options=TYPE_OPTIONS,
                status_options=STATUS_OPTIONS
            )

        rating = convert_empty_to_none(rating)
        release_year = convert_empty_to_none(release_year)

        connection = get_db_connection()
        connection.execute(
            """INSERT INTO collection_items
            (user_id, title, item_type, creator, genre, status, rating, notes, release_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (session["user_id"], title, item_type, creator, genre, status, rating, notes, release_year)
        )
        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    return render_template(
        "add_item.html",
        type_options=TYPE_OPTIONS,
        status_options=STATUS_OPTIONS
    )


@app.route("/read/<int:item_id>")
@login_required
def read_item(item_id):
    connection = get_db_connection()
    item = connection.execute(
        "SELECT * FROM collection_items WHERE id = ? AND user_id = ?",
        (item_id, session["user_id"])
    ).fetchone()
    connection.close()

    if item is None:
        return "item not found"

    return render_template("read_item.html", item=item)


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    connection = get_db_connection()
    item = connection.execute(
        "SELECT * FROM collection_items WHERE id = ? AND user_id = ?",
        (item_id, session["user_id"])
    ).fetchone()

    if item is None:
        connection.close()
        return "item not found"

    if request.method == "POST":
        title = request.form["title"].strip()
        item_type = request.form["item_type"]
        creator = request.form["creator"].strip()
        genre = request.form["genre"].strip()
        status = request.form["status"]
        rating = request.form["rating"]
        notes = request.form["notes"].strip()
        release_year = request.form["release_year"]

        error = validate_item_form(title, item_type, status, rating, release_year)
        if error is not None:
            connection.close()
            return render_template(
                "edit_item.html",
                item=item,
                error=error,
                type_options=TYPE_OPTIONS,
                status_options=STATUS_OPTIONS
            )

        rating = convert_empty_to_none(rating)
        release_year = convert_empty_to_none(release_year)

        connection.execute(
            """UPDATE collection_items
            SET title = ?, item_type = ?, creator = ?, genre = ?, status = ?,
                rating = ?, notes = ?, release_year = ?
            WHERE id = ? AND user_id = ?""",
            (title, item_type, creator, genre, status, rating, notes, release_year, item_id, session["user_id"])
        )
        connection.commit()
        connection.close()

        return redirect(url_for("read_item", item_id=item_id))

    connection.close()
    return render_template(
        "edit_item.html",
        item=item,
        type_options=TYPE_OPTIONS,
        status_options=STATUS_OPTIONS
    )


@app.route("/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    connection = get_db_connection()
    connection.execute(
        "DELETE FROM collection_items WHERE id = ? AND user_id = ?",
        (item_id, session["user_id"])
    )
    connection.commit()
    connection.close()

    return redirect(url_for("home"))


def validate_item_form(title, item_type, status, rating, release_year):
    if title == "":
        return "Title is required."

    if item_type not in TYPE_OPTIONS:
        return "Type is not valid."

    if status not in STATUS_OPTIONS:
        return "Status is not valid."

    if not validate_rating(rating):
        return "Rating must be between 1 and 5."

    if not validate_year(release_year):
        return "Year is not valid."

    return None


def convert_empty_to_none(value):
    if value is None or value == "":
        return None

    return value


if __name__ == "__main__":
    app.run(debug=True)
