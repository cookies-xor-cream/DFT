# DFT
Files that take you from a jpeg or jpg file to the plotting of a the outline via a DFT.


Keep in mind that many of these processes take a moment,
while the image/csv is processing the pygame window might not respond.
Be patient and wait for the file to run.


Instructions to trace an image:
  run FindEdges on the desired file.
  This prints the dimensions of the image firstly:
    if your image is bigger than 800x800 you definately need to increase 'downscale'
    
  It then also prints out the number of points on an edge:
    anything more than 3,500 or 4,000 could take a moment. 
    Anything more than 8,000 or 9,000 and it will take a couple minutes to run the later files.

  run EdgesToPath until you find a path you're satisfied with,
  this isn't what your output will exactly be, but a rough sketch of the path it will take.
  
  There's a chance it doesn't include all the points you want it to:
    if this happens, run it again.
  

  Once you think your path is roughly correct, run DFTSketch.
  Depending on your image this could take a while.
  Pygame window could stop responding for a period of time.
  Give the program 2-3 minutes.
  
  

FindEdges and its inputs:
  filename: the filename of any jpg or jpeg file. I'm not sure if it works
  threshold: this is how sensetive the function is to flagging a point as an edge. The lower the number, the better.
  downscale: this is how small your image will be scaled, it can be any float, higher numbers mean smaller images.
  fidelity: highest fidelity is 1, this can be any integer, the higher it is, the lower the fidelity
