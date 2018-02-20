# TriloBits
<p>Team Name: Team P
<p>Challenge: Trilobite Bits

## Progress
	<p> Focused only on the identification of Segments and differentiation between head, body, and tail
	<p> Further modules will have to be developed to detect triolobyte in an image if not centered and either
	1. rectify image to center
	2. provide coordinates of start and end
	<p> Using Derivative filtering as the main player in detecting segments we look for drastic changes in intensity along the center of the image and draw lines on those peaks yeilding optimistic results.  Details on how we might improve the accuracy and remove false positives aswell as how we can actually use this information in solving the problem are documented in the file segment.py
	<p> Included is also a scraper that will collect the entire catalog of images from the museam website
## Within
	*. scraper.py use: "python scraper.py"
	*. segment.py use: "python segment.py [filename]"  output:[output.jpg]


