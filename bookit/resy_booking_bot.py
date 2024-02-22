import configparser
import pytz
import time
from datetime import datetime

from bookit.models import DesiredReservation, ResyAuth, SnipeTime
from bookit.resy_client import ResyClient
from bookit.resy_booking_workflow import ResyBookingWorkflow

class ResyBookingBot:
    def __init__(self) -> None:
        pass

    def main(self):
        resy_config = configparser.ConfigParser()
        resy_config.read("resy.ini")
        resy_auth = ResyAuth(**resy_config['resy.keys'])
        reservation_details = DesiredReservation(**resy_config['resy.reservation.details'])
        snipe_info = SnipeTime(**resy_config['resy.snipe'])

        resy_client = ResyClient(resy_auth=resy_auth)
        resy_booking_workflow = ResyBookingWorkflow(
            resy_client=resy_client,
            reservation_details=reservation_details
        )
        
        tz_NY = pytz.timezone('America/New_York')
        success = False
        while not success:
            current_time = datetime.now(tz=tz_NY)
            print(f'Starting run for {current_time}')
            if current_time >= snipe_info.start_time:
                response = resy_booking_workflow.run()
                print(f'FINAL RESPONSE: {response}')
                if response:
                    success = True
            else:
                print(f'Not time to snipe. Sleeping for {snipe_info.attempt_interval} seconds...')
                time.sleep(snipe_info.attempt_interval)


if __name__ == "__main__":
    bot = ResyBookingBot()
    bot.main()
