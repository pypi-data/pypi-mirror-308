[![PyPI](https://img.shields.io/pypi/v/rcounting.svg)](https://pypi.org/project/rcounting/)
![GitHub](https://img.shields.io/github/license/cutonbuminband/rcounting)


A collection of tools for working with data on the counting threads in /r/reddit.com/r/counting.

## Description
There's a [community on reddit](www.reddit.com/r/counting) that likes to count collaboratively. Any kind of count - if you can think of a sequence of numbers (or letters, or words) what could be fun to count in order, we've probably tried counting it.

As well as counting, we also make stats on who's made how many counts, how fast they were, and who managed to count numbers ending in lots of nines or zeros.

This repository has tools for interacting with the reddit api through the [Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/), to help gathering these statistics.

## Installation and usage
The package is available on `pypi` as a package, so installation is as easy as `pip3 install rcounting`. If you want the very latest commit, you can install by typing `pip3 install git+https://github.com/cutonbuminband/rcounting.git`.

The command line interface for the package is all under the command `rcounting`. Type `rcounting -h` to see what options there are -- the main ones are described below.

The first time you run the program you will be asked to authorize it to interact with reddit on your behalf. Specifically, it needs to be able to

- Read posts on reddit
- Read wiki pages on reddit
- Edit wiki pages (for updating the thread directory)

### Thread Logging

The package has functionality for logging threads which can be invoked by typing `rcounting log`. The default behaviour is to log the latest complete thread (as found in the [directory](http://reddit.com/r/counting/wiki/directory), saving the output to csv files. You can specify that you want to log a different threads, want to log a while chain of threads, or want to store the output in a database instead. Try typing `rcounting log_thread -h` to see a more detailed usage explanation.

### Validation
The package can also validate threads according to specific rules. This is done by typing `rcounting validate`, and the program takes an additional `--rule` parameter specifying which rule should be checked. The following options are available:

- default: No counter can reply to themselves
- wait2: Counters can only count once two others have counted
- wait3: Counters can only count once three others have counted
- once\_per\_thread: Counters can only count once on a given reddit submission
- slow: One minute must elapse between counts
- slower: Counters must wait one hour between each of their counts
- slowestest: One hour must elapse between each count, and counters must wait 24h between each of their counts
- only\_double\_counting: Counters must reply to themselves exactly once before it's somebody else's turn.

If no rule is supplied, the program will only check that nobody double counted.

After you run it, it'll print out whether all the counts in the chain were valid, and if there was an invalid count, which one it was.

### Updating the thread directory

Finally, there's a program to update the [directory of side threads](www.reddit.com/r/counting/wiki/directory). It's invoked by calling `rcounting update-directory`, and roughly follows the following steps

1. It gets all submissions to r/counting made within the last six months
2. It tries to find a link to the parent submission of each submission
   - First it looks for a reddit url in the body of each submission (trying to find the "continued from here" line
   - If that fails, it goes through all the top level comments of the submission looking for a reddit url
3. It constructs a chain for each thread from parent submission to child submission
4. For each row in each table in the directory, it extracts
  - Which side thread it is, based on the link to the first thread
  - What the previous submission, comment and total count were.
5. It then uses the chain of submissions to find the latest submission of each thread type
6. And walks down the comments on each submission to the latest one. At each level of comments it goes to the first valid reply based on
  - A per-thread rule describing when a count is valid
  - A per-thread rule describing what looks like a count (to skip over mid-thread conversations)
7. If the latest submission is not the same as the previous one, it tries to update the total count field

Some threads hang around for a long time, so there's also an [archive](http://reddit.com/r/counting/wiki/archive) of older threads. If a submission is more than six months old and still been completed, the thread is moved to the archive.

Some of the threads from the last six months might not be in the directory (yet). These are potentially new or revived threads. If a submission contains no links to previous submissions, it's considered a new thread, and once it has more than 50 counts by 5 different users, it's automatically added to the directory. Submissions which link to archived threads are considered to be revivals of the archived thread, and once the submission has 20 counts, it's moved from the archive to the new threads table.

If you run the script with no parameters it takes around 15 minutes to run, depending on how out of date the directory pages are. That's an unavoidable consequence of the rate-limiting that reddit does.

## Data analysis
Using the scripts here (and an archive supplied by members of r/counting), I've scraped every comment in the main counting chain, including the comment bodies. There are a number of interesting plots and tables that can be made using this data; here's a list of [examples](https://cutonbuminband.github.io/counting-analysis/) of working with the data.

## Dependencies

The program has been tested on python 3.7, 3.8 and 3.10, on Windows and on Linux.

The program makes use of the [Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/) to interact with reddit and `pandas` to work with tabular data. Updating some of the side threads requires `scipy` -- yes, really!

The command line interface is built using `click`.

## License

This project is licensed under the terms of the GNU General Public License v3.0, or, at your discretion, any later version. You can read the license terms [here](/LICENSE.md).

## Contributing and Future Ideas
This is a loosely organised list of things which could be done in the future. If you have any suggestions, don't hesitate to write, or to send a pull request. As a heads up, when you submit a pull request, you are also agreeing to license your code under the GPL (see github's [terms of service](https://docs.github.com/en/github/site-policy/github-terms-of-service#6-contributions-under-repository-license)).

* Recovering gracefully if a linked comment is inaccessible because it's been deleted or removed
* Making the comment and url extraction less brittle

## Get in touch

If you have any questions, suggestions or comments about this project, you can contact the maintainer at cutonbuminband@gmail.com, or visit the [counting subreddit](www.reddit.com/r/counting) and post in the weekly Free Talk Friday thread.
