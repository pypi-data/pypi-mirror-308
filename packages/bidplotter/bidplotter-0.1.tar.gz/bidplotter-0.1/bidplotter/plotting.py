import matplotlib.pyplot as plt

def plot_bidding_progress(times, prices):
    plt.figure(figsize=(10, 6))
    plt.plot(times, prices, label='Bid Price Over Time', color='blue', marker='o')
    
    plt.title('Auction Bid Progression')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bid Price ($)')
    plt.grid(True)
    plt.legend()

    # Save the plot to an image file
    plt.savefig('static/media/bid_progress.png')  # Save in the static directory
    plt.close()
