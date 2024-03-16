# Team Software Project Starter Template - Flask

**InkVue Blog Application**
InkVue is a simple blog application built using Flask, Prisma Database, HTML templates, Python files for routing, and JavaScript for interactivity. It allows users to perform CRUD (Create, Read, Update, Delete) operations on tasks.

**Features**
-Create, Read, Update, and Delete tasks: Easily manage tasks with comprehensive CRUD functionality.
-Simple and intuitive user interface: Designed for ease of use, ensuring a smooth user experience.
-Prisma Database integration: Efficient data management powered by Prisma.
-Flask-based backend: Utilizes Flask for server-side routing and handling requests.
-HTML templates: Clear and customizable templates for rendering pages.
-Enhanced interactivity: JavaScript enhances user interactivity and experience.
## Installation

1. Clone the repository:
```bash
git clone git@github.com:kiboschool/tsp-flask-starter-template.git

cd tsp-flask-starter-template

```
2. Setup and activate your virtual environment:

`python3 -m venv .venv`

`source .venv/bin/activate`

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create and seed the database

Run the following command to create your SQLite database file. This also creates the `User` and `Post` tables that are
defined in [`prisma/schema.prisma`](./prisma/schema.prisma):

```bash
prisma db push
```

Seed the database by running the `./prisma/seed.py` file

```bash
python3 ./prisma/seed.py
```

**Access the application:**

Navigate to http://localhost:5000 in your browser.

**Future Development**
InkVue is designed with future development in mind:

-Scalability: The application architecture is modular and scalable, allowing for easy expansion.
-Customization: HTML templates and CSS stylesheets can be easily customized to match specific requirements.
-Additional Features: Consider adding features such as user authentication, task categorization, share, comments and liking of a post
-Performance Optimization: Continuously optimize code and database queries for improved performance.

**Project Organization**
.venv folder
app folder: Contains Flask application setup, routing, and main logic.
templates floder: Directory for HTML templates.
static/: Contains static files such as CSS, JavaScript, and images.
requirements.txt: Lists project dependencies for easy installation

**Acknowledgements**
InkVue was made possible thanks to the following technologies and libraries:

Flask: A micro web framework for Python.
Prisma: Modern Database Access for TypeScript & Node.js.

**Contact**
For any inquiries or issues regarding InkVue, feel free to contact the project maintainer at emmanuel.usen@kibo.school

**Deployed Link:**
https://ink-vue-test.onrender.com/

**TeamGreatCodez**
Princewill Onyekah - https://github.com/princeonyekah
Emmanuel Usen - https://github.com/DauntlessUs
Daniel Apolola - https://github.com/DannyBaine-Entity
Destiny Williams - https://github.com/DESTINY16-debug