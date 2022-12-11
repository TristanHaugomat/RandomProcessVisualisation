## Summary

This repository is a short example of usage of Flask in streamlit.
The app is deployed here:
[https://share.streamlit.io/tristanhaugomat/randomprocessvisualisation/main/main.py](https://share.streamlit.io/tristanhaugomat/randomprocessvisualisation/main/main.py).

## Description

* The file `app.py` contain the Flask API.
* The file `main.py` run the streamlite app and is called by streamlite cloud.
* The `requirement.txt` is used by the streamlite cloud to setup the python environment.

The main blocking point is the running of the Flask app in the cloud. This is done by

```
@st.cache
def run_api():
    subprocess.Popen([sys.executable, 'app.py'])
run_api()
```

Use `@st.cache` to run the Flask app only one time,
`subprocess.Popen` to execute a bash command and `sys.executable` to obtain the path of python executable (you don't
know the cloud setup).

In local, you can comment `run_api()` and run it in other way for more interactivity.

## The very useful docs

* [Streamlit](https://docs.streamlit.io/library/get-started/main-concepts)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
* [Requests](https://docs.python-requests.org/en/latest/user/quickstart/)
