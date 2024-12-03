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
4. Run
   - Run development mode
    ```
    invoke run-dev
    ```
   - Run tests
    ```
    invoke run-test
    ```

<br>

In case of error, try to use:
```commandline
pip install -e .
```
