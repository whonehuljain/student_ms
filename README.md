# Student Management API

## Deployed base url: https://student-ms-api.onrender.com

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following:
```bash
MONGO_URI=your_mongodb_connection_string
```
4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### from Docker

Prerequisites: docker, docker-compose

1. Clone the repository
2. Create a `.env` file in the root directory with the following:
```bash
MONGO_URI=your_mongodb_connection_string
```
3. Start with docker-compose
```bash
docker-compose up
```

