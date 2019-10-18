

The file brokenlinks.py is a module that detects broken links in HTML when passed a URL.
It performs well with either http or https connection, but can occasionally call a not-broken link broken.
Here is how it performed on the following webpages:

On the webpage http://people.reed.edu/~esroberts/csci396/index.html:
	finds Broken link http://people.reed.edu/~esroberts/csci396/lectures/05-TheVictorianInternet.zip 
	in <a> tag at line 114 which is actually broken. 

On the webpage http://people.reed.edu/~esroberts/csci396/
	it finds Broken link http://people.reed.edu/~esroberts/csci396/lectures/05-TheVictorianInternet.zip 
	in <a> tag at line 114 which is actually broken. 

On the webpage http://people.reed.edu/~agroce/index.html
	it finds no broken links... which I believe is correct.


On the webpage http://people.reed.edu/~agroce/teaching.html
	it says the following are broken links and all but one are actually broken:
	http://www.saintannsny.org/ in <a> tag at line 67 (This one is not actually broken)*
	http://www.cs.umd.edu/class/fall2008/cmsc250/ in <a> tag at line 66
	http://www.cs.umd.edu/class/spring2009/cmsc351/ in <a> tag at line 65
	http://www.academicchallenge.org in <a> tag at line 63

	*I am not sure why the www.saintannsny link fails, during debugging it gave error code:
	<urlopen error [Errno 8] nodename nor servname provided, or not known> but it is up.

On the webpage http://people.reed.edu/~esroberts/
	It says the following link is broken but it is not:
	mailto:eroberts@cs.stanford.edu
	I'm not sure how to handle these kinds of links.
