<h1> DFT </h1>
<h2> Input Image:
  <br>
  <img fifu-featured="1" src="https://sketchok.com/images/articles/01-cartoons/000-va/168/12.jpg" alt="How to draw Wile E. Coyote" title="How to draw Wile E. Coyote" width="400px" height="400px">
</h2>

<br>

<h2> Example Output:
  <br>
  <a href="https://imgur.com/YDlCGs8"><img src="https://i.imgur.com/YDlCGs8.gif" alt="Wile E. Coyote Path Tracing" title="Wile E. Coyote Path Tracing" /></a>
</h2>

<br>

<br><br>
<h2> Dependencies </h2>

In order to run this program you need to install pygame.
This can be done through the python package manager with the following command:
    ```pip3 install pygame```

<br><br>
<h2> Usage Manual </h2>

<u> Instructions to use the program: </u>
run FindEdges on the desired file.
    This prints the dimensions of the image firstly:
    if your image is bigger than 800x800 you will need to increase 'downscale' to make it run quickly

It then also prints out the number of points on an edge:    
    anything more than 3,500 or 4,000 could take a moment. 
    Anything more than 8,000 or 9,000 will be very slow.

run EdgesToPath until you find a path you're satisfied with:
    this process is randomized in the case that any arbitrary path doesn't meet your expectations,
    this will provide a rough sketch of what the epicycles will trace in the final step.
  
There's a chance it doesn't include all the points you want it to,
    this is because it excludes some points that are 'too far' from the overall image:
    in this case you should run the function again to produce a new (randomized) path.
  

Once you think the path is correct, run DFTSketch:
    Depending on your image this could take a few minutes to precompute.
    Pygame window <b> will </b> stop responding for a period of time: don't panic!
    Give the program 2-3 minutes maximum.
  

<br>
<h4> FindEdges and its inputs </h4>

filename: the filename of any jpg or jpeg file. I'm not sure if it works
threshold: this is how sensetive the function is to flagging a point as an edge. The lower the number, the better.
downscale: this is how small your image will be scaled, it can be any float, higher numbers mean smaller images.
fidelity: highest fidelity is 1, this can be any integer, the higher it is, the lower the fidelity.

<br><br>
<h2> Purpose and Goal of the project </h2>

The Fourier transform is widely used in image compression in order to turn a series of colour values into a series of functions that can approximate those colour values with less space.

My goal in making this project wasn't to create an efficient and sleek application. It was to explore the mathematics and concepts behind lossy compression and create a working implementation of DFT, there are many places where this algorithm could be more efficient (and if you want to create a high performance implementation then refer to the "Optimizations" sections to figure out how to change my algorithm to streamline performance.

My choice of not using libraries (numpy, pillow, etc.) and using python as opposed to something with better performance like C++ was intentional. I wanted to build a fully working prototype from first principles: including all the functionality needed to implement such an algorithm such at image convolutions or the DFT algorithm itself.

My implementations of these algorithms are not generic and are specialized towards the usecase of this project, so be aware that there are superior alternatives if you are trying to adapt them to a different circumstance.

<br><br>
<h2> Algorithm Overview </h2>

An image is taken as an input, a Sobel filter is passed over it. A list of the edges are written into a CSV file.
Then a greedy approximation of the Travelling Salesman Problem (TSP) is used to find a suitable path around the edges.
Once this path is computed the x and y coordinates are separated into 2 different sequences.
A Discrete Fourier Transform (DFT) is ran over these

<br><br>
<h2> Disclaimer </h2>

Keep in mind that many of these processes take a moment,
while the image/csv is processing the pygame window will stop responding.
Flushing the pygame event queue will fix the freezing but significantly increase the runtime.
Please be patient and wait for the file to run.

A small image will take under a minute to fully process and then a few minutes to draw.
Large images can take a very, very long time.

<br><br>
<h2> Optimizations </h2>

There are a few points in this algorithm that significantly hinder performance:
    Kernel convolution (is done manually in this project)
    Nearest neighbour search (in the TSP)
    The DFT itself
    Computation of the path of the image itself (the actual drawing part)
  
<br>
<h3> Solutions and Implementations of Optimizations </h3>

<br>
<h4> Kernel Convolution </h4>

To fix this you can use a pre-existing image processing library (I recommend pillow).
If you want to implement it without the use of a library then do so as a shader that runs parallel on the GPU.

<br>
<h4> Nearest Neighbour Search </h4>

This current runs in quadratic time ( O(n^2) )
It can be improved to linearithmic ( O(n * log(n) ) time with the use of appropriate data structure

There are many different tree data structures that can be used to subdivide space recursively.
This will reduce the search time of the neighbours of a specific node from n to log(n).

My personal recommendation is that you use a quadtree, simply as the implementation is easier and quicker.
A k-d tree might offer better performance for this but it might be a little painful to implement.

As these trees are not easy to delete points from but are easy to reconstruct (insertion on a tree is log(n) time therefore construction of a tree with n nodes is n * log(n) time) then it is advisable to simply reconstruct the tree periodically or mark points already visited with a boolean flag.

<br>
<h4> Computation of the Path </h4>

The pathing of the epicycles are actually computed real-time in python.
This is not a wise choice from a performance perspective: the drawing will run much faster if it is precomputed.
The coordinate (singular as each epicycle only moves on one axis) of each epicycle can be recorded at each timestep if you wish to draw all epicycles.
Otherwise the overall summation of the coordinates of the epicycles can be recorded to draw the pathing of the edges.

When run the function that is to draw instead of calculating these values for each frame will read them in from a file.

<br>
<h4> The DFT itself </h4>

This is possibly the biggest hit on the performance of the overall application and it can be fixed by a very commonly known algorithm called FFT. FFT actually represents a family of algorithms that can compute the DFT of any given sequence in linearithmic time ( O(n * log(n) ).

This will drastically improve the performance at any non-trivial number of points, especially since the functions used to compute it (the exponential function) is so expensive.

A further improvement you can make is to use a single series of epicycles by analysing the (x,y) coordinates in the complex plane instead of parameterising them and working with them separately. This will do half the number of computations and therefore run twice as fast but it gives a different aesthetic of the program overall and I personally don't find it to my liking.

<br><br>
<h2> Features to implement </h2>

I've actually finished a program recently that does a compression on an image using a quadtree and have been experimenting with them.
A small modification on that program will likely result in a new and improved fastest version of this one.

Since I have learned what I want to from this project then over the next university break I will implement an efficient version of this using library functions to do the DFT, using Quadtrees to do the nearest neighbour search, and using pillow to do kernel convolutions (the latter two of which I have actually already accomplished).
