import pandas as pd
import os


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    current = os.path.join(root_dir, 'data', 'processed', 'current_data.csv')
    reference = os.path.join(root_dir, 'data', 'processed', 'reference_data.csv')

    current_data = pd.read_csv(current)
    current_data.to_csv(reference, index=False)


if __name__ == '__main__':
    main()