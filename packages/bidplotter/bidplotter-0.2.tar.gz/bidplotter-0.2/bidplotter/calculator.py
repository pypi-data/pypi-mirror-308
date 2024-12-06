import matplotlib.pyplot as plt
import os

class BidCalculator:
    def __init__(self, starting_price, bid_increment, duration_in_minutes):
        self.starting_price = starting_price
        self.bid_increment = bid_increment
        self.duration_in_minutes = duration_in_minutes
        self.duration_in_seconds = duration_in_minutes * 60

    def calculate_final_price(self):
        total_bids = self.duration_in_seconds / 10  # Assuming bids every 10 seconds
        price_increase = self.bid_increment * total_bids
        final_price = self.starting_price + price_increase
        return final_price

    def plot_bidding_progress(self):
        # Generate the price progression graph
        times = [i for i in range(0, self.duration_in_seconds, 10)]  # Every 10 seconds
        prices = [self.starting_price + self.bid_increment * (i / 10) for i in range(len(times))]

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(times, prices, label='Bid Progression', color='b')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Price ($)')
        plt.title('Bid Progression Over Time')
        plt.legend()

        # Ensure the directory exists before saving the image
        media_dir = 'static/media'
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Save the plot to a file in the media folder
        file_path = os.path.join(media_dir, 'bid_progress.png')  # Save to static/media
        plt.savefig(file_path)
        plt.close()  # Close the plot to avoid memory issues
