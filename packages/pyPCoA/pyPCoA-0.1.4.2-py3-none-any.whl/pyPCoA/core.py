import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import argparse
import os
import tempfile
import pkg_resources

def load_data(file_path):
    tbl_new = pd.read_csv(file_path, header=None)
    bacterial_labels = tbl_new.iloc[1, 2:].tolist()
    data = tbl_new.iloc[2:, 2:].values.astype(float)
    return bacterial_labels, data

def pcoa(distance_matrix):
    n = distance_matrix.shape[0]
    H = np.eye(n) - np.ones((n, n)) / n
    B = -H.dot(distance_matrix**2).dot(H) / 2
    eigvals, eigvecs = np.linalg.eigh(B)
    idx = eigvals.argsort()[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    return (eigvecs[:, :2] * np.sqrt(np.abs(eigvals[:2]))).real

def pcoa_biplot(score, title='', output_path=None):
    plt.figure(figsize=(10, 8))
    plt.scatter(score[:, 0], score[:, 1])
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title(title)
    plt.grid()
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()

def adjust_pcoa_signs(data_pcoa, reference_pcoa):
    for i in range(2):  # PC1とPC2を順番に調整
        if np.sign(data_pcoa[:, i]).sum() != np.sign(reference_pcoa[:, i]).sum():
            data_pcoa[:, i] = -1 * data_pcoa[:, i]
    return data_pcoa

def main():
    args = parse_arguments()

    # Load sample data and reference R PCoA data
    sample_data_path = pkg_resources.resource_filename(__name__, 'data/sample_data.csv')
    reference_data_path = pkg_resources.resource_filename(__name__, 'data/PCoA_BrayCurtis_R.csv')

    try:
        bacterial_labels_sample, data_sample = load_data(sample_data_path)
    except FileNotFoundError:
        print("Error: 'sample_data.csv' not found. Please ensure the file is in the correct directory.")
        return

    try:
        pcoa_braycurtis_r = pd.read_csv(reference_data_path)
    except FileNotFoundError:
        print("Error: 'PCoA_BrayCurtis_R.csv' not found. Please ensure the file is in the correct directory.")
        return

    # Calculate Bray-Curtis distance for sample data
    dist_braycurtis_sample = pdist(data_sample, metric='braycurtis')
    dist_braycurtis_sample = squareform(dist_braycurtis_sample)
    data_pcoa_braycurtis_sample = pcoa(dist_braycurtis_sample)

    # Save PCoA data for sample to a temporary CSV
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        df_braycurtis_sample = pd.DataFrame(data_pcoa_braycurtis_sample, columns=["PC1", "PC2"])
        df_braycurtis_sample.to_csv(temp_file.name, index=False)
        temp_csv_path = temp_file.name

    # Adjust signs of sample PCoA to match reference PC2 if necessary
    data_pcoa_braycurtis_sample = adjust_pcoa_signs(data_pcoa_braycurtis_sample, pcoa_braycurtis_r.values)

    # Process input file if provided
    if args.input_file:
        try:
            bacterial_labels, data = load_data(args.input_file)
        except FileNotFoundError:
            print(f"Error: '{args.input_file}' not found. Please ensure the file is in the correct directory.")
            return
        dist_braycurtis = pdist(data, metric='braycurtis')
        dist_braycurtis = squareform(dist_braycurtis)
        data_pcoa_braycurtis = pcoa(dist_braycurtis)

        # Adjust signs to match reference PC2 if necessary
        data_pcoa_braycurtis = adjust_pcoa_signs(data_pcoa_braycurtis, pcoa_braycurtis_r.values)

        # Visualize the PCoA biplots
        if args.plot_output:
            pcoa_biplot(data_pcoa_braycurtis, title="PCoA Biplot using Bray-Curtis", output_path=args.plot_output)
        else:
            pcoa_biplot(data_pcoa_braycurtis, title="PCoA Biplot using Bray-Curtis")

        # Save PCoA data to CSV
        df_braycurtis = pd.DataFrame(data_pcoa_braycurtis, columns=["PC1", "PC2"])
        df_braycurtis.to_csv(args.output_file, index=False)

def parse_arguments():
    parser = argparse.ArgumentParser(description='PCoA analysis using Bray-Curtis distance metric.')
    parser.add_argument('--input_file', type=str, help='Path to the input CSV file containing the data. If not specified, sample_data.csv will be used.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save the PCoA CSV result.')
    parser.add_argument('--plot_output', type=str, help='Path to save the PCoA plot image. If not specified, the plot will be shown on screen.')
    return parser.parse_args()

if __name__ == "__main__":
    main()
