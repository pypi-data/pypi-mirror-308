import os
from pyspark import SparkFiles
from pyspark.sql import SparkSession


def copy_file_to_spark(session: SparkSession, path: str):
    filename = os.path.basename(path)
    content = open(path).read()

    session.sparkContext.addFile(path)

    def write_keyfile():
        keyfile_path = SparkFiles.get(filename)
        print("keyfile_path: ", keyfile_path)
        with open(keyfile_path, 'w') as keyfile:
            keyfile.write(content)

    executor = session.sparkContext.defaultParallelism
    session.sparkContext.parallelize(range(executor * 8), executor * 8).foreach(lambda _: write_keyfile())
