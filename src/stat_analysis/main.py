import summary_stats as st

def main():
    data = [45, 18, 18,15, 15 ]
    freqs = [10, 5, 30, 21, 2]
    dataset = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15)]
    print(st.get_percentile(dataset, freqs, 0.1))

if __name__ == "__main__":
    main()