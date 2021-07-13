### Initialization

- Clone the repo and cd into the base directory
```
git clone https://github.com/b4skyx/PROJ-8
cd PROJ-8
```

- Install the dependencies using pip (Ensure pip and python3 are installed and in path)
```
pip install -r requirements.txt
```

- Head over to [mongodb atlas](cloud.mongodb.com/) and create an account.
- Instantize a database cluster and grab the database key

- Set an environment variable `DATABASE_CLIENT_URL=YOUR_MONGODB_URL` or save it in a .env file

### Project Structure

````
~/.env
├── documents
├── keybase
├── requirements.txt
├── runner.py
├── signature
└── utilities
````

- `/documents` : Directory that contains the documents saved documents with the document ID
- `/keybase` : Stores the RSA key-pairs assorted by client ID
- `/signatiure` : Directory that contains signatures of documents assorted by document ID
- `/utilities` : Has the files that contain utility functions that interact with database and cryptographic library
- `/runner.py` : Sample program that works as a client to couple everything together
