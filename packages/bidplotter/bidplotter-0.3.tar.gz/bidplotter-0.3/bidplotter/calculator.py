from .plotting import plot_bidding_progress
import matplotlib.pyplot as plt
import os

class BidCalculator:
    def __init__(self, starting_price, bid_increment, duration_in_minutes):
        self.starting_price = starting_price
        self.bid_increment = bid_increment
        self.duration_in_minutes = duration_in_minutes

    def calculate_final_price(self):
        # Convert duration to seconds
        duration_in_seconds = self.duration_in_minutes * 60
        
        # Calculate total number of bids
        time_between_bids = 10  # Assume each bid happens every 10 seconds
        total_bids = duration_in_seconds // time_between_bids
        
        # Calculate price increase
        price_increase = self.bid_increment * total_bids
        predicted_final_price = self.starting_price + price_increase
        
        return predicted_final_price

    def simulate_bidding(self):
        # Simulate bidding over time for plotting
        duration_in_seconds = self.duration_in_minutes * 60
        time_between_bids = 10
        total_bids = duration_in_seconds // time_between_bids
        
        times = [i * time_between_bids for i in range(total_bids)]
        prices = [self.starting_price + self.bid_increment * i for i in range(total_bids)]
        
        return times, prices

    def plot_bidding_progress(self):
        times, prices = self.simulate_bidding()
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

