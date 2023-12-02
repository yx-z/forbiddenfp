from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from operator import mul
from typing import Optional, Iterable

from typing_extensions import List, Self, Dict

from forbiddenfp import equals


class Pulse(Enum):
    NONE = auto()
    LOW = auto()
    HIGH = auto()


@dataclass
class Signal:
    src: str
    dst: str
    pulse: Pulse


@dataclass
class Module(ABC):
    name: str
    outputs: List[str] = field(default_factory=list)

    def send_signal(self: Self, recevied: Signal) -> List[Signal]:
        pulse = self.determine_pulse(recevied)
        if pulse != Pulse.NONE:
            return [Signal(self.name, output, pulse) for output in self.outputs]
        return []

    @abstractmethod
    def determine_pulse(self: Self, signal: Signal) -> Pulse:
        ...


class Broadcaster(Module):
    def determine_pulse(self: Self, signal: Signal) -> Pulse:
        return signal.pulse


@dataclass
class FlipFlop(Module):
    state: bool = False

    def determine_pulse(self: Self, signal: Signal) -> Pulse:
        if signal.pulse == Pulse.HIGH:
            return Pulse.NONE
        self.state = not self.state
        return self.state.if_true_val(Pulse.HIGH).or_else(Pulse.LOW)


@dataclass
class Conjunction(Module):
    input_pulses: Dict[str, Pulse] = field(default_factory=dict)

    def determine_pulse(self: Self, signal: Signal) -> Optional[Pulse]:
        self.input_pulses[signal.src] = signal.pulse
        if self.input_pulses.values().all(equals(Pulse.HIGH)):
            return Pulse.LOW
        return Pulse.HIGH


class UnTyped(Module):
    def determine_pulse(self: Self, signal: Signal) -> Pulse:
        return Pulse.NONE


class Button(Module):
    def determine_pulse(self: Self, signal: Signal) -> Pulse:
        return Pulse.LOW


circuit_str = """%vh -> qc, rr
&pb -> gf, gv, vp, qb, vr, hq, zj
%zj -> kn, pb
%mm -> dj
%gp -> cp
&dc -> ns
%qc -> gp
%dx -> fq, dj
%tg -> nl, ks
%pr -> nl
%gx -> xf
%hd -> lt, nl
%dq -> dj, jc
%ht -> jv
%bs -> pb, rd
&nl -> ks, cq, tc, xf, gx, hd, lt
&dj -> dc, fq, jz, ht, zs, jc
&rr -> gp, rv, jt, qc, sq
%vr -> qb
%jz -> dj, ht
%hq -> nx
%cf -> jg, rr
%hj -> cf, rr
%mt -> rr
%sq -> rr, vh
%jg -> rr, pd
%gf -> gv
%xv -> dj, dx
%rh -> nl, gx
broadcaster -> hd, zj, sq, jz
%jv -> dj, zs
%rd -> vs, pb
%pd -> rr, mt
&rv -> ns
&vp -> ns
%vs -> pb
%nx -> pb, bs
%zp -> mm, dj
&ns -> rx
%lt -> rh
%pf -> pr, nl
%tc -> qz
%xz -> dj, zp
%qb -> hq
%rl -> pf, nl
%fq -> xz
%kn -> pb, xn
%xf -> tg
%qz -> nl, rl
%ks -> tc
%jt -> kb
%jc -> xv
%kb -> hj, rr
%zs -> dq
%gv -> vr
&cq -> ns
%cp -> rr, jt
%xn -> pb, gf""".splitlines().map(lambda line: line.split(" -> ")).list()

circuits = circuit_str.map_unpack(lambda prefix, _: prefix[0].map_val({
    "b": ("broadcaster", Broadcaster("broadcaster")),
    "%": (prefix[1:], FlipFlop(prefix[1:])),
    "&": (prefix[1:], Conjunction(prefix[1:])),
})).dict()
# dummy circuits from problem statement
circuits.update({"rx": UnTyped("rx"), "button": Button("button").apply(lambda b: b.outputs.append("broadcaster"))})
# fill in outputs
for prefix, out_str in circuit_str:
    name = prefix.replace("%", "").replace("&", "")
    for out in out_str.split(", "):
        circuits[name].outputs.append(out)
        if isinstance(circuits[out], Conjunction):
            circuits[out].input_pulses[name] = False


def push_button() -> Iterable[Signal]:
    queue = [Signal("button", "broadcaster", Pulse.LOW)]
    while queue:
        tmp = []
        for sig in queue:
            yield sig
            tmp += circuits[sig.dst].send_signal(sig)
        queue = tmp


# 1
pulse_count = {"low": 0, "high": 0}
for _ in range(1000):
    for signal in push_button():
        if signal.pulse == Pulse.LOW:
            pulse_count["low"] += 1
        elif signal.pulse == Pulse.HIGH:
            pulse_count["high"] += 1
print(pulse_count["low"] * pulse_count["high"])

# 2 (need to comment out 1 part to clear state)
# in my setup, S={&rv, &vp, &dc, &cq} -> &ns -> rx. Hence i need to find cycles for s in S -> ans = lcm(their length)
# where each length can be debug printed from the loop of push_button above.
required = ("rv", "vp", "dc", "cq").zip((0).infinite()).dict()
pressed_cnt = 0
while not required.values().all():
    pressed_cnt += 1
    for signal in push_button():
        if signal.src in required and signal.pulse == Pulse.HIGH and not required[signal.src]:
            required[signal.src] = pressed_cnt
required.values().reduce(mul).print()
