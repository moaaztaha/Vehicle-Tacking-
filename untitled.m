clc;
close all;
foregroundDetector = vision.ForegroundDetector('NumGaussians', 3, ...
    'NumTrainingFrames', 50);

videoReader = VideoReader('Case1.wmv');
for i = 1:150
    frame = readFrame(videoReader); % read the next video frame
    foreground = step(foregroundDetector, frame);
end

figure;
subplot(1,2,1) ;imshow(frame); title('Video Frame');
subplot(1,2,2) ;imshow(foreground); title('Foreground');

se = strel('Disk', 20);
filteredForeground = imdilate(foreground, se);
figure; imshow(filteredForeground); title('Clean Foreground');





blobAnalysis = vision.BlobAnalysis('BoundingBoxOutputPort', true, ...
    'AreaOutputPort', false, 'CentroidOutputPort', false, ...
    'MinimumBlobArea', 200);
bbox = step(blobAnalysis, filteredForeground);

result = insertShape(frame, 'Rectangle', bbox, 'Color', 'green');

numCars = size(bbox, 1);
result = insertText(result, [10 10], numCars, 'BoxOpacity', 1, ...
    'FontSize', 14);
figure; imshow(result); title('Detected Cars');


videoPlayer = vision.VideoPlayer('Name', 'Detected Cars');
videoPlayer.Position(3:4) = [650,400];  % window size: [width, height]
se = strel('Disk', 17); % morphological filter for noise removal


while hasFrame(videoReader)

    frame = readFrame(videoReader); % read the next video frame

    % Detect the foreground in the current video frame
    foreground = step(foregroundDetector, frame);

    % Use morphological opening to remove noise in the foreground
    filteredForeground = imopen(foreground, se);

    % Detect the connected components with the specified minimum area, and
    % compute their bounding boxes
    bbox = step(blobAnalysis, filteredForeground);

    % Draw bounding boxes around the detected cars
    result = insertShape(frame, 'Rectangle', bbox, 'Color', 'green');

    % Display the number of cars found in the video frame
    numCars = size(bbox, 1);
    result = insertText(result, [10 10], numCars, 'BoxOpacity', 1, ...
        'FontSize', 14);

    step(videoPlayer, result);  % display the results
end