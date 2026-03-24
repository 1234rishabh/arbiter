from __future__ import annotations

import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import NextTimeStep, ReadOnly, RisingEdge
from cocotb_tools.runner import get_runner


def expected_grant(req: int) -> int:
    if req & 0b1000:
        return 0b1000
    if req & 0b0100:
        return 0b0100
    if req & 0b0010:
        return 0b0010
    if req & 0b0001:
        return 0b0001
    return 0b0000


@cocotb.test()
async def fixed_priority_arbiter_test(dut) -> None:
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start(start_high=False))

    dut.req.value = 0
    await RisingEdge(dut.clk)

    for req in range(16):
        await NextTimeStep()
        dut.req.value = req
        await RisingEdge(dut.clk)
        await ReadOnly()

        actual = int(dut.grant.value)
        expected = expected_grant(req)
        assert actual == expected, (
            f"req={req:04b}, expected={expected:04b}, got={actual:04b}"
        )


def test_fixed_priority_arbiter_runner() -> None:
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    sources = [proj_path / "sources/arb.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="fixed_priority_arbiter",
        always=True,
    )

    runner.test(
        hdl_toplevel="fixed_priority_arbiter",
        test_module="test_arbiter",
    )
