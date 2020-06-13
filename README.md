# Geostationary obit satellite detection
For [ESA "Spot the GEO satellites" challenge](https://kelvins.esa.int/spot-the-geo-satellites/problem/)

## Science background

### 2. Difference between stars and satellites

- The angular velocity of the GEO satellites and the Earth are the same, so satellites, from ground view, station on fixed positions in the sky.
- The star rotates relative to the Earth North-South axis.

**Based on this fact, the satellites look like a dot in the sky, while the stars create traits across the view.**

### 1. Difference between sensor noise and satellites

There are three types of noises that effect the light from an outter space object seen from ground:

- Atmospheric distortion
- Optical abberation 
- Sensor noise

The sensor (camera) artifacts, i.e hot pixels and background noises, are sensor noise only. However, light from satellites and stars suffer not only sensor noise, but also atmospheric distortion and optical abberation; which result in a characteristic gradient bondary. 
**Based on this characteristic, we can distinguish between sensor noise and satellites, and similarize satellites to stars based on the gradient feature.**

A hot pixel example
![alt text](https://github.com/tranqkhue/geo_sat_detection/blob/master/doc/satellite.png)
  A crop with 2 satellites and star traits
![alt text](https://github.com/tranqkhue/geo_sat_detection/blob/master/doc/star.png)
## Algorithm

There are two steps: find the satellites in one dividiual frame, and matching multiple frames' satellites in one sequence

### 1. In one individual frame

- Find stars as stars are frequently **the brightest objects** in a frame and stars usually form **traits with same length and direction**
- Resize the bounding boxes around the stars with *dark background* (use *find stars* step threshold above as mask) to squares.
- Get the gradient of the bounding boxes as *positive datasets*
- Crop large bonding boxes in a frame **without** stars (may have satellites inside), perform Gaussian blur and resize them, and use them as *negative datasets*
- Train HOG+SVM or any classifier with datasets generated
- Inference on the whole frame, in particular, *sliding window* method

### 2. In a whole sequence

- Use SIFT/SURF to find translation and rotation transformation between frames
- Apply the transformation for the satellites found in individual frames
- Verify if a satellite does exist in a same position (after transformation) between frames

## FAQ

1. Why do not use Deep Learning? YOLO?
  > The objects' features are not that hard to use deep learning. Based on a human's perspective, I think the problem could be solved by studying the gradients of objects in frames

2. Why use *bounding boxes around the stars* as positive data?
  > Because, without taking account in Earth's rotation, the satellites and stars are relative (small) pin-point objects in the sky. So (hopefully), when we resize the stars' bounding boxes into a square, the stars would be points, while reserving their gradient properties
  
3. Why use HOG? Isn't it outdated?
  > Because we use *gradient* feature. Also we need rotation variance as the **gradients' traits** (not to be confused with *stars' traits*) are the same   
  *A remind of gradient's traits as the pixels' values ascending from left to right (you may need to zoom in)*
![alt text](https://github.com/tranqkhue/geo_sat_detection/blob/master/doc/star.png)
  
4. Why a negative frame may even have satellites in it? It must be positive?
  > Because satellites are usually small objects, while the sensor's background noise usually uneven and spread out. So that when we take a large bounding box without stars (oppose to satellites, stars are usually big and bright objects in frames), Gaussian blur and resize it, the * satellites' little dots* is gone :) 
