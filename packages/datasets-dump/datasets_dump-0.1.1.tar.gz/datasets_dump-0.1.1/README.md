# datasets-dump

Dump embedded datasets to audio folder or images folder.

Get the audio folder / image folder back from parquet files.

## Usage

```bash
datasets-dump someone/dataset ./dist
```

Python API:

```python
def dump(
    dataset: Union[str, Dataset],
    dist: str | Path,
    audio_column: Optional[str] = None,
    image_column: Optional[str] = None,
    metadata_format: Literal["jsonl", "csv"] = "jsonl",
) -> None
```
