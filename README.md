# Aptilectual API
Aptitude Platform is a web application that allows users to attempt daily aptitude problems, track their performance, and compete on daily and monthly leaderboards.

## Features

- **User Registration and Login**: Users can register, login, and have a profile displaying their stats, including the number of questions attempted, correct answers, current streak, and highest streak.
- **Daily Problems**: Two problems go live daily, and users can attempt them.
- **Answer Submission**: Users submit answers, and the system checks if the answer is correct, updating stats.
- **Leaderboards**: Daily and monthly leaderboards based on user performance.
- **Past Problems**: Users can view past problems and see their answers and scores.
- **Session Management**: Session persistence for 30 days.
- **Admin Panel**: Admin interface for managing users, problems, and submissions.

## Installation

### Prerequisites

- Python 3.7+
- Django 3.0+
- Django REST Framework

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/aptitude-platform.git
    cd aptitude-platform
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

7. **Access the application**:

    Open your browser and go to `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication

- **Register**: `POST /api/register/`
  - Registers a new user.
  - **Fields**: `username`, `email`, `password`

- **Login**: `POST /api/login/`
  - Logs in a user.
  - **Fields**: `email`, `password`

### User

- **Profile**: `GET /api/profile/`
  - Fetches the user's profile and stats.
  - **Authentication**: Required

### Problems

- **Daily Problems**: `GET /api/problems/daily/`
  - Gets the two daily problems for the user (only between 5 PM and 9 PM).
  - **Authentication**: Required

- **Submit Answer**: `POST /api/submit_answer/`
  - Submits an answer to a problem.
  - **Fields**: `problem`, `selected_option`, `solution_image_url`
  - **Authentication**: Required

- **Past Problems**: `GET /api/problems/past/`
  - Gets the list of problems that have already been solved.
  - **Authentication**: Required

### Leaderboards

- **Daily Leaderboard**: `GET /api/leaderboard/daily/`
  - Gets the daily leaderboard.
  - **Authentication**: Required

- **Monthly Leaderboard**: `GET /api/leaderboard/monthly/`
  - Gets the monthly leaderboard.
  - **Authentication**: Required

## Models

### CustomUser

- **Fields**:
  - `email`: EmailField (unique)
  - `username`: CharField (unique)
  - `total_attempted`: IntegerField
  - `total_correct`: IntegerField
  - `current_streak`: IntegerField
  - `highest_streak`: IntegerField
  - `is_active`: BooleanField
  - `is_staff`: BooleanField
  - `date_joined`: DateTimeField
  - `first_position_count`: IntegerField
  - `second_position_count`: IntegerField
  - `third_position_count`: IntegerField

### Problem

- **Fields**:
  - `question`: TextField
  - `option1`: CharField
  - `option2`: CharField
  - `option3`: CharField
  - `option4`: CharField
  - `correct_option`: PositiveSmallIntegerField
  - `is_active`: BooleanField
  - `done`: BooleanField

### UserAnswer

- **Fields**:
  - `user`: ForeignKey to CustomUser
  - `problem`: ForeignKey to Problem
  - `selected_option`: IntegerField
  - `solution_image_url`: URLField
  - `time_solved`: DateTimeField
  - `is_correct`: BooleanField

### LeaderDaily

- **Fields**:
  - `show_leaderboard`: BooleanField

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
