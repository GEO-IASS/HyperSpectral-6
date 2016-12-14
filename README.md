# HyperSpectral

##Methods implemented:<br/>
1. Pixel wise matching with queried material: The broad class and specific material within that class is taken as input.
Corresponding to the central wavelengths of the bands of the test image, a vector with the corresonding nearest neighbour
wavelengths of the queried material is determined. For each pixel, the squared error between the image band reflectances and the
reflectances for the nearest neighbour wavelength vector is determined. This error is tested against the threshold for appropriate
classification.<br/>
2. Segmentation: For the test image, the central wavelengths for each band is considered. For each such wavelength, the
entire spectral library data is processed initially so that: for each broad class and for every material in a particular class,
the tuple with the nearest wavelength is considered. Now, when the test image is processed, for each pixel, the material having
the minimum squared difference between the pixel reflectance and the spectral library data's reflectance is taken and the pixel is
assigned its corresponding class. In this way, the entire image is segmented.
