#!/usr/bin/env python3
"""Original exercise arithmetic only; not a native editor or adapter test."""
from fractions import Fraction as F
import json
from pathlib import Path

def tc(frame, origin_hours=0, rate=25):
    seconds, ff = divmod(frame, rate)
    minutes, ss = divmod(seconds, 60)
    hours, mm = divmod(minutes, 60)
    return f"{hours+origin_hours:02}:{mm:02}:{ss:02}:{ff:02}"

checks = {
 "W01": {"selected_frames": 200-100, "duration_seconds": str(F(100,25)),
         "handle_range": [100-12,200+12], "handle_frames": 200+12-(100-12),
         "handle_seconds": str(F(124,25)), "source_in_tc": tc(100,10),
         "source_out_exclusive_tc": tc(200,10), "source_last_tc": tc(199,10),
         "record_in_tc": tc(250,1), "record_out_exclusive_tc": tc(350,1),
         "record_last_tc": tc(349,1), "event_record_frame": 250+125-100,
         "unavailable_handle_frames": 496+12-500},
 "W02": {"slip_event_record": 100+220-210, "original_event_record": 100+220-200,
         "roll_event_record": 108+220-208, "roll_total_frames": 108+92,
         "reaction_original_frames": len(set(range(205,209))&set(range(200,300))),
         "reaction_slip_frames": len(set(range(205,209))&set(range(210,310))),
         "reaction_roll_frames": len(set(range(205,209))&set(range(208,300))),
         "combined_slip_then_roll_B_source": [218,310]},
 "W03": {"correct_span_seconds": str(F(240,24)), "wrong_rate_span_seconds": str(F(240,25)),
         "rate_30000_1001_seconds_for_30000_frames": str(F(30000)/F(30000,1001)),
         "rate_30_seconds_for_30000_frames": str(F(30000,30)),
         "rate_error_seconds": str(F(30000)/F(30000,1001)-F(30000,30))}
}
assert checks["W01"]["handle_range"] == [88,212]
assert checks["W01"]["source_last_tc"] == "10:00:07:24"
assert checks["W01"]["record_last_tc"] == "01:00:13:24"
assert checks["W01"]["event_record_frame"] == 275
assert checks["W01"]["unavailable_handle_frames"] == 8
assert checks["W02"]["slip_event_record"] == 110
assert checks["W02"]["roll_event_record"] == 120
assert checks["W02"]["roll_total_frames"] == 200
assert [checks["W02"][x] for x in ("reaction_original_frames","reaction_slip_frames","reaction_roll_frames")] == [4,0,1]
assert checks["W03"]["wrong_rate_span_seconds"] == "48/5"
assert checks["W03"]["rate_error_seconds"] == "1"
print(json.dumps({"status":"ARITHMETIC_CHECKS_PASS","native_editor_tests":"NOT_RUN","cases":checks}, indent=2))
