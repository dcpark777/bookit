import configparser

from resy_client import ResyClient
from bookit.models import DesiredReservation, ResyAuth, SnipeTime


class ResyBookingWorkflow:
    def __init__(self, resy_client: ResyClient, reservation_details: DesiredReservation) -> None:
        # resy_config = configparser.ConfigParser()
        # resy_config.read("resy.ini")
        # self.resy_auth = ResyAuth(**resy_config['resy.keys'])
        # self.reservation_details = DesiredReservation(**resy_config['resy.reservation.details'])
        # self.snipe_time = SnipeTime(**resy_config['resy.snipe.time'])
        self.resy_client: ResyClient = resy_client
        self.reservation_details = reservation_details

    def run(self):
        print('Running now...')
        # resy_client = ResyClient(resy_auth=self.resy_auth)

        # Find all available reservation slots
        available_reservations = self.resy_client.find_reservations(reservation_details=self.reservation_details)
        print(f'\nAvailable Reservations: {available_reservations}')
        first_slot_time = next(iter(available_reservations.keys()))
        first_slot = available_reservations[first_slot_time]
        print(first_slot)
        
        # Get details for slot to book
        booking_details = self.resy_client.get_reservation_details(
            config_token=first_slot.config_token,
            date=self.reservation_details.date,
            party_size=self.reservation_details.party_size,
        )
        print(f'\nBooking Details: {booking_details}')

        # Book reservation slot
        resy_token = self.resy_client.book_reservation(payment_method_id=booking_details.payment_method_id, book_token=booking_details.book_token)
        print(f'\nResy Token: {resy_token}')
        print('Reservation Complete!')
        
