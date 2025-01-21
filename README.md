# CaptchaPass

## How to start


1. Install python virtual environment
    ```
    pip3 install virtualenv
    ```
2. Create new virtual env
    ```
    python3 -m venv venv
    ```
3. Activate venv \
    ```commandline
    source venv/bin/activate
    ```
    **⬆️ Remember to always have venv activated when you are developing!**
    ```commandline
    pip install -r src/requirements.txt
    ```
4. Add variable environments \
   Create file `.env` in root project folder
   - `BACKEND_HOST` ( optional ) - backend hostname \
   Example: `http://127.0.0.1:5000`
   - `DATABASE_URI` ( required ) - uri to mongodb database ( tested only in remote database but in local should work too) \
   Example: `mongodb+srv://<login>:<password>@test.jrzu6.mongodb.net/?retryWrites=true&w=majority&appName=test`
   - `DATABASE_NAME` - database name \
   Example: `test`
5. Run
   - Run development mode
    ```
    invoke run-dev
    ```
   - Run tests
    ```
    invoke run-test
    ```
   - Upload photos to database <br> 
      In file `uploadImages` you can change what categories and how many elements you want to upload
    ```
    invoke initial-images
    ```

<br>

In case of error, try to use:
```commandline
pip install -e .
```
