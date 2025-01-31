# BellsMCT Nexus

BellsMCT Nexus is a Django-based web application for a departmental website at Bells University Department of Mecatronics

## Features

- User authentication and authorization
- Resource management (Blogs, News)
- Events
- Activity tracking
- Reporting and analytics

## Requirements

- Python 3.x
- Django 3.x

## Tech Stack
| Technology      | Description                           |
|-----------------|---------------------------------------|
| Python          | Backend Programming language          |
| Django          | Web framework                         |
| MYSQL           | Development Database                  |
| HTML/CSS        | Frontend markup and styling           |
| JavaScript      | Frontend scripting                    |
| Bootstrap       | CSS framework for responsive design   |
| Git             | Version control system                |
| GitHub          | Repository hosting service            |
| Bunny.net       | Content Delivery Network (CDN)        |

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/theadeyemiolayinka/BellsMCT.git
    ```
2. Navigate to the project directory:
    ```bash
    cd BellsMCT
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Navigate to the server folder:
    ```bash
    cd server
    ```
6. Set up the database:
    ```bash
    python manage.py migrate
    ```
7. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
8. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:8000/`.
2. Log in with the superuser credentials you created.

### Using Docker

1. Build the Docker image:
    ```bash
    docker build -t bellsmct-nexus .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 bellsmct-nexus
    ```
3. Open your web browser and go to `http://127.0.0.1:8000/`.
4. Create and Log in with the superuser credentials as deacribed.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Description of changes"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

- [Adeyemi Olayinka](https://theadeyemiolayinka.com)
- Adekola Oluwasegun
- Onechojon Blessing
- Orji Daniel
- Odukoya Moyinoluwa