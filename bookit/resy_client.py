
import requests

from http import HTTPStatus
from retry import retry
from typing import Dict, List

from bookit.models import AvailableReservationSlot, BookingInfo, DesiredReservation, ResyAuth, ReservationTimeType


class ResyClient:
    def __init__(self, resy_auth: ResyAuth) -> None:
        self.resy_auth: ResyAuth = resy_auth

    # Find available reservations
    def find_reservations(
        self,
        reservation_details: DesiredReservation = None,
        date: str = None,
        party_size: int = None,
        venue_id: int = None,
        time_table_types: List[ReservationTimeType] = None
    ):
        print(f'Finding reservations..')
        response = self._send_get_request(
            base_url="api.resy.com/4/find",
            params={
                "lat": 0,
                "long": 0,
                "day": reservation_details.date,
                "party_size": reservation_details.party_size,
                "venue_id": reservation_details.venue_id
            }
        )
        print(f'Find Reservations Response: {response}')
        available_slots = response['results']['venues'][0]['slots']
        # return available_slots
        reservation_map = self.build_reservation_map(available_slots=available_slots)
        return reservation_map
        # print(reservation_map)
        # Filter out undesired times and tables
        available_slot_time = self.find_reservation_time(reservation_map=reservation_map, reservation_time_types=reservation_details.reservation_time_types)
        available_config_id = available_slot_time.config_id if available_slot_time else None
        # print(f'Available confid: {available_config_id}')
        print(f'Available slot: {available_slot_time}')
        return available_config_id

    def filter_criteria(self, available_slots: List[AvailableReservationSlot], start_time: str, end_time: str):
        """
        Filter out undesired available slots 
        """
        for time in available_slots:
            pass
        pass

    # TODO: change ReservationTimeType to have a priority field
    def find_reservation_time(self, reservation_map: AvailableReservationSlot, reservation_time_types: ReservationTimeType):
        for time_type in reservation_time_types:
            available_slot: AvailableReservationSlot = reservation_map.check(time_type=time_type)
        return available_slot if available_slot else None

    """
    Build Map:
    {
        time: AvailableSlot(time, table_type, config_id, config_token),
        ...
    }
    """
    def build_reservation_map(self, available_slots: List[AvailableReservationSlot]):
        reservation_map = {}
        for slot in available_slots:
            time = slot['date']['start']
            config = slot['config']
            s = AvailableReservationSlot(
                time=time,
                table_type=config['type'],
                # config_id=config['id'],
                config_token=config['token']
            )
            reservation_map[time] = s
        return reservation_map
    
    def get_reservation_details(self, config_token: str, date: str, party_size: int):
        response = self._send_get_request(
            base_url="api.resy.com/3/details",
            params={
                "config_id": config_token,
                "day": date,
                "party_size": party_size
            }
        )
        print(f"Get Reservation Details Response: {response}")
        payment_method_id = response['user']['payment_methods'][0]['id']
        book_token = response['book_token']['value']
        return BookingInfo(payment_method_id=payment_method_id, book_token=book_token)
    
    def book_reservation(self, payment_method_id: int, book_token: str):
        response = self._send_post_request(
            base_url="api.resy.com/3/book",
            params={
                "book_token": book_token,
                "struct_payment_method": '{"id": %s}' % payment_method_id
            }
        )
        print(f'Book Reservation Response: {response}')
        return response['resy_token']
        

    def _generate_request_headers(self):
        """
        Find your User-Agent here: https://useragentstring.com/
        """
        return {
            "Authorization": f'ResyAPI api_key="{self.resy_auth.api_key}"',
            "x-resy-auth-token": self.resy_auth.auth_token,
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Origin": "https://widgets.resy.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://widgets.resy.com/",
            "Cache-Control": "no-cache"
        }

    @retry(tries=3, delay=1, backoff=2, jitter=3)
    def _send_get_request(self, base_url: str, params: Dict[str, str]):
        response = requests.get(
            f"https://{base_url}",
            headers=self._generate_request_headers(),
            params=params
        )
        if response.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED]:
            raise RuntimeError(f"""
                GET request failed with status code: {response.status_code}. 
                \nMessage: {response.content}
                \nHeaders: {response.headers}
            """)
        return response.json()

    def _send_post_request(self, base_url: str, params: Dict[str, str]):
        response = requests.post(
            f"https://{base_url}",
            headers=self._generate_request_headers(),
            data=params
        )
        if response.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED]:
            raise RuntimeError(f"""
                POST request failed with status code: {response.status_code}. 
                \nMessage: {response.content} 
                \nHeaders: {response.headers}"
            """)
        return response.json()