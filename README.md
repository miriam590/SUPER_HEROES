# Superheroes Database

## Description
This project is a simple Flask application that manages a database of superheroes and their powers. It allows users to seed the database with predefined heroes and powers and provides an API to retrieve the list of heroes.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone <git@github.com:miriam590/SUPER_HEROES.git>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Ensure you have SQLite installed.
   - The database will be created automatically when you run the seed script.

## Usage
1. Run the application:
   ```bash
   python app.py
   ```

2. Seed the database with heroes and powers:
   ```bash
   python seed.py
   ```

3. Access the API endpoint to retrieve heroes:
   - Open your web browser and navigate to `http://127.0.0.1:5000/heroes`.

## API Endpoints
- `GET /heroes`: Retrieves a list of all heroes in the database.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.


