# 5293_hw1
### Work Flow
1. read image data and turn color info to lab in one-dimensional array.
2. use k-means algorithm to classify color to  different category.
3. separate different category color, turn into True/False matrix for next step.
4. check coverage from top left to right bottom, if coverage in scope, then set position as target area.

### Variables explain
| variables | meaning |
| --- | --- |
| n_clusters | how many color categories |
| source_file_name | source image file name|
| img_data | lab color info in one-dimensional array |
| result | data after k-means calculate | 
| imgs | different category color matrix | 
|current_rate | cover percent | 

### Function explain

##### rgb2lab
this function turn rgb tuples to lab tuples, reference https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python.
    
##### read_img
this function read image data, use rgb2lab to get lab info of every pixel, and return array, and row number and col number of image pixel matrix.

##### check_face
this function check a box area row by row and col by col, when find a area coverage in targer scope, then mark as face area.

##### generate_result
this function draw the separate category pixel of source image, and draw a rectangle border for the face.

### Result
Multi face detecting is not implemented now.

.![](89_48result.jpg)

### Limitations
It can be noticed that some hair and three fingers show up in the output, because these hair and fingers have similar color with skin. And further regularization processing must be applied to filter removing these noises. Also, my script currently can only detect one face by the area coverage check, because the way checking face is simple, just check percentage. I think k-means can only help separating image parts (and I need to adjust n manually for better effect), but human face detecting is particular domain, we may need face model to help improving the result. 
