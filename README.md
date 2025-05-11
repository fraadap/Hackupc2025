# The Perfect Reunion

## Inspiration

The idea for "The Perfect Reunion" came from the universal challenge of planning group trips. Coordinating travel with friends often involves endless back-and-forth messages, conflicting preferences, and difficulty finding a destination that truly satisfies everyone. We wanted to simplify this process, making group travel planning collaborative and enjoyable. The goal was to create a tool that helps friends discover destinations they'll collectively love, based on shared interests and priorities, taking the stress out of finding that "perfect reunion" spot.

## What we Learned

This project was a great learning experience, particularly in:

*   **Full-Stack Development:** Integrating a Python (FastAPI) backend with a React/TypeScript frontend provided hands-on experience with building a complete web application.
*   **Database Design & ORM:** Designing the SQLite schema and using SQLAlchemy for data modeling and interaction reinforced database fundamentals.
*   **API Design:** Creating a RESTful API to handle communication between the frontend and backend, including authentication and data retrieval.
*   **Recommendation Systems:** Implementing a basic content-based recommendation algorithm using cosine similarity to match group preferences with city features.
*   **Data Simulation:** Learning techniques to generate realistic-looking data for development and testing when real-world data or external APIs are not available.
*   **Frontend State Management:** Utilizing React Context API for managing user authentication state across the application.
*   **Troubleshooting & Debugging:** Overcoming various challenges, from dependency conflicts (`npm install --legacy-peer-deps` became a good friend!) to database integrity errors and environment-specific execution issues.

## How we Built It

1.  **Conceptualization & Planning:** Defined the core problem and sketched out the initial features: user profiles based on preferences, city data, group formation, recommendation logic, and a voting mechanism.
2.  **Technology Stack Selection:** Chose Python/FastAPI for the backend due to its speed and ease of use, SQLite for a simple database solution suitable for a hackathon, and initially Vue.js for the frontend. Later switched to React/TypeScript with Material UI for a more modern UI/UX and type safety.
3.  **Backend Development:**
    *   Set up the FastAPI project structure.
    *   Defined the database schema and created `create_db.py`.
    *   Implemented data generation scripts (`generate_data.py`, `generate_data_flights_groups.py`) to populate the database with simulated cities, users, groups, flights, and votes.
    *   Developed SQLAlchemy models corresponding to the database tables.
    *   Built API endpoints for user authentication (registration, login), city swiping, user preference updates, group management (creation, joining, viewing), flight searching, and voting.
    *   Implemented helper functions for password hashing, JWT authentication, database sessions, and the core recommendation logic (calculating user vectors, group vectors, and city similarities).
    *   Created an initialization script (`init_db.py`) to set up and populate the database.
4.  **Frontend Development:**
    *   Set up the React/TypeScript project using Create React App.
    *   Installed necessary dependencies (MUI, Axios, React Router).
    *   Defined TypeScript types (`types/index.ts`) to match the backend API models.
    *   Created an API service (`services/api.ts`) to interact with the backend endpoints.
    *   Implemented an `AuthContext` for managing login state.
    *   Built reusable components (`CityCard`, `SwipeableCity`, `Navbar`).
    *   Developed pages for different views (`Login`, `Register`, `Onboarding`, `Dashboard`, `Groups`, `GroupDetail`).
    *   Set up client-side routing using React Router.
    *   Styled components using Material UI.
5.  **Integration & Testing:** Connected the frontend to the backend API, tested user flows (registration, login, swiping, group interactions), and debugged issues across the stack.

## Challenges Faced

*   **Frontend Dependency Issues:** Encountered several dependency conflicts, particularly with React versions and Material UI, requiring troubleshooting and the use of `--legacy-peer-deps`.
*   **Data Generation Complexity:** Generating realistic and interconnected data (especially user votes reflecting preferences and flights matching criteria) required careful scripting and debugging, particularly handling potential database constraint violations.
*   **Environment Differences:** Running Python scripts sometimes behaved differently depending on the terminal environment or Python interpreter used, necessitating specific commands (like using `py` on Windows).
*   **Scope Management:** Balancing the desired features with the time constraints of a hackathon meant focusing on core functionality.
*   **Debugging Across Stacks:** Identifying whether bugs originated in the frontend, backend, API communication, or database required systematic testing and logging.
*   **UI Refinement:** While basic functionality is in place, achieving a polished and fully responsive UI with libraries like Material UI takes significant time.

Overall, "The Perfect Reunion" was a challenging but rewarding project that brought together various aspects of web development to solve a common real-world problem. 

## Screenshots 📷
![swipe](https://github.com/user-attachments/assets/eb408cba-93f0-4caf-813f-9cc25b7cc47c)
![dashboard](https://github.com/user-attachments/assets/0a8b1511-1da5-484f-ab9d-511ce605085d)
![groups](https://github.com/user-attachments/assets/f0629727-1d1c-4da2-bf4f-907ec769ed9c)
![search](https://github.com/user-attachments/assets/222883b7-bd87-4d6f-87a1-79df4b546f86)
![deatails](https://github.com/user-attachments/assets/7619366a-0543-47f2-a740-7e1d90f77a1d)



