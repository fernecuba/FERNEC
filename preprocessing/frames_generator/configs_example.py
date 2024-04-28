# copy this file as configs.py and define paths as you wish. This is just an example

# TODO: improve me with new changes
# TODO consider using https://docs.python.org/3/library/configparser.html
def get_configs():
    return [
        {
            "dataset": "IFEED",
            "source": "images",
            "dataset_path": "./data/IFEED/raw-images/",
            "labels_path": "./data/IFEED/labels/labels.csv",
            "dataset_output_path": "./data/IFEED/frames/",
            "output_path": "./data/IFEED/output/",
            "processed_stats_path": "./data/IFEED/output/processed_images.csv",
            "destination_folder": "./data/IFEED/output/rearranged_by_labels/",
            "temp_path": "temp/",
            "array_split": 100,
            "dataset_sort": ["file_name"],
            "dataset_filters": {},
            "verbose": True,
            "is_test_mode": False,
            "thumbnail_size": (112, 112),
            "channels": 3,
            "load_csv": True,
            "rearrange_by_labels": True
        },
        {
            "dataset": "Aff-Wild2",
            "source": "videos",
            "dataset_path": "./data/Aff-Wild2/raw-videos/",
            "labels_path": "./data/Aff-Wild2/labels/videos.csv",
            "dataset_output_path": "./data/Aff-Wild2/frames/",
            "labels_output_path": "./data/Aff-Wild2/labels/labels.csv",
            # necessary to create one file with all image labels from each video labels
            "images_labels_path": "./data/Aff-Wild2/labels/",
            "temp_path": "temp/",
            "batch_size": 30,
            # to fill name when creating frames files
            "frames_order_magnitude": 5,
            "thumbnail_size": (48, 48),
            "array_split": 100,
            "dataset_sort": ["video_name", "file_name"],
            "verbose": True,
            "is_test_mode": True,
        },
        {
            "dataset": "Aff-Wild2",
            "source": "videos",
            "dataset_path": "./data/Aff-Wild2/frames/",
            "labels_path": "./data/Aff-Wild2/labels/labels.csv",
            "output_path": "/Aff-Wild2/output/",
            "dataset_output_path": "./data/Aff-Wild2/frames/",
            "labels_output_path": "./data/Aff-Wild2/labels/labels.csv",
            # necessary to create one file with all image labels from each video labels
            "images_labels_path": "./data/Aff-Wild2/labels/",
            "temp_path": "temp/",
            "batch_size": 64,
            # to fill name when creating frames files
            "frames_order_magnitude": 5,
            "thumbnail_size": (112, 112),
            "channels": 3,
            "array_split": 150,
            "dataset_sort": ["video_name", "file_name"],
            "dataset_filters": {"labels_expression":
                  ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]},
            "verbose": True,
            "is_test_mode": True,
            "load_csv": True,
            "database_config": {
                "uri": "mongodb://localhost:27017/",
                "database": "fernec",
                "collection": "test_aff_wild2_112x112x3_test",
                "documents_stats_path": "./data/Aff-Wild2/output/mongo_documents.csv"
            }
        },
    ]


# TODO: define default values. Consider using configparser
DEFAULTS = {
    "output_path": "/data/output/",
    "array_split": 1,
    "dataset_sort": [],
    "verbose": False,
    "temp_path": "temp/",
    "is_test_mode": False
}
