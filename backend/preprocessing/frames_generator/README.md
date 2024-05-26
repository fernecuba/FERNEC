# frames_generator

## execution

Create virtual environment for `frames_generator` module

`$ python3 -m venv venv`

Activate venv

`$ source venv/bin/activate`

and install requirements

`$ pip install -r requirements.txt`

Finally, configure `configs.py` and run 

`python3 main.py`

## configs

- `dataset`: unique name for dataset
- `source`: type of source (`images` or `videos`)
- `labels_path`: path to the labels file. This is the data used as entry point of the script, where all videos or images are loaded and processed
- `dataset_path`: path to the source files
- `output_path`: output path
- `temp_path`: relative path to store temp files inside `output_path` (TODO: these are not being deleted, however are useless by the end of the process)
- `array_split`: number of arrays in which to split dataframe to process (TODO: default should be one)
- `thumbnail_size`: tuple of size 2 with dimensions to be resized (TODO: default should be `None`)
- `batch_size`: batch size used to detect faces in frames using facenet_pytorch's MTCNN implementation
- `frames_order_magnitude`: order magnitude used to name frames produced in video processing
- `dataset_sort`: array of columns used to sort dataset
- `verbose`: verbose mode
- `is_test_mode`: test mode tries to accomplish one complete execution of each part of script. Useful to test the environment


## input files
For video processing, you should dispose all videos in a single folder. Besides, you need to have an input file containing these fields
 - video_name: this must contain the video name, e.g. `first_video`
 - video_file: this must contain the video file name with its extension, e.g. `first_video.mp4`
 - label_file: this must contain the name of a csv file where information per frame is disponibilized

For each label_file for each video, these files must contain a title and one row per frame. If the file is larger than the video or viceversa, 
last frame or last line will be replicated to fullfill the missing entries. These are the fiels required in each file
- labels: a number for each expression
- labels_expression: the actual name of the expression for the emotion recognised


For image processing, you must dispose all images into a single folder and have a single file containing these fields:
- file_name: this must contain the file name with its extension, e.g. `angry_actor_104.jpg`
- labels_expression: the actual name of the expression for the emotion recognised
