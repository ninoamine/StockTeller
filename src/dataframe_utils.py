import pandas as pd
from pathlib import Path


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame.

    Args:
        path: file path to the CSV file.

    Returns:
        A DataFrame with the CSV contents.

    Raises:
        FileNotFoundError: if the file does not exist.
    """
    return pd.read_csv(path)


def describe_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return a statistical summary of a DataFrame.

    Combines shape info, data types, and descriptive statistics
    into a single overview useful for quick data inspection.

    Args:
        df: the DataFrame to describe.

    Returns:
        The output of df.describe(), which includes count, mean,
        std, min, 25%, 50%, 75%, and max for numeric columns.
    """
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    print(f"Dtypes:\n{df.dtypes}\n")
    return df.describe()


from datetime import date

def scrape_to_dataframe(
    quotes: list[dict[str, str]],
    output_dir: str | Path = "data",
) -> pd.DataFrame:
    """Convert a list of quote dicts to a DataFrame and save as CSV.

    Args:
        quotes: list of dicts as returned by scrape_all_quotes().
        output_dir: directory where the CSV file will be saved.

    Returns:
        A DataFrame containing all the quote data.
    """
    df = pd.DataFrame(quotes)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = output_path / f"quotes_{date.today().isoformat()}.csv"
    df.to_csv(filename, index=False)

    return df