# REST API project

## SETUP

1. Install Python 3.7, if not already done so.
2. Install package requirements using `pip install -r requirements.txt`
2. Go to the code directory and run the code using `python app.py`
3. The server is now running at `localhost:5000` and you can send queries using the program of your choice.

## EXAMPLE


## TESTING

1. Start the server, as described in the **SETUP** section.
2. In a new terminal, go to the code directory and run the test using `python test_app.py`

## API HELP

You can see help for the API by either going to [the help page](http://patrickignoto.com/2019/12/22/help-page-for-rest-api-project/) or get redirected to the help page using `localhost:5000/help`

## KNOWN ISSUES AND LIMITATIONS
- I misundersood the offset parameter when I first started the project, and instead of using the index of the result, I paginated the results, and then used offset to work as a page number. Only after mostly completing the task did I realize this. Rather than delay further I submitted it. 
- Queries are slow and will probably get slower as the size of results from the provided APIs increase. With some further code review, we could find a more efficient way of solving this problem.
- You must have an internet connection accessible by app.py to retrieve results from upstream rest APIs.
