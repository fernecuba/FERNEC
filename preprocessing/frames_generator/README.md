# frames_generator

## configs

- `dataset`: unique name for dataset
- `source`: type of source (`images` or `videos`)
- `labels_path`: path to the labels file. This is the data used as entry point of the script, where all videos or images are loaded and processed
- `dataset_path`: path to the source files
- `output_path`: output path
- `temp_path`: relative path to store temp files inside `output_path` (TODO: these are not being deleted, however are useless by the end of the process)
- `array_split`: number of arrays in which to split dataframe to process (TODO: default should be one)
- `thumbnail_size`: tuple of size 2 with dimensions to be resized (TODO: default should be `None`)
- `frames_batch_size`: batch size used to detect faces in frames using facenet_pytorch's MTCNN implementation
- `frames_order_magnitude`: order magnitude used to name frames produced in video processing
- `dataset_sort`: array of columns used to sort dataset
- `verbose`: verbose mode
- `is_test_mode`: test mode tries to accomplish one complete execution of each part of script. Useful to test the environment

## execution

Create virtual environment for `frames_generator` module

`$ python3 -m venv venv`

Activate venv

`$ source venv/bin/activate`

and install requirements

`$ pip install -r requirements.txt`

Finally, configure `configs.py` and run 

`python3 main.py`
