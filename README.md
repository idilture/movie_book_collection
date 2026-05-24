Movie & Book Collection Manager is a multi-user Flask web application developed for the Software Engineering final project. The application allows users to create an account, sign in, and manage their personal collection of movies and books. After logging in, each user can add new items, view their own collection, edit item details, delete items, and filter the collection by type or status. Each collection item includes information such as title, type, creator, genre, status, rating, notes, and release year.

The project uses Flask, SQLite, raw SQL queries, sessions, and basic unit tests. User passwords are stored as hashed passwords, and each collection item is connected to the logged-in user through a user_id field. This ensures that users can only access their own data and cannot view, edit, or delete another user’s collection. The business logic, such as rating validation, release year validation, status/type validation, and average rating calculation is separated into logic.py and tested with Pytest.
User Stories
[US1] Add movie or book

As a user, I want to add a movie or book to my collection so that I can track what I watch or read.
Acceptance Criteria:
User can add title, type, genre, status, rating, review, and release year.
Title cannot be empty.
Type must be Movie or Book.
Rating must be between 1 and 5 if provided.
The item is saved with the logged-in user's user_id.

[US2] View personal collection

As a user, I want to view my own collection so that I can see my saved movies and books.
Acceptance Criteria:
User sees only their own items.
Other users items are not displayed.
Items are displayed on the dashboard.

[US3] Delete item

As a user, I want to delete an item so that I can remove it from my collection.
Acceptance Criteria:
User can delete only their own item.
Deleted item disappears from the dashboard.
Other users collections are not affected.

[US4] Edit item details

As a user, I want to edit an item so that I can keep my collection accurate.
Acceptance Criteria:
User can edit only their own item.
Invalid rating or year is not accepted.
Updated item information is saved in the database.