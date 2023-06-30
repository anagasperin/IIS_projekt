import pandas as pd
import os


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    current = os.path.join(root_dir, 'data', 'processed', 'current_data.csv')
    train = os.path.join(root_dir, 'data', 'processed', 'train.csv')
    test = os.path.join(root_dir, 'data', 'processed', 'test.csv')

    current_data = pd.read_csv(current)

    # Calculate the cutoff index
    cutoff_index = int(len(current_data) * 0.1)
    test_data = current_data.iloc[:cutoff_index + 1]
    train_data = current_data.iloc[cutoff_index + 1:]

    train_data.to_csv(train, index=False)
    test_data.to_csv(test, index=False)


if __name__ == '__main__':
    main()