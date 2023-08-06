# API Documentation

## Introduction

Propylon Document Manager is a RESTful application designed to streamline file management processes. With its 
intuitive interface, users can effortlessly upload, store, and retrieve files on the server. 
The application also empowers users by enabling the maintenance of multiple versions for each file, ensuring a 
comprehensive history of document updates. Propylon Document Manager simplifies document management while promoting 
organized collaboration and efficient file tracking."


## Authentication

To access the features of Propylon Document Manager, you'll need an authentication token. You can obtain this token by 
making a `POST` request with usrname and password to the `/auth-token` endpoint of our API and include the `Authorization` header with the 
generated token. This token serves as your key to unlocking the APIs provided by Propylon Document Manager.

#### Sample Request
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

#### Sample Response
```json
{
"token": "your_generated_token"
}
```


[//]: # (## Base URL)

[//]: # ()
[//]: # (The base URL for all API endpoints is `https://api.example.com`.)

## Endpoints

### Upload File

- **HTTP Method:** `POST`
- **Endpoint:** `/file-manager/file-upload`
- **Parameters:**
    - `source-path` (required): Path of the file on the server
    - `version` (required): Version of the file
- **Request:**

  | Field        | Value                               |
  |-------------------------------------|-----------------------------|
  | file-content | Base64 encoded file content         |
  | file-type    | Type of the file                    |
  | file-name    | Name of the file                    |
  | target-path            | Path to store the the file on the server |

- **Response:**

  | Field    | Value               |
  |----------|---------------------|
  | version  | Version of the file |
  | message  | Response message    |

#### Sample Request
```json
{
    "file-content": "JVBERi0xLjcNCiW1tbW1DQoxIDAgb2JqDQ",
    "file-type": "application/pdf",
    "file-name": "my_doc.pdf",
    "target-path": "/docs/personal/"
}
```

#### Sample Response
```json
{
"message": "File uploaded successfully",
"version": 0
}
```

### Retrieve File

- **HTTP Method:** `GET`
- **Endpoint:** `/file-manager/ffile-retrieve`
- **Parameters:**
    - `source-path` (required): Path of the file on the server
    - `version` (required): Version of the file
- **Response:**
    
    | Field        | Value                      |
    |----------------------------|--------------------------|
    | file-content | Base64 encoded file content |
    | file-type    | Type of the file           |
    | file-name    | Name of the file           |
    | message      | Response message           |

#### Sample Response
```json
{
    "file-content": "JVBERi0xLjcNCiW1tbW1DQoxIDAgb2JqDQ",
    "file-type": "application/pdf",
    "file-name": "DCU_LinkedIn_Tips.pdf",
    "message": "File retrieved successfully"
}
```

### View File Structure

- **HTTP Method:** `GET`
- **Endpoint:** `/file-manager/file-structure`
- **Parameters:** NA
- **Response:** Nested json structure of folders and files with version and last modified date

#### Sample Response

```json
{
  "personal": {
    "docs": {
      "my_doc.pdf": {
        "version-0": "08-06-2023 11:56:02"
      },
    },
    "another_doc.pdf": {
      "version-0": "08-06-2023 00:16:52"
    }
  }
}
```