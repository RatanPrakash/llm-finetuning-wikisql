import pandas as pd
import datasets

class MyParquetDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="My custom dataset of question-answer pairs",
            features=datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://example.com",
            citation="citation"
        )

    def _split_generators(self, dl_manager):
        parquet_file = "ema/archive/datasetOriginal.parquet"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": parquet_file}
            ),
        ]

    def _generate_examples(self, filepath):
        df = pd.read_parquet(filepath)
        for id_, row in df.iterrows():
            yield id_, {
                "question": row["question"],
                "answer": row["answer"]
            }
