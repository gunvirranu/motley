import dataclasses
import enum
import random
import time
import queue
from collections import deque
from threading import Thread
from math import pi as PI, cos, sin, dist, atan2
from typing import Any, Deque, Dict, List, Optional, Tuple

# Set `True` to visualize simulation real-time using `matplotlib`
DRAW_SIM = True
if DRAW_SIM:
    import matplotlib.pyplot as plt


Uid = int
Loc = Tuple[float, float]


@dataclasses.dataclass(frozen=True)
class Runway:
    """A possible runway to land on."""

    pos: Loc
    heading: float
    length: float

    def get_line_points(self) -> Tuple[Loc, Loc]:
        """Returns 2-tuple of (x, y) points for drawing runway line."""
        x, y = self.pos
        dx = self.length * cos(self.heading)
        dy = self.length * sin(self.heading)
        return ((x, y), (x + dx, y + dy))


class ControlZone:
    """Just a namespace to hold some spatial parameters."""

    AIRSPACE_RADIUS = 10_000  # [m]
    MIN_AIRCRAFT_SEP = 100  # [m]
    RUNWAYS = [
        Runway((-250-50, -250), PI/2, 500),
        Runway((250+50, -250), PI/2, 500),
    ]


@enum.unique
class AircraftState(enum.Enum):
    """Possible flight states for each aircraft."""
    FLIGHT = enum.auto()
    HOLD = enum.auto()
    APPROACH = enum.auto()
    LANDING = enum.auto()

@dataclasses.dataclass
class Aircraft:
    """Represents each individial aircraft state."""

    uid: Uid
    loc: Loc
    heading: float
    speed: float = 140  # [m / s]
    state: AircraftState = AircraftState.FLIGHT
    runway: Optional[Runway] = None


@enum.unique
class PlaneCommand(enum.Enum):
    """Commands that the ATC can send to a specific aircraft."""
    HEADING = enum.auto()
    HOLDING = enum.auto()
    LAND = enum.auto()

class Comms:
    """Emulates communication between ATC and actual aircraft."""

    def __init__(self):
        # Use queue message passing for inter-thread communication
        self.sim_to_atc = queue.SimpleQueue()
        self.atc_to_sim = queue.SimpleQueue()

    def update_plane_locs(self, plane_locs: List[Tuple[Uid, Loc]]):
        self.sim_to_atc.put(plane_locs)

    def get_plane_locs(self) -> List[Tuple[Uid, Loc]]:
        last = self.sim_to_atc.get()
        # Flush recieve queue to get latest update
        while True:
            try:
                last = self.sim_to_atc.get_nowait()
            except queue.Empty:
                return last

    def send_command(self, uid: Uid, command: PlaneCommand, data: Any = None):
        self.atc_to_sim.put((uid, command, data))

    def check_for_command(self) -> Optional[Tuple[Uid, PlaneCommand, Any]]:
        try:
            return self.atc_to_sim.get_nowait()
        except queue.Empty:
            return None


class ATCSystem:
    """System that tracks and commands aircraft."""

    def __init__(self, comms: Comms):
        self.comms = comms
        self.planes: Dict[Uid, Aircraft] = {}
        self._land_qs: List[Deque[Uid]] = [deque() for _ in ControlZone.RUNWAYS]
        self._land_assigned: List[Optional[Uid]] = [None for _ in ControlZone.RUNWAYS]

    def mainloop(self):
        """Runs system by recieving location updates and sending commands."""
        while True:
            self._update_locations()
            self._handle_potential_collision()
            self._assign_holding()

            for runway_idx, uid in enumerate(self._land_assigned):
                # Assign aircraft to land if free runway
                if uid is None and self._land_qs[runway_idx]:
                    next_land = self._land_qs[runway_idx].popleft()
                    self._land_assigned[runway_idx] = next_land
                    self.planes[next_land].state = AircraftState.LANDING
                    self.comms.send_command(next_land, PlaneCommand.LAND, runway_idx)

    def _update_locations(self):
        """Recieves and updates all aircraft locations."""
        aircraft_locs = self.comms.get_plane_locs()
        for uid, loc in aircraft_locs:
            if uid in self.planes:
                self.planes[uid].loc = loc
            else:
                # Track a new aircraft
                self._new_aircraft(uid, loc)
        if len(aircraft_locs) < len(self.planes):
            # Remove any aircraft that have now landed
            sent_uids = [x[0] for x in aircraft_locs]
            to_remove = [uid for uid in self.planes.keys() if uid not in sent_uids]
            for uid in to_remove:
                self._remove_aircraft(uid)

    def _handle_potential_collision(self):
        """Checks for imminent proximity danger and attempt to correct."""
        for plane in self.planes.values():
            for other in self.planes.values():
                if plane is other:
                    continue
                if dist(plane.loc, other.loc) <= 3 * ControlZone.MIN_AIRCRAFT_SEP:
                    print("POTENTIAL COLLISION:",  plane, other)
                    # TODO: Adjust headings to handle proximity

    def _assign_holding(self):
        """Intelligently assigns holding patterns to "free" aircraft."""
        for plane in self.planes.values():
            if plane is AircraftState.FLIGHT:
                # TODO: Assign holding pattern location if needed
                pass

    def _new_aircraft(self, uid: Uid, loc: Loc):
        """Sets up tracking of new aircraft and assign landing runway."""
        plane = Aircraft(uid, loc, float("NaN"))
        runway_idx = self._find_closest_runway(loc)
        plane.runway = ControlZone.RUNWAYS[runway_idx]
        self.planes[plane.uid] = plane
        self._land_qs[runway_idx].append(plane.uid)

    def _remove_aircraft(self, uid: Uid):
        """Removes tracking of specific aircraft."""
        self._land_assigned[self._land_assigned.index(uid)] = None
        self.planes.pop(uid)

    def _find_closest_runway(self, loc: Loc) -> int:
        """Returns index of physically closest runway."""
        min_i, min_dist = -1, float("inf")
        for i, runway in enumerate(ControlZone.RUNWAYS):
            d = dist(loc, runway.pos)
            if d < min_dist:
                min_i, min_dist = i, d
        return min_i


class Sim:
    """Track and simulate physical aircraft."""

    def __init__(self, comms: Comms, spawn_prob: float = 0.98, dt: float = 0.1):
        self.comms = comms
        self.spawn_prob = spawn_prob
        self.dt = dt
        self.n = 0
        self.planes: Dict[Uid, Aircraft] = {}
        random.seed(3)

    def mainloop(self):
        """Simulates aircraft movement, sends location updates, and spawns aircraft."""
        while True:
            tmp = self.comms.check_for_command()
            if tmp:
                uid, command, data = tmp
                if command is PlaneCommand.HEADING:
                    self.planes[uid].heading = data
                elif command is PlaneCommand.HOLDING:
                    # TODO: Implement simulation of circular flight
                    raise RuntimeError("Haven't implemented this")
                elif command is PlaneCommand.LAND:
                    plane = self.planes[uid]
                    plane.runway = ControlZone.RUNWAYS[data]
                    plane.state = AircraftState.APPROACH
                    dy, dx = plane.runway.pos[1] - plane.loc[1], plane.runway.pos[0] - plane.loc[0]
                    plane.heading = atan2(dy, dx)

            self._simulate_planes()

            if random.random() > self.spawn_prob:
                self.add_random_plane()

            plane_locs = [(plane.uid, plane.loc) for plane in self.planes.values()]
            self.comms.update_plane_locs(plane_locs)
            time.sleep(self.dt)

    def add_random_plane(self):
        """Add a new random plane on the perimeter."""
        plane = self._gen_random_plane()
        self.planes[plane.uid] = plane

    def _simulate_planes(self):
        """Simulates a time-step for aircraft."""
        to_remove = []
        for uid, plane in self.planes.items():
            x, y = plane.loc
            vx, vy = plane.speed * cos(plane.heading), plane.speed * sin(plane.heading)
            plane.loc = (x + self.dt * vx, y + self.dt * vy)

            if plane.state is AircraftState.APPROACH:
                if dist(plane.loc, plane.runway.pos) < (2 * plane.speed * self.dt):
                    plane.heading = plane.runway.heading
                    plane.state = AircraftState.LANDING
            elif plane.state is AircraftState.LANDING:
                if dist(plane.loc, plane.runway.pos) >= plane.runway.length:
                    to_remove.append(uid)
        for uid in to_remove:
            self.planes.pop(uid)

    def _gen_random_plane(self):
        """Generates random plane on airspace perimeter."""
        n, self.n = self.n, self.n + 1
        angle = 2 * PI * random.random()
        x = ControlZone.AIRSPACE_RADIUS * cos(angle)
        y = ControlZone.AIRSPACE_RADIUS * sin(angle)
        return Aircraft(n, (x, y), angle - PI)


def draw_loop(planes):
    """Draws live plot of airspace and all aircraft. Requires `matplotlib`."""
    zone = plt.Circle((0, 0), ControlZone.AIRSPACE_RADIUS, color="k", fill=False)
    plt.gca().add_patch(zone)
    for runway in ControlZone.RUNWAYS:
        a, b = runway.get_line_points()
        plt.plot([a[0], b[0]], [a[1], b[1]], "k")
    plt.axis("equal")
    plane_dots = plt.plot([], [], "+k")[0]
    plt.show(block=False)

    while True:
        xs = [plane.loc[0] for plane in planes.values()]
        ys = [plane.loc[1] for plane in planes.values()]
        plane_dots.set_xdata(xs)
        plane_dots.set_ydata(ys)
        plt.pause(0.05)


def main():
    comms = Comms()
    atc = ATCSystem(comms)
    sim = Sim(comms)

    tatc = Thread(target=atc.mainloop)
    tsim = Thread(target=sim.mainloop)
    tatc.start()
    tsim.start()
    if DRAW_SIM:
        draw_loop(sim.planes)


if __name__ == "__main__":
    main()
