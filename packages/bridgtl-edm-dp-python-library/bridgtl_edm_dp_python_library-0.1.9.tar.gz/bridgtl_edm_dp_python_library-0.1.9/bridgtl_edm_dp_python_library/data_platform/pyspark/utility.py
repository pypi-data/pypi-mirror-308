import os
from pyspark.sql import SparkSession


def copy_file_to_spark(session: SparkSession, path: str, instance: int):
    content = open(path).read()

    session.sparkContext.addFile(path)

    def write_keyfile():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as keyfile:
            keyfile.write(content)

    session.sparkContext.parallelize(range(instance), instance).foreach(lambda _: write_keyfile())
