# Fast Api Post Task

A brief description of what this project does and who it's for.

## Installation 

Install project with pip

```bash 
  git clone https://github.com/javadsalman/fastapi-task.git
  cd fastapi-task
  pip install -r requirements.txt
```
Create `.env` file and fill it according to .env.example to setup database connection

## Running

To run project, run the following command

```bash
uvicorn src.main:app --reload
```

## API Reference

#### Get all posts

```http
  GET /posts
```

#### Add post

```http
  POST /posts
```

#### Delete post

```http
  DELETE /posts/{id}
```

#### Sign Up

```http
  POST /sugnup
```

#### Login

```http
  POST /login
```

## Authors

- [@javadsalman](https://www.github.com/javadsalman)

## License

[MIT](https://choosealicense.com/licenses/mit/)